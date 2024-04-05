import json
from azure.core.exceptions import ResourceNotFoundError
from azure.ai.formrecognizer import FormRecognizerClient, FormTrainingClient
from azure.core.credentials import AzureKeyCredential

credentials = json.load(open("creds.json"))

API_KEY = credentials["API_KEY"]
ENDPOINT = credentials["ENDPOINT"]

url = "https://some_pdf_url_which_contains_tables.pdf" #or image url which contains 
                                                       #table

form_recognizer_client = FormRecognizerClient(ENDPOINT, AzureKeyCredential(API_KEY))
poller = form_recognizer_client.begin_recognize_content_from_url(url)
form_data = poller.result()

for page in form_data:
    for table in page.tables:
        for cell in table.cells:
            for item in cell.text:
                print(item)
               