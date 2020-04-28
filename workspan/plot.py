import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#Run plot.py and update csv name in it to plot the graph.
#Test by running code in jupyter notebook
sns.set()
csv_name = "URL_STATUS_REPORThttpsodataintelcom.csv"
df = pd.read_csv(csv_name)


df.columns = ['time', 'status','response_time']
df.time = pd.to_datetime(df.time)
df.set_index('time', inplace=True)
df.plot(figsize=(20,10), linewidth=5, fontsize=20)
plt.xlabel('DateTime', fontsize=20);
plt.ylabel('URLStatusAndResponse', fontsize=20);


