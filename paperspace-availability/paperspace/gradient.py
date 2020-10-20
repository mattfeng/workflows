#!/usr/bin/env python

import requests

class GradientAvailability(object):
    TARGET_URL = "https://api.paperspace.io/notebooks/getNotebooks?access_token={}&modelName=team&filter=%7B%7D&teamId={}&namespace={}"

    def __init__(self, access_tok, team_id, namespace):
        self.target = self.TARGET_URL.format(access_tok, team_id, namespace)

    def get_free_notebooks(self):
        req = requests.get(self.target)

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

