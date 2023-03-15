import json
import boto3
import uuid
import ast

import os
from google.cloud import pubsub_v1
from google.auth import jwt
from lambda_response_builder import *
from authentication import *

dyn_client = boto3.client('dynamodb')


def getOrderFromDatabase(orderId):
    TABLE_NAME = 'Order'
    order = dyn_client.scan(TableName=TABLE_NAME, FilterExpression='orderId = :orderId',
                            ExpressionAttributeValues={
                                ':orderId': {'S': orderId}
                            })

    return order


def validateTrackOrderSlots(slots):
    print('in validation')
    print(slots)
    if not slots['Name']:
        print("Inside Empty Name")
        return {
            'isValid': False,
            'violatedSlot': 'Name'
        }

    userName = str(slots['Name']['value']['originalValue'])
    authentication_result = authenticateUser(userName)
    print(authentication_result)
    if (authentication_result['userFound'] == True):
        if (authentication_result['user']['status'] == 'LoggedOut'):
            return {
                'isValid': False,
                'violatedSlot': 'Name',
                'message': 'Please login to complaint.'
            }
    else:
        return {
            'isValid': False,
            'violatedSlot': 'Name',
            'message': 'User not found. Please enter valid Username.'
        }

    if not slots['OrderId']:
        print("Inside Empty orderId")
        return {
            'isValid': False,
            'violatedSlot': 'OrderId'
        }

    TABLE_NAME = 'Order'

    print(slots['OrderId']['value']['originalValue'])
    orderId = str(slots['OrderId']['value']['originalValue'])
    order = getOrderFromDatabase(orderId)

    if (order['Count'] == 0):
        return {
            'isValid': False,
            'violatedSlot': 'OrderId',
            'message': 'Please enter valid order id.'
        }
    else:
        if (order['Items'][0]['Name']['S'] != userName):
            return {
                'isValid': False,
                'violatedSlot': 'OrderId',
                'message': 'Please enter odrer id of your order.'
            }

    return {'isValid': True, 'order': order}


def trackOrder(intent_request):
    TABLE_NAME = 'Order'

    intent = intent_request['sessionState']['intent']
    intent_name = intent['name']
    slots = intent['slots']

    validation_result = validateTrackOrderSlots(slots)

    if intent_request['invocationSource'] == 'DialogCodeHook':
        return DialogCodeHookResponse(intent_name, slots, validation_result)

    if intent_request['invocationSource'] == 'FulfillmentCodeHook':

        orders = validation_result['order']
        for order in orders['Items']:
            print(order)
            message = order['orderStatus']['S']

        return close(intent_name, 'Fulfilled', message)

    return null