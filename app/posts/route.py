from app.posts import posts_bp
from app.system_db.posts import Posts
from app.posts.form import PostNameBodyForm
from flask_login import current_user,login_required
from flask import render_template,redirect,url_for,g,request
from app._jwt import decode_token
from app.system_db.elastic import get_posts

@posts_bp.route('/')
@login_required
def posts():
    return 

@posts_bp.route('/create_post',methods=['GET','POST'])
@login_required
def create_post():
    form = PostNameBodyForm()
    if form.validate_on_submit():
        title = form.post_name.data
        body = form.body.data
        Posts.add(title,body,current_user.user_id)
        return redirect(url_for('profile_bp.profile',token=g.token('username',current_user.username)))
    return render_template('post/create_post.html',form=form)

@posts_bp.route('/post/<token>')
def post(token):
    post_id = decode_token(token)
    post_id = post_id['post_id']
    post = Posts.get_post(post_id=post_id)
    return render_template('post/post.html',post=post)

@posts_bp.route('/search_posts/<search>')
def search_posts(search):
    if request.args.get('page'):
        page = request.args.get('page')
    else:
        page = 1
    posts = get_posts('index_post',search)
    count_group = int(-1*(len(posts)/3)//1*-1)
    posts = posts[(int(page)-1)*3:int(page)*3]
    return render_template('post/search_posts.html',
                           posts=posts,
                           count_group=count_group,
                           search=search,
                           page = int(page))