import pytest
import requests
import json
import pandas as pd

url = "https://mbtnvb29hk.execute-api.us-west-2.amazonaws.com/getHistoricalEarnings"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
json_dict = json.loads(response.text)
dict_df = pd.DataFrame.from_dict(json_dict)
print(dict_df[0])