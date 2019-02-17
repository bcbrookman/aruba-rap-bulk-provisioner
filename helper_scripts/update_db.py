import csv
import json
import os
import time
from db_models import *


db.connect()
db.create_tables([Device, Image])

with open("inventory/inventory.json", "r") as file:
    inventory = json.load(file)
    inventory_date = time.ctime(os.path.getmtime('inventory.json'))

with open("static/image_map.csv", "r") as file:
    image_map = csv.reader(file, delimiter=",")
    images = []
    for row in image_map:
        images.append(row)

image_model = Image()
device_model = Device()

for device in inventory["devices"]:
    device_model.replace(serialNumber=device["serialNumber"],
                         mac=device["mac"],
                         apGroupName=device["additionalData"]["apGroupName"],
                         deviceDescription=device["additionalData"]["deviceDescription"],
                         deviceFullName=device["additionalData"]["deviceFullName"],
                         deviceName=device["additionalData"]["deviceName"],
                         firstSeen=device["additionalData"]["firstSeen"],
                         folder=device["additionalData"]["folder"],
                         folderId=device["additionalData"]["folderId"],
                         lastAosVersion=device["additionalData"]["lastAosVersion"],
                         lastBootVersion=device["additionalData"]["lastBootVersion"],
                         lastSeen=device["additionalData"]["lastSeen"],
                         partCategory=device["additionalData"]["partCategory"],
                         partNumber=device["partNumber"],
                         sourceIpAddress=device["additionalData"]["sourceIpAddress"],
                         status=device["status"],
                         inventoryDate=inventory_date,
                         ).execute()

    # Get values from the image_map to determine the path for each image
    # TODO: Replace images list with a dictionary to remove need for loop.
    img_path = "notfound.png"
    for row in images:
        if device["partNumber"] == row[0] and row[1] is not "":
            img_path = row[1]
            break

    image_model.replace(partNumber=device["partNumber"],
                        image_path=img_path,
                        ).execute()

db.close()
