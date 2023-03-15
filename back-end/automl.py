import json
import uuid

from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

from numpy import dot
from numpy.linalg import norm



def distance(list1, list2):
    """Distance between two vectors."""
    squares = [(p-q) ** 2 for p, q in zip(list1, list2)]
    return sum(squares) ** .5





def automl(request):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    requestData = request.get_json()

    confidence1 = predict_text_classification_single_label_sample("1018129956430",
                                                    "5873155708974792704",
                                                    requestData["first"])

    confidence2 = predict_text_classification_single_label_sample("1018129956430",
                                                    "5873155708974792704",
                                                    requestData["second"])
    print(requestData)

    print(confidence1)

    print(confidence2)

    d2 = 1 / (distance(confidence1, confidence2) * 1000)

    print(d2)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    res = {
        "similar": True if d2 > 5 else False,
        "similarity": d2
    }

    return (json.dumps(res) , 200, headers)




def predict_text_classification_single_label_sample(
    project: str,
    endpoint_id: str,
    content: str,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    instance = predict.instance.TextClassificationPredictionInstance(
        content=content,
    ).to_value()
    instances = [instance]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)

    predictions = response.predictions


    return predictions[0]["confidences"]