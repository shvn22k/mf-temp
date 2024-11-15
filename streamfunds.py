import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import numpy as np

st.title("Mutual Funds Insights")

st.image("mutualfs.png")
url = 'https://api.mfapi.in/mf'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
else:
    st.write("Error:", response.status_code)

available_funds = pd.DataFrame(data)
fundlist = list(available_funds['schemeName'])

fund_name = st.selectbox("Select Mutual Fund", fundlist)
sid = available_funds.iloc[fundlist.index(fund_name)]['schemeCode']
schemeDataUrl = f"https://api.mfapi.in/mf/{sid}"

response2 = requests.get(schemeDataUrl)

if response2.status_code == 200:
    histData = response2.json()
else:
    st.write("Error:", response2.status_code)

df = pd.DataFrame(histData['data'], columns=['date', 'nav'])
schemeHistData = df

schemeHistData['date'] = pd.to_datetime(schemeHistData['date'], format='%d-%m-%Y') 
schemeHistData['nav'] = pd.to_numeric(schemeHistData['nav'])

if st.button("Show Insights"):
    st.write(f"Displaying insights for {fund_name}")
    schemeHistData['date'] = pd.to_datetime(schemeHistData['date'])
    schemeHistData.set_index('date', inplace=True)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=schemeHistData.index, 
                             y=schemeHistData['nav'], 
                             mode='lines', 
                             name='NAV'))

    x = np.arange(len(schemeHistData['nav']))
    z = np.polyfit(x, schemeHistData['nav'], 1)
    p = np.poly1d(z)

    fig.add_trace(go.Scatter(x=schemeHistData.index, 
                             y=p(x), 
                             mode='lines', 
                             name='Trend Line', 
                             line=dict(dash='dash', color='red')))

    fig.update_layout(
        title='Scheme NAV with Trend Line',
        xaxis_title='Date',
        yaxis_title='NAV',
        legend=dict(x=0, y=1),
        template='plotly'
    )

    st.plotly_chart(fig)
