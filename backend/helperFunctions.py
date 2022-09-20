import hashlib
from uuid import uuid4
from models import User, Sessions, db

def hashFunction(password):
    m = hashlib.sha1()
    salt = 'gvUiUR88'
    b = bytes(password + salt, 'utf-8')
    m.update(b)
    hashed = m.hexdigest()
    return hashed

def isUserValid(username_email, password_hash):
    user = User.query.filter_by(username=username_email).first()
    if user == None:
        user = User.query.filter_by(email=username_email).first()    
    if user == None or user.password_hash != hashFunction(password_hash):
        return False
    return True

def createSession(username_email): 
    sessionId = uuid4()
    user = User.query.filter_by(username=username_email).first()
    if user == None:
        user = User.query.filter_by(email=username_email).first()
    
    if Sessions.query.filter_by(userId = user.id).first() != None:
        db.session.delete(Sessions.query.filter_by(userId = user.id).first())
        db.session.commit()
    
    session = Sessions(sessionId=sessionId.hex, userId=user.id)
    db.session.add(session)
    db.session.commit()
    return sessionId.hex
