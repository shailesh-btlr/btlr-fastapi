from statemachine import State, StateMachine


class UserExperienceMachine(StateMachine):
    started = State("started", initial=True)
    idle = State("idle")
    assigned = State("assigned")
    owned = State("owned")
    checked_out = State("checked_out", final=True)

    check_in = started.to(idle)
    assign = idle.to(assigned) | owned.to(assigned)
    accept = assigned.to(owned)
    decline = assigned.to(idle)
    unassign = owned.to(idle)
    check_out = owned.to(checked_out)

    def on_assign(self, department_id, role_id=None, user_id=None):
        self.model.assigned_department_id = department_id
        self.model.assigned_role_id = role_id
        self.model.assigned_user_id = user_id

    def on_accept(self, department_id, role_id, user_id):
        self.model.assigned_department_id = department_id
        self.model.assigned_role_id = role_id
        self.model.assigned_user_id = user_id

    def on_unassign(self):
        self.model.assigned_department_id = None
        self.model.assigned_role_id = None
        self.model.assigned_user_id = None
