import requests

API_KEY = '3b9177c4128330b81a72'
API_SECRET = 'f72004d86684bd629c8ec3c3aa30c6bfda807262c40f4ec74870bef6c21593b6'

def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"
    
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "pinata_api_key": API_KEY,
        "pinata_secret_api_key": API_SECRET
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    cid = response_json.get("IpfsHash")
    return cid

def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), "get_from_ipfs accepts a cid in the form of a string"
    gateway_url = "https://fuchsia-accepted-dingo-811.mypinata.cloud/ipfs/"
    url = gateway_url + cid
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error retrieving data: {response.status_code} - {response.text}")
    
    if content_type == "json":
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            raise Exception(f"Error decoding JSON from IPFS: {e}")
    else:
        data = response.text
    
    if content_type == "json" and not isinstance(data, dict):
        raise Exception("get_from_ipfs should return a dict")
    return data
