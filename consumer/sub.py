from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

import os

project_path = os.environ["PROJECT"]
subscription_id = "worker1"

def callback(message):
    head = "*" * 20 + " START MESSAGE " + "*" * 20
    print(head)
    print(
        "Recv message {} of message ID {}".format(
            message, message.message_id
            )
    )
    message.ack()
    print("Ack message {}".format(message.message_id))
    print("*" * len(head))

print(project_path)
print(subscription_id)

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(
    project_path,
    subscription_id
)

streaming_pull_future = subscriber.subscribe(
    subscription_path, callback=callback
)

print("Listening for messages on {}".format(subscription_path))

with subscriber:
    try:
        streaming_pull_future.result(timeout=100)
    except Exception as e:
        print("Error, canceling")
        print(e)
        streaming_pull_future.cancel()