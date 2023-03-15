# https://stackoverflow.com/questions/70352258/python-aws-lambdas-event-body-returning-string-instead-of-my-json-object
# https://www.gcptutorials.com/post/how-to-read-files-from-s3-using-python-aws-lambda
# https://stackoverflow.com/questions/33535613/how-to-put-an-item-in-aws-dynamodb-using-aws-lambda-with-python
# https://www.gcptutorials.com/post/how-to-read-files-from-s3-using-python-aws-lambda
import json
import boto3
import uuid
from boto3.dynamodb.conditions import Key, Attr

AWS_ACCESS_KEY_ID = "AKIAWIJZ3H7VEOV42RLX"
AWS_SECRET_ACCESS_KEY = "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"
AWS_REGION = "us-east-1"

TABLE_NAME = "Recipe"


def lambda_handler(event, context):
    print(event)

    body = event["body"]

    data = json.loads(body)

    comprehend = boto3.client('comprehend')

    s3 = boto3.client("s3",
                      region_name=AWS_REGION,
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    dynamo = boto3.client("dynamodb",
                          region_name=AWS_REGION,
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    bucket_name = "food-recipes-server"

    print(data)

    try:

        text = str(s3.get_object(Bucket=bucket_name, Key=data["fileName"])["Body"].read())
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps("error occured while reading file" + str(e))
        }

    textEntities = []

    try:
        entities = comprehend.detect_entities(Text=text, LanguageCode='en')
        entities = entities['Entities']
        textEntities = [dict_item['Text'] for dict_item in entities]
    except:
        return {
            "statusCode": 500,
            "body": json.dumps("error occured while getting the named entities")
        }

    try:

        dynamo.update_item(TableName=TABLE_NAME,
                           Key={"receipeId": {"S": data["id"]}},
                           UpdateExpression="set entities = :r",
                           ExpressionAttributeValues={
                               ':r': {"S": ", ".join(textEntities)},
                           }
                           )
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps("error occured while uploading data to dynamo" + str(e))
        }

    return {
        'statusCode': 200,
        # 'headers': {'Access-Control-Allow-Origin': '*' },
        'body': json.dumps(data)
    }
