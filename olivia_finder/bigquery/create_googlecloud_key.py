import os

from google.oauth2 import service_account
import googleapiclient.discovery

def create_key(service_account_email):
    '''
    Creates a new key for a service account.
    is Needed to have a key to access the Google Cloud Platform.

    Parameters
    ----------
    service_account_email : str
        Email of the service account.
    
    Returns 
    -------
    None
    '''

    # Read the base private key file.
    # We need a funcional key to use it to create a new key by code.
    # Doc: https://cloud.google.com/docs/authentication/provide-credentials-adc?hl=es-419#local-key
    curr_path = os.getcwd()
    target_directory = f'{curr_path}{os.sep}olivia_finder{os.sep}bigquery{os.sep}googlecloud_key'
    key_file = f'{target_directory}{os.sep}key.json'

    credentials = service_account.Credentials.from_service_account_file(
        filename = key_file, 
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    
    service = googleapiclient.discovery.build('iam', 'v1', credentials=credentials)

    key = service.projects().serviceAccounts().keys().create(
        name='projects/-/serviceAccounts/' + service_account_email, body={}
    ).execute()

    import base64
    json_key_file = base64.b64decode(key['privateKeyData']).decode('utf-8')

    if json_key_file:

        print('Created json key')

        # Save the key to a file at the current directory.
        account_name = service_account_email.split('@')[0]
        output_file = f'{target_directory}{os.sep}{account_name}_priv_key.json'

        with open(output_file, 'w') as f:
            f.write(json_key_file)

        print('Saved key to file: {}'.format(output_file))
    
    else:
        print('Key is not created')

create_key('libraries-io-big-query@eternal-wavelet-241808.iam.gserviceaccount.com')
