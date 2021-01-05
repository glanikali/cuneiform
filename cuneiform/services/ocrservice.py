class OcrService:
    def __init__(self, http_client):
        self.client = http_client


    def _imageTo64(image):
            return convertIMgeto64(image)


    def _createJsonBody(base64):
            ..../
            jsonBody = pythonLibrary(base64)
            json += jsonBody
            return json

    def _buildRequest(json):
            ...
            return request

    def _parseResponse(response):
            ...look for '-'...
            return #[]

    def _addItems(listItems):
            for item in listItems:
                    addItem to Db
        return 0



    def worker(image):
        base64 = _imageTo64(image)
        json = _createJsonBody(base64)
        reqest = _buildRequest(json)
        response = self.client.post            #MOCK THIS
        listItems = _parseResponse(response)
        addItems(list)
        return success/failure


http_client = HttpClient()
ocr_service = OcrService(http_client)
ocr_service.convert(request.get('image'))