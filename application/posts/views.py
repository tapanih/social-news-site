from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.posts.models import Post
from application.posts.forms import PostForm

@app.route("/posts", methods=["GET"])
def posts_index():
  return render_template("posts/list.html", posts = Post.query.all())


@app.route("/posts/new/")
@login_required
def posts_form():
  return render_template("posts/new.html", form = PostForm())


@app.route("/posts/<post_id>/upvote", methods=["POST"])
@login_required
def posts_upvote(post_id):
  post = Post.query.get(post_id)
  if post:
    post.upvotes += 1
    db.session().commit()

  return redirect(url_for("posts_index"))


@app.route("/posts/", methods=["POST"])
@login_required
def posts_create():
  form = PostForm(request.form)

  if not form.validate():
    return render_template("posts/new.html", form=form)

  post = Post(form.title.data, False, form.url.data)
  post.author = current_user

  if not form.url.data:
    post.content = form.text.data
    post.is_text = True
  
  db.session().add(post)
  db.session().commit()

  return redirect(url_for("posts_index"))

  
@app.route("/posts/<post_id>/delete", methods=["POST"])
@login_required
def posts_delete(post_id):
  post = Post.query.get(post_id)
  if post and current_user == post.author:
    db.session().delete(post)
    db.session().commit()

  return redirect(url_for("posts_index"))