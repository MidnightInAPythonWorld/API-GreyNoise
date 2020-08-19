#!/usr/bin/env python
__author__ = 'MidnightInAPythonWorld'

# Check for Python3
import sys
if sys.version_info[0] != 3:
    print("[-] This script requires Python 3")
    print("[-] Exiting script")
    exit()

# stdlib
import json,os,pprint,requests,argparse
import pandas as pd

# Silence HTTPS errors
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def query_grey_noise(api_key,api_params):
    api_headers = {}
    api_headers['Accept'] = 'application/json'
    api_headers['Accept-Language'] = 'en-US'
    api_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
    api_headers['Accept-Encoding'] = 'gzip, deflate'
    api_headers['Connection'] = 'Keep-Alive'
    api_headers['key'] = api_key
    url = 'https://api.greynoise.io/v2/experimental/gnql'
    api_requests = requests.get(url, headers = api_headers, params=api_params, timeout=15.000, verify=True)
    api_json = api_requests.json()
    return api_json


def write_results_to_csv(api_data):
    api_results = []
    for item in api_data['data']:
        ip = item['ip']
        classification=  item['classification'] 
        actor =  item['actor']
        tags = item['tags']
        api_results.append([ip,classification,actor,tags])
    df = pd.DataFrame(api_results)
    # if file does not exist write header
    if not os.path.isfile('hash_results.csv'):
        df.to_csv('api_results.csv')
    else: # else it exists so append without writing the header
        df.to_csv('api_results.csv', mode='a', header=False)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('api_key', help='The API key used to query Grey Noise API.')
    parser.add_argument('api_query', help='The Query used to query Grey Noise API.')
    parser.add_argument('api_size', help='Size of the results returned by Grey Noise API.')
    args=parser.parse_args()
    api_key = args.api_key
    api_params = {}
    api_params['query'] = args.api_query
    api_params['size'] = args.api_size
    api_data = query_grey_noise(api_key,api_params)
    write_results_to_csv(api_data)


if __name__== "__main__":
  main()


exit()
