import streamlit as st
import pickle 
import pandas as pd

if 'token' not in  st.session_state:
    st.error("Not Logged In")
else:
    #category
    def recommend_category(productCat, cosine_sim,product_df):
        idx = product_df[product_df['sub_category']==productCat].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x:x[1],reverse=True)
        sim_scores = sim_scores[1:11]
        product_indices = [i[0] for i in sim_scores]

        return product_df['product_name'].iloc[product_indices]


    #product
    def product_recommend(prod_name):
        prodIndex  = product_df[product_df['product_name']==prod_name].index[0]
        distances_ = similarity_mat[prodIndex]
        prod_list = sorted(list(enumerate(distances_)),reverse=True,key=lambda x:x[1])[1:10]
        recommended_prod = []
        for i in prod_list:
            prodName = product_df.iloc[i[0]].product_name
            recommended_prod.append(prodName)

        return recommended_prod
        


    #category
    with open(r"C:\FinalYearProject\code\code\data\TFrecommender.pkl","rb") as f:
        loaded_data = pickle.load(f)

    #product
    with open(r"C:\FinalYearProject\code\code\data\prodList.pkl","rb") as f:
        prod = pickle.load(f)
        product_df =pd.DataFrame(prod)

    with open(r"C:\FinalYearProject\code\code\data\similarity.pkl","rb") as f:
        similarity_mat= pickle.load(f)




    tab1,tab2= st.tabs(["Category","Product"])
    with tab1:
        tfidf_matrix, cosine_sim, cat_df = loaded_data

        st.title("Category Recommendation")
        category_list = cat_df['sub_category'].values
        selected_cat = st.selectbox(
            "Type or select a product from the dropdown",
            category_list
        )

        recommend = st.button("Recommend Categories")
        if recommend:
            recommendations = recommend_category(selected_cat,cosine_sim,cat_df)
            st.write("Recommended Items :")
            for item in recommendations:
                st.write(item)

    with tab2:

        st.title("Product Recommendation")
        prod_list = product_df['product_name'].tolist()
        selected_prod = st.selectbox(
            "Type or select a product from the dropdown",
            prod_list
        )

        recommend = st.button("Recommend Products")
        if recommend:
            recommendations = product_recommend(selected_prod)
            st.write("Recommended Items :")
            for item in recommendations:
                st.write(item)

