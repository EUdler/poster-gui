from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def index(name="Home"):
    foods = ["broccoli", "apple", "oatmeal coockie", "milk", "chicken", "omelette"]
    return render_template('base.html', name=name, foods=foods)


