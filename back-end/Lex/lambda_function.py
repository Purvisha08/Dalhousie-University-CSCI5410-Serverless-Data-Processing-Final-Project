import json
import boto3
import uuid
import ast

import os
from google.cloud import pubsub_v1
from google.auth import jwt

from website_navigation_intent import *
from lambda_response_builder import *
from authentication import *
from add_recipe_intent import *
from rate_order_intent import *
from complaint_order_intent import *
from track_order_intent import *


def lambda_handler(event, context):
    intent_name = event['sessionState']['intent']['name']

    print(event)
    if intent_name == 'WebsiteNavigation':
        return websiteNavigation(event)
    elif intent_name == 'AddReceipe':
        return addRecipe(event)
    elif intent_name == 'RateOrder':
        return rateOrder(event)
    elif intent_name == 'TrackOrder':
        return trackOrder(event)
    elif intent_name == 'OrderComplaint':
        return complaintOrder(event)
    else:
        print('hello')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
