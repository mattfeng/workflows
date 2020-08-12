#!/usr/bin/env python

import logging
import boto3
import random
import string
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(verbose=True)

def upload_file(fname, bucket, oname=None):
    """Upload a file to an S3 bucket.

    :param str oname: the object name (destination name).
    """

    if oname is None:
        oname = fname

    client = boto3.client("s3")

    try:
        resp = client.upload_file(fname, bucket, oname)
    except ClientError as e:
        logging.error(e)
        return False

    return True

def main():
    alphabet = string.ascii_letters

    outfile = "sample-{}.out".format(datetime.now().isoformat())

    with open(outfile, "w") as f:
        randstr = "".join(random.choice(alphabet) for _ in range(20))
        logging.info(f"random string: {randstr}")
        f.write(f"{randstr}\n")

    upload_file(outfile, "mattfeng-workflow-output")

if __name__ == "__main__":
    main()
