import os
from azure.storage.blob import  BlobServiceClient, generate_blob_sas,BlobSasPermissions
from datetime import datetime, timedelta


connect_str = os.getenv('AZURESTORAGECONNECTIONSTRING')
account_name = os.getenv('ACCOUNTNAME')
account_key = os.getenv('ACCOUNTKEY')
container_name = 'data'
urls_file = 'urls.txt'

class GenerateUrl:
    """ 
    Called when new blob is uploaded to data container.
    generates sas token & url.
    Appends url to urls.txt file in same container.
    """
    def __init__(self,blob_name):
        self.blob_name = blob_name

  
    def get_blob_sas(self, account_name,account_key, container_name, blob_name):
        sas_blob = generate_blob_sas(account_name=account_name, 
                                    container_name=container_name,
                                    blob_name=self.blob_name,
                                    account_key=account_key,
                                    permission=BlobSasPermissions(read=True),
                                    expiry=datetime.utcnow() + timedelta(days=21))
        return sas_blob


    def generate_url(self):
        """ Outputs url for public read. Print statemets for debugging locally."""
        print("blob name:")
        print(self.blob_name)
        blob_sas = self.get_blob_sas(account_name,account_key, container_name, self.blob_name)
        url = f'https://{account_name}.blob.core.windows.net/{container_name}/{self.blob_name}?{blob_sas}'

        return url


    def upload_to_blob(self):
        data = self.generate_url()
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=urls_file)
        blob_client.append_block(data)

        return "urls file updated!"
