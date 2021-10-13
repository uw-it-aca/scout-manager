# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from openpyxl import *
from django.conf import settings
from uw_spotseeker import Spotseeker
from django.core.management.base import BaseCommand
import re
import json


class Command(BaseCommand):
    help = "This performs operations to import data into the database.\
            Only works with one file at a time!"

    def add_arguments(self, parser):
        parser.add_argument("filename", nargs="+", type=str)

    def handle(self, *args, **options):
        """
        Runs the management command as required.
        """
        if options["filename"]:
            workbook = options["filename"][0]
            try:
                load_workbook(workbook)
                self.importdata(workbook)
            except IOError:
                print("Could not open file %s!" % workbook)
                print("Also make sure the spotseeker server is running.")
            except Exception as e:
                print("Unexpected error occured!")
                raise
        else:
            print("A filename is needed to import data from.")

    def importdata(self, workbook):
        wb = load_workbook(filename=workbook)
        sheet_equipment = wb["Equipment"]
        sheet_types = wb["Types"]

        jsondict_kane = {
            "name": "KNE 035 - STF",
            "location": {"latitude": "47.656659", "longitude": "-122.309132"},
            "extended_info": {
                "has_whiteboards": "true",
                "app_type": "tech",
                "campus": "seattle",
            },
            "items": [],
        }
        jsondict_health = {
            "name": "HS Bldg I - STF",
            "location": {"latitude": "47.650663", "longitude": "-122.308847"},
            "extended_info": {
                "has_whiteboards": "true",
                "app_type": "tech",
                "campus": "seattle",
            },
            "items": [],
        }
        jsondict_hub = {
            "name": "HUB",
            "location": {"latitude": "47.655328", "longitude": "-122.305066"},
            "extended_info": {
                "has_whiteboards": "true",
                "app_type": "tech",
                "campus": "seattle",
            },
            "items": [],
        }
        jsondict_ougl = {
            "name": "OUGL - STF",
            "location": {"latitude": "47.656578", "longitude": "-122.310357"},
            "extended_info": {
                "has_whiteboards": "true",
                "app_type": "tech",
                "campus": "seattle",
            },
            "items": [],
        }

        row = 2
        while sheet_types["A" + str(row)].value:
            if sheet_types["D" + str(row)].value == "UW Student":
                item = {}
                item["name"] = sheet_types["E" + str(row)].value
                if item["name"] == "" or item["name"] is None:
                    item["name"] = "Placeholder Name"
                item["category"] = "Placeholder Category"
                item["subcategory"] = sheet_types["B" + str(row)].value
                item["extended_info"] = {}
                item["extended_info"]["i_model"] = self.i_model_data_manager(
                    sheet_types["H" + str(row)].value
                )
                item["extended_info"]["i_brand"] = sheet_types[
                    "G" + str(row)
                ].value
                item["extended_info"]["i_checkout_period"] = sheet_types[
                    "I" + str(row)
                ].value
                item["extended_info"]["i_has_access_restriction"] = "true"
                item["extended_info"]["i_access_limit_role"] = "true"
                item["extended_info"]["i_access_role_students"] = "true"
                item["extended_info"]["i_reservation_required"] = "true"
                # needs to check if data is active in equipment table?
                item["extended_info"]["i_is_active"] = "true"
                item_location = sheet_types["C" + str(row)].value
                item_model = "%s %s" % (
                    sheet_types["G" + str(row)].value,
                    item["extended_info"]["i_model"],
                )

                # loop through equipment table to get values for i_quantity.
                equipment_row = 2
                i_quantity = 0
                while sheet_equipment["A" + str(equipment_row)].value:
                    if (
                        sheet_equipment["E" + str(equipment_row)].value
                        == "UW Student"
                    ):
                        equipment_location = sheet_equipment[
                            "D" + str(equipment_row)
                        ].value
                        equipment_model = self.i_model_data_manager(
                            sheet_equipment["G" + str(equipment_row)].value
                        )
                        if (equipment_location == item_location) and (
                            equipment_model == item_model
                        ):
                            i_quantity += 1
                    equipment_row += 1
                item["extended_info"]["i_quantity"] = i_quantity

                if item_location == "HUB":
                    jsondict_hub["items"].append(item)
                elif item_location == "HS Bldg I - STF":
                    jsondict_health["items"].append(item)
                elif item_location == "KNE 035 - STF":
                    jsondict_kane["items"].append(item)
                elif item_location == "OUGL - STF":
                    jsondict_ougl["items"].append(item)
                else:
                    print("INVALID DATA : " + item)
            row += 1

        # Post data to database.
        headers = {
            "X-OAuth-User": settings.OAUTH_USER,
            "Content-Type": "application/json",
        }
        jsondicts = [
            jsondict_hub,
            jsondict_ougl,
            jsondict_health,
            jsondict_kane,
        ]
        client = Spotseeker().get_implementation()
        for jsondict in jsondicts:
            space_json = json.dumps(jsondict)
            resp, content = client.postURL(
                "/api/v1/spot/", headers, space_json
            )
            if resp.status == 201:
                print("A spot for " + jsondict[
                    "name"
                ] + " has been created on " + resp["location"])
            else:
                print("Error " + str(
                    resp.status
                ) + " occured while creating a spot for " + jsondict["name"])

    def i_model_data_manager(self, i_model_bad):
        i_model = re.split(
            r"([0-9]*[- ]?day)", i_model_bad, flags=re.IGNORECASE
        )
        i_model = re.split(
            r"[([0-9]*[/]?){1,}]", i_model[0], flags=re.IGNORECASE
        )
        return i_model[0].strip()
