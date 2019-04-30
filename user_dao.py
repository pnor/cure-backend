from db import db, User
import time

def get_user_by_email(email):
    User.query.filter(User.email == email).first() 

def get_user_by_session(session_token):
    User.query.filter(User.session_token == session_token).first() 

def get_user_by_update(update_token):
    User.query.filter(User.update_token == update_token).first() 

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
    user = get_user_by_update(update_token)

    if user is None: # Update token can't exist without a user first
        raise Exception('Invalid update token')

    user.renew_session()
    db.session.commit()
    return user