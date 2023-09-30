from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/greet", methods=["POST"])
def greet():
    name = request.form["name"]
    greeting = f"Hello, {name}!"
    return render_template("greet.html", greeting=greeting)

if __name__ == "__main__":
    app.run()
