# from base64 import b64encode
from binascii import b2a_base64
import json
import requests


def pretty_print_POST(req):
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


def send_request(json_body):
    mykey = "AIzaSyAtLkPibiWLSNvanh5s7WzNQP9qPeBnCn0"
    url = f"https://vision.googleapis.com/v1/images:annotate"
    data = {"key": mykey}
    req = requests.Request(
        "POST", url, headers={"X-Custom": "Test"}, params=data, json=json_body
    )
    # response = requests.post(url, data = myobj, json=json_body)
    prepared = req.prepare()
    pretty_print_POST(prepared)
    s = requests.Session()
    response = s.send(prepared)
    return response


def create_json_body(base64_bytes):
    # ENCODING = 'utf-8'
    # base64_str = base64_bytes[2:-1].decode(ENCODING) #convert from byte string
    # print()
    # print(base64_str)
    # print()
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
                "imageContext": {"cropHintsParams": {"aspectRatios": [0.8, 1, 1.2]}},
            }
        ]
    }

    return json_dict


# def imageTo64(image="C:/Users/ishan/Documents/Python/test_img_to_txt.png"):
#         with open(image, "rb") as image_file:
#                 base64_bytes = base64.b64encode(image_file.read())
#         return base64_bytes


# class OcrService:
#     def __init__(self, http_client):
#         self.client = http_client


#     def _imageTo64(image="C:/Users/ishan/Documents/Python/test_img_to_txt.png"):
#             with open(image, "rb") as image_file:
#                 encoded_string = base64.b64encode(image_file.read())
#             return encoded_string


#     def _createJsonBody(base64):
#             ....
#             jsonBody = pythonLibrary(base64)
#             json += jsonBody
#             return json

#     def _sendRequest(json):
#             ...
#             return response

#     def _parseResponse(response):
#             ...look for '-'...
#             return #[]

#     def _addItems(listItems):
#             for item in listItems:
#                     addItem to Db
#         return 0


#     def worker(image):
#         base64 = _imageTo64(image)
#         json = _createJsonBody(base64)
#         reqest = _buildRequest(json)
#         response = self.client.post            #MOCK THIS
#         listItems = _parseResponse(response)
#         addItems(list)
#         return success/failure


# http_client = HttpClient()
# ocr_service = OcrService(http_client)
# ocr_service.convert(request.get('image'))
# base64_bytes = imageTo64() # TO DO needs image object
# print(str(base64_bytes))
# json_body = create_json_body(str(base64_bytes))


def read_image_base64(filename):
    with open(filename, "rb") as f:
        return b2a_base64(f.read(), newline=False).decode("ascii")


def make_request(inputfile="C:/Users/ishan/Documents/Python/test_img_to_txt.png"):
    """ Create a request batch (one file at a time) """
    return {
        "requests": [
            {
                "image": {"content": read_image_base64(inputfile)},
                "features": [
                    {"type": "LABEL_DETECTION", "maxResults": 10},
                    {"type": "TEXT_DETECTION", "maxResults": 10},
                    {"type": "FACE_DETECTION", "maxResults": 20},
                ],
            }
        ]
    }


def test_read_image_base64():
    res = read_image_base64("C:/Users/ishan/Documents/Python/test_img_to_txt.png")
    print(res[0:10])
    assert res[0:10] == "iVBORw0KGg"


# print(json_body)
json_body = make_request()
# print(json_body)
response = send_request(json_body)
print(response)
print(response.json())
# print(response.jsonBody)

# decode_s = base64_bytes.decode('utf-8')
# print(str(base64_bytes))


# base64str = read_image_base64("C:/Users/ishan/Documents/Python/test_img_to_txt.png")
# print(base64str)

test_read_image_base64()
