from app.profile import profile_bp
from app._jwt import decode_token
from app.system_db.users import Users
from app.system_db.posts import Posts
from flask import render_template,redirect,url_for,g,current_app,request,flash
from app.profile.form import ChangeDataProfileForm,AvatarForm
from flask_login import current_user,login_required
from app.system_db import db_session
from werkzeug.utils import secure_filename

@profile_bp.route('/<token>',methods=['GET','POST'])
@login_required
def profile(token):
    form_avatar = AvatarForm()
    username = decode_token(token)
    username = username['username']
    user = Users.get_data(username=username)
    
    if not request.args.get('page'):
        page = 1
    else:
        page = request.args.get('page')
    my_posts = Posts.get_user_posts(username,int(page))
    count_group = Posts.get_count_my_post_group(username)
    if request.method == 'POST':
        if request.form.get('send_search') == 'search':
            search = request.form.get('search')
            return redirect(url_for('post_bp.search_posts',search=search))
        elif request.form.get('change_avatar') == 'change avatar':
            file = form_avatar.avatar.data
            if getattr(file,'filename',None):
                
                file.filename = secure_filename(f'{current_user.username}.jpg')
                file.save(f'{current_app.config["UPLOAD_FOLDER"]}/{file.filename}')
                Users.update_avatar(current_user.user_id,f'images/avatars/{file.filename}')
                db_session.commit()
            else:
                flash('Вы не выбрали аватарку')
            return redirect(url_for('profile_bp.profile',token=token))
    form_search = g.search
    return render_template('profile/profile.html',
                           user=user,
                           token=token,
                           form=form_avatar,
                           form_search=form_search,
                           my_posts=my_posts,
                           count_group = count_group,
                           page = int(page),
                           username=username)


@profile_bp.route('/<token>/change_profile',methods=['GET','POST'])
@login_required
def change_profile(token):
    form = ChangeDataProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db_session().commit()
        return redirect(url_for('profile_bp.profile',token=g.token('username',form.username.data)))
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
    return render_template('profile/change_profile.html',form=form,token=token)

    