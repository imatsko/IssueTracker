# coding: utf8

db.define_table('team',
    Field('name', requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'team.name')]),
    Field('description', 'text'),
    Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('created_by', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
    format='%(name)s'
    )

db.define_table('team_membership',
    Field('auth_user', 'reference auth_user', notnull=True, readable=False, writable=False),
    Field('team', 'reference team', notnull=True, readable=False, writable=False),
    Field('is_member', 'boolean', readable=False, writable=False),
    Field('set_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('set_by', 'reference auth_user', default=auth.user_id, readable=False, writable=False)
    )

db.define_table('team_management',
    Field('auth_user', 'reference auth_user', notnull=True, readable=False, writable=False),
    Field('team', 'reference team', notnull=True, readable=False, writable=False),
    Field('is_manager', 'boolean', readable=False, writable=False),
    Field('set_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('set_by', 'reference auth_user', default=auth.user_id, readable=False, writable=False)
    )

def has_team_membership(team, auth_user):
    last = db((db.team_membership.team == team.id) &
        (db.team_membership.auth_user == auth_user.id)).select(orderby=db.team_membership.set_on).last()
    if not last is None:
        return last.is_member
    return False


def has_team_management(team, auth_user):
    last = db((db.team_management.team == team.id) &
        (db.team_management.auth_user == auth_user.id)).select(orderby=db.team_management.set_on).last()
    if not last is None:
        return last.is_manager
    return False
