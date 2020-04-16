from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.posts.models import Comment, Post, Upvote
from application.posts.forms import CommentForm, PostForm, EditTextPostForm, EditUrlPostForm, EditCommentForm

@app.route("/", methods=["GET"])
def posts_index():
  return render_template("posts/list.html",
      posts=Post.list_posts_dangerously_ordered_by("post.upvotes"))


@app.route("/new", methods=["GET"])
def posts_newest():
  return render_template("posts/list.html",
      posts=Post.list_posts_dangerously_ordered_by("post.date_created"))


@app.route("/submit")
@login_required
def posts_form():
  return render_template("posts/new.html", form=PostForm())


@app.route("/posts/<post_id>/upvote", methods=["POST"])
@login_required
def posts_upvote(post_id):
  post = Post.query.get(post_id)
  if not post or Upvote.query.filter_by(account_id=current_user.id, post_id=post.id).first():
    return redirect(url_for("posts_index"))

  post.upvotes += 1
  upvote = Upvote(current_user.id, post.id)
  db.session().add(upvote)
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


@app.route("/posts/<post_id>/edit", methods=["GET", "POST"])
@login_required
def posts_edit(post_id):
  post = Post.query.get(post_id)
  if not post or current_user != post.author:
    return redirect(url_for("posts_index"))

  if request.method == "GET":
    form = None
    if post.is_text:
      form = EditTextPostForm(title=post.title, content=post.content)
    else:
      form = EditUrlPostForm(title=post.title, content=post.content)

    return render_template("posts/edit.html", form=form, id=post.id)
  
  if request.method == "POST":
    form = EditTextPostForm(request.form) if post.is_text else EditUrlPostForm(request.form)

    if not form.validate():
      return render_template("posts/edit.html", form=form, id=post.id)
    
    post.title = form.title.data
    post.content = form.content.data
    db.session().commit()
  
    return redirect(url_for("posts_index"))


@app.route("/posts/<post_id>/comments", methods=["GET"])
def posts_comments(post_id):
  post = Post.query.get(post_id)
  if not post:
    return redirect(url_for("posts_index"))

  comments = (Comment.query.filter_by(post_id=post.id)
                           .order_by(Comment.date_created.desc()).all())

  return render_template("posts/comments.html", form=CommentForm(), post=post,
      comments=comments)


@app.route("/posts/<post_id>/comments", methods=["POST"])
@login_required
def posts_add_comment(post_id):
  post = Post.query.get(post_id)
  if not post:
    return redirect(request.referrer)

  comments = (Comment.query.filter_by(post_id=post.id)
                           .order_by(Comment.date_created.desc()).all())

  form = CommentForm(request.form)
  if not form.validate():
    return render_template("posts/comments.html", form=form, post=post, comments=comments)
  comment = Comment(form.content.data)
  comment.author = current_user
  comment.post_id = post.id
  db.session().add(comment)
  db.session().commit()
  return redirect(url_for("posts_comments", post_id=post.id))


@app.route("/posts/<post_id>/comments/<comment_id>/edit", methods=["GET", "POST"])
@login_required
def posts_edit_comment(post_id, comment_id):
  post = Post.query.get(post_id)
  comment = Comment.query.get(comment_id)
  if not post or not comment or current_user != comment.author:
    return redirect(request.referrer)

  if request.method == "GET":
    comments = (Comment.query.filter_by(post_id=post.id)
                          .order_by(Comment.date_created.desc()).all())
    form = EditCommentForm(content=comment.content)
    return render_template("posts/comments.html",
      form=form, post=post, comments=comments, comment_id=comment.id)

  if request.method == "POST":
    form = EditCommentForm(request.form)
    if not form.validate():
      return render_template("posts/comments.html",
        form=form, post=post, comments=comments, comment_id=comment.id)

    comment.content = form.content.data
    db.session().commit()
    return redirect(url_for("posts_comments", post_id=post.id))


@app.route("/comments/<comment_id>/delete", methods=["POST"])
@login_required
def posts_delete_comment(comment_id):
  comment = Comment.query.get(comment_id)
  if comment and current_user == comment.author:
    db.session().delete(comment)
    db.session().commit()

  return redirect(request.referrer)
