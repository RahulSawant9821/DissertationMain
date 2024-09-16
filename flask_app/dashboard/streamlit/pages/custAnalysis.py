import streamlit as st
import pandas as pd
import requests
import matplotlib.cm as cm
import matplotlib.pyplot as plt


if 'token' not in st.session_state:
    st.warning("Please Log in")
else:

    #fetching data from session
    clusterdf = st.session_state.clusterdata
    RFMCustdf = st.session_state.RFMCust



    #editing DF
    clusterdf = clusterdf.drop(columns=['category','product_id','product_name','ship_mode','sub_category','country'])
    RFMCustdf = RFMCustdf.drop(columns=['Recency','Frequency','Monetary','R_rank_norm','F_rank_norm','M_rank_norm'])



    #extracting year from order date
    clusterdf['order_date'] = pd.to_datetime(clusterdf['order_date'])
    clusterdf['Order_year'] = clusterdf['order_date'].dt.year 


    def filterData():
        chosenSegment  = st.session_state.segment_selected
        chosenYear  = st.session_state.year_selected
        chosenRegion  = st.session_state.region_selected
        filtered_df = clusterdf[(clusterdf['segment'] == chosenSegment) & (clusterdf['Order_year']==chosenYear) & (clusterdf['region']==chosenRegion)]
        return filtered_df

    #--------------------------------------------------- visualizations code below ---------------------------------------------




    st.title("Customer Dashboard")

    

    #Interactive components :
    #https://docs.streamlit.io/develop/api-reference/layout/st.columns

    #expander widget from streamlit for applying filters
    with st.expander("Filters"):
        left, right = st.columns(2,vertical_alignment="bottom")
        segment_options = clusterdf['segment'].unique()
        region_options = clusterdf['region'].unique()

        #dropdown for filtering segments of customers
        #the key parameter, stores the current option in session state.
        left.selectbox("Customer Segment :",segment_options,0,key="segment_selected")
        

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
    st.markdown("")

    st.divider()



    #------------------------------------------------ Charts, Graphs and tables -------------------------------------------------------

    # Segregating customer names and the profit each customer derives
    customers = filteredData['customer_name'].unique()
    customer_profits = {}
    for customer in customers:
        customer_data = filteredData[filteredData['customer_name']==customer]
        sum_profit  = customer_data['profit'].sum()
        customer_profits[customer] = {
            "Customer ID" : customer_data['customer_id'].iloc[0],
            "City" : customer_data['city'].iloc[0],
            "State" : customer_data['state'].iloc[0],
            "Total Profit" :sum_profit
            
        }


    # Segregating customer names and the quantity each customer orders
    states = filteredData['state'].unique()
    customer_quantity = {}
    for state in states:
        customer_data = filteredData[filteredData['state']==state]
        sum_quantity =  customer_data['quantity'].sum()
        customer_quantity[state] = {
            "Customer Name" : customer_data['state'].iloc[0],
            "Customer ID" : customer_data['customer_id'].iloc[0],
            "City" : customer_data['city'].iloc[0],
            "Total quantity" :sum_quantity
            
        }



    #https://docs.streamlit.io/develop/api-reference/charts/st.line_chart
    st.subheader("Profit generated according to state")
    st.line_chart(filteredData,x="state",y="profit")
    customer_profit_ = pd.DataFrame.from_dict(customer_profits,orient='index' )
    st.dataframe(customer_profit_,use_container_width=True)
    st.divider()


    st.markdown("")
    st.subheader("Quantity ordered by each Customer")
    st.bar_chart(filteredData,x="customer_name",y="quantity")
    customer_quantity_ = pd.DataFrame.from_dict(customer_quantity,orient='index' )
    st.dataframe(customer_quantity_,use_container_width=True)
    st.divider()


    st.markdown("")
    st.markdown("")
    st.markdown("")


    #https://www.statology.org/left-join-pandas/
    #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.join.html
    RFMCustdf = RFMCustdf.merge(filteredData, on="customer_name",how="inner")

    st.markdown("")
    st.subheader("Customer segments Distribution :")
    #https://discuss.streamlit.io/t/how-to-draw-pie-chart-with-matplotlib-pyplot/13967/2
    fig,ax = plt.subplots()
    count_seg = RFMCustdf['Customer_segment'].value_counts()
    ax.pie(count_seg,labels=RFMCustdf['Customer_segment'].unique(),autopct='%1.1f%%',startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    st.markdown("")
    st.markdown("")
    st.markdown("")

    unique_seg = RFMCustdf['Customer_segment'].unique()
    st.selectbox(label="Select customer segment...", options=unique_seg,key="segment_opted")

    if st.session_state.segment_opted:
        RFMCustdf = RFMCustdf[RFMCustdf['Customer_segment'] == st.session_state.segment_opted]
        st.dataframe(RFMCustdf[['customer_name','customer_id','discount','profit','quantity','sales']].head(10),use_container_width=True,hide_index=True)
    st.divider()




    st.markdown("")
    unique_clusters = filteredData['cluster'].unique()
    st.subheader("Cluster performance based on sales and profit")
    st.scatter_chart(filteredData,x="sales",y="profit",color='cluster')
    st.selectbox(label="Select Cluster...", options=unique_clusters,key="cluster_selected")
    cluster_df = filteredData[filteredData['cluster']==st.session_state.cluster_selected]
    cluster_df = cluster_df.drop(columns=['order_date','order_id','region','segment','ship_date','state','Order_year','postal_code'])
    st.dataframe(cluster_df,use_container_width=True)
    st.divider()
    st.markdown("")





    st.subheader("Sales as per City")
    st.markdown("")
    st.map(filteredData,latitude=filteredData['latitude'],longitude=filteredData['longitude'],size="sales")
    st.divider()



        



   

