import uuid
import requests


class Translator(object):

    def __init__(self):
        self.key = '6e5021f027974f9dbaebb4b39c3afcf3'

    def translate(self, text, to_lang):

        base_url = 'https://api.cognitive.microsofttranslator.com'
        path = '/translate?api-version=3.0'
        params = '&to=' + to_lang
        constructed_url = base_url + path + params

        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{
            'text': text
        }]

        request = requests.post(constructed_url, headers=headers, json=body)

        if request.status_code == requests.codes.ok:
            request.encoding = 'utf-8'
            return request.json()
        else:
            raise Exception('Failed to obtain translation')
