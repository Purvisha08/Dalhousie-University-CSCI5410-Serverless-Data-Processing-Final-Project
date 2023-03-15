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
PUB_SUB_TOPIC_NAME = 'projects/serverless-project-370320/topics/customer_complaints'
def getOrderFromDatabase(orderId):
    TABLE_NAME = 'Order'
    order = dyn_client.scan(TableName=TABLE_NAME,FilterExpression='orderId = :orderId',
        ExpressionAttributeValues={
            ':orderId': {'S': orderId}
        })

    return order

def validateComplaintOrderSlots(slots):
    if not slots['userName']:
        print("In empty username")
        return{
        'isValid':False,
        'violatedSlot':'userName'
        }

    userName = str(slots['userName']['value']['originalValue'])
    authentication_result = authenticateUser(userName)
    print(authentication_result)
    if(authentication_result['userFound']==True):
        if(authentication_result['user']['status']=='LoggedOut'):
            return {
                'isValid':False,
                'violatedSlot':'userName',
                'message': 'Please login to complaint.'
            }
    else:
        return {
                'isValid':False,
                'violatedSlot':'userName',
                'message': 'User not found. Please enter valid Username.'
            }


    if not slots['orderId']:
        print("Inside Empty OrderId")
        return {
        'isValid': False,
        'violatedSlot': 'orderId'
        }


    orderId = str(slots['orderId']['value']['originalValue'])
    order = getOrderFromDatabase(orderId)

    if(order['Count']==0):
        return {
            'isValid':False,
            'violatedSlot':'orderId',
            'message': 'Please enter valid order id.'
        }
    else:
        print("In order complaint")
        print(order['Items'])
        if(order['Items'][0]['userName']['S'] != userName):
            return {
            'isValid':False,
            'violatedSlot':'orderId',
            'message': 'Please enter odrer id of your order.'
        }

    return {'isValid':True}

def setupPubSubPublisher():
    service_account_info = {
      "type": "service_account",
      "project_id": "serverless-project-370320",
      "private_key_id": "63124e9ab52f05470b456f93e0ce10dec3ba99e0",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDPlQVXtkeO+gFp\nDCF0/l73Vj45ZOhjUqEL2SuGMyO31Z8e9JYZ+wr7126kTzwBKiONJAOs2yeGWeQI\nVR9mNULq/DAbLxqr/n7KZJtN8KkxEEP8HKM6DLNtrgls+rTAofDLwvt75VE1d+ak\n22uy+oGwYsT0mKmukRcvuvmg+CfY3RZGwlqdlPOCT2Qa3KbllSZoZLv8KXIpIde6\nDmDGzWgmOgvXCxcSVZyaA1lceGG19fWsMKVrjGFD2TQjphqQ15GbNfcbOiWRtI0v\nI2RI2K2O48AZo2KUQcJPJpts1TjiKgj1iuI6lUR0BFZEq6ZcjQ03O5mOtgj9mRdh\npT9FqxnvAgMBAAECggEAIJWsZoXa+sMc2JAKanKJlrrHfrvrzLeKRzFaZzD84N0c\nIsBTFZX2Ne0t1YYIjcg/F2c5Wnd2X10Z8gLmsGUY8YkPxhyhS7Fh1sRvKo9mB6kd\neuRF7RVUTxm8Kgq6t+hTw7CCSIMJOeLt5h/5anlvRTBj6V9Td28YHCp2CAIcQyq8\n9V1Vzb44ZsF6Z0OK7v9l2nYCJ/h48l1UbV0XMze0MBL7rB123CWYM0qJwQkpg19A\nf+8zhFo+KNzAnkAVXFUA2oVaLYiKoKQI0PF+4xahYGa32WJxwLQkNjg21DA+Pi1q\nBptD1vJ7x7nJQPg/E1vV0mGNsyOoAeK10sQGeuyzWQKBgQDpIXvR///nk6MSBLm5\nV2E6G2OUzyYrxeZH5CckPiHuJSkI/ImzlpG+SwEn2IYOj3uOyq/yUl4s14FzS1J8\n/SeB54TzAxOonrYmzIGWdTr9+wbxDVxbt95XHSYF04fJus+EiENDUplr65DMQzK5\nWEwhjAZWBIuGLyjHl43JSrA25wKBgQDj8fGcYmf28VnpVC/8yKkuzu4ml3DeX8qt\nnhljxOfDBWEyDp9sxmuB0MaRoVZcC7Ib8uRdDwI4k4nFkrHQNOfin3e23jBQQIFR\nmENST1qin9eTqIuUkyfcEA/DQ7KhBj2iOcLwAxzDMHU09NS8gGR55CJ2Jm6qiJhC\nNyobENyLuQKBgEcVlZqns1DaPHvPAw5XbWb5WPjT3PC17Ax5rdGoPFJP9F4wGpCu\n1YuvdQ/APsgLygH1HYcGxH5py6frDKDd1AERJgGvK3xbwHC+JLlKz40H0MsJZuL0\ngpAPbDuUjy/cjU/8+H17nxo//qu5xaqsGLKV7oyl4CEvGgEZ3frFkkt7AoGARW02\nktQiKEOgiAG9T/fqF7itLpHnrcNtXu4Ne6bIlEy6Kt3rTt0sd3CYWljSjdx+Ficn\nyPQ+T+8YAlZI1EqY6hx6APexrW/IM4r1zkcfKvMWXQHz6X/cnxlBQ88FxCe7dAK1\nzhaUlxrWSBfeB7/vWnTSzjusb0KFZX2Z1H6RPfkCgYEAyZ+J4/5rYWYSCGUBghDS\nUNbSVK1xN9sCqILa8F/SDXEgCzJA08WqKNKv00VU8eomcGUJDMpX5Db7M4tOlELw\nzFD44TxqaF0Dwr+IVA4qw+Sd4wtHzSNhspzvFVA4+vKl4zWluiPeAuQ5pZgLV7n7\ngS4Swp3n0vjhIyF7y5HNlNY=\n-----END PRIVATE KEY-----\n",
      "client_email": "severless-multicloud@serverless-project-370320.iam.gserviceaccount.com",
      "client_id": "102336663434443077065",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/severless-multicloud%40serverless-project-370320.iam.gserviceaccount.com"
    }

    audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"

    credentials = jwt.Credentials.from_service_account_info(
        service_account_info, audience=audience
    )

    subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

    # The same for the publisher, except that the "audience" claim needs to be adjusted
    publisher_audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
    credentials_pub = credentials.with_claims(audience=publisher_audience)

    publisher = pubsub_v1.PublisherClient(credentials=credentials_pub)
    return publisher

def getMessageForOrderComplaint(intent_request):
    TABLE_NAME = 'Order'
    intent = intent_request['sessionState']['intent']
    intent_name = intent['name']

    orderId = intent['slots']['orderId']['value']['originalValue']
    userName = intent['slots']['userName']['value']['originalValue']

    orders = dyn_client.scan(TableName=TABLE_NAME,FilterExpression='orderId = :orderId and userName = :uname',
    ExpressionAttributeValues={
        ':orderId': {'S': orderId},
        ':uname':{'S':userName}
    })
    print(orders)
    print(orderId)
    print(userName)
    restaurantId = ""

    if(orders['Count']>0):
            for order in orders['Items']:
                print(order)
                restaurantId = order['restaurantId']['S']
                restaurantOwner = order ['restaurantOwner']['S']
    restaurantId = 'vaishwipatel@gmail.com'
    message = {"orderId":orderId,"userName":userName,"restaurantId":restaurantId,"restaurantOwner":restaurantOwner}
    return message

def complaintOrder(intent_request):
    intent = intent_request['sessionState']['intent']
    intent_name = intent['name']
    slots = intent['slots']

    validation_result = validateComplaintOrderSlots(slots)

    if intent_request['invocationSource'] == 'DialogCodeHook':
        return DialogCodeHookResponse(intent_name,slots,validation_result)

    if intent_request['invocationSource'] == 'FulfillmentCodeHook':

        publisher = setupPubSubPublisher()
        message = getMessageForOrderComplaint(intent_request)
        restaurantOwner = message['restaurantOwner']

        topic_name = PUB_SUB_TOPIC_NAME

        message = json.dumps(message)

        print(message)

        message = bytes(message, 'utf-8')

        future = publisher.publish(topic_name,message, spam='eggs')
        future.result()

        siteId = os.getenv("siteId",default = "https://localhost:3000")
        siteId += "/chat?email"+restaurantOwner
        chatBotmessage = "Shortly restaurant owner will chat with you. \n You can wait for them by clicking this link: "+siteId
        return close(intent_name,"Fulfilled",chatBotmessage)

    return null

