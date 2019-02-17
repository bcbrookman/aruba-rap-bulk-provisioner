from flask import Flask, render_template, request, jsonify
import json
import csv
import os
import time
from db_models import *

db.connect()

app = Flask(__name__)

with open("inventory/inventory.json", "r") as file:
    inventory = json.load(file)
    inventory_date = time.ctime(os.path.getmtime('inventory.json'))


with open("static/image_map.csv", "r") as file:
    image_map = csv.reader(file, delimiter=",")
    images = []
    for row in image_map:
        images.append(row)


def get_img(model):
    for r in images:
        if r[0] == model and r[1]:
            return r[1]
    else:
        return "notfound.png"


@app.route('/')
@app.route('/search')
def search_page():
    return render_template("search.html", title="Search")


@app.route('/about')
def about_page():
    return render_template("about.html", title="About")


# search query
@app.route('/api/search')
def rap_search_db():
    result = {
        'devices': []
    }

    query = request.args.get('query', type=str).strip()
    resp = Device.select(Device, Image).join(Image).where(Device.deviceFullName.contains(query) |
                                                          Device.mac.contains(query) |
                                                          Device.serialNumber.contains(query) |
                                                          Device.deviceDescription.contains(query) |
                                                          Device.deviceName.contains(query)
                                                          ).dicts()

    for r in resp:
        device = {
            'additionalData': {
                'apGroupName': r['apGroupName'],
                'deviceDescription': r['deviceDescription'],
                'deviceFullName': r['deviceFullName'],
                'deviceName': r['deviceName'],
                'firstSeen': r['firstSeen'],
                'folder': r['folder'],
                'folderId': r['folderId'],
                'img': r['image_path'],
                'lastAosVersion': r['lastAosVersion'],
                'lastBootVersion': r['lastBootVersion'],
                'lastSeen': r['lastSeen'],
                'partCategory': r['partCategory'],
                'sourceIpAddress': r['sourceIpAddress'],
                },
            'firstSeen': r['firstSeen'],
            'folderId': r['folderId'],
            'inventoryDate': r['inventoryDate'],
            'lastSeen': r['lastSeen'],
            'mac': r['mac'],
            'serialNumber': r['serialNumber'],
            'partNumber': r['partNumber'],
            'status': r['status'],
            }
        result['devices'].append(device)

    # If there are no results, return Not Found error instead
    if len(result['devices']) == 0:
        result = {'error': "Not Found"}

    return jsonify(result)


app.run(debug=True)
