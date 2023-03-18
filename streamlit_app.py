import streamlit as st
import psycopg2
import pandas as pd

def test():
    print(123)


def connect_to_db(query, index, text=""):
    conn = psycopg2.connect(
        host=st.secrets["hostname"],
        port=st.secrets["port"],
        dbname=st.secrets["database"],
        user=st.secrets["username"],
        password=st.secrets["password"]
    )

    cur = conn.cursor()

    

    df = pd.read_sql_query(query, conn, index_col=index)
    
    if len(df) == 0: 
        query = f"SELECT english, irish FROM words WHERE irish = '{text}';"
        df = pd.read_sql_query(query, conn, index_col='irish')

    conn.close()
    print(query)
    return df
    
col1, col2 = st.columns([1,1])
with col1:
    display_button = st.button('Click')
with col2:
    if display_button: 
        close_display_button = st.button('close',)

if display_button:
    data = connect_to_db("SELECT * FROM words",'id')
    st.write(data)

input_text = st.text_input('Search for a word',key='input_text',autocomplete='on')

if input_text:
    text = st.session_state['input_text'].strip().lower()
    out_put = connect_to_db(f"SELECT english, irish FROM words WHERE english = '{text}';", 'english', text)
    if len(out_put) == 0:
        st.write(f"Sorry  nothing found for {text}")
    else:
        st.write(out_put)




