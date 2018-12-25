import json, random
import asyncio
import concurrent.futures
from docs_for_processes.document_types import tender_dt
from faker import Faker
from docs_for_processes.document_generator import DocumentReadyToAttach

fake_data = Faker('ro_RO')
format_types_1 = ['docx', 'pdf', 'doc', 'rtf', 'xls']


# tender_dt - это список типов документов для создания CN.

# for t in tender_dt:
#     f_size = random.randint(1024, 5200000)
#     dfv = random.choice(format_types_1)
#     type_d = t
#     doc = DocumentReadyToAttach(doc_size_kb=f_size, file_name=fake_data.word(), doc_format=dfv, document_type=type_d)
#     doc.create_document()
#     doc.calculate_md5_sum()
#     doc.calculate_doc_size()
#     doc.create_payload_4_registration()
#     doc.register_doc()
#     doc.upload_doc()
#     doc = doc.docs_2_cn()
#     doc = json.dumps(doc, indent=2)
#     print(doc)


def doc_upl():
    for t in tender_dt:
        f_size = random.randint(1024, 5200000)
        dfv = random.choice(format_types_1)
        type_d = t
        doc = DocumentReadyToAttach(doc_size_kb=f_size, file_name=fake_data.word(), doc_format=dfv,
                                    document_type=type_d)
        doc.create_document()
        doc.calculate_md5_sum()
        doc.calculate_doc_size()
        doc.create_payload_4_registration()
        doc.register_doc()
        doc.upload_doc()
        doc = doc.docs_2_cn()
        doc = json.dumps(doc, indent=2)
        print(doc)
        return doc


async def main():

    with concurrent.futures.ThreadPoolExecutor(max_workers=2000) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor,
                doc_upl(),
                print('1 iteration')
                )
            for i in range(200)
        ]
        for response in await asyncio.gather(*futures):
            pass

loop = asyncio.get_event_loop()
loop.run_until_complete(main())