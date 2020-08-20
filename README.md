# Grey-Noise-API

To run this Grey Noise API script, perform the following:

    python3 grey_noise_gnql_api.py 'your_api_key'
    
The user will be prompted for the following inputs:
    
    Enter your query string in GNQL format: metadata.organization:Microsoft classification:malicious
    Enter Size (max is 10000): 10
    Enter filename to write results to: new.csv

After the script completes, a CSV file will be written to the current working directory with the results of the API call.

More query examples can be found here:
https://docs.greynoise.io/#greynoise-api-gnql

