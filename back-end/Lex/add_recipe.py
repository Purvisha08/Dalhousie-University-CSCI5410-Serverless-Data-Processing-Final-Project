import json
import boto3
import uuid
import ast

import os
from lambda_response_builder import *
from authentication import *

dyn_client = boto3.client('dynamodb')


def validateAddRecipeSlots(slots):
    print('in validation')
    print(slots)
    if not slots['UserName']:
        print("Inside Empty UserName")
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
                'message': 'Please login to add recipe.'
            }
        elif (authentication_result['user']['type'] != 'Restaurateur'):
            return {
                'isValid': False,
                'violatedSlot': 'UserName',
                'message': 'You are not authorized to add recipe.'
            }

    else:
        return {
            'isValid': False,
            'violatedSlot': 'UserName',
            'message': 'User not found. Please enter valid Username.'
        }

    if not slots['Restaurant']:
        print("Inside Empty Restaurant")
        return {
            'isValid': False,
            'violatedSlot': 'Restaurant'
        }
    if not slots['RecipeName']:
        print("Inside Empty RecipeName")
        return {
            'isValid': False,
            'violatedSlot': 'RecipeName'
        }
    if not slots['Price']:
        print("Inside Empty Price")
        return {
            'isValid': False,
            'violatedSlot': 'Price'
        }
    price = int(slots['Price']['value']['originalValue'])

    if (price < 0):
        return {
            'isValid': False,
            'violatedSlot': 'Price',
            'message': 'Price must be positive.'
        }
    return {'isValid': True}


def addRecipe(intent_request):
    TABLE_NAME = 'Recipe'

    intent = intent_request['sessionState']['intent']
    intent_name = intent['name']
    slots = intent['slots']

    validation_result = validateAddRecipeSlots(slots)

    if intent_request['invocationSource'] == 'DialogCodeHook':
        return DialogCodeHookResponse(intent_name, slots, validation_result)

    if intent_request['invocationSource'] == 'FulfillmentCodeHook':
        userName = intent['slots']['UserName']['value']['originalValue']
        restaurant = intent['slots']['Restaurant']['value']['originalValue']
        recipeName = intent['slots']['RecipeName']['value']['originalValue']
        price = intent['slots']['Price']['value']['originalValue']

        item = {'receipeId': {'S': str(uuid.uuid4())},
                'restaurant': {'S': restaurant},
                'recipeName': {'S': recipeName},
                'price': {'S': price}
                }

        response = dyn_client.put_item(TableName=TABLE_NAME, Item=item)

        message = 'Receipe successfully added.'
        return close(intent_name, 'Fulfilled', message)

    return null


