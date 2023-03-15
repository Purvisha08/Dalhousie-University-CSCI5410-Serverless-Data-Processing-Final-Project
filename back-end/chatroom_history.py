import base64
import json
import os

from google.cloud import pubsub_v1

# Publishes a message to a Cloud Pub/Sub topic.
# https://cloud.google.com/functions/docs/samples/functions-pubsub-publish
def publish(request):
    # request_json = request.get_json(silent=True)

    # Instantiates a Pub/Sub client
    publisher = pubsub_v1.PublisherClient()
    PROJECT_ID = "serverless-project-370320"
    # topic_name = request_json.get("topic")
    message = "Message from cloud function"

    topic_name = "projects/serverless-project-370320/topics/communication_history"
    topic_name ="communication_history"

    if not topic_name or not message:
        return ('Missing "topic" and/or "message" parameter.', 400)

    print(f'Publishing message to topic {topic_name}')

    # References an existing topic
    topic_path = publisher.topic_path(PROJECT_ID, topic_name)

    message_json = json.dumps({
        'data': {'message': message},
    })
    # message_bytes = message_json.encode('utf-8')
    message_json = json.dumps(message_json)
    message_bytes = bytes(message_json, 'utf-8')

    # Publishes a message
    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()  # Verify the publish succeeded
        return ('Message published.',200)
    except Exception as e:
        print(e)
        return (e, 500)