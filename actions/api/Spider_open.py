# import requests
#
#
# def open_s(question):
#     testData = {'question': question}
#
#     response = requests.post('http://172.20.68.14:8888/', json=testData)
#     return response.text


import requests


def open_s(question):
    testData = {'question': question}

    response = requests.post('http://172.20.68.14:8888/', json=testData)
    return response.text