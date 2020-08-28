#!/usr/bin/env python
__author__ = 'MidnightInAPythonWorld'

# Check for Python3
import sys
if sys.version_info[0] != 3:
    print("[-] This script requires Python 3")
    print("[-] Exiting script")
    exit()

# stdlib
import json,os,requests,argparse

# Check for Pandas
try:
    import pandas as pd
except:
    print("[-] This script requires Pandas to be installed.")
    print("[-] Exiting script")
    exit()


def query_grey_noise(api_key,api_params):
    """ 
    This function will accept API Key (provided via argpaser) and Params from user input.
    Documentation for this API are located here: https://docs.greynoise.io/#greynoise-api-gnql
    """
    api_headers = {
            'Accept' : 'application/json' ,
            'Accept-Language' : 'en-US' ,
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko' ,
            'Accept-Encoding' : 'gzip, deflate' ,
            'Connection' : 'Keep-Alive' ,
            'key' : api_key ,
            }
    url = 'https://api.greynoise.io/v2/experimental/gnql'
    try:
        print('[*] Attempting GreyNoise API request for query: ' , api_params['query'] )
        api_requests = requests.get(url, headers = api_headers, params=api_params, timeout=15.000, verify=True)
        api_json = api_requests.json()
        print('[*] Successfully queried GreyNoise API.')
    except:
        print("[!] Failed to fetch GreyNoise API with base URL of: ", url)
    if api_json['count'] >=1:
        return api_json
    else:
        return None


def write_results_to_csv(api_data,filename):
    ''' This function will parse the data that is returned from API.
        Function is using Pandas as a quick way to write to CSV.
    '''
    for item in api_data['data']:
        del item['raw_data']
    df = pd.DataFrame(api_data['data'])
    # if file does not exist write header
    if not os.path.isfile(filename):
        df.to_csv(filename)
    else: # else it exists so append without writing the header
        df.to_csv(filename, mode='a', header=False)
    print('[*] Successfully created file: ', filename) 


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('api_key', help='The API key used to query Grey Noise API.')
    args=parser.parse_args()
    api_key = args.api_key
    api_params = {}
    api_params['query'] = input("Enter query string in GNQL format: ")
    api_params['size'] = int(input("Enter Size (max is 10000): "))
    filename = input("Enter filename to write results to: ")
    api_data = query_grey_noise(api_key,api_params)
    if api_data:
        print("[!] Search had " + str(api_data['count']) + " matches.")
        write_results_to_csv(api_data,filename)
    else:
        print("[!] Search had 0 matches.")

if __name__== "__main__":
  main()

exit()
