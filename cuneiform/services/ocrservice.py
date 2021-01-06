import base64
import json
import requests

def send_request(json_body):
        url = 'https://vision.googleapis.com/v1/images:annotate'
        myobj = {'key': 'AIzaSyAtLkPibiWLSNvanh5s7WzNQP9qPeBnCn0'}
        response = requests.post(url, data = myobj, json=json_body)
        return response

def create_json_body(base64_bytes):
        #ENCODING = 'utf-8'
        #base64_str = base64_bytes[2:-1].decode(ENCODING) #convert from byte string
        #print()
        #print(base64_str)
        #print()
        base64_str = base64_bytes
        json_dict ={ "requests":
                        [{"features":
                                [{ "maxResults": 50,
                                "type": "OBJECT_LOCALIZATION"},
                                {"maxResults": 50,
                                "type": "LABEL_DETECTION"},
                                {"maxResults": 50,
                                "type": "DOCUMENT_TEXT_DETECTION"}
                                ],
                        "image": {"content": base64_str },
                        "imageContext":
                                {"cropHintsParams": {"aspectRatios": [0.8,1,1.2]}}
                        }]
                }

        return json_dict

def imageTo64(image="C:/Users/ishan/Documents/Python/test_img_to_txt.png"):
        with open(image, "rb") as image_file:
                base64_bytes = base64.b64encode(image_file.read())
        return base64_bytes


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


#http_client = HttpClient()
#ocr_service = OcrService(http_client)
#ocr_service.convert(request.get('image'))
base64_bytes = imageTo64() # TO DO needs image object
json_body = create_json_body(base64_bytes)
#print(json_body)
response = send_request(json_body)
print(response)
print(response.json())
print(response.jsonBody)

#decode_s = base64_bytes.decode('utf-8')
#print(str(base64_bytes))