def index():
    msg = 'Voce é o usuário'
    return dict(msg=msg)

def new():
    postform = SQLFORM(db.user)
    if postform.accepts(request.vars,session):
       redirect(URL(r=request, f="view", args=postform.vars.id))
    return dict(postform=postform)

def edit():
        return redirect(URL('default', 'user'))
    

def view():
    userid = request.args(0)
    user = db(db.user.id == userid).select()[0]
    return dict(user=user)

def listUsers():
    query = request.vars.query
    records = db(query).select(db.auth_user.ALL)
    return dict(records=records)