import json
import requests


class SendVehicleData:
    """
    This class will be in charge of sending and receiving messages between
    the command line application and the database.
    For documentation on requests, visit http://docs.python-requests.org/en/master/
    """

    def __init__(self, url):
        self.url = url
        self.r = None

    def put(self, data):
        """
        Uses the python requests library to put data
        Put can be used to create or update
        :param data: json vehicle data
        :return: None but the response code is stored in self.r
        """
        data_json = json.dumps(data)
        payload = {'vehicle_payload': data_json}
        self.r = requests.put(self.url + '/put', data=payload)

    def post(self, data):
        """
        Uses the python requests library to post data
        Post can be used to create data
        :param data: json vehicle data
        :return: None but the response code is stored in self.r
        """
        data_json = json.dumps(data)
        payload = {'vehicle_payload': data_json}
        self.r = requests.post(self.url + '/post', data=payload)

    def delete(self):
        self.r = requests.delete()

    def head(self):
        pass

    def options(self):
        pass

    def status_is_valid(self):
        """
        Checks if the status code of the previous request is valid
        :return: True if status is ok, false otherwise
        """
        return self.r.status_code == requests.codes.ok

    def get_status(self):
        """
        Will return the HTTP status code of the previous request and also print it
        :return: the numeric HTTP status code
        """
        if not self.status_is_valid():
            print(self.r.raise_for_status())
        else:
            print("HTTP status code: ", self.r.status_code)
            print("Additional Details:\n", self.r.text)
        return self.status_code
