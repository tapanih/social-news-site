from application import app

@app.route("/version")
def version():
  return "0.0.1"

@app.route("/health")
def health():
  return "ok"
