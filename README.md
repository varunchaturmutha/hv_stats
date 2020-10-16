# hv_stats

You can find coverages and histograms in the link below. More plots to follow.

https://varunchaturmutha.github.io/hv_stats/

# Installation

Download hv_stats.py, cred.txt, embed.csv

Run in Python3.7.4 (or >v3)

### Use the following command to install the required packages

pip3 install numpy scipy datetime pandas  mysql-connector-python bokeh==2.2.1  matplotlib pathlib joblib

# SQL Credentials
Expecting either of the two files to contain SQL database credentials:

"/var/www/api.helioviewer.org/install/settings.cfg" 
OR
"./cred.cfg"
in the following format:

### config file
[database]
dbhost = "host"<br />
dbname = "name"<br />
dbuser = "user"<br />
dbpass = "password"<br />

### end of config file
