
def index():
    teams = db(db.team.id > 0).select()
    return dict(teams=teams)

def create():
    create_form = SQLFORM(db.team)
    
    if create_form.process().accepted:
        response.flash = T("New team created")
    return dict(create_form=create_form)

def edit():
    this_team = db.team(request.args(0,cast=int)) or redirect(URL('index'))
    edit_form = SQLFORM(db.team, this_team)
    
    if edit_form.process().accepted:
        response.flash = T("Team updated")
    return dict(edit_form=edit_form)

def show():
    this_team = db.team(request.args(0,cast=int)) or redirect(URL('index'))
    
    membership_history = db(db.team_membership.team == this_team.id).select(orderby=db.team_membership.set_on)

    current_members = db(db.team_membership.team == this_team.id).select(db.team_membership.ALL,
        orderby=db.team_membership.set_on,
        groupby=db.team_membership.auth_user,
        having=(db.team_membership.is_member == True))
    
    for member in current_members:
        member.delete_form = SQLFORM(db.team_membership)
        
        member.delete_form.vars.auth_user = member.auth_user
        member.delete_form.vars.team = member.team
        member.delete_form.vars.is_member = False
        if member.delete_form.process(next=URL('show', args=request.args),
            _formname='delete_member_'+str(member.auth_user)).accepted:
            response.flash = T("Member removed")
        
    db.team_membership.auth_user.readable = db.team_membership.auth_user.writable = True
    new_member_form = SQLFORM(db.team_membership)
    new_member_form.vars.is_member = True
    new_member_form.vars.team = this_team
    
    if new_member_form.process(next=URL('show', args=request.args), _formname="new_member").accepted:
        response.flash = T("New member added")

    management_history = db(db.team_management.team == this_team.id).select(orderby=db.team_management.set_on)

    current_managers = db(db.team_management.team == this_team.id).select(db.team_management.ALL,
        orderby=db.team_management.set_on,
        groupby=db.team_management.auth_user,
        having=(db.team_management.is_manager == True))
    
    for manager in current_managers:
        manager.delete_form = SQLFORM(db.team_management)
        
        manager.delete_form.vars.auth_user = manager.auth_user
        manager.delete_form.vars.team = manager.team
        manager.delete_form.vars.is_manager = False
        if manager.delete_form.process(next=URL('show', args=request.args),
            _formname='delete_manager_'+str(manager.auth_user)).accepted:
            response.flash = T("Member removed")
        
    db.team_management.auth_user.readable = db.team_management.auth_user.writable = True
    new_manager_form = SQLFORM(db.team_management)
    new_manager_form.vars.is_manager = True
    new_manager_form.vars.team = this_team
    
    if new_manager_form.process(next=URL('show', args=request.args), _formname="new_manager").accepted:
        response.flash = T("New manager added")
        
    return dict(team=this_team,
                membership_history=membership_history, 
                current_members=current_members, 
                new_member_form=new_member_form,
                management_history=management_history, 
                current_managers=current_managers, 
                new_manager_form=new_manager_form
                )
    
