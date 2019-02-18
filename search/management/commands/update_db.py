import csv
import json
import os
import time
from search.models import Device, Image


with open("inventory/inventory.json", "r") as file:
    inventory = json.load(file)
    inventory_date = time.ctime(os.path.getmtime('inventory/inventory.json'))


with open("RAPpy/static/image_map.csv", "r") as file:
    image_map = csv.reader(file, delimiter=",")
    images = []
    for row in image_map:
        images.append(row)


for device in inventory["devices"]:

    # Get values from the image_map to determine the path for each image
    # TODO: Replace images list with a dictionary to remove need for loop.
    img_path = "notfound.png"
    for row in images:
        if device["partNumber"] == row[0] and row[1] is not "":
            img_path = row[1]
            break

    # Save record in image table
    image_model = Image(partNumber=device["partNumber"], image_path=img_path,)
    image_model.save()

    # Save record in device table
    device_model = Device(serialNumber=device["serialNumber"],
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
                          partNumber=image_model,  # Foreign key field; must pass an instance of the foreign table
                          sourceIpAddress=device["additionalData"]["sourceIpAddress"],
                          status=device["status"],
                          inventoryDate=inventory_date,
                          ).save()
