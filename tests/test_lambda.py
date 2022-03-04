import pytest
import requests
import json
import pandas as pd

def test_get_request():
    url = "https://mbtnvb29hk.execute-api.us-west-2.amazonaws.com/getHistoricalEarnings"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    json_dict = json.loads(response.text)
    dict_df = pd.DataFrame.from_dict(json_dict)
    
    assert dict_df.shape[1] == 4
    assert "eps" in dict_df.columns
    
    
def test_post_request():
    url = "https://mbtnvb29hk.execute-api.us-west-2.amazonaws.com/predictEPS"
    
    # Open JSON file as dictionary
    with open('tests/mock_data/model_input_mock.json') as json_file:
        payload = json.load(json_file)
        
    headers = {
        'Content-Type': 'application/json'
    }
        
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    
    assert isinstance(response.text, str)
    assert response.text == str(3.3589999999999995)
    