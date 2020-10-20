#!/usr/bin/env python

import os
import argparse

from datetime import datetime
from pymongo import MongoClient
from paperspace.gradient import GradientAvailability

def main(access_token, team_id, namespace, mongo_uri):
    if access_token is None:
        raise Exception("Access token (`--access-token`) cannot be null.")
    
    if team_id is None:
        raise Exception("Team id (`--team-id`) cannot be null.")

    if namespace is None:
        raise Exception("Namespace (`--namespace`) cannot be null.")

    avail = GradientAvailability(access_token, team_id, namespace)

    data = avail.get_free_notebooks()
    print(data)

    # try to save if mongo uri is provided
    if mongo_uri is not None:
        client = MongoClient(mongo_uri)
        db = client.get_default_database()

        info = db.info

        doc = {
            "type": "paperspace-free-notebooks",
            "date": datetime.utcnow(),
            "data": data
        }

        info.insert_one(doc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--access-token",
        dest="access_token",
        default=os.environ.get("ACCESS_TOKEN")
        )

    parser.add_argument("-i", "--team-id",
        dest="team_id",
        default=os.environ.get("TEAM_ID")
        )

    parser.add_argument("-n", "--namespace",
        dest="namespace",
        default=os.environ.get("NAMESPACE")
        )

    parser.add_argument("-m", "--mongo-uri",
        dest="mongo_uri",
        default=os.environ.get("MONGO_URI")
        )

    args = parser.parse_args()

    main(args.access_token, args.team_id, args.namespace, args.mongo_uri)
