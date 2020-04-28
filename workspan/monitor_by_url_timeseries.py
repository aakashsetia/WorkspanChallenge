#!/usr/bin/python3

import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
import requests
import csv
import threading
from pathlib import Path 
import time

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

#    current_time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    current_time = datetime.now()
    try:
        req = requests.get(url, timeout=5)
        req.raise_for_status()
        req_code = req.status_code

        if req_code == 200:
           req_status = 1
           req_response_time = req.elapsed.total_seconds()
        else:
            req_status = 0
            req_response_time = 0

        csv_writer(url,current_time,req_status,req_response_time)
        
    except requests.exceptions.HTTPError as e:
        print ("HTTP error: ", e)
        req_status = 0
        req_response_time = 0
        req_code = 0

        csv_writer(url,current_time,req_status,req_response_time)
 
    except requests.exceptions.ConnectionError as e:
        print ("Error connecting: ", e)
        req_status = 0
        req_response_time = 0
        req_code = 0

        csv_writer(url,current_time,req_status,req_response_time)

    except requests.exceptions.Timeout as err03:
        print ("Timeout error:", e)
        req_status = 0
        req_response_time = 0
        req_code = 0

        csv_writer(url,current_time,req_status,req_response_time)

    except requests.exceptions.RequestException as e:
        print ("RequestException Error : ", e)  
        req_status = 0
        req_response_time = 0
        req_code = 0

        csv_writer(url,current_time,req_status,req_response_time)
# To create and write in a csv file.   
def csv_writer(url,current_time,req_status,req_response_time):

    report_file = "URL_STATUS_REPORT"+url.replace('/', '').replace('.','').replace(':','')+".csv"
    fields = ['DateTime', 'STATUS','RESPONSE_TIME' ]
    if Path(report_file).is_file():

          with open(report_file, mode='a+') as csvfile:
             csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
             csvwriter.writerow([current_time,req_status,req_response_time])
    else:

          with open(report_file, mode='w') as csvfile:
              csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
              csvwriter.writerow(fields)
              csvwriter.writerow([current_time,req_status,req_response_time])



url_list = get_url_list("url_list.txt")
batch_size = 30
split_url_list = [url_list[i:i + batch_size] for i in range(0, len(url_list), batch_size)]
for batch_url_list in split_url_list:
    threads = list()
    for url in batch_url_list:
            print (url)
            thread = threading.Thread(target = get_url_status_responsetime ,args=(url,))
            thread.start()
            threads.append(thread)
    for thread in threads:
            thread.join()
    time.sleep(3)
                        










    
