from injector import singleton
from cuneiform.services.ocrservice import OcrService
import requests


def configure(binder):
    binder.bind(OcrService, to=OcrService(requests.Session()), scope=singleton)