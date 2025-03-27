#Application (UI) file

import streamlit as st
import pandas as pd
from detector import detect_siphonage
from utils import preprocess_data

def main():
    st.title("Fuel Siphonage Detection System")
    st.write("Upload a vehicle telemetry CSV file. Siphonage events will be detected using rule-based logic.")
    
    #File uploading
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Uploaded Data Sample")
        st.dataframe(df.head())
        
        #Preprocessing the data
        processed_df = preprocess_data(df)
        #Applying rule-based detection (this will add or update the 'siphonage' column)
        processed_df = detect_siphonage(processed_df)
        
        #Mapping output for easier understanding
        processed_df['siphonage'] = processed_df['siphonage'].map({0:"No", 1:"Yes"})

        #Using the 'siphonage' column to filter siphonage periods
        st.write("### Detected Siphonage Vehicle and Period")
        siphonage_events = processed_df[processed_df['siphonage'] == "Yes"]
        st.dataframe(siphonage_events)
        
        # Saving the output
        if st.button("Download Processed Data"):
            processed_df.to_csv("siphonage_results.csv", index=False)
            st.success("File saved as siphonage_results.csv")

if __name__ == "__main__":
    main()
