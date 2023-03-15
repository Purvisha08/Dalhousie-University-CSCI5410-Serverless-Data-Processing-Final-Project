import json
import base64

# https://firebase.google.com/docs/firestore/quickstart

def lambda_handler(event, context):
    # TODO implement

    # print(event)
    body = event["body"]

    body = json.loads(body)

    print(body)
    print(type(body))

    user_email = ""

    if ("message" in body.keys()):

        message = base64.b64decode(body["message"]["data"]).decode('utf-8')
        print(message)
        message = json.loads(message)
        print(message)
        user_email = message["email"]
    else:
        user_email = body["email"]

    print(user_email)

    if not firebase_admin._apps:
        cred = credentials.Certificate("key.json")
        default_app = firebase_admin.initialize_app(cred)


    db = firestore.client()
    doc_ref = db.collection('users').where('userName', '==', user_email)
    docs = doc_ref.get()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
