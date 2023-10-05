from langchain.chat_models import ChatOpenAI
from langchain.schema import(
    SystemMessage,
    HumanMessage,
    AIMessage
)

import streamlit as st
from streamlit_chat import message
# This function class is used to display messages in a chat like layout


# loading the OpenAI api key from .env (OPENAI_API_KEY="sk-********")
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)


# S07-54 Building the Application

st.set_page_config(
    page_title='You Custom Assistant',
    page_icon='🤖'
)
st.subheader('Your Custom ChatGPT 🤖')

# Can use any other model supported, but 3.5-turbo is the cheapest
chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5)

# creating the messages (chat history) in the Streamlit session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# creating the sidebar to set the Assistant settings
with st.sidebar:
    # streamlit text input widget for the system message (role)
    system_message = st.text_input(label='System role')
    # streamlit text input widget for the user message
    user_prompt = st.text_input(label='Send a message')

    if system_message:
        if not any(isinstance(x, SystemMessage) for x in st.session_state.messages):
            st.session_state.messages.append(
                SystemMessage(content=system_message)
                )

        st.write(st.session_state.messages)

    # How we handle the users questions
    # Append any questions entered to 'HumanMessages in the session state
    if user_prompt:
        st.session_state.messages.append(
            HumanMessage(content=user_prompt)
        )

        # Add symbol that indicates we are fetching a response
        with st.spinner('Working on your request ...'):
            # creating the ChatGPT response that contains all the system prompts and human questions
            response = chat(st.session_state.messages)

        # adding the response's content to the session state
        st.session_state.messages.append(AIMessage(content=response.content))


st.session_state.messages


# S07-55
message('this is chatgpt', is_user=False) # If no a user, align messages to the LEFT
message('this is the user', is_user=True) # If a user, align messages to the RIGHT  

# Check if the first message is of type SystemMessage
# If so, adding a default SystemMessage if the user didn't entered one since next FOR loop starts after any SystemMessage
if len(st.session_state.messages) >= 1:
    if not isinstance(st.session_state.messages[0], SystemMessage):
        st.session_state.messages.insert(0, SystemMessage(content='You are a helpful assistant.'))

# displaying the messages (chat history)
# Note, starting a FOR loop after the SystemMessage, which is at index 0
for i, msg in enumerate(st.session_state.messages[1:]):
    if i % 2 == 0:
        message(msg.content, is_user=True, key=f'{i} + 🤓') # user's question @ odd indexes
    else:
        message(msg.content, is_user=False, key=f'{i} +  🤖') # ChatGPT response @ even indexes

# run the app: streamlit run ./project_streamlit_custom_chatgpt.py
