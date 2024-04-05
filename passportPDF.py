import requests


if __name__=="__main__":

endpoint = "https://passportpdfapi.com/api/document/DocumentLoadFromURI"

headers = {
"X-PassportPDF-API-Key" : "YOUR-PASSPORT-CODE",
}

data = {
"URI" : "https://passportpdfapi.com/test/invoice_with_barcode.pdf"
}

response = requests.post(endpoint, json=data, headers=headers)

if(response.status_code == 200):

json_response = response.json()
file_id = json_response["FileId"]

data = {
"FileId" : file_id,
"PageRange" : "1"
}

# Extract barcode
read_barcodes_endpoint = "https://passportpdfapi.com/api/pdf/ReadBarcodes"
barcodes_response = requests.post(read_barcodes_endpoint, json=data, headers=headers)

if(barcodes_response.status_code == 200):
print(barcodes_response.json())
else:
print("Something went wrong when trying to read barcodes!")

# Close document
close_document_endpoint = "https://passportpdfapi.com/api/document/DocumentClose"
close_response = requests.post(close_document_endpoint, json={"FileId" : file_id}, headers=headers)

if(close_response.status_code == 200):
print("Document closed successfully.")
else:
print("Could not close document!")

else:
print("Something went wrong!")