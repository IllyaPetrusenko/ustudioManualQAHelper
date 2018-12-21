import json
from docs_for_processes.document_types import planning_dt, tender_dt
from docs_for_processes.fake_data import word, dfv, dfnv, text
from pprint import pprint, pformat
from faker import Faker
from docs_for_processes.document_generator import DocumentReadyToAttach

fake_data = Faker('ro_RO')

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

