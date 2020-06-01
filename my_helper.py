from models import Activity, User

# id = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.String(400))
#     spot = db.Column(db.String(100))
#     policy_type = db.Column(db.Integer)  # 0 = no, 1 = modertet, 2 = strict
#     penalty_price = db.Column(db.Integer)
#     penalty_time = db.Column(db.Integer)
#     days = db.Column(db.JSON)   # {"sunday": True, "monday": True, ...} or {"1": True, "2": True, ...}
#     time_step = db.Column(db.JSON)  # {"start": hour, "end": hour} or {1: {"0": hour, "1": hour}, 2...}
#     weekly = db.Column(db.Boolean)
#
#     # relationship handle
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


def update_act(description, spot, policy_type, penalty_price, penalty_time, days, time_step, weekly, act_id):
    act = Activity.query.filter_by(id=act_id).first()

    if description is not None:
        if isinstance(description, str):
            act.description = description
        else:
            return False
    if spot is not None:
        if isinstance(spot, str):
            act.spot = spot
        else:
            return False
    if policy_type is not None:
        if isinstance(policy_type, int):
            act.policy_type = policy_type
        else:
            return False
    if penalty_price is not None:
        if isinstance(penalty_price, int):
            act.penalty_price = penalty_price
        else:
            return False
    if penalty_time is not None:
        if isinstance(penalty_time, int):
            act.penalty_time = penalty_time
        else:
            return False
    if days is not None:
        if isinstance(days, dict):
            act.days = days
        else:
            return False
    if time_step is not None:
        if isinstance(time_step, dict):
            act.time_step = time_step
        else:
            return False
    if weekly is not None:
        if isinstance(weekly, bool):
            act.weekly = weekly
        else:
            return False
    return act


def create_act(description, spot, policy_type, penalty_price, penalty_time, days, time_step, weekly, user_id):
    act = Activity(user_id=user_id)

    if isinstance(description, str):
        act.description = description
    else:
        return False

    if isinstance(spot, str):
        act.spot = spot
    else:
        return False

    if isinstance(policy_type, int):
        act.policy_type = policy_type
    else:
        return False

    if isinstance(penalty_price, int):
        act.penalty_price = penalty_price
    else:
        return False

    if isinstance(penalty_time, int):
        act.penalty_time = penalty_time
    else:
        return False

    if isinstance(days, dict):
        act.days = days
    else:
        return False

    if isinstance(time_step, dict):
        act.time_step = time_step
    else:
        return False

    if isinstance(weekly, bool):
        act.weekly = weekly
    else:
        return False

    return act


def create_user(username, hased):
    user = User()
    if isinstance(username, str):
        user.username = username
    else:
        return False
    if isinstance(hased, str):
        user.password_hash = hased
    else:
        return False

    return user
