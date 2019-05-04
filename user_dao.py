from db import db, User
import time

def get_user_by_email(email):
    return User.query.filter(User.email == email).first() 

def get_user_by_session(session_token):
    return User.query.filter(User.session_token == session_token).first() 

def get_user_by_update(update_token):
    return User.query.filter(User.update_token == update_token).first() 

def verify_credentials(email, password):
    user = get_user_by_email(email)

    if user is None:
        return False, None

    return user.verify_password(password), user 

def create_user(email, password):
    user = get_user_by_email(email)

    if user is not None: # Already exists!
        return False, user

    unix_time = int(time.time())
    user = User(
        email= email,
        password= password,
        createdAt= unix_time,
        updatedAt= unix_time 
    )
    db.session.add(user)
    db.session.commit()
    return True, user

def renew_session(update_token):
    """
    Renews a user's session
    """
    user = user_dao.get_user_by_update_token(update_token)
    if user is not None:
        user.renew_session()
        db.session.commit()
        return user
    # User doesn't exist
    raise Exception('Invalid update token')