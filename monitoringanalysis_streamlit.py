import streamlit as st
import pandas as pd
import plotly.express as px


def main():
    # Add title
    st.title("Media Coverage Analysis Dashboard")

    # File uploader
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file,
                        dtype={'Number': 'int64',
                                'Tier': 'int64'},
                        thousands=',')
        
        # Data preprocessing
        df['ASR(MYR)'] = pd.to_numeric(df['ASR(MYR)'], errors='coerce')
        df['PRV (MYR)'] = pd.to_numeric(df['PRV (MYR)'], errors='coerce')
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%y')

        # Create three columns for key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Coverage", df['Media Outlet'].count())
        with col2:
            st.metric("Total Events", len(df[df['Event'] != 'General']['Event'].unique()))
        with col3:
            st.metric("Total AVE", f"MYR {df['ASR(MYR)'].sum():,.2f}")
        with col4:
            st.metric("Total PRV", f"MYR {df['PRV (MYR)'].sum():,.2f}")

        # Create two columns for charts
        col1, col2 = st.columns(2)

        with col1:
            # Daily coverage line chart
            st.subheader("Total Daily Coverage")
            daily_coverage = df.groupby('Date')['Media Outlet'].count().reset_index()
            fig_line = px.line(daily_coverage, x='Date', y='Media Outlet')
            fig_line.update_layout(xaxis_title='Date', yaxis_title='Coverage')
            st.plotly_chart(fig_line, use_container_width=True)

        with col2:
            # Coverage distribution pie chart
            st.subheader("Coverage Distribution")
            df['Event Category'] = df['Event'].apply(lambda x: 'General' if x == 'General' else 'Others')
            event_coverage = df.groupby('Event Category')['Media Outlet'].count().reset_index()
            fig_pie = px.pie(event_coverage, values='Media Outlet', names='Event Category')
            st.plotly_chart(fig_pie, use_container_width=True)

        # Stacked bar chart for full width
        st.subheader("Coverage by MDEC Events and Releases")
        filtered_df = df[df['Event'] != 'General']
        event_coverage2 = filtered_df.groupby(['Event', 'Tier'])['Media Outlet'].count().reset_index()
        fig_bar = px.bar(event_coverage2, x='Event', y='Media Outlet', color='Tier')
        fig_bar.update_layout(xaxis_title='Event', yaxis_title='Coverage', barmode='stack')
        st.plotly_chart(fig_bar, use_container_width=True)

        # Detailed event summary in an expander
        with st.expander("View Detailed Event Summary"):
            event_summary = df[df['Event'] != 'General'].groupby('Event').agg({
                'Media Outlet': 'count',
                'ASR(MYR)': 'sum',
                'PRV (MYR)': 'sum'
            }).reset_index()
            
            # Format the currency columns
            event_summary['ASR(MYR)'] = event_summary['ASR(MYR)'].apply(lambda x: f"MYR {x:,.2f}")
            event_summary['PRV (MYR)'] = event_summary['PRV (MYR)'].apply(lambda x: f"MYR {x:,.2f}")
            
            # Rename columns for better display
            event_summary.columns = ['Event', 'Total Coverage', 'Total AVE', 'Total PRV']
            
            st.dataframe(event_summary, use_container_width=True)

    else:
        st.info("Please upload a CSV file to view the dashboard")


    # Link to go to N-gram Analyzer page
    #st.write("[Go to Word Cloud Generator](?page=monitoringanalysis_ngram)")
    #st.markdown("[Go to Word Cloud Generator](?page=monitoringanalysis_ngram){: target='_self'}:")
    st.markdown("<a href='?page=monitoringanalysis_ngram' target='_self'>Go to Word Cloud Generator</a>", unsafe_allow_html=True)

# If you want to do something specific when the script is executed directly:
if __name__ == "__main__":
    main()
    #st.write("This is executed if the dashboard is run directly.")