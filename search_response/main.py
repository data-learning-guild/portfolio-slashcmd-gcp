# The Timeout problem
# - https://qiita.com/saken649/items/b70e462ae41614b72f77
# - https://dev.to/googlecloud/getting-around-api-timeouts-with-cloud-functions-and-cloud-pub-sub-47o3
# - https://github.com/abbycar/doge-a-chat
# - https://api.slack.com/reference/surfaces/formatting
# - https://app.slack.com/block-kit-builder

# [START functions_slack_setup]

import os
import time
import requests
import json

from google.cloud import pubsub_v1

import base64


class UserSearchException(Exception):
    pass

class MentaikoApiException(UserSearchException):
    pass


publisher_client = pubsub_v1.PublisherClient()

project_id = "salck-visualization"
topic_name = "user_search"
topic_path = publisher_client.topic_path(project_id, topic_name)

futures = dict()

# [START functions_send_message_to_slack]
def send_message(response_url, api_response):
    """ Sends a formatted message back to the Slack channel containing
    the recommendation list.
    Args:
        timestamp (string): The current time in the format yyyymmdd-hhmmss
        response_url (string): The URL location where the Slack interaction occurred.
    """
    
    # make slack friendly message
    recommended_users = api_response['recommended_users']
    recommended_users_str = ""
    for ru in recommended_users:
        recommended_users_str += '> {0}(<@{1}>)\t{2}\n'.format(ru['name'], ru['user_id'], ru['score'])
    
    kw = api_response['kw']
    msg_str_markdown = " *{}* に関連度の高いユーザー一覧\n".format(kw)
    msg_str_markdown += recommended_users_str

    message = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": msg_str_markdown
                }
            }
        ]
    }
    
    requests.post(
        response_url, json=message, headers={"Content-type": "application/json"}
    )
# [END functions_send_message_to_slack]

# [START functions_call_recommendation_api]
def call_recommendation_api(request):
    # parse slash cmd args
    args = request['text'].split(' ')
    keyword = args[0]
    max_list_size = 3
    if len(args) > 1:
        args_max_list_size = int(args[1])
        # 負荷を考えて最大でも20以下とする
        if args_max_list_size < 21:
            max_list_size = args_max_list_size
    
    print('kw: {0}\nmax: {1}'.format(keyword, max_list_size))

    try:
        # request to mentaiko-api and get result
        api_entrypoint = 'https://mentaiko-api-dot-salck-visualization.appspot.com/users/search'
        params = {'kw': keyword, 'max': max_list_size}
        response = requests.get(api_entrypoint, params=params)
    except :
        raise MentaikoApiException("Mentaiko Err")

    json_data = response.json()
    print(request['response_url'])
    print(json_data)

    return json_data
# [END functions_call_recommendation_api]

# [START functions_slack_search]
def user_search_response(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
        Detail.
            - request to mentaiko-api
            - get recommendation result
            - return result to slack
        Args:
            event (dict): The data associated with the Pub/Sub event.
            context (google.cloud.functions.Context): The metadata for the Cloud Function
        Returns:
            A response message to the slack channel containing the dogefied image.
    """
    request = json.loads(base64.b64decode(event["data"]).decode("utf-8"))

    try:
        json_data = call_recommendation_api(request)
    except UserSearchException as e:
        requests.post(
            request["response_url"],
            json={"text": "❌ " + str(e) + " ❌"},
            headers={"Content-type": "application/json"},
        )
        return

    return send_message(request['response_url'], json_data)
# [END functions_slack_search]


