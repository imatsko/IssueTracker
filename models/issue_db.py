# coding: utf8


db.define_table('issue',
    Field('title'),
    Field('body', 'text'),
#     Field('created_on', 'datetime', default=request.now),
#     Field('created_by', 'reference auth_user', default=auth.user_id),
#     Field('modified_on', 'datetime', default=request.now),
#     Field('modified_by', 'reference auth_user', default=auth.user_id),
#     Field('root_comment', 'reference comment'),
    format='%(title)s')

db.issue.id.readable = False
db.issue.title.requires = IS_NOT_IN_DB(db, 'issue.title')
db.issue.body.requires = IS_NOT_EMPTY()
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



# db.define_table('comment',
#     Field('prev_comment', 'reference comment'),
#     Field('body', 'text'),
#     Field('created_on', 'datetime', default=request.now),
#     Field('created_by', 'reference auth_user', default=auth.user_id))

# db.comment.body.requires = IS_NOT_EMPTY()
# db.comment.prev_comment.readable = db.comment.prev_comment.writable = False
# db.comment.created_by.readable = db.comment.created_by.writable = False
# db.comment.created_on.readable = db.comment.created_on.writable = False
