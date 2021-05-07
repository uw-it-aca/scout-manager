# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from openpyxl import *
from django.conf import settings
from uw_spotseeker import Spotseeker
from django.core.management.base import BaseCommand
import re
import json


class Command(BaseCommand):
    help = "This performs operations to PUT items into an existing spot.\
            Only works with one file at a time!"

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        Runs the management command as required.
        """
        if options['filename']:
            workbook = options['filename'][0]
            try:
                load_workbook(workbook)
                self.addspotitems(workbook)
            except IOError:
                print "Could not open file %s!" % workbook
                print "Also make sure the spotseeker server is running."
            except Exception as e:
                print "Unexpected error occured!"
                raise
        else:
            print "A filename is needed to import data from."

    def addspotitems(self, workbook):
        wb = load_workbook(filename=workbook)
        sheet_equipment = wb['Equipment']
        sheet_types = wb['Types']
        sheet_descriptions = wb['Descriptions']

        # GET and PUT data to server.
        headers = {"X-OAuth-User": settings.OAUTH_USER,
                   "Content-Type": "application/json"}
        client = Spotseeker().get_implementation()

        # Replace <spot_id> with the appropriate spot id.
        spot_kane = client.getURL(
            "/api/v1/spot/<spot_id>",
            headers
        )
        spot_kane = json.loads(spot_kane[1])
        spot_kane["items"] = []

        spot_health = client.getURL(
            "/api/v1/spot/<spot_id>",
            headers
        )
        spot_health = json.loads(spot_health[1])
        spot_health["items"] = []

        row = 2
        while sheet_types['A' + str(row)].value:
            if sheet_types['D' + str(row)].value == "UW Student":
                item = {}
                item["name"] = sheet_types["E" + str(row)].value
                if item["name"] == "" or item['name'] is None:
                    item["name"] = "Placeholder Name"
                item["category"] = "Placeholder Category"
                item["subcategory"] =\
                    self.subcategory_manager(
                        sheet_types["B" + str(row)].value
                    )
                item["extended_info"] = {}
                item["extended_info"]["i_model"] =\
                    self.item_data_cleaner(
                        sheet_types["H" + str(row)].value
                    )
                item["extended_info"]["i_brand"] =\
                    sheet_types["G" + str(row)].value
                item["extended_info"]["i_checkout_period"] =\
                    sheet_types["I" + str(row)].value
                item["extended_info"]["i_has_access_restriction"] = "true"
                item["extended_info"]["i_access_limit_role"] = "true"
                item["extended_info"]["i_access_role_students"] = "true"
                item["extended_info"]["i_reservation_required"] = "true"
                # needs to check if data is active in equipment table?
                item["extended_info"]["i_is_active"] = "true"
                item_location = sheet_types["C" + str(row)].value
                # manages item quantity
                model = "%s %s" % (sheet_types['G' + str(row)].value,
                                   item["extended_info"]["i_model"])
                item["extended_info"]["i_quantity"] =\
                    self.i_quantity_manager(
                        model,
                        sheet_equipment,
                        sheet_types,
                        item_location
                    )
                # manages item description, manual url and reservation url
                description_id = sheet_types['K' + str(row)].value
                item = self.add_item_descriptions(
                    item,
                    description_id,
                    sheet_descriptions
                )

                if(item_location == "HS Bldg I - STF"):
                    spot_health["items"].append(item)
                elif(item_location == "KNE 035 - STF"):
                    spot_kane["items"].append(item)
                else:
                    print "No matching spot found for : " + str(item)
            row += 1

        # PUT the spots with items back on the server.
        spots = [spot_kane, spot_health]
        for spot in spots:
            headers["If-Match"] = spot["etag"]
            spot_json = json.dumps(spot)
            resp, content = client.putURL(spot["uri"],
                                          headers,
                                          spot_json)
            if resp.status == 201 or resp.status == 200:
                print "Spot " + spot['name'] +\
                      " has been updated with the items"
            else:
                print "Error " + str(resp.status) +\
                      " occured while updating the spot for " + spot['name']

    def item_data_cleaner(self, i_model_bad):
        i_model = re.split(r'([0-9]*[- ]?day)',
                           i_model_bad,
                           flags=re.IGNORECASE)
        i_model = re.split(r'[([0-9]*[/]?){1,}]',
                           i_model[0],
                           flags=re.IGNORECASE)
        return i_model[0].strip()

    def i_quantity_manager(self, model, sheet_equipment, sheet_types,
                           item_location):
        equipment_row = 2
        i_quantity = 0
        while sheet_equipment['A' + str(equipment_row)].value:
            if (sheet_equipment['E' + str(equipment_row)].value ==
               "UW Student"):
                equipment_location =\
                    sheet_equipment['D' + str(equipment_row)].value
                equipment_model =\
                    self.item_data_cleaner(
                        sheet_equipment['G' + str(equipment_row)].value
                    )
                if (equipment_location == item_location) and\
                   (equipment_model == model):
                    i_quantity += 1
            equipment_row += 1
        return i_quantity

    def subcategory_manager(self, subcategory):
        if "DSLR Accessories" in subcategory:
            subcategory = "DSLR Accessories"
        elif "Laptop Computer" in subcategory:
            subcategory = "Laptop Computer"
        return subcategory

    def add_item_descriptions(self, item, descr_id, sheet_descriptions):

        if(descr_id == ""):
            descr_id = 0

        row = 2
        while sheet_descriptions['A' + str(row)].value:
            if (sheet_descriptions['A' + str(row)].value == descr_id):
                # handle item description and it's 350 limit.
                item_description = sheet_descriptions['C' + str(row)].value
                if(len(item_description) >= 350):
                    item_description = item_description[:345] + "..."
                item["extended_info"]["i_description"] = item_description

                item["extended_info"]["i_reserve_url"] =\
                    str(sheet_descriptions['D' + str(row)].value)
                if(sheet_descriptions['E' + str(row)].value):
                    item["extended_info"]["i_manual_url"] =\
                        str(sheet_descriptions['E' + str(row)].value)
                return item
            row += 1

        # Some generic description and urls!
        item["extended_info"]["i_reserve_url"] =\
            "https://www.cte.uw.edu/stfequip/request"
        return item
