import requests
import time
from etherscan import Etherscan
from web3 import Web3

#etherscan API auth
eth = Etherscan('NS5WPY3VNNAKZUGKQ8PVFYWM5HDZQC9ZGU')

#accept contract address user input - but in all lowercase (.lower())
input_address = str(input('Enter contract address: ')).lower()

#get contract abi
abi = eth.get_contract_abi(input_address)

#connect to node
inufa_url = 'https://mainnet.infura.io/v3/e187dce07e71440495048ced60462b0c'
web3 = Web3(Web3.HTTPProvider(inufa_url))
#check connection
web3.isConnected()

#convert to Checksum format (uppercase)
address = Web3.toChecksumAddress(input_address)
#get contact
contr = web3.eth.contract(address=address, abi=abi)

#call tokenURI method to get metadata link
token_URI_link = contr.functions.tokenURI(1).call()[:-1]

print("#############")
print('Checking Token URI...')

if 'ipfs' in token_URI_link:
    if_ipfs = 'Y'
    print('IPFS ✅')
else:
    if_ipfs = 'N'
    print('Custom ✅')

#if_ipfs = str(input(f'The Token URI is {token_URI_link}... IPFS? (Y/N): ')).upper()



if if_ipfs == 'Y':
    token_URI_link = 'https://ipfs.io/ipfs/' + token_URI_link[7:]
    keyword_only = str(input('Keyword Only? (Y/N): ')).upper()
    if keyword_only == 'N':
        ipfs_target_key = str(input('Target Key: ')).lower()
    ipfs_target_attribute = str(input('Target Attribute: ')).lower()
else:
    target_key = str(input('Target Key: ')).lower().title()
    target_value = str(input('Target Value: ')).lower().title()

start_token_search = int(input('Token ID Start: '))
end_token_search = int(input('Token ID End: '))
ids = range(start_token_search,end_token_search+1)
ids_list = list(ids)

target_ids = []
for i in ids:
    request_url = token_URI_link + str(i)
    resp = requests.get(request_url, headers = {'User-agent': 'dyl_bot_01'})
    resp.raise_for_status()
    if resp.status_code != 204:
        output = resp.json()
        #print(f"token {i} received a successful json response")
        ################## NON IPFS ##################
        if if_ipfs == 'N':
            try: 
                if output['attributes'][target_key] == target_value:
                    target_ids.append(i)
                    print(f"Token {i}✅")
                else:
                    print(f"Token {i} has no {target_key} attribute ❌")
            
                time.sleep(2)
            except KeyError as e:
                print(f'Token {i} ❌ no attr')
        ################## IPFS ##################
        else:
            values = [li['value'].lower() for li in output['attributes']]
            keys = [li['trait_type'].lower() for li in output['attributes']]
            #print(values)
            #print(keys)
            match_count = 0
            
            for index, item in enumerate(values):
                if keyword_only == 'N':
                    if item == ipfs_target_attribute and keys[index] == ipfs_target_key:
                        target_ids.append(i)
                        match_count = match_count + 1
                        print(f"Token {i} ✅")
                if item == ipfs_target_attribute:
                    target_ids.append(i)
                    match_count = match_count + 1
                    print(f"Token {i} ✅")
            if match_count == 0:
                print(f"Token {i} ❌")
            time.sleep(2)
    else:
        print(f"Token {i} received a response of {resp.status_code}")

print("#############")
print('Target Token IDs:')
print(target_ids)
