import streamlit as st
import wrapper

def main():
    st.sidebar.title('Choose Action!')
    appMode = st.sidebar.selectbox('Select Mode',
        ['Demo Mode','Hashtag Analytics','User Analytics','Replies Analytics'])

    if appMode == "Demo Mode":
        st.sidebar.success('Demo Mode On !')
        st.sidebar.text('Already Scrapped tweets !')
        wrapper.runHashTagScrap(True)

    elif appMode == "Hashtag Analytics":
        st.sidebar.success('Scrap And Analyze !')
        st.sidebar.text('Scrap The Tweets for your hashtag')
        wrapper.runHashTagScrap(False)

    elif appMode == "User Analytics":
        st.sidebar.text('Scrap The Tweets for specific User.')
        wrapper.getUserInfo()

    elif appMode == "Replies Analytics":
        st.sidebar.text('Scrap The Replies for specific Tweet.')
        wrapper.getReplies()

if __name__ == "__main__":
    main()