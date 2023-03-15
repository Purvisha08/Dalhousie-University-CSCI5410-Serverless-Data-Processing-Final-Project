# https://predictivehacks.com/sentiment-analysis-with-aws-comprehend-in-python/

# https://stackoverflow.com/questions/57714143/lambda-function-to-write-to-csv-and-upload-to-s3

# https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
# https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import csv
import io

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# use creds to create a client to interact with the Google Drive API
# scope = ['https://spreadsheets.google.com']
# https://docs.google.com/spreadsheets/d/1ip87WOBNNOTz7-5ggwp-d3BBdQH5kbitv6Ae-2Iwrwo/edit?usp=sharing

AWS_ACCESS_KEY_ID = "AKIAWIJZ3H7VEOV42RLX"
AWS_SECRET_ACCESS_KEY = "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"
AWS_REGION = "us-east-1"


def lambda_handler(event, context):
    print(event)

    body = event["body"]

    data = json.loads(body)

    restaurantId = data["restaurantId"]

    comprehend = boto3.client('comprehend')

    s3 = boto3.client("s3",
                      region_name=AWS_REGION,
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    dynamo = boto3.resource("dynamodb",
                            region_name=AWS_REGION,
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    bucket_name = "food-recipes-server"

    creds = ServiceAccountCredentials.from_json_keyfile_name('config.json')
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("Data").sheet1

    sheet.clear()

    rating_sentiments = []

    index = [
        'user_id',
        'restaurant_id',
        'sentiment',
        'rating'
    ]

    csvio = io.StringIO()
    writer = csv.writer(csvio)
    writer.writerow(index)

    sheet.insert_row(index, 1)

    try:

        ratings = dynamo.Table("Feedback").scan(
            FilterExpression=Attr("restaurantId").eq(restaurantId),
        )

        print(ratings)

        for index, rating in enumerate(ratings["Items"]):
            try:
                # print(rating)
                # print(type(rating))
                sentiments = comprehend.detect_sentiment(Text=rating["feedback"], LanguageCode='en')

                res = {"userId": rating["userId"],
                       "restaurantId": rating["restaurantId"],
                       "sentiment": sentiments["Sentiment"],
                       "rating": round(sentiments["SentimentScore"]["Positive"] * 5)
                       }

                rating_sentiments.append(res)

                row = [rating["userId"],
                       rating["restaurantId"],
                       sentiments["Sentiment"],
                       int(sentiments["SentimentScore"]["Positive"] * 5) + 1
                       ]

                sheet.insert_row(row, index + 2)

                writer.writerow(row)
            except Exception as e:
                raise e
                return {
                    "statusCode": 500,
                    "body": json.dumps("error occured while getting the named entities")
                }

        s3.put_object(Body=csvio.getvalue(), ContentType='application/vnd.ms-excel', Bucket=bucket_name,
                      Key='sentiment.csv')
        csvio.close()

    except Exception as e:
        raise e
        print(str(e))
    return {
        'statusCode': 200,
        # 'headers': {'Access-Control-Allow-Origin': '*' },
        'body': json.dumps(rating_sentiments)
    }