#!/usr/bin/python3

import os
import time
import smtplib
from email.message import EmailMessage
from datetime import datetime
import requests
import csv
import threading 
import multiprocessing.pool as mpool
import socket

_db_lock=threading.Lock()
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

# Get list of the url by reading the txt file
def get_url_list(filename):

    url_list = []
    with open(filename,'r') as file:
        for line in file:
           url_list.append(line.rstrip("\n"))
    return url_list

# send email function for alerting
def send_alet(SUBJECT, BODY, TO, FROM):


    msg = EmailMessage()
    msg['Subject'] = SUBJECT
    msg['From'] =   FROM
    msg['To'] = TO
    msg.set_content(BODY)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
         smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
         smtp.send_message(msg)

# Provides the reponse details of a URL passed to it.
def get_url_status_responsetime(url):

    current_time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

    try:
        req = requests.get(url, timeout=5)
        req.raise_for_status()
        req_code = req.status_code

        if req_code == 200:
           req_status = "Up"
           req_response_time = req.elapsed.total_seconds()
        else:
            req_status = "Down"
            req_response_time = "NA"


        csvwriter.writerow([current_time,url,req_status,req_response_time,req_code,'NA'])
    except requests.exceptions.HTTPError as e:
  
        req_status = "Down"
        req_response_time = "NA"
        req_code = "NA"

        csvwriter.writerow([current_time,url,req_status,req_response_time,req_code,e])
 
    except requests.exceptions.ConnectionError as e:

        req_status = "Down"
        req_response_time = "NA"
        req_code = "NA"

        csvwriter.writerow([current_time,url,req_status,req_response_time,req_code,e])

    except requests.exceptions.Timeout as err03:

        req_status = "Down"
        req_response_time = "NA"
        req_code = "NA"

        csvwriter.writerow([current_time,url,req_status,req_response_time,req_code,e])

    except requests.exceptions.RequestException as e:
  
        req_status = "Down"
        req_response_time = "NA"
        req_code = "NA"

        csvwriter.writerow([current_time,url,req_status,req_response_time,req_code,e])
   

    except requests.exceptions.ReadTimeout as e: 
        req_status = "Down"
        req_response_time = "NA"
        req_code = "NA"

        csvwriter.writerow([current_time,url,req_status,req_response_time,req_code,e])
    


url_list = get_url_list("url_list.txt")
#TO run a batch of n number for url check
batch_size = 30
split_url_list = [url_list[i:i + batch_size] for i in range(0, len(url_list), batch_size)]
#Headers
fields = ['DateTime','URL', 'STATUS','RESPONSE_TIME', 'RESPONSE_CODE', 'RESPONSE_ERROR' ]
current_time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
report_file = "URL_STATUS_REPORT"+current_time+".csv"
with open(report_file, mode='w') as csvfile:
              
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(fields) 

        
        for batch_url_list in split_url_list:

            threads = list()
            for url in batch_url_list:
            #Threading to handle 1000s of requests.
                thread = threading.Thread(target = get_url_status_responsetime ,args=(url,))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()
            time.sleep(5)

                        










    
