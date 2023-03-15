import json
import boto3


def authenticateUser(userName):
    lambda_client = boto3.client('lambda')
    lambda_payload = json.dumps({"userName": userName})
    print("Authentication function invoked")
    response = lambda_client.invoke(FunctionName='authentication',
                                    InvocationType='RequestResponse',
                                    Payload=lambda_payload)
    print(response)

    payload_read = response['Payload'].read().decode("utf-8")

    # https://stackoverflow.com/questions/25613565/python-json-loads-returning-string-instead-of-dictionary
    json_data = json.loads(json.loads(payload_read))
    if (json_data['user']['status'] == "LoggedOut" or json_data['user']['status'] == "LoggedIn"):
        json_data['userFound'] = True
    else:
        json_data['userFound'] = False

    return json_data
