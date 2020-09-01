import csv
import json
import os
import time
from datetime import datetime
from netaddr import *
from search.models import Device, Image
from progress.bar import Bar
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Updates the inventory database using inventory.json and the image map'

    def handle(self, *args, **options):
        with open("search/inventory/inventory.json", "r") as file:
            inventory = json.load(file)
            # inventory_date = time.ctime(os.path.getmtime('search/inventory/inventory.json'))
            inventory_date = datetime.strptime(
                time.ctime(os.path.getmtime('search/inventory/inventory.json')), "%a %b %d %H:%M:%S %Y")\
                .isoformat()  # Convert to ISO8601

        with open("search/inventory/image_map.csv", "r") as file:
            image_map = csv.reader(file, delimiter=",")
            images = []
            for row in image_map:
                images.append(row)

        bar = Bar('Processing', max=len(inventory["devices"]), suffix='%(index)d/%(max)d in %(elapsed)s seconds')

        for device in inventory["devices"]:
            # Get values from the image_map to determine the path for each image
            # TODO: Replace images list with a dictionary
            img_path = "notfound.png"
            for row in images:
                if device["partNumber"] == row[0] and row[1] is not "":
                    img_path = row[1]
                    break

            # Save record in image table
            image_model = Image(partNumber=device["partNumber"], image_path=img_path, )
            image_model.save()

            # Convert MAC address to different notations
            mac_cisco_str = str(EUI(device["mac"], dialect=mac_cisco))
            mac_dashed_str = str(EUI(device["mac"], dialect=mac_unix))
            mac_bare_str = str(EUI(device["mac"], dialect=mac_bare))

            # Save record in device table
            device_model = Device(serialNumber=device["serialNumber"],
                                  mac=device["mac"],
                                  mac_cisco=mac_cisco_str,
                                  mac_dashed=mac_dashed_str,
                                  mac_bare=mac_bare_str,
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
                                  partNumber=image_model,
                                  # Foreign key field; must pass an instance of the foreign table
                                  sourceIpAddress=device["additionalData"]["sourceIpAddress"],
                                  status=device["status"],
                                  inventoryDate=inventory_date,
                                  inventoryFileDate=inventory_date,
                                  ).save()
            bar.next()
        bar.finish()

        self.stdout.write(self.style.SUCCESS('Updated database'))
