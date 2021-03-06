# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
T.current_languages=['en','en-us']
if request.vars._language: session._language=request.vars._language
if session._language: T.force(session._language)
else: T.force(T.http_accept_language)


#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae://mynamespace')             # connect to Google BigTable
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## (more options discussed in gluon/tools.py)
#########################################################################




from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()

mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

auth.settings.hmac_key = 'sha512:a667c7a1-8129-45c6-a7c5-397d1085dabe'   # before define_tables()

##Colocando o auth_user

db.define_table(
    auth.settings.table_user_name,
    Field('first_name', length=128, default=''),
    Field('last_name', length=128, default=''),
    Field('email', length=128, default='', unique=True),
    Field('photo', 'upload',label=T('Photo')),
    Field('aboutMe', 'text',label=T('About Me')),
    Field('homeTown','string', label=T('HomeTown')),
    Field('currentCity','string', label=T('Current City')),
    Field('languages','string', label=T('Languages')),
    Field('college_University','string', label=T('College/University')),
    Field('highSchool','string',label=T('High School')),
    Field('employer','string', label=T('Employer')),
    Field('interestedIn','string', label=T('Interested In')),
    Field('phone', 'integer', label=T('Phone')),
    Field('website','string',label=T('Website')),
    Field('birthday','date',label=T('Birthday')),
    Field('password', 'password', length=512,
          readable=False, label=T('Password')),
    Field('registration_key', length=512,
          writable=False, readable=False, default=''),
    Field('reset_password_key', length=512,
          writable=False, readable=False, default=''),
    Field('registration_id', length=512,
          writable=False, readable=False, default=''),
                )

custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.first_name.requires = \
  IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires = \
  IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.password.requires = [IS_NOT_EMPTY(), CRYPT()]
custom_auth_table.email.requires = [
  IS_EMAIL(error_message=auth.messages.invalid_email),
  IS_NOT_IN_DB(db, custom_auth_table.email)]

auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table


auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'

#########################################################################
## If you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, uncomment and customize following
# from gluon.contrib.login_methods.rpx_account import RPXAccount
# auth.settings.actions_disabled=['register','change_password','request_reset_password']
# auth.settings.login_form = RPXAccount(request, api_key='...',domain='...',
#    url = "http://localhost:8000/%s/default/user/login" % request.application)
## other login methods are in gluon/contrib/login_methods
#########################################################################

crud.settings.auth = None                      # =auth to enforce authorization on crud

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################



db.define_table('category',
    Field('title', label=T('Title')),
    Field('About_this_category', 'text', label=T('About this Category')),
)

db.define_table('post',
    #Field('created_by', db.auth_user, default=auth.user_id, readable=False, writable=False),
    Field('title', label=T('Title')),
    Field('category', db.category, requires=IS_IN_DB(db, 'category.title') ),
    Field('body', 'text', label=T('Body')),
    Field('dateline', 'datetime', default=request.now,readable=False, writable=False),
)

db.define_table('comment',
    Field('post', db.post, readable=False, writable=False),
    Field('name', requires=IS_NOT_EMPTY(error_message=T('Please enter your name') ) ),
    Field('email', requires=IS_NOT_EMPTY(error_message=T('Please enter your e-mail') )),
    Field('commentbody', 'text', requires=IS_NOT_EMPTY(error_message="Please enter your comment.")),
    Field('dateline',  'datetime', default=request.now, readable=False, writable=False),
)
