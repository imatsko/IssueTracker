# coding: utf8

db.define_table('team',
    Field('name', requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'team.name')]),
    Field('description', 'text'),
    Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('created_by', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
    format='%(name)s'
    )

db.define_table('team_membership',
    Field('auth_user', 'reference auth_user', readable=False, writable=False),
    Field('team', 'reference team', readable=False, writable=False),
    Field('is_member', 'boolean', readable=False, writable=False),
    Field('set_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('set_by', 'reference auth_user', default=auth.user_id, readable=False, writable=False)
    )

#db.define_table('team_leadership',
#    Field('auth_user', 'reference auth_user', readable=False, writable=False),
#    Field('team', 'reference team', readable=False, writable=False),
#    Field('is_member', 'boolean', readable=False, writable=False),
#    Field('set_on', 'datetime', default=request.now, readable=False, writable=False),
#    Field('set_by', 'reference auth_user', default=auth.user_id, readable=False, writable=False)
#    )
