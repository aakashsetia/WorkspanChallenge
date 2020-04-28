# Script For Monitoring URLs


# Features!

- Monitors URLs provided in a text file.
- Send Alerts in case of URL Down.
- Provides information on:
    - URL_STATUS 
    - RESPONSE_TIME 
    - RESPONSE_CODE 
    - RESPONSE_ERROR

# How to Execute Script?

- Download this repository.
- Install Python3 and above version
- create a virtual environment and activate it.
- Run pip -r requirements.txt 
- Add all the urls to be monitored in url_list.txt file.
- Run the script "python monitor_url.py" to get csv with all the response details on urls in the url_list.txt file.
- Run the script "python monitor_by_url_timeseries.py" to get the csv with timesearies response status of each url in the url_list.txt.

# Schedule jobs 
 Make a cron and schedule these jobs periodically to get the csv files.
 # Type of csv files generated
 - One with the Name of URL having timeseries data 
 - One with the Timestamp having information of all URL consolidated.
 
# How alerts can be generated?
 Use email_alert.py to send alerts. Also a function send_alet(SUBJECT, BODY, TO, FROM) is defined and can be called upon for alerting.

 # How Longterm trends can be analysed ?
Schedule script "monitor_by_url_timeseries.py" and it will generate a csv with time and site updown respnse.
You can use a built-in pandas visualization method .plot() to plot your data from the csv generated as the data in this csv is in timeseries and 0/1 for response status.

We can send the respnse data to a data base of a logmanagment framework(like Splunk,ELK) and many analytical graphs can be plotted.

# Methods of setting up monitoring from different regions of the world

We can use a proxy to hit urls from different proxies.
Example 
>import requests

>proxies = {
>  'http': 'http://10.10.1.10:3128',
>  'https': 'http://10.10.1.10:1080' }

>requests.get('http://example.org', proxies=proxies)


# Scaling of this tool to monitor  1000s of URLs
 We are using threading in this and it is scalable and tested with 1000s of urls.
 
# How to plot a timeseries graph to analyse the url status and response time?
Run command "jupyter notebook" where the plot.py is present.
Edit plot.py with the csv you want to analyse.

Run the notebook and plot the graph.
Code to plot a graph
>import numpy as np
>import pandas as pd
>import matplotlib.pyplot as plt
>import seaborn as sns

>sns.set()
>csv_name = "URL_STATUS_REPORThttpsodataintelcom.csv"
>df = pd.read_csv(csv_name)


>df.columns = ['time', 'status','response_time']
>df.time = pd.to_datetime(df.time)
>df.set_index('time', inplace=True)
>df.plot(figsize=(20,10), linewidth=5, fontsize=20)
>plt.xlabel('DateTime', fontsize=20);
>plt.ylabel('URLStatusAndResponse', fontsize=20);



