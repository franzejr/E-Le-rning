def index():
    redirect(URL(r=request, f="listposts"))
  


@auth.requires_login()  
def new():
    postform = SQLFORM(db.post)
    if postform.accepts(request.vars,session):
       redirect(URL(r=request, f="view", args=postform.vars.id))
    return dict(postform=postform)
    

def edit():
    postid = request.args(0)
    post = db(db.post.id == postid).select()[0]
    editform = SQLFORM(db.post, post, deletable=True)
    if editform.accepts(request.vars, session):
        redirect(URL(r=request,f = "view",args=postid))
    return dict(editform=editform, post=post)

def listposts():
    query = request.vars.query
    records = db(query).select(db.post.ALL)
    return dict(records=records)
    
def view():
    postid = request.args(0)
    post = db(db.post.id == postid).select()[0]
    db.comment.post.default = postid
    commentform = SQLFORM(db.comment)
    if commentform.accepts(request.vars, session):
        redirect(URL(r=request, f = "view", args=postid))
    return dict(post=post, commentform=commentform)
        
def search():
    form, rows=crud.search(db.post)
    return dict(form=form, rows=rows)
    