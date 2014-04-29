# coding: utf8

def index():
    issues = db().select(db.issue.id, db.issue.title, orderby=db.issue.title)
    return dict(issues=issues)

@auth.requires_login()
def create():    
    db.comment_post.body.requires = None
    form = SQLFORM(db.issue)

    comment_element = TR(LABEL('Comment'),
        TEXTAREA(_id='comment',value=''))
    form[0].insert(-1,comment_element)
    
    def on_validation_comment(form):
        form.vars.root_comment = db.comment_post.insert(body=form.vars.comment)
    
    if form.process(onvalidation=on_validation_comment).accepted:
        db.status.insert(issue=form.vars.id, stat_value='new')
        response.flash = T('issue added')
        redirect(URL('show', args=[form.vars.id]))
    
    return dict(form=form)

@auth.requires_login()
def edit():
    this_issue = db.issue(request.args(0,cast=int)) or redirect(URL('index'))
    form = SQLFORM(db.issue, this_issue, deletable = True)
    root_comment = db.comment_post(this_issue.root_comment)
    
    db.comment_post.body.requires = None
    
    form.vars.modified_on = request.now
    form.vars.modified_by = auth.user_id
    
    comment_element = TR(LABEL(T('Comment')),
    TEXTAREA(_id='comment',value=root_comment.body))
    form[0].insert(-1,comment_element)

    def on_validation_comment(form):
        db.comment_post[root_comment.id] = dict(body=form.vars.comment)
        if form.vars.deleted:
            del db.comment_post[root_comment.id]

    form.process(onvalidation=on_validation_comment, next=URL('show',args=request.args))
        
    return dict(form=form)

def show():
    issue = db.issue(request.args(0,cast=int)) or redirect(URL('index'))    
    root_comment = db.comment_post[issue.root_comment]   
    
    def make_comment_tree(comment):
        tree_elem = dict()
        tree_elem['body'] = comment.body
        user = db.auth_user[comment.created_by]
        tree_elem['created_by'] = '%s %s' % (user.first_name, user.last_name)
        tree_elem['created_on'] = str(comment.created_on)
        tree_elem['children'] = list()
        
        for child in db(db.comment_post.prev_comment == comment.id).select():
            tree_elem['children'].append(make_comment_tree(child))
        
        tree_elem['new_comment_form'] = SQLFORM(db.comment_post, submit_button=T("Post comment"), _formname='comment_'+str(comment.id))
        tree_elem['new_comment_form'].vars.prev_comment = comment.id
        tree_elem['new_comment_form'].process(next=URL('show', args=request.args),formname='comment_'+str(comment.id))
        return tree_elem
    
    comment_tree = make_comment_tree(root_comment)
    
    issue.created_by_user = db.auth_user[issue.created_by]
    issue.modified_by_user = db.auth_user[issue.modified_by]
    
    attachments = db(issue.id == db.attachment.issue_id).select()
    
    status_history = db(db.status.issue == issue.id).select(orderby=db.status.set_on)
    
    last_stat = status_history.last()
    if last_stat.stat_value == 'closed':
        stat_set = {s:statuses[s] for s in ('reopened',)}
    elif last_stat.stat_value == 'started':
        stat_set = {s:statuses[s] for s in ('closed','started')}
    elif last_stat.stat_value == 'reopened':
        stat_set = {s:statuses[s] for s in ('started','closed')}
    elif last_stat.stat_value == 'new':
        stat_set = {s:statuses[s] for s in ('started','closed')}
    db.status.stat_value.requires = IS_IN_SET(stat_set, zero=None)
    db.status.stat_value.default = stat_set.keys()[0]

        
    new_status_form = SQLFORM(db.status)
    new_status_form.vars.issue = issue.id
    if new_status_form.process().accepted:
        response.flash = T("new status is set")
        redirect(URL('show', args=request.args))
        
    ###################################################    
#    this_team = db.team(request.args(0,cast=int)) or redirect(URL('index'))
    
#    membership_history = db(db.team_membership.team == this_team.id).select(orderby=db.team_membership.set_on)

    current_teams = db(db.team_working.issue == issue.id).select(db.team_working.ALL,
        orderby=db.team_working.set_on,
        groupby=db.team_working.team,
        having=(db.team_working.is_working == True))
    
    for team_working in current_teams:
        team_working.delete_form = SQLFORM(db.team_working,
            hidden=dict(formname='delete_working_'+str(team_working.team)),
            submit_button = T("Remove"))
        
        team_working.delete_form.vars.team = team_working.team
        team_working.delete_form.vars.issue = issue.id
        team_working.delete_form.vars.is_working = False
        if team_working.delete_form.process(next=URL('show', args=request.args),
            formname='delete_working_'+str(team_working.team)
            ).accepted:
            response.flash = T("Team removed")
        
    db.team_working.team.readable = db.team_working.team.writable = True
    new_team_form = SQLFORM(db.team_working, hidden=dict(formname="new_team"))
    new_team_form.vars.is_working = True
    new_team_form.vars.issue = issue.id
    
    if new_team_form.process(next=URL('show', args=request.args), formname="new_team").accepted:
        response.flash = T("New team added")
        
    return dict(issue=issue, 
        attachments=attachments, 
        comment_tree=comment_tree, 
        status_history=status_history, 
        new_status_form=new_status_form,
        current_teams=current_teams,
        new_team_form=new_team_form
        )

def attachments():
     issue = db.issue(request.args(0,cast=int)) or redirect(URL('index'))
     db.attachment.issue_id.default = issue.id
     db.attachment.issue_id.writable = False
     grid = SQLFORM.grid(db.attachment.issue_id==issue.id,args=[issue.id], csv=False, searchable=False, fields=[db.attachment.name, db.attachment.doc])
     return dict(issue=issue, grid=grid)

def download():
     return response.download(request, db)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())