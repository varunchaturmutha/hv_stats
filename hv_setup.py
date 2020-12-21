import numpy as np
from scipy import stats
import time
import datetime
import pandas as pd

import MySQLdb as mysqldb

from bokeh.plotting import *
from bokeh.layouts import gridplot
from bokeh.models import *# Span, ColumnDataSource, LogColorMapper, ColorMapper, LogTicker, ColorBar, BasicTicker, LinearColorMapper, PrintfTickFormatter, HoverTool, CategoricalColorMapper, Range1d, Title
from bokeh.models.widgets import Tabs, Panel
from bokeh.models.glyphs import Text
import bokeh.palettes as bp
from bokeh.transform import factor_cmap

# import hail as hl
import json
import urllib
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

from pathlib import Path
from joblib import Parallel, delayed

# def sql_query(sql_select_Query):
#     import mysql.connector
#     from mysql.connector import Error
#     import pandas as pd

#     '''Return data frame obtained with SQL query in the database hv
#     '''
#     try:
#         connection = mysql.connector.connect(host='localhost',
#                                              database='hv',
#                                              user='hv_varun',
#                                              password='Helioviewer@2020')

#     #     sql_select_Query = "SELECT date_format(date, '%Y-%m-%d 00:00:00') as date, count(*) as count FROM data FORCE INDEX (date_index) WHERE sourceId={} GROUP BY date_format(date, '%Y-%m-%d 00:00:00');".format(sourceId)
#     #     sql_select_Query = "SELECT filepath, date, sourceid FROM data WHERE sourceId=%d LIMIT 20;" %sourceId
#     #     sql_select_Query = "SELECT sourceId, date_format(date, '%Y-%m-%d 00:00:00') as date, count(*) as count FROM data FORCE INDEX (date_index) WHERE sourceId=8 GROUP BY date_format(date, '%Y-%m-%d 00:00:00'), sourceId;"
# #         sql_select_Query = "SELECT date_format(timestamp, '%Y-%m-%d 00:00:00') as date, count(*) as count FROM movies GROUP BY date_format(timestamp, '%Y-%m-%d 00:00:00');"#.format(sourceId)
#     #     sql_select_Query = "SELECT date_format(date, '%Y-%m-%d 00:00:00') as date, count(*) as count FROM data FORCE INDEX (date_index) GROUP BY date_format(date, '%Y-%m-%d 00:00:00');"
#     #     sql_select_Query = "SELECT count(*) FROM data WHERE filepath LIKE '/AIA/1600/%';"
#     #     sql_select_Query = "SELECT * FROM movies LIMIT 20;"
#         cursor = connection.cursor()
#         cursor.execute(sql_select_Query)
#         records = cursor.fetchall()
#         return pd.DataFrame(records, columns=cursor.column_names)
#     except Error as e:
#         print("Error reading data from MySQL table", e)
#     finally:
#         if (connection.is_connected()):
#             connection.close()
#             cursor.close()

# def sql_hv(sourceId, obs=None):
#     query = "SELECT date_format(date, '%Y-%m-%d 00:00:00') as date, count(*) as count FROM data FORCE INDEX (date_index) WHERE sourceId={} GROUP BY date_format(date, '%Y-%m-%d 00:00:00');".format(sourceId)
#     hv = sql_query(query)
#     return hv_prepare(hv, sourceId, obs)

# def hv_prepare(hv, sourceId, obs=None):
#     if(hv.empty):
#         hv['SOURCE_ID']=[]
#         return hv
#     hv = hv.sort_values('date').reset_index(drop=True)
#     hv['date'] = pd.to_datetime(hv['date'])
#     hv = hv.set_index('date')
#     hv = hv.reindex(pd.date_range(hv.index.min(), hv.index.max(), freq='D').to_period('D').to_timestamp(), 
#                 fill_value=0)
#     hv = hv.reindex(pd.date_range(hv.index.min().replace(day=1), (hv.index.max() + pd.tseries.offsets.MonthEnd(1)), freq='D').to_period('D').to_timestamp(), 
#                 fill_value=-1)
#     hv['count'] = hv['count'].astype(int)
#     hv['date'] = hv.index
#     hv = hv.reset_index(drop=True)
#     hv.loc[hv['count']<0, 'count'] = np.nan
#     hv['Year'] = hv['date'].dt.year.astype(str) + ' ' + hv['date'].dt.month_name()
#     hv['Day'] = hv['date'].dt.day.astype(str)
#     hv['SOURCE_ID'] = sourceId
#     hv['OBS'] = obs
#     return hv

# def major_features(p, df):
#     p.line(y=np.arange(0, np.nanmax(df['count'])+1), x=pd.Timestamp('2011/06/07'), line_width=1.5, line_dash='dotdash', color='red', alpha=1, legend_label= "failed eruption (2011/06/07)")
#     p.line(y=np.arange(0, np.nanmax(df['count'])+1), x=pd.Timestamp('2013/11/28'), line_width=1.5, line_dash='dotdash', color='purple', alpha=1, legend_label= "Comet ISON (2013/11/28)")
#     p.harea(y=np.arange(0, np.nanmax(df['count'])+1), x1=pd.Timestamp('2017/09/06'), x2=pd.Timestamp('2017/09/10'), fill_color='teal', fill_alpha=1, legend_label= "large flares (2017/09/06-09)")

# def service_pause(p, df):
#     p.harea(y=np.arange(0, np.nanmax(df['count'])+1), x1=pd.Timestamp('2011/08/11'), x2=pd.Timestamp('2011/09/18'), fill_color='gray', fill_alpha=0.3, legend_label= "GSFC server repair (2011/08/11 - 2011/09/18)")
#     p.harea(y=np.arange(0, np.nanmax(df['count'])+1), x1=pd.Timestamp('2013/10/01'), x2=pd.Timestamp('2013/10/16'), fill_color='green', fill_alpha=0.3, legend_label= "U.S. Fed. Gov. shutdown (2013/10/01 - 2013/10/16)")
#     p.harea(y=np.arange(0, np.nanmax(df['count'])+1), x1=pd.Timestamp('2015/02/04'), x2=pd.Timestamp('2015/09/23'), fill_color='red', fill_alpha=0.1, legend_label= "GSFC server down (2015/02/04 - 2015/09/23)")

# def bin_width(m):

#     n = np.int(np.log10(m+1))
#     n = 10**(n-1)
#     q = np.ceil(m/(n*(36))).astype(int)
#     bw = max(q*n,1)
#     return bw#, m//n+1

from bokeh.io import export_png
# from bokeh.io import export_svgs
def plot_png(plot, filename, image_size='big'):
	if(image_size == 'small'):
		plot.toolbar.logo = None
		plot.toolbar_location = None
		plot.xaxis.axis_label_text_font_size="18pt"
		plot.yaxis.axis_label_text_font_size="18pt"
		plot.xaxis.major_label_text_font_size="15pt"
		plot.yaxis.major_label_text_font_size="15pt"
		plot.legend.label_text_font_size = "15pt"
		export_png(plot, filename="%s.png"%filename)#, height=800, width=600)
	elif(image_size == 'big'):
		plot.toolbar.logo = None
		plot.toolbar_location = None
		plot.xaxis.axis_label_text_font_size="24pt"
		plot.yaxis.axis_label_text_font_size="24pt"
		plot.xaxis.major_label_text_font_size="20pt"
		plot.yaxis.major_label_text_font_size="20pt"
		plot.legend.label_text_font_size = "20pt"
		export_png(plot, filename="%s.png"%filename)
    # plot.output_backend = "svg"
    # export_svgs(plot, filename="%s.svg"%filename)

