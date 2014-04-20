# coding: utf8
def index():
    issues = db().select(db.issue.id, db.issue.title, orderby=db.issue.title)
    return dict(issues=issues)

def create():
    form = SQLFORM(db.issue).process(next=URL('index'))
    return dict(form=form)

def edit():
    this_issue = db.issue(request.args(0,cast=int)) or redirect(URL('index'))
    form = SQLFORM(db.issue, this_issue, deletable = True).process(
        next = URL('show',args=request.args))
    return dict(form=form)

def show():
    issue = db.issue(request.args(0,cast=int)) or redirect(URL('index'))
#      db.post.page_id.default = this_page.id
#      form = SQLFORM(db.post).process() if auth.user else None
#      pagecomments = db(db.post.page_id==this_page.id).select()
    attachments = db(issue.id == db.attachment.issue_id).select()
    return dict(issue=issue, attachments=attachments)

def attachments():
     issue = db.issue(request.args(0,cast=int)) or redirect(URL('index'))
     db.attachment.issue_id.default = issue.id
     db.attachment.issue_id.writable = False
     grid = SQLFORM.grid(db.attachment.issue_id==issue.id,args=[issue.id], csv=False, searchable=False, fields=[db.attachment.name, db.attachment.doc])
     return dict(issue=issue, grid=grid)



def download():
     return response.download(request, db)
