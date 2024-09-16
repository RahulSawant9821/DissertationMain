import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest

#https://docs.kanaries.net/topics/Streamlit/streamlit-upload-file

if 'token' not in st.session_state:
    st.error("Please login")
else:
    if st.session_state.role == 'User':
        st.warning("Not authorized")

    else:

        def cleanData(file):
            if file is None:
                return st.error("No file Uploaded")
            data = pd.read_csv(file,encoding="unicode_escape").dropna().drop_duplicates()

            #seperating categorical and numerical columns
            col = data.columns
            num_df = pd.DataFrame()
            cats_Col= []
            nums_Col = []
            for i in col:
                if data[i].dtypes == object:
                    cats_Col.append(i)
                else:
                    nums_Col.append(i)
            num_df = data[nums_Col]
            cat_df = data[cats_Col]  

            #initializing Isolation forest
            clf = IsolationForest(random_state=0).fit(num_df)
            data['IF_Outliers'] = pd.DataFrame(clf.predict(num_df))

            outlier_data = data[data['IF_Outliers']==-1]
            # labeling outliers with label
            data = data[data['IF_Outliers']!=-1]
            #droping all the outlier rows with label -1
            data = data.drop(columns=['IF_Outliers'])
            data_original = pd.DataFrame(data)

            return [data_original,outlier_data]

        #https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader

        st.subheader("Let's Clean your data :")
        file = st.file_uploader(
                "Choose a csv file :", accept_multiple_files=False,type='csv'
            )

        if st.button("Clean"):
            cleanedData =  cleanData(file)

            if cleanedData is not None:
                clean_ , outlier_ = st.tabs(["Clean","Outliers"])
                clean,outlier = cleanedData
                with clean_:
                    st.subheader("Cleaned Data:")
                    st.write(clean.shape)
                    st.dataframe(clean)

                with outlier_:
                    st.subheader("Outliers :")
                    st.write(outlier.shape)
                    st.dataframe(outlier)           
