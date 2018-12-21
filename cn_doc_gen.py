import json, random
from ast import literal_eval
from docs_for_processes.document_types import planning_dt, tender_dt
from pprint import pprint, pformat
from faker import Faker
from docs_for_processes.document_generator import DocumentReadyToAttach

fake_data = Faker('ro_RO')
format_types_1 = ['docx', 'pdf', 'doc', 'rtf', 'xls']

for t in tender_dt:
    f_size = random.randint(1024, 52000000)
    dfv = random.choice(format_types_1)
    type_d = t
    doc = DocumentReadyToAttach(doc_size_kb=f_size, file_name=fake_data.word(), doc_format=dfv, document_type=type_d)
    doc.create_document()
    doc.calculate_md5_sum()
    doc.calculate_doc_size()
    doc.create_payload_4_registration()
    doc.register_doc()
    doc.upload_doc()
    doc = doc.docs_2_cn()
    doc = json.dumps(doc, indent=2)
    print(doc, ',')

