from flask import Flask, render_template, request, jsonify
import json
import csv


app = Flask(__name__)


with open("static/inventory.json", "r") as file:
    inventory = json.load(file)


with open("static/img/map.csv", "r") as file:
    image_map = csv.reader(file, delimiter=",")
    images = []
    for row in image_map:
        images.append(row)


def get_img(model):
    for r in images:
        if r[0] == model:
            return r[1]
    else:
        return "notfound.gif"


@app.route('/')
@app.route('/search')
def search_page():
    return render_template("search.html", title="Search")


@app.route('/about')
def about_page():
    return render_template("about.html", title="About")


# search query
@app.route('/api/search')
def rap_search():
    query = request.args.get('query', type=str).strip().lower()
    result = jsonify(error="Not Found")
    for device in inventory['devices']:

        if query == device["mac"].strip().lower() \
                or query == device["serialNumber"].strip().lower():
            device["additionalData"]["img"] = get_img(device["partNumber"])
            result = jsonify(device)
            break

        elif device["additionalData"]["deviceFullName"] is not None \
                and query == device["additionalData"]["deviceFullName"].strip().lower():
            device["additionalData"]["img"] = get_img(device["partNumber"])
            result = jsonify(device)
            break

    return result


app.run(debug=True)

