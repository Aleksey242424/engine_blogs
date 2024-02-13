from app.chat import chat_bp
from flask_login import current_user,login_required
from app.chat.form import ChatForm
from flask import render_template,redirect,url_for,g
from app.system_db.messages import Messages


@chat_bp.route('/',methods=['GET','POST'])
@login_required
def chat():
    form = ChatForm()
    form_search = g.search
    if form.validate_on_submit():
        message = form.message.data
        Messages.add(message=message,user_id = current_user.user_id)
        return redirect(url_for('chat_bp.chat'))
    messages = Messages.get_all()
    return render_template('chat/chat.html',form=form,messages=messages,form_search=form_search)

