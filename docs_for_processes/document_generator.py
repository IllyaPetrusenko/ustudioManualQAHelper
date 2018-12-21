import requests, os, hashlib, json, random
from requests.auth import HTTPBasicAuth
from docs_for_processes.document_types import planning_dt, tender_dt
from docs_for_processes.fake_data import word, dfv, dfnv, text
from pprint import pprint, pformat
from faker import Faker


class DocumentReadyToAttach:

    def __init__(self, file_name, document_type=None, process_type=None, doc_size_kb=None, doc_format=None, doc_list=None):
        self.document_type = document_type
        self.process_type = process_type
        self.doc_size_kb = doc_size_kb
        self.doc_format = doc_format
        self.file_name = file_name
        self.doc_list = doc_list

    def create_document(self):

        with open("{}/{}.{}".format('files', self.file_name, self.doc_format), 'wb') as fout:
            fout.write(os.urandom(self.doc_size_kb))
        return 'successfully done.', self.file_name

    def calculate_md5_sum(self):

        self.md5_returned = hashlib.md5(open('files/{}.{}'.format(self.file_name, self.doc_format),
                                        'rb').read()).hexdigest()
        return self.md5_returned

    def calculate_doc_size(self):

        self.size = os.path.getsize('files/{}.{}'.format(self.file_name, self.doc_format))
        return str(self.size)

    def create_payload_4_registration(self):

        self.file_name = '{}.{}'.format(self.file_name, self.doc_format)
        self.payload = {"fileName": self.file_name,
                        "hash": self.md5_returned,
                        "weight": self.size}
        self.payload = json.dumps(self.payload)

        return self.payload

    def register_doc(self):

        get_auth_token = requests.get('http://10.0.20.125:8900/api/v1/auth/signin', auth=HTTPBasicAuth('user', 'password')).json()

        self.auth_token = get_auth_token['data']['tokens']['access']

        headers = {"Authorization": 'Bearer {}'.format(self.auth_token), 'Content-Type': 'application/json'}

        self.register_data = requests.post('http://10.0.20.126:8900/api/v1/storage/registration',
                                           data=self.payload, headers=headers).json()

        self.register_data = str(self.register_data['data']['id'])
        return self.register_data

    def upload_doc(self):

        headers = {"Authorization": 'Bearer {}'.format(self.auth_token)}
        files = {'file': open('files/{}'.format(self.file_name), 'rb')}
        self.uploaded_doc = requests.post('http://10.0.20.126:8900/api/v1/storage/upload/' + self.register_data,
                                          headers=headers, files=files).json()
        return self.uploaded_doc

    def docs_2_cn(self):
        fake_data = Faker('ro_RO')
        return {
                "documentType": self.document_type,
                "id": self.uploaded_doc['data']['id'],
                "url": self.uploaded_doc['data']['url'],
                "title": fake_data.word(),
                "description": fake_data.text()
               }



for t in tender_dt:
    type_d = t
    doc = DocumentReadyToAttach(doc_size_kb=1024, file_name=word, doc_format=dfv, document_type=type_d)
    doc.create_document()
    doc.calculate_md5_sum()
    doc.calculate_doc_size()
    doc.create_payload_4_registration()
    doc.register_doc()
    doc.upload_doc()
    print(json.dumps(doc.docs_2_cn()))