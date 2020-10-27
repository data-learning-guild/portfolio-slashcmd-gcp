# The Timeout problem
# - https://qiita.com/saken649/items/b70e462ae41614b72f77
# - https://dev.to/googlecloud/getting-around-api-timeouts-with-cloud-functions-and-cloud-pub-sub-47o3
# - https://github.com/abbycar/doge-a-chat

# [START functions_slack_setup]
import json
import os

from google.cloud import pubsub_v1
from slack.signature import SignatureVerifier

publisher_client = pubsub_v1.PublisherClient()

project_id = "salck-visualization"
topic_name = "user_search"
topic_path = publisher_client.topic_path(project_id, topic_name)

futures = dict()

# [START functions_verify_webhook]
def verify_signature(request):
    request.get_data()  # Decodes received requests into request.data

    verifier = SignatureVerifier(os.environ['SLACK_SECRET'])

    if not verifier.is_valid_request(request.data, request.headers):
        raise ValueError('Invalid request/credentials.')
# [END functions_verify_webhook]


# [START functions_search_queue]
def user_search_queue(request):
    """HTTP Cloud Function. Takes a Slack request and passes it to
    a second Cloud Function for processing via Pub/Sub.
    Args:
        request (flask.Request): A Slack request
    Returns:
        A response to the slack channel
    """

    if request.method != "POST":
        return "Only POST requests are accepted", 405

    verify_signature(request)
    data = json.dumps(request.form)

    futures.update({data: None})

    # When you publish a message, the client returns a future.
    future = publisher_client.publish(
        topic_path, data=data.encode("utf-8")  # data must be a bytestring.
    )

    """
    Check if future.result() resolved with the ID of the message.
    This indicates the message was successful.
    """
    try:
        print(future.result())
    except Exception as e:
        print("Error publishing: " + str(e))

    return "Working on it! 🐕"
# [END functions_search_queue]
