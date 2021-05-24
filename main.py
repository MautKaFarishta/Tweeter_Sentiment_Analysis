import streamlit as st
import wrapper

def main():
    st.sidebar.title('Choose Action!')
    appMode = st.sidebar.selectbox('Select Mode',
        ['Demo Mode','Analytics With Hashtag'])

    if appMode == "Demo Mode":
        st.sidebar.success('Demo Mode On !')
        st.sidebar.text('Already Scrapped tweets !')
        wrapper.runHashTagScrap(True)
    elif appMode == "Analytics With Hashtag":
        st.sidebar.success('Scrap And Analyze !')
        st.sidebar.text('Scrap The Tweets for your hashtag')
        wrapper.runHashTagScrap(False)

if __name__ == "__main__":
    main()