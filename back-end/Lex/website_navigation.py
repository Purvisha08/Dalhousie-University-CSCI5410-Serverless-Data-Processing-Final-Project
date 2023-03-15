from lambda_response_builder import *


def websiteNavigation(intent_request):
    intent = intent_request['sessionState']['intent']
    intent_name = intent['name']

    navigationSelection = intent['slots']['NavigationSelection']['value']['originalValue']
    print(navigationSelection)
    if navigationSelection == 'need a help':
        message = 'Go to Dashboard -> Chatbot'

    elif navigationSelection == 'more insights on recipes':
        message = 'Go to Dashboard -> Receipe Insights'

    elif navigationSelection == 'find similar recipes':
        message = 'Go to Dashboard -> Similar Receipes'

    elif navigationSelection == 'feedback polarity':
        message = 'Go to Dashboard -> Polarity on feedback'

    elif navigationSelection == 'visualization':
        message = 'Go to Dashboard -> Visualization'

    else:
        message = 'Wrong selection'

    return close(intent_name, "Fulfilled", message)