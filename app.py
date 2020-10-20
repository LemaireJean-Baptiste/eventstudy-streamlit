import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import eventstudy as es
import datetime


#st.beta_set_page_config(layout="wide")

es.Single.import_returns('returns.csv')

dates = es.Single._parameters["returns"]["date"]


def np_to_datetime(datetime64):
    unix_epoch = np.datetime64(0, 's')
    one_second = np.timedelta64(1, 's')
    seconds_since_epoch = (datetime64 - unix_epoch) / one_second
    return datetime.datetime.utcfromtimestamp(seconds_since_epoch)

def settings():
    c1, margin, c2 = st.beta_columns((1,.1, 1))
    with c1:
        ticker = st.selectbox("Company", ("AAPL","AMZN","FB","GOOG","MSFT"))
        event_date = np.datetime64(
            st.date_input("Event date", 
                value = datetime.datetime(2007,1,9), 
                min_value= np_to_datetime(dates[0]), 
                max_value = np_to_datetime(dates[-1])
            )
        )
    
    with c2:
        event_window = st.slider("Event window", min_value = -30, max_value=30, value=(-5,5))
        buffer_size = st.slider("Buffer window size", min_value = 0, max_value=100, value=30)
        estimation_size = st.slider("Estimation window size", min_value = 30, max_value=600, value=300)

    return ticker, event_date, event_window, estimation_size, buffer_size

"""
# Event study
An interactive demo for the Eventstudy package.
"""

with st.beta_expander("Settings"):
    ticker, event_date, event_window, estimation_size, buffer_size = settings()

event = es.Single.market_model(
    security_ticker = ticker,
    market_ticker = "SPY",
    event_date=event_date,
    event_window = event_window,
    estimation_size = estimation_size,
    buffer_size = buffer_size
)

fig = event.plot()
fig.set_size_inches(8, 4)

f'Result for an eventstudy of {ticker} on the {np_to_datetime(event_date).strftime("%d %B, %Y")}, using the market model as returns estimation model against S&P 500 index.'

st.pyplot(fig)

with st.beta_expander("Show data"):
    st.table(event.results())

with st.sidebar:
    """
    Want to use the package for your own project, go to the [Eventstudy package's documentation](https://lemairejean-baptiste.github.io/eventstudy/).
    """