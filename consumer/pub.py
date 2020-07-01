import os
import time
from google.cloud import pubsub_v1

project_id = os.environ["PROJECT"]
topic_id = os.environ["TOPIC_NAME"]

client = pubsub_v1.PublisherClient()
topic_path = client.topic_path(project_id, topic_id)
data = b"Hello world!"

ref = {"num_messages": 0}

def callback(x, data, ref):
    try:
        print("Published message {} now has message ID {}".format(
            data, x.result()
        ))
        ref["num_messages"] += 1
    except Exception as e:
        print("An error occured")
        print(e)
        print("data:")
        print(data)
        print("exception:")
        print(x.exception())
        raise


while True:
    api_future = client.publish(topic_path, data=data)
    api_future.add_done_callback(lambda x: callback(x, data, ref))
    while api_future.running():
        time.sleep(1)
        print("published {} messages".format(ref["num_messages"]))