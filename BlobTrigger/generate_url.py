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
    Appends url to urls.txt file in different container.
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
        url = f'https://{account_name}.blob.core.windows.net/{container_name}/{self.blob_name}?{blob_sas}\n'

        return url


    def upload_to_blob(self):
        data = self.generate_url()
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_client = blob_service_client.get_container_client("urls")
        
        try:
            blob_client = container_client.get_blob_client(urls_file)
            if blob_client.exists():
                blob_client.append_block(data)
            else:
                container_client.create_container()
                # Create and write to text file
                with open(urls_file, "w") as f:
                    f.write(data)
                # Upload content to the Page Blob
                with open(urls_file, "rb") as f:
                    blob_client.upload_blob(f, blob_type="AppendBlob")

        except Exception as e:
            print(f'Unexpected error: {e}')
                
        return
