from app.models import Post, User
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from app.__init__ import db
import json

views = Blueprint('views', __name__) # declaring blueprint

@views.route('/', methods=['GET'])
def index():
    return render_template('index.html', user=current_user)

@views.route('/home', methods=['POST','GET'])
@login_required # only executes if user is logged in
def home():
    if request.method == 'POST':
        post = request.form.get('post')
        if len(post) < 1: # checking for errors
            flash('The post must be at least 1 character long', category='error')
        elif len(post) > 280:
            flash('The post cannot be longer than 280 characters', category='error')
        else:
            new_post = Post(data=post, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post added', category='info')

    return render_template('home.html', user=current_user)

@views.route('/delete-post', methods=['POST'])
def delete_post():
    post = json.loads(request.data)
    postId = post['postId']
    post = Post.query.get(postId)
    if post:
        if post.user_id == current_user.id:
            db.session.delete(post)
            db.session.commit()
            flash('Post deleted', category='warning')

    return jsonify({})

