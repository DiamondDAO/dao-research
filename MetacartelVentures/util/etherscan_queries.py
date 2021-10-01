import json
import requests as r
import os

# get block number from a timestamp
def get_block_from_timestamp(timestamp):

    etherscan_api_url = """
    https://api.etherscan.io/api
        ?module=block
        &action=getblocknobytime
        &timestamp=
        &closest=after
        &apikey=
        """

    etherscan_api_url = etherscan_api_url.replace("\n", "")
    etherscan_api_url = etherscan_api_url.replace(" ", "")
    etherscan_api_url = etherscan_api_url.replace("&timestamp=", f"&timestamp={timestamp}")
    etherscan_api_url = etherscan_api_url.replace("&apikey=", f"&apikey={os.environ.get('ETHERSCAN_API_KEY')}")

    response = json.loads(r.get(etherscan_api_url).text)

    if response["status"] == "0":
        raise Exception(f"Etherscan query failed. Error is: {response['result']}.")

    return response["result"]


# get block number from a timestamp
def get_timestamp_from_block(block):

    etherscan_api_url = """
    https://api.etherscan.io/api
        ?module=block
        &action=getblockreward
        &blockno=
        &apikey=
        """

    etherscan_api_url = etherscan_api_url.replace("\n", "")
    etherscan_api_url = etherscan_api_url.replace(" ", "")
    etherscan_api_url = etherscan_api_url.replace("&blockno=", f"&blockno={block}")
    etherscan_api_url = etherscan_api_url.replace("&apikey=", f"&apikey={os.environ.get('ETHERSCAN_API_KEY')}")

    response = json.loads(r.get(etherscan_api_url).text)

    if response["status"] == "0":
        raise Exception(f"Etherscan query failed. Error is: {response['result']}.")

    return response["result"]["timeStamp"]
