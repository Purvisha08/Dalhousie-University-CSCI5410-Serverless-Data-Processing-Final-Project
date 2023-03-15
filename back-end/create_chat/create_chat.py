
from google.cloud import firestore
import base64
import json

import smtplib

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# https://medium.com/voice-tech-podcast/auto-text-classification-using-googles-automl-80f151ffa176
# https://www.aheadofthyme.com/50-best-italian-recipes/
# https://www.feastingathome.com/indian-recipes/
# https://codelabs.developers.google.com/codelabs/vertex-ai-custom-code-training#2
def send_email(receiver, subject, body):
    # Change the items with: ######Change Me#######
    gmail_user = 'khushalgondaliya020@gmail.com'
    gmail_app_password = "anfncuoclqkvubka"
    sent_from = gmail_user
    sent_to = [receiver]
    sent_subject = subject
    sent_body = body

    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sent_from
    msg['To'] = ', '.join(sent_to)
    part = MIMEText(body, "plain")
    msg.attach(part)
    msg.preamble = 'Decision'

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(sent_from, sent_to, msg.as_string())
        server.close()
        print('Email sent!')
    except Exception as exception:
        print("Error: %s!\n\n" % exception)


def chatroom(request):
    request_json = request.get_json()
    request_args = request.args

    message = base64.b64decode(request_json['message']['data']).decode('utf-8')
    message = json.loads(message)
    print(message)
    print(type(message))
    print(message.keys())
    userName = message['userName']
    restaurantOwner = message['restaurantOwner']
    orderId = message['orderId']
    '''
    {'orderId': '7da705a6-a28e-48bd-86bc-f836a932d3f5', 'userName': 'vaishwi@gmail.com', 'restaurantId': '123e4567-e89b-12d3-a456-426652340000'}

    '''

    # restaurantId = "vaishwipatel82110@gmail.com"

    db = firestore.Client()
    documentId = userName + "_" + restaurantOwner

    doc_ref = db.collection(u'chatMessages').document(documentId)
    doc_ref.set({
        u'restaurantOwner': restaurantOwner,
        u'userName': userName,
        u'messages': []
    })

    subject = "Customer needs you.."
    # https://www.educative.io/answers/what-is-osgetenv-method-in-python
    siteId = os.getenv("siteId", default="group7-halifax-foodie-ggti3p5h5q-uc.a.run.app")
    print(type(siteId))
    siteId += "/chat?email=" + userName
    body = "User " + userName + " have a complaint for orderId: " + orderId + "\nClick here to chat :" + siteId
    send_email(restaurantOwner, subject, body)

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return 'Hello {}!'.format(name)
