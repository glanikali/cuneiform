# from base64 import b64encode
from binascii import b2a_base64
import json
import requests
from injector import inject


class OcrService:
    @inject
    def __init__(self, http_session):
        self.session = http_session

    def pretty_print_POST(self, req):
        """
        At this point it is completely built and ready
        to be fired; it is "prepared".

        However pay attention at the formatting used in
        this function because it is programmed to be pretty
        printed and may differ from the actual request.
        """
        print(
            "{}\n{}\r\n{}\r\n\r\n{}".format(
                "-----------START-----------",
                req.method + " " + req.url,
                "\r\n".join("{}: {}".format(k, v) for k, v in req.headers.items()),
                req.body,
            )
        )

    def send_request(self, json_dict):
        mykey = "AIzaSyAtLkPibiWLSNvanh5s7WzNQP9qPeBnCn0"
        url = f"https://vision.googleapis.com/v1/images:annotate"
        data = {"key": mykey}
        req = requests.Request(
            "POST", url, headers={"X-Custom": "Test"}, params=data, json=json_dict
        )
        prepared = req.prepare()
        # pretty_print_POST(prepared)

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

    def worker(self, image):
        json_dict = self.make_request(image)
        response = self.send_request(json_dict)
        print(response.json())


# def test_read_image_base64():
#     res = read_image_base64("C:/Users/ishan/Documents/Python/test_img_to_txt.png")
#     print(res[0:10])
#     assert res[0:10] == "iVBORw0KGg"

def ocr_service_test():
    mock_session = 