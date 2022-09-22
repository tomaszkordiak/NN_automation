from dataclasses import dataclass

import requests


@dataclass
class Response:
    status_code: int
    text: str
    as_dict: object
    headers: dict


class APIRequest:
    def get(self, url, auth):
        response = requests.get(url, auth=auth)
        return self.__get_responses(response)

    def post(self, url, headers, auth):
        response = requests.post(url, headers=headers, auth=auth)
        return self.__get_responses(response)

    def put(self, url, payload, headers, auth):
        response = requests.put(url, data=payload, headers=headers, auth=auth)
        return self.__get_responses(response)

    def delete(self, url, auth):
        response = requests.delete(url, auth=auth)
        return self.__get_responses(response)

    def __get_responses(self, response):
        status_code = response.status_code
        text = response.text

        try:
            as_dict = response.json()
        except Exception:
            as_dict = {}

        headers = response.headers

        return Response(status_code, text, as_dict, headers)
