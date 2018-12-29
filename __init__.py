from flask import Flask, flash, make_response, render_template, request, jsonify
import json
import sys

app = Flask(__name__)


with open("static/inventory.json", "r") as file:
    inventory = json.load(file)


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
    result = "Not Found"
    for device in inventory['devices']:

        if query == device["mac"].strip().lower() \
                or query == device["serialNumber"].strip().lower():
            result = jsonify(device)
            break

        elif device["additionalData"]["deviceFullName"] is not None \
                and query == device["additionalData"]["deviceFullName"].strip().lower():
            result = jsonify(device)
            break

    return result


app.run(debug=True)

