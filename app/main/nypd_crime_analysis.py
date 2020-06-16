import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title("NYPD Crime Analysis")

DATA_URL = "./files/NYPD_Arrests_Data.csv"

st.subheader('Pick the number of rows')
rows_filter = st.slider('', 0, 100000, 100)

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL,nrows=nrows)
    data['ARREST_DATE'] = pd.to_datetime(data['ARREST_DATE'])
    data.rename(columns={'PERP_RACE':'RACE',
                          'PERP_SEX':'SEX',
                        }, 
                 inplace=True)
    

    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    
    return data

data = load_data(rows_filter)
first_data_cut = data[['arrest_key', 'arrest_date', 'age_group', 'sex', 'race','latitude', 'longitude']]

first_data_cut = first_data_cut.assign(accident_count=1)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(first_data_cut)



st.subheader('Arrest By Date')
st.bar_chart(first_data_cut[['arrest_date']])
st.subheader('Arrest By Sex')
st.bar_chart(first_data_cut[['sex']])
st.subheader('Arrest By Race')
st.bar_chart(first_data_cut[['race']])

chart = (
    alt.Chart(first_data_cut[['race','accident_count','sex']])
    .mark_bar()
    .encode(x="race:O", y="sum(accident_count):Q", color="race:N", column="sex:N")
)

st.write(chart)

line_chart = (
    alt.Chart(first_data_cut[['accident_count','arrest_date']])
    .mark_line()
    .encode(x="arrest_date:O", y="sum(accident_count):Q")
)

st.write(line_chart)

alt.Chart(first_data_cut[['accident_count','arrest_date']]).transform_filter(
    'datum.symbol==="GOOG"'
).mark_area(
    line={'color':'darkgreen'},
    color=alt.Gradient(
        gradient='linear',
        stops=[alt.GradientStop(color='white', offset=0),
               alt.GradientStop(color='darkgreen', offset=1)],
        x1=1,
        x2=1,
        y1=1,
        y2=0
    )
).encode(
    alt.X('date:T'),
    alt.Y('price:Q')
)



st.subheader('Geo View')
st.map(first_data_cut)