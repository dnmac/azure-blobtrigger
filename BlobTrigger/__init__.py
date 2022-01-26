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
        run_once = 0
        while 1:
            if run_once == 0 and myblob_name != "urls.txt": #should run once on trigger. Also avoids urls.txt upload trigger GenerateUrl
                url = GenerateUrl(myblob_name)
                url.upload_to_blob()
                print("main while")
                run_once = 1
            else:
                pass
    except Exception as e:
        print(e)