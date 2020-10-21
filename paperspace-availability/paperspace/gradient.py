#!/usr/bin/env python

import requests

class GradientAvailability(object):
    TARGET_URL = "https://api.paperspace.io/notebooks/getNotebooks?modelName=team&filter=%7B%7D&teamId={}&namespace={}"

    def __init__(self, api_key, team_id, namespace):
        self.api_key = api_key
        self.target = self.TARGET_URL.format(team_id, namespace)

    def get_free_notebooks(self):
        headers = {
            "x-api-key": self.api_key
        }
        req = requests.get(self.target, headers=headers)

        print(req.text)

        machines = req.json()["availableMachines"]

        ret = []

        for machine in machines:
            if machine["cluster"]["isFreeTier"]:
                active = machine["numActiveNodes"]
                available = machine["numAvailableNodes"]
                is_available = machine["isAvailable"]

                vm_type_map = {
                    89: "Free CPU",
                    90: "Free GPU",
                    97: "Free P5000"
                }

                vm_type = vm_type_map[machine["vmTypeId"]]

                ret.append({
                    "vm_type": vm_type,
                    "is_available": is_available,
                    "available": available,
                    "active": active,
                })

        return ret

