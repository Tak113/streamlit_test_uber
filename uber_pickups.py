import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

# this is for converting to time format in the data
DATE_COLUMN = 'date/time'
#this data has over 1M
DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# caching data so we could avoid data re-load when we refresh
# load the data
@st.cache
def load_data(nrows):
	data = pd.read_csv(DATA_URL, nrows=nrows)
	lowercase = lambda x: str(x).lower()
	data.rename(lowercase, axis='columns', inplace=True)
	data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN]) #convert to time format
	return data

# create a text commement and let the reader know the data is loading
data_load_state = st.text('Loading data...')
# load 10,000 rows of data into the dataframe
data = load_data(10000)
#notiy the reader that the data was successfully loaded
data_load_state.text('Loading data...done!')

# see raw data
if st.checkbox('Show raw data'):
	st.subheader('Raw data')
	st.write(data)

# draw a histogram
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
	data[DATE_COLUMN].dt.hour, bins = 24, range =(0,24))[0]
st.bar_chart(hist_values)

# plot data on a map
st.subheader('Map of all pickups')
st.map(data)

# filter results with a slider
# st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.subheader('Map of all pickups at an hour from slider')
hour_to_filter = st.slider('hour', 0,23,17) #in: 0h, mad: 23h, default:17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.map(filtered_data)


