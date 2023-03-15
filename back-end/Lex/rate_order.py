import json
import boto3
import uuid
import ast

import os
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


def validateRateOrderSlots(slots):
    print('in validation')
    print(slots)
    if not slots['UserName']:
        print("In empty username")
        return {
            'isValid': False,
            'violatedSlot': 'UserName'
        }

    userName = str(slots['UserName']['value']['originalValue'])
    authentication_result = authenticateUser(userName)
    if (authentication_result['userFound'] == True):
        if (authentication_result['user']['status'] == 'LoggedOut'):
            return {
                'isValid': False,
                'violatedSlot': 'UserName',
                'message': 'Please login to rate order.'
            }
    else:
        return {
            'isValid': False,
            'violatedSlot': 'UserName',
            'message': 'User not found. Please enter valid Username.'
        }

    if not slots['OrderId']:
        print("Inside Empty OrderId")
        return {
            'isValid': False,
            'violatedSlot': 'OrderId'
        }

    orderId = str(slots['OrderId']['value']['originalValue'])

    order = getOrderFromDatabase(orderId)

    if (order['Count'] == 0):
        return {
            'isValid': False,
            'violatedSlot': 'OrderId',
            'message': 'Please enter valid order id.'
        }

    if not slots['Rating']:
        print("Inside Empty orderId")
        return {
            'isValid': False,
            'violatedSlot': 'Rating'
        }
    rating = int(slots['Rating']['value']['originalValue'])
    if (rating < 0 or rating > 10):
        return {
            'isValid': False,
            'violatedSlot': 'Rating',
            'message': 'Please rate order between 1 and 10.'
        }
    return {'isValid': True}


def rateOrder(intent_request):
    print(intent_request)
    TABLE_NAME = 'Order'

    intent = intent_request['sessionState']['intent']
    intent_name = intent['name']
    slots = intent['slots']

    validation_result = validateRateOrderSlots(slots)

    if intent_request['invocationSource'] == 'DialogCodeHook':
        return DialogCodeHookResponse(intent_name, slots, validation_result)

    if intent_request['invocationSource'] == 'FulfillmentCodeHook':
        orderId = intent['slots']['OrderId']['value']['originalValue']
        rating = intent['slots']['Rating']['value']['originalValue']
        updateStatus = dyn_client.update_item(TableName=TABLE_NAME,
                                              Key={
                                                  'orderId': {'S': orderId}
                                              },
                                              UpdateExpression='SET #rating = :val1',
                                              ExpressionAttributeNames={'#rating': 'rating'},
                                              ExpressionAttributeValues={':val1': {'S': rating}})

        message = 'Your rating has been stored successfully.'

        return close(intent_name, 'Fulfilled', message)

    return null
