from database import insert_item, get_items, top_things
from flask import current_app, Blueprint, render_template, request
from json import loads
from utils import get_domain

app = Blueprint('merveilles', __name__, template_folder='templates')

@app.route("/submit", methods=['POST'])
def submit():
    url = request.json['url']
    person = request.json["person"]
    return insert_item(url, person, current_app.config["DB_FILE"])

@app.route("/intrigue", methods=['GET'])
def intrigue():
    user = request.args.get("user", "")
    items = get_items(
        lambda x: loads(x[1])["person"].lower() == user.lower(),
        current_app.config["DB_FILE"])

    return render_template("index.html", items=items, channel=current_app.config["CHANNEL"])

@app.route("/introspect", methods=['GET'])
def introspect():
    domain = request.args.get("domain", "")
    items = get_items(
        lambda x: get_domain(loads(x[1])).lower() == domain.lower(),
        current_app.config["DB_FILE"])

    return render_template("index.html", items=items, channel=current_app.config["CHANNEL"])

@app.route("/", methods=['GET'])
def root():
    items = get_items(lambda x: True, current_app.config["DB_FILE"])
    for item in items:
        if item['title'] is None or item['title'] == "":
            item['title'] = item['url']

    return render_template("index.html", items=items, channel=current_app.config["CHANNEL"])

@app.route("/top")
def top():
    items = top_things(current_app.config["DB_FILE"])
    graph_data = items[2]
    return render_template("top.html", items=items, graph_data=graph_data, channel=current_app.config["CHANNEL"])