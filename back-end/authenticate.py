import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

# https://firebase.google.com/docs/firestore/quickstart
def lambda_handler(event, context):
    userName = event['userName']
    print(userName)
    if not firebase_admin._apps:
        cred = credentials.Certificate("key.json")
        default_app = firebase_admin.initialize_app(cred)

    db = firestore.client()
    doc_ref = db.collection('users').where('email', '==', userName)
    docs = doc_ref.get()
    print(docs)
    message = {}

    if (len(docs) == 1):

        for doc in docs:
            print(doc)
            print(doc.to_dict())
            user = doc.to_dict()
            print(user)
            message = {'user': user}

    else:
        user = {}
        user['status'] = 'No user found'
        message = {'user': user}
    print(json.dumps(message))
    return json.dumps(message)
