from app.posts import posts_bp
from app.system_db.posts import Posts
from app.system_db.likes_dislikes import LikesDislikes
from app.posts.form import PostNameBodyForm,LikeDislikeForm
from flask_login import current_user,login_required
from flask import render_template,redirect,url_for,g,request
from app._jwt import decode_token
from app.system_db.elastic import get_posts

@posts_bp.route('/',methods=['GET','POST'])
@login_required
def posts():
    if request.args.get('page'):
        page = request.args.get('page')
    else:
        page = 1
    posts = Posts.get_recom_posts(page)
    group = Posts.get_count_posts_group()
    form_search = g.search
    if form_search.validate_on_submit():
        search = form_search.search.data
        return redirect(url_for('post_bp.search_posts',search=search))
    return render_template('post/posts.html',
                           posts=posts,
                           form_search=form_search,
                           group = group,
                           page=int(page))

@posts_bp.route('/create_post',methods=['GET','POST'])
@login_required
def create_post():
    form = PostNameBodyForm()
    if request.method == 'POST':
        if request.form.get('create_post') == 'create_post':
            title = form.post_name.data
            body = form.body.data
            Posts.add(title,body,current_user.user_id)
            return redirect(url_for('profile_bp.profile',token=g.token('username',current_user.username)))

    
    return render_template('post/create_post.html',
                           form=form,
                           token=g.token('username',current_user.username))

@posts_bp.route('/post/<token>',methods=['GET','POST'])
def post(token):
    form_search = g.search
    form = LikeDislikeForm()
    if form_search.validate_on_submit():
        search = form_search.search.data
        return redirect(url_for('post_bp.search_posts',
                                search=search))
    post_id = decode_token(token)
    post_id = post_id['post_id']
    post = Posts.get_post(post_id=post_id)
    avg_likes = LikesDislikes.get(post_id=post_id)
    if form.validate_on_submit():
        like = request.form.get('like')
        dislike = request.form.get('dislike')
        LikesDislikes.add(current_user.user_id,post_id=post_id,
                          like = str(bool(like)),dislike=str(bool(dislike)))
        return redirect(url_for('post_bp.post',token=g.token('post_id',post_id)))
    
    return render_template('post/post.html',post=post,
                           form_search=form_search,
                           token=g.token('username',current_user.username),
                           post_token = g.token('post_id',post_id),
                           form=form,
                           avg_likes=avg_likes)

@posts_bp.route('/search_posts/<search>',methods=['GET','POST'])
def search_posts(search):
    token = g.token('username',current_user.username)
    if request.args.get('page'):
        page = request.args.get('page')
    else:
        page = 1
    form_search = g.search
    if form_search.validate_on_submit():
        search = form_search.search.data
        return redirect(url_for('post_bp.search_posts',search=search))
    posts = get_posts(search)
    count_group = int(-1*(len(posts)/3)//1*-1)
    posts = posts[(int(page)-1)*3:int(page)*3]
    return render_template('post/search_posts.html',
                           posts=posts,
                           count_group=count_group,
                           search=search,
                           page = int(page),
                           form_search=form_search,
                           token=token)