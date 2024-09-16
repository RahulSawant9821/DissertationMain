import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

if 'token' not in st.session_state:
    st.error("Please login")

else:
    #fetching data from session
    clusterdf = st.session_state.clusterdata
    RFMProddf = st.session_state.RFMProd


    #editing DF
    clusterdf = clusterdf.drop(columns=['segment','customer_id','customer_name','country'])
    RFMProddf = RFMProddf.drop(columns=['Recency','Frequency','Monetary','R_rank_norm','F_rank_norm','M_rank_norm'])





    #extracting year from order date
    clusterdf['order_date'] = pd.to_datetime(clusterdf['order_date'])
    clusterdf['Order_year'] = clusterdf['order_date'].dt.year 


    def filterData():
        chosenCategory  = st.session_state.category_selected
        chosenYear  = st.session_state.year_selected
        chosenRegion  = st.session_state.region_selected
        filtered_df = clusterdf[(clusterdf['category'] == chosenCategory) & (clusterdf['Order_year']==chosenYear) & (clusterdf['region']==chosenRegion)]
        return filtered_df

    #--------------------------------------------------- visualizations code below ---------------------------------------------




    st.title("Product Dashboard")

    #Interactive components :
    #https://docs.streamlit.io/develop/api-reference/layout/st.columns

    #explander widget from streamlit for applying filters
    with st.expander("Filters"):
        left, right = st.columns(2,vertical_alignment="bottom")
        category_options = clusterdf['category'].unique()
        region_options = clusterdf['region'].unique()

        #dropdown for filtering category of products
        #the key parameter, stores the current option in session state.
        left.selectbox("Product Category :",category_options,0,key="category_selected")
        

        #interactive Slider for year filtering
        if "year_" not in st.session_state.clusterdata:
            st.session_state.clusterdata.year_ = 2014

        right.slider(
            "Select year : ",
                min_value= 2014,
                max_value= 2017,
                key='year_selected'
                )

        st.markdown("")
        st.markdown("")
        st.markdown("")

        st.selectbox(" US Region :",region_options,0,key="region_selected")

        
        

    filteredData = filterData()

    st.markdown("")

    st.divider()



    st.markdown("")


    #------------------------------------------------ Charts, Graphs and tables -------------------------------------------------------
    # Segregating product names and the profit each product derives used after barchart
    products = filteredData['product_name'].unique()
    product_profits = {}
    for product in products:
        product_data = filteredData[filteredData['product_name']==product]
        sum_profit  = product_data['profit'].sum()
        product_profits[product] = {
            "Product ID" : product_data['product_id'].iloc[0],
            "Ship Mode" : product_data['ship_mode'].iloc[0],
            "Total Profit" :sum_profit
            
        }

    # Segregating product names and the sales each product derives 
    products = filteredData['product_name'].unique()
    product_sales = {}
    for product in products:
        product_data = filteredData[filteredData['product_name']==product]
        sum_sales  = product_data['sales'].sum()
        product_sales[product] = {
            "Product ID" : product_data['product_id'].iloc[0],
            "Ship Mode" : product_data['ship_mode'].iloc[0],
            "Total sales" :sum_sales
            
        }

    # Segregating product names and the quantity each product sells 
    products = filteredData['product_name'].unique()
    product_quantity = {}
    for product in products:
        product_data = filteredData[filteredData['product_name']==product]
        sum_quantity  = product_data['quantity'].sum()
        product_quantity[product] = {
            "Product ID" : product_data['product_id'].iloc[0],
            "Ship Mode" : product_data['ship_mode'].iloc[0],
            "Total Quantity" :sum_quantity
            
        }

    #bar chart for profit
    #https://docs.streamlit.io/develop/api-reference/charts/st.line_chart
    st.subheader(f"Profit : {st.session_state.year_selected}")
    st.bar_chart(filteredData,x="sub_category",y="profit")
    product_profit_ = pd.DataFrame.from_dict(product_profits,orient='index' )
    st.dataframe(product_profit_,use_container_width=True)
    st.divider()


    #bar chart for sales
    st.subheader(f"Sales : {st.session_state.year_selected}")
    st.bar_chart(filteredData,x="sub_category",y="sales")
    product_sales_ = pd.DataFrame.from_dict(product_sales,orient='index' )
    st.dataframe(product_sales_,use_container_width=True)
    st.divider()

    #bar chart for discount
    st.subheader(f"Discount Offered : {st.session_state.year_selected}")
    st.bar_chart(filteredData,x="sub_category",y="discount")
    product_quantity_ = pd.DataFrame.from_dict(product_quantity,orient='index' )
    st.dataframe(product_quantity_,use_container_width=True)
    st.divider()

    st.markdown("")
    st.markdown("")
    st.markdown("")


    # Pie chart
    RFMProddf = RFMProddf.merge(filteredData, on="sub_category",how="inner")
    st.markdown("")
    st.subheader(f"Product Segment Distribution : {st.session_state.year_selected}")
    #https://discuss.streamlit.io/t/how-to-draw-pie-chart-with-matplotlib-pyplot/13967/2
    fig,ax = plt.subplots()
    count_seg = RFMProddf['Product_segment'].value_counts()
    ax.pie(count_seg,labels=RFMProddf['Product_segment'].unique(),autopct='%1.1f%%',startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    st.markdown("")
    st.markdown("")
    st.markdown("")


    unique_seg = RFMProddf['Product_segment'].unique()
    st.selectbox(label="Select product segment...", options=unique_seg,key="psegment_opted")

    if st.session_state.psegment_opted:
        RFMProddf = RFMProddf[RFMProddf['Product_segment'] == st.session_state.psegment_opted]
        st.dataframe(RFMProddf[['product_name','product_id','ship_mode','quantity']].head(10),use_container_width=True,hide_index=True)
    st.divider()


       



   

