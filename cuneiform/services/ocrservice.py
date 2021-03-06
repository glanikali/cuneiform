# from base64 import b64encode
from binascii import b2a_base64
import json
import requests
from injector import inject
import os


class OcrService:
    err_code_to_message = {
        1: "Could not connect to Google Vision API",
        2: "Issue processing image",
        3: "Issue processing text in image",
    }

    @inject
    def __init__(self, http_session):
        self.session = http_session
        self.err_code = None

    def pretty_print_POST(self, req):

        print(
            "{}\n{}\r\n{}\r\n\r\n{}".format(
                "-----------START-----------",
                req.method + " " + req.url,
                "\r\n".join("{}: {}".format(k, v) for k, v in req.headers.items()),
                req.body,
            )
        )

    def send_request(self, json_dict):
        url = f"https://vision.googleapis.com/v1/images:annotate"
        mykey = os.environ.get("GOOGLE_API_KEY")
        data = {"key": mykey}
        req = requests.Request(
            "POST", url, headers={"X-Custom": "Test"}, params=data, json=json_dict
        )
        prepared = req.prepare()

        response = self.session.send(prepared)
        return response

    def create_json_body(self, base64_bytes):

        base64_str = base64_bytes
        json_dict = {
            "requests": [
                {
                    "features": [
                        {"maxResults": 50, "type": "OBJECT_LOCALIZATION"},
                        {"maxResults": 50, "type": "LABEL_DETECTION"},
                        {"maxResults": 50, "type": "DOCUMENT_TEXT_DETECTION"},
                    ],
                    "image": {"content": base64_str},
                    "imageContext": {
                        "cropHintsParams": {"aspectRatios": [0.8, 1, 1.2]}
                    },
                }
            ]
        }

        return json_dict

    def read_image_base64(self, image):
        return b2a_base64(image, newline=False).decode("ascii")

    def make_request(self, image):
        """ Create a request batch (one file at a time) """
        return {
            "requests": [
                {
                    "image": {"content": self.read_image_base64(image)},
                    "features": [
                        {"type": "LABEL_DETECTION", "maxResults": 10},
                        {"type": "TEXT_DETECTION", "maxResults": 10},
                        {"type": "FACE_DETECTION", "maxResults": 20},
                    ],
                }
            ]
        }

    def process_image(self, image):
        self.err_code = None
        json_dict = self.make_request(image)
        resp = self.send_request(json_dict)
        if resp.status_code != 200:
            print("Could not connect to google vision api")
            self.err_code = 1
            return None, self.err_code
        resp_json_dict = resp.json()
        if resp_json_dict == None:
            self.err_code = 2
            print("Issue processing image")
            return None, self.err_code

        text_annotation = resp_json_dict.get("responses")[0].get("fullTextAnnotation")

        if text_annotation == None:
            self.err_code = 3
            print("Issue processing text in image")
            return None, self.err_code

        output_text = text_annotation.get("text")
        items_list = self._parse_text(output_text)
        return items_list, self.err_code

    def _parse_text(self, str):
        if str == None:
            return None
        # Replace any special new line characters with a dash
        str_wo_nl = str.replace("\n", "-")
        # Split the string into a list, seperated by '-'
        str_ls = str_wo_nl.split("-")
        # Filter out any empty strings from the list
        str_ls = list(filter(None, str_ls))
        str_ls = [str.strip() for str in str_ls]
        return str_ls
