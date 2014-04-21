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
        response.flash = 'issue added'
        redirect(URL('show', args=[form.vars.id]))

    return dict(form=form)

@auth.requires_login()
def edit():
    this_issue = db.issue(request.args(0,cast=int)) or redirect(URL('index'))
    form = SQLFORM(db.issue, this_issue, deletable = True)
    root_comment = db.comment_post(this_issue.root_comment)
    
    db.comment_post.body.requires = None
    
    comment_element = TR(LABEL('Comment'),
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
        
        tree_elem['new_comment_form'] = SQLFORM(db.comment_post, submit_button="Post comment", _formname='comment_'+str(comment.id))
        tree_elem['new_comment_form'].vars.prev_comment = comment.id
        if(tree_elem['new_comment_form'].process(next=URL(show, args=request.args),formname='comment_'+str(comment.id)).accepted):
            response.flash = T("Comment posted")
        return tree_elem
    
    comment_tree = make_comment_tree(root_comment)
    

    attachments = db(issue.id == db.attachment.issue_id).select()
    return dict(issue=issue, attachments=attachments, comment_tree=comment_tree)

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