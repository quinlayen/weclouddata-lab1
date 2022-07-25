#!/usr/bin python3
"""
This is the main file for the py_cloud project if user does not have direct access to our AWS account
"""

import requests
import json
import toml
import pandas as pd
from collections import ChainMap
from dotenv import load_dotenv
import os
import boto3

def read_api(url):
    response = requests.get(url)
    return response.json()

# main function
# This is where python script will start
if __name__=='__main__':
    app_config = toml.load('config.toml')
    url = app_config['api']['url']
    
    # read the API
    print('Reading the API...')
    data=read_api(url)
    print('API Reading done')
    
    # get company names
    print('Building the dataframe...')
    company_list = [data['results'][i]['company']['name'] for i in range(len(data['results']))]
    company_name = {'company':company_list}
    
    # get locations
    location_list = [data['results'][i]['locations'][0]['name'] for i in range(len(data['results']))]
    location_name = {'locations':location_list}
    
    # get job names
    job_list = [data['results'][i]['name'] for i in range(len(data['results']))]
    job_name = {'job':job_list}
    
    # get job types
    job_type_list = [data['results'][i]['type'] for i in range(len(data['results']))]
    job_type = {'job_type':job_type_list}
    
    # get publication date
    publication_date_list = [data['results'][i]['publication_date'] for i in range(len(data['results']))]
    publication_date = {'publication_date':publication_date_list}
    
    # Merge dictionaries with ChainMap and dict "from collections import ChainMap"
    data = dict(ChainMap(company_name, location_name, job_name, job_type, publication_date))
    df = pd.DataFrame.from_dict(data)
    
    # Cut publication date to date
    df['publication_date'] = df['publication_date'].str[:10] # slice out the time so only date left
    
    # split location to city and country and drop the location column
    df['city'] = df['locations'].str.split(',').str[0]
    df['country'] = df['locations'].str.split(',').str[1]
    df.drop('locations', axis=1, inplace=True) # once the data we want is extracted (city, country) we dont want the locations column data anymore
    
    # save the dataframe to a csv file locally first
    df.to_csv('jobs.csv', index=False)
    print('dataframe saved to local')
    
    # read secret access_key of AWS from the .env file
    print('uploading to AWS S3...')
    load_dotenv()
    access_key=os.getenv('access_key')
    secret_access_key=os.getenv('secret_access_key')
    
    # upload the csv file to S3
    bucket = app_config['aws']['bucket']
    folder = app_config['aws']['folder']
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)
    s3.upload_file('jobs.csv', bucket, folder+'jobs.csv')
    
    print('File uploading done!')