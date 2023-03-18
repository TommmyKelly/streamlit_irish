import streamlit as st
import streamlit_authenticator as stauth
import bcrypt
import psycopg2
import time

def reset():
    
    st.session_state['add_user']="not done"

def connection():
    conn = psycopg2.connect(
        host=st.secrets["hostname"],
        port=st.secrets["port"],
        dbname=st.secrets["database"],
        user=st.secrets["username"],
        password=st.secrets["password"]
    )
    return conn

names = []
usernames = []
passwords = []

def get_inital_users():
    global names, usernames, passwords
    conn = connection()
    

    cur = conn.cursor()

    query = "SELECT * FROM users;"

    cur.execute(query)

    # items = [row[1] for row in cur]
    # print(items)
    # names = [row[0] for row in cur.execute(query)]
    # usernames = [row[1] for row in cur]
    # password = [row[2] for row in cur]
    for row in cur:
        id ,name, username, password = row
        names.append(name)
        usernames.append(username)
        passwords.append(password)
    
    
    cur.close()
    conn.close()

   
 
get_inital_users()


if "add_user" not in st.session_state:
    st.session_state['add_user']="not done"

def add_user(name: str, username: str, password: bytes, conn :connection) -> None:
    if name == "" or username == "" or password == "":
        st.session_state['add_user']="missing_data"
        print(2)
        return
    hashed = bcrypt.hashpw(bytes(password,'utf-8'), bcrypt.gensalt())
    hashed = hashed.decode('utf-8')
    query = f"INSERT INTO users (name, username, password) VALUES (%s, %s, %s);"
    cur = conn.cursor()
    try:
        cur.execute(query, (name, username, hashed))
        conn.commit()
        st.session_state['add_user']="added"
        # time.sleep(20)
        # st.session_state['add_user']="not done"
    except psycopg2.errors.UniqueViolation:
        st.session_state['add_user']="user_all_ready"
        # time.sleep(20)
      
    finally:
        print(st.session_state['add_user'])
        cur.close()
        conn.close()

   
    


authenticator = stauth.Authenticate(names, usernames, passwords, 'cookie_name', 'signature_key', cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login', 'main')



if authentication_status == False:
    st.error('Username/password is incorrect')
   
if authentication_status == None:
    st.warning('Please enter your username and password')
if authentication_status:
    st.write('Welcome *%s*' % (name))
    authenticator.logout('logout')
    # admin_status = users.fetch({'email': username}).items[0]['admin']
   
    # admin only
    st.write(f"Welcome {name}")
                
    st.write('---')    

    with st.expander('Add user'):
        with st.form('Add user'):
            name_input = st.text_input('Name',key='name_value')
            username_input = st.text_input('Username',key='username_input')
            password_input = st.text_input('Password',key='password_input')
            input_date = st.date_input('date_input')
            st.form_submit_button(label='Submit',on_click=lambda: add_user(st.session_state['name_value'], st.session_state['username_input'], st.session_state['password_input'], connection()))


if st.session_state['add_user'] == "added":
    msg = st.success('User add successfully')
    

elif st.session_state['add_user'] == "user_all_ready":
    st.warning('User all ready')
elif st.session_state['add_user'] == "missing_data":
    st.error("Please fill out all fields")