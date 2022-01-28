import logging
import os
import azure.functions as func
from .generate_url import GenerateUrl


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")


    myblob_name = myblob.name.replace("data/", "") # Remove path from blob name. Not able to do in function.json
    print(myblob_name)

    try:
        url = GenerateUrl(myblob_name)
        url.upload_to_blob()
    except Exception as e:
        print(f'Exception has occured: {e}')