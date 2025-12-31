from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "DevOps Project Deployed Successfully!"

app.run(host="127.0.0.2", port=5000)

