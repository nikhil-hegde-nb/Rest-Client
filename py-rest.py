# python program for simple rest client
"""
How to run the code?

1. Create a JSON file with the below structure. 
    {
        "url":"https://reqres.in/api/users",
        "method": "GET",
        "params": {"page":1},
        "header": {"ContentType": "application/json"},
        "data": {}
        "auth": {"username": "", "password": ""}
    }
    Note: Only url and method are mandatory attributes
    Save as input.json
2. To run the file 
    "python3 py-rest.py --file-name input.json"
    or
    "python3 py-rest.py -f input.json"
"""

import json
from requests import Request, Session
import urllib3
from requests.auth import HTTPBasicAuth
from argparse import ArgumentParser

urllib3.disable_warnings()


class RequestObj:
    def __init__(
        self,
        method: str,
        url: str,
        header: dict = None,
        auth: HTTPBasicAuth = None,
        data: dict = None,
        params: dict = None,
    ):
        self.method = method
        self.url = url
        self.header = header
        self.auth = auth
        self.data = data
        self.params = params

    @classmethod
    def from_json_file(cls, filename: str):
        data = None
        try:
            with open(filename, "r") as file:
                data = json.load(file)
        except Exception as e:
            print(e)
            exit(1)

        if data.get("auth"):
            return cls(
                method=data.get("method"),
                url=data.get("url"),
                header=data.get("header"),
                auth=HTTPBasicAuth(data.get("username"), data.get("password")),
                data=data.get("data"),
                params=data.get("params"),
            )
        else:
            return cls(
                method=data.get("method"),
                url=data.get("url"),
                header=data.get("header"),
                data=data.get("data"),
                params=data.get("params"),
            )

    def __str__(self):
        value = f"method: {self.method}\nurl: {self.url}"
        if self.header:
            value += f"\nheader: {self.header}"
        if self.auth:
            value += f"\nauth: {self.auth}"
        if self.data:
            value += f"\ndata: {self.data}"
        if self.params:
            value += f"\nparams: {self.params}"
        return value


class RestClient:
    def __init__(self, req: RequestObj):
        self.req = req

    def send(self):
        with Session() as session:
            if self.req.params:
                req = Request(self.req.method, self.req.url, params=self.req.params)
            else:
                req = Request(self.req.method, self.req.url)
            prepared_req = req.prepare()
            if self.req.header:
                prepared_req.headers = self.req.header
            if self.req.auth:
                prepared_req.auth = self.req.auth
            if self.req.data:
                prepared_req.data = json.dumps(self.req.data)
            response = session.send(prepared_req, verify=False)
            return response


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-f", "--file-name", type=str, help="JSON file path", required=True
    )
    args = parser.parse_args()
    if args.file_name:
        req_obj = RequestObj.from_json_file(args.file_name)
        print(req_obj)
        rc = RestClient(req_obj)
        response = rc.send()
        print(f"status code: {response.status_code}")
        if response.status_code >= 200 and response.status_code <= 300:
            print(f"response: \n{response.text}")
        else:
            print(f"response: \n{response.reason}")


if __name__ == "__main__":
    main()
