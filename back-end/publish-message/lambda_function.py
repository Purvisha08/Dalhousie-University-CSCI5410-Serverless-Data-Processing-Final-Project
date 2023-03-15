import os
from google.cloud import pubsub_v1

import json
from google.auth import jwt
# https://cloud.google.com/pubsub/docs/publish-receive-messages-client-library
# https://docs.aws.amazon.com/lambda/latest/dg/nodejs-package.html
# https://cloud.google.com/pubsub/docs/publisher#python
print(jwt.__file__)

def lambda_handler(event, context):
    
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
    # topic_name = 'projects/{project_id}/topics/{topic}'.format(
    #     project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
    #     topic='MY_TOPIC_NAME',  # Set this to something appropriate.
    # )
    
    topic_name = "projects/serverless-project-370320/topics/customer_complaints"
    # publisher.create_topic(name=topic_name)
    future = publisher.publish(topic_name, b'My first message!', spam='eggs')
    future.result()
    
    return {
        "statusCode": 200,
        "body": "message published"
    }
    
if __name__ == "__main__":
    lambda_handler("a", "b")
