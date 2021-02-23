import json
import pandas as pd
import os
from simple_salesforce import Salesforce, SalesforceLogin, SFType
import pandas_gbq
from google.cloud.exceptions import NotFound
from google.cloud.exceptions import Forbidden
from google.oauth2 import service_account


    #gcloud creds
credentials = service_account.Credentials.from_service_account_info(
    {},
)

#simple salesforce creds (update with yours)
sf = Salesforce(username='', password='', security_token='')
print("Attempting to connect to Salesforce instance...")
print(sf)
print("Connection established.. ")
print("Running SOQL query..")

querySOQL = """SELECT yourfield FROM yourobject"""

# query records method
response = sf.query(querySOQL)
lstRecords = response.get('records')
nextRecordsUrl = response.get('nextRecordsUrl')

while not response.get('done'):
    response = sf.query_more(nextRecordsUrl, identifier_is_url=True)
    lstRecords.extend(response.get('records'))
    nextRecordsUrl = response.get('nextRecordsUrl')
print(response)
df_records = pd.DataFrame(lstRecords)
df = df_records.drop('attributes', axis=1)
print(df)

#upload to bigquery
destination_table = 'yourdestination.table'
project = 'your-project'
df.to_gbq(destination_table, project_id=project, chunksize=None, reauth=False, if_exists='replace', auth_local_webserver=False, table_schema=None, location=None, progress_bar=True, credentials=credentials)

#export to csv option
#df.to_csv(r'C:\file.csv')

