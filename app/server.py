from flask import Flask

app = Flask(__name__)

@app.route('/')
def home_page():
  return "Hello World"

app.run(host="0.0.0.0", port=9000, debug=True)