import os
import requests
import time
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Downloads the Aruba Activate Inventory via API'

    def handle(self, *args, **options):
        # Activate credentials
        username = ""
        password = ""

        # Login to Activate and acquire session cookies
        login_params = {
            "url": "https://activate.arubanetworks.com/LOGIN",
            "data": {
                "credential_0": username,
                "credential_1": password,
            }
        }

        with requests.post(**login_params) as login_response:
            login_response.raise_for_status()

        # Send request for entire inventory.json
        inventory_params = {
            "url": "https://activate.arubanetworks.com/api/ext/inventory.json",
            "cookies": login_response.cookies,
            "params": {
                "action": "query",
            }
        }

        # Iterate up to five times
        downloaded = False
        tries = 0
        while downloaded is False:
            if tries >= 5:
                self.stderr.write('Too many unsuccessful attempts!')
                break
            try:
                with requests.get(**inventory_params) as inventory_response:
                    inventory_response.raise_for_status()

                    # Make a copy of existing inventory.json with date appended if exists
                    if os.path.exists('search/inventory/inventory.json'):
                        inventory_mtime = time.gmtime(os.path.getmtime('search/inventory/inventory.json'))
                        os.rename('search/inventory/inventory.json',
                                  'search/inventory/inventory_{}.json'.format(time.strftime("%m%d%Y_%H%M%S", inventory_mtime)))

                    # Write inventory.json to a file
                    with open('search/inventory/inventory.json', 'wb') as handle:
                        for block in inventory_response.iter_content():
                            handle.write(block)

                    downloaded = True

            except requests.exceptions.ChunkedEncodingError:
                self.stderr.write('ChunkedEncodingError, trying again...')
                tries += 1
                continue

        self.stdout.write(self.style.SUCCESS('Downloaded inventory.json successfully!'))
