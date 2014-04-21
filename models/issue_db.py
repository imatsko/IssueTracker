# coding: utf8

db.define_table('comment_post',
    Field('prev_comment', 'reference comment_post', readable=False, writable=False),
    Field('body', 'text'),
    Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('created_by', 'reference auth_user', default=auth.user_id, readable=False, writable=False)
    )

db.comment_post.prev_comment.requires = IS_EMPTY_OR(IS_IN_DB(db, 'comment_post.id'))
db.comment_post.body.requires = IS_NOT_EMPTY()


db.define_table('issue',
    Field('title'),
    Field('body', 'text'),
    Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('created_by', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('modified_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('modified_by', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('root_comment', 'reference comment_post', readable=False, writable=False),
    format='%(title)s')

db.issue.id.readable = False
db.issue.title.requires = IS_NOT_IN_DB(db, 'issue.title')
db.issue.body.requires = IS_NOT_EMPTY()
db.issue.root_comment.requires = IS_IN_DB(db, 'comment_post.id')

# db.issue.created_by.readable = db.issue.created_by.writable = False
# db.issue.created_on.readable = db.issue.created_on.writable = False

db.define_table('attachment',
    Field('issue_id', 'reference issue'),
    Field('name'),
    Field('doc', 'upload'),
    Field('description', 'text'),
#     Field('created_on', 'datetime', default=request.now),
#     Field('created_by', 'reference auth_user', default=auth.user_id),
    format='%(name)s')


# db.document.name.requires = IS_NOT_IN_DB(db, 'document.name')
db.attachment.id.readable = db.attachment.id.writable = False
db.attachment.issue_id.readable = db.attachment.issue_id.writable = False
# db.document.created_by.readable = db.document.created_by.writable = False
# db.document.created_on.readable = db.document.created_on.writable = False

