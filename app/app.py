from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "DevOps Project Deployed Successfully!"

app.run(host="0.0.0.0", port=80)

