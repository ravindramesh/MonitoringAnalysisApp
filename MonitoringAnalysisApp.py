import streamlit as st
from monitoringanalysis_streamlit import main as dashboard_main
from monitoringanalysis_ngram import main as ngram_analyzer_main

# Set page config
st.set_page_config(
    page_title="Media Coverage Dashboard",
    page_icon="📊",
    layout="wide"
)

def main():
    page = st.query_params["page"] if "page" in st.query_params else "monitoringanalysis_streamlit"
    
    if page == "monitoringanalysis_streamlit":
        dashboard_main()
    elif page == "monitoringanalysis_ngram":
        ngram_analyzer_main()
    else:
        st.error(f"Page not found! Received page value: '{page}'")

if __name__ == "__main__":
    main()
