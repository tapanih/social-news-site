from application import app, db
from flask import redirect, render_template, request, url_for
from application.threads.models import Thread

@app.route("/threads", methods=["GET"])
def threads_index():
  return render_template("threads/list.html", threads = Thread.query.all())

@app.route("/threads/new/")
def threads_form():
  return render_template("threads/new.html")

@app.route("/threads/<thread_id>/upvote", methods=["POST"])
def threads_upvote(thread_id):
  t = Thread.query.get(thread_id)
  t.upvotes += 1
  db.session().commit()

  return redirect(url_for("threads_index"))

@app.route("/threads/", methods=["POST"])
def threads_create():
  title = request.form.get("title")
  content = request.form.get("url")
  is_text = False

  if not content:
    content = request.form.get("text")
    is_text = True

  t = Thread(title, is_text, content)
  
  db.session().add(t)
  db.session().commit()

  return redirect(url_for("threads_index"))