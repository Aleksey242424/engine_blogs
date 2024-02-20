from app.chat import chat_bp
from flask_login import current_user,login_required
from app.chat.form import ChatForm,MessageForm
from flask import render_template,redirect,url_for,g,request,session
from app.system_db.messages import Messages
from app.system_db.chats import Chats
from app.system_db.users import Users
from app.system_db.chat_messages import ChatsMessages
from app._jwt import decode_token


@chat_bp.route('/',methods=['GET','POST'])
@login_required
def chat():
    form = ChatForm()
    form_search = g.search
    if request.method == 'POST':
        if request.form.get('send_search') == 'search':
            search = request.form.get('search')
            if search:
                return redirect(url_for('post_bp.search_posts',search=search))
        if request.form.get('send') == 'send':
            message = form.message.data
            if message:
                Messages.add(message=message,user_id = current_user.user_id)
            return redirect(url_for('chat_bp.chat'))
    messages = Messages.get_all()
    return render_template('chat/chat.html',form=form,messages=messages,form_search=form_search)


@chat_bp.before_app_request
def generate_chat_id_token():
    username = request.args.get('username')
    if username:
        username = decode_token(username)
        username = username['username']
        second_user_id = Users.get_id(username)
        session.pop(current_user.username,default=None)
        session[current_user.username] = {'chat_id':g.token('chat_id',g.chat_id(first_user_id = current_user.user_id,second_user_id=second_user_id)),
                                          'recipient':username}
        

@chat_bp.route('/messages',methods=['GET','POST'])
@login_required
def messages():
    form = MessageForm()
    form_search=g.search
    session_data =session.get(current_user.username,default=None)
    chat_id = decode_token(session_data['chat_id'])
    chat_id = chat_id['chat_id']
    recipient_name = session_data['recipient']
    recipient_id = Users.get_id(recipient_name)
    Chats.add(first_user_id=current_user.user_id,second_user_id=recipient_id)
    if request.method == 'POST':
        if request.form.get('send_search') == 'search':
            search = request.form.get('search')
            return redirect(url_for('post_bp.search_posts',search=search))
        if request.form.get('send') == 'send':
            message = form.message.data
            if message:
                ChatsMessages.add(chat_id,current_user.user_id,recipient_id,message)
            return redirect(url_for('chat_bp.messages',chat_id=chat_id,recipient_name=recipient_name))
    messages = ChatsMessages.get(chat_id)
    return render_template('chat/chat_messages.html',
                           form=form,messages=messages,
                           form_search=form_search)

@chat_bp.route('/chats_user',methods=['GET','POST'])
def chats_user():
    form_search =  g.search
    chats = Chats.get(current_user.user_id)
    if form_search.validate_on_submit():
        search = request.form.get('search')
        return redirect(url_for('post_bp.search_posts',search=search))
    return render_template('chat/chats_user.html',
                           chats=chats,
                           form_search = form_search)


