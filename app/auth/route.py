from app.auth import auth_bp
from app.auth.form import LoginForm,RegisterForm,ResetPasswordForm,NewPasswordForm
from flask import render_template,redirect,url_for,flash
from app.system_db.users import Users
from flask_login import login_user,current_user
from app._jwt import generate_token,decode_token
from app.auth.messages import reset_password_message


@auth_bp.route('/',methods=['GET','POST'])
@auth_bp.route('/auth/',methods=['GET','POST'])
def login():
    if current_user.is_anonymous:
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            remember_me = form.remember_me.data
            user = Users.get_instance(username=username,password=password)
            if user:
                login_user(user,remember=remember_me)
                return redirect(url_for('chat_bp.chat'))
            flash('Данные не коректны')
        return render_template('auth/login.html',form=form)
    return redirect(url_for('chat_bp.chat'))

@auth_bp.route('/auth/register',methods=['GET','POST'])
def register():
    if current_user.is_anonymous:
        form = RegisterForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            email = form.email.data
            remember_me = form.remember_me.data
            if Users.add(username=username,password=password,email=email):
                user = Users.get_instance(username=username,password=password)
                login_user(user,remember=remember_me)
                return redirect(url_for('chat_bp.chat'))
            flash('Такое имя или почта уже заняты')
        return render_template('auth/register.html',form=form)
    return redirect(url_for('chat_bp.chat'))

@auth_bp.route('/auth/reset_password',methods=['GET','POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user_id = Users.get_user_id_by_email(email)
        if user_id:
            token = generate_token('user_id',user_id)
            reset_password_message(token,email)
            flash('Проверьте вашу почту')
        else:
            flash('Данные не коректны')
    return render_template('auth/reset_password.html',form=form)

@auth_bp.route('/auth/reset_password/new_password/<token>',methods=['GET','POST'])
def new_password(token):
    user_id = decode_token(token)
    user_id = user_id['user_id']
    form = NewPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        Users.update_password(user_id,password)
        return redirect(url_for('auth_bp.login'))
    return render_template('auth/new_password.html',form=form,token=token)