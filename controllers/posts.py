def registerPost():
    form = SQLFORM(db.posts)
    if(form.accepts(request.vars, session)):
        response.flash = T('Post registered!!')
    elif(form.errors):
        response.flash = T('There are errors!!')
    return dict(form=form)

    
        
        
    
    