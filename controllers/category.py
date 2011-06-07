def index():
    redirect(URL(r=request, f="listCategories"))
    
def new():
    categoryform = SQLFORM(db.category)
    if categoryform.accepts(request.vars,session):
       redirect(URL(r=request, f="view", args=categoryform.vars.id))
    return dict(categoryform=categoryform)
    

def edit():
    categoryid = request.args(0)
    category = db(db.category.id == categoryid).select()[0]
    editform = SQLFORM(db.category, category, deletable=True)
    if editform.accepts(request.vars, session):
        redirect(URL(r=request,f = "view",args=categoryid))
    return dict(editform=editform, category=category)

def view():
    categoryid = request.args(0)
    category = db(db.category.id == categoryid).select()[0]
    return dict(category=category)

def listCategories():
    query = request.vars.query
    records = db(query).select(db.category.ALL)
    return dict(records=records)