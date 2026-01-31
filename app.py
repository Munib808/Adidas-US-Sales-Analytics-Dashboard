### Importing required modules
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

### Preprocessed data for making Dashboard
@st.cache_data
def load_data():
    df = pd.read_csv("adidas_cleaned.xls")
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    df['month_name'] = pd.Categorical(df['month_name'], categories=month_order, ordered=True)
    return df


df = load_data()
st.sidebar.title("ADIDAS SALES DATA Analysis 2020 - 2021")
img = Image.open("logo.png")
st.sidebar.image(img)
st.set_page_config(
    page_title="Adidas US Sales Dashboard"
)
side = st.sidebar.radio("Go to",["Data Set Overview","DashBoard"])
if side == "Data Set Overview":
    st.title("WelCome To The ADIDAS US SALES DASHBOARD OF YEAR 2020-2021")
    st.divider()
    st.header("Data Set Overview")
    st.text(
        "About Dataset An Adidas sales dataset is a collection of data that includes information on the sales of Adidas products."
        " This type of dataset may include details such as the number of units sold, the total sales revenue,"
        " the location of the sales, the type of product sold, and any other relevant information. "
        " Adidas sales data can be useful for a variety of purposes, such as analyzing sales trends, "
        " identifying successful products or marketing campaigns, and developing strategies for future sales. "
        " It can also be used to compare Adidas sales to those of competitors, or to analyze the effectiveness of different marketing or sales channels. "
        " There are a variety of sources that could potentially provide an Adidas sales dataset, "
        " including Adidas itself, market research firms, government agencies, or other organizations that track sales data. "
        " The specific data points included in an Adidas sales dataset may vary depending on the source and the purpose for which it is being used")
    st.header("Column Description")
    with st.expander("Dataset Column Details"):
        st.markdown("""
        - **retailer**: Retailer selling Adidas products  
        - **region**: Geographic region in the US  
        - **state**: State where the sale happened  
        - **city**: City of the sale  

        - **product**: Product category  
        - **sales_method**: Sales channel (In-store / Online / Outlet)  

        - **price_per_unit**: Price per item  
        - **units_sold**: Number of items sold  
        - **total_sales**: Total revenue generated  
        - **operating_profit**: Profit after operating costs  
        - **operating_margin**: Profit percentage  

        - **invoice_date**: Date of transaction  
        - **year**: Year of sale  
        - **month**: Month number  
        - **month_name**: Month name
        """)
    st.header("Data set First Few Rows")
    st.dataframe(df.head())

if side == "DashBoard":
    option = st.sidebar.radio("Go To ",["Univariate Analysis","Bivariate Analysis and Multivariate Analysis"])
    if option == "Univariate Analysis":
        st.header("Univariate Analysis")

        df["invoice_date"] = pd.to_datetime(df["invoice_date"])

        df_2020 = df[(df["invoice_date"] >= "2020-01-01") & (df["invoice_date"] <= "2020-12-31")]
        df_2021 = df[(df["invoice_date"] >= "2021-01-01") & (df["invoice_date"] <= "2021-12-31")]

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sales", f"${df['total_sales'].sum():,.0f}")
        col2.metric("Total Units Sold", f"{df['units_sold'].sum():,.0f}")
        col3.metric("Total Operating Profit", f"${df['operating_profit'].sum():,.0f}")

        col4, col5 = st.columns(2)
        col4.metric("Avg Operating Margin (2020) in Percent", f"{df_2020['operating_margin'].mean():,.0f}")
        col5.metric("Avg Operating Margin (2021) in Percent", f"{df_2021['operating_margin'].mean():,.0f}")

        col6, col7, col8 = st.columns(3)
        col6.metric("Total Sales (2020)", f"${df_2020['total_sales'].sum():,.0f}")
        col7.metric("Total Sales (2021)", f"${df_2021['total_sales'].sum():,.0f}")
        col8.metric("Units Sold (2020)", f"{df_2020['units_sold'].sum():,.0f}")

        col9, col10, col11 = st.columns(3)
        col9.metric("Units Sold (2021)", f"{df_2021['units_sold'].sum():,.0f}")
        col10.metric("Operating Profit (2020)", f"${df_2020['operating_profit'].sum():,.0f}")
        col11.metric("Operating Profit (2021)", f"${df_2021['operating_profit'].sum():,.0f}")

        st.metric("Overall Avg Operating Margin in Percent", f"{df['operating_margin'].mean():,.0f}")
        st.subheader("Above Insights are Fix in terms of Date if Want to see above stats in Different Periods Use DashBoard Below")

        st.subheader("Dynamic Period Analysis")
        start_date = st.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
        end_date = st.date_input("End Date", value=pd.to_datetime("2021-12-31"))

        start_ts = pd.Timestamp(start_date)
        end_ts = pd.Timestamp(end_date)

        df_period = df[(df["invoice_date"] >= start_ts) & (df["invoice_date"] <= end_ts)]

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sales", f"${df_period['total_sales'].sum():,.0f}")
        col2.metric("Total Units Sold", f"{df_period['units_sold'].sum():,.0f}")
        col3.metric("Total Operating Profit", f"${df_period['operating_profit'].sum():,.0f}")

        col4, col5 = st.columns(2)
        col4.metric("Average Operating Margin", f"{df_period['operating_margin'].mean():,.0f}")

    if option == "Bivariate Analysis and Multivariate Analysis":

        tab1, tab2 = st.tabs(["# Graphs", "# Univariate Analysis of filtered Data"])
        with tab1:
            st.header("Bivariate Analysis and Multivariate Analysis")
            region = st.sidebar.multiselect(
            "Select Region",
            options=df["region"].unique(),
            default=df["region"].unique()
            )

            retailer = st.sidebar.multiselect(
            "Select Retailer",
            options=df["retailer"].unique(),
            default=df["retailer"].unique()
            )

            product = st.sidebar.multiselect(
            "Select Product",
            options=df["product"].unique(),
            default=df["product"].unique()
            )

            sales_method = st.sidebar.multiselect(
            "Select Sales Method",
            options=df["sales_method"].unique(),
            default=df["sales_method"].unique()
            )

            year = st.sidebar.multiselect(
            "Select Year",
            options=sorted(df["year"].unique()),
            default=sorted(df["year"].unique())
            )

            state = st.sidebar.multiselect(
            "Select state",
            options=df["state"].unique(),
            default=df["state"].unique()
            )
            city = st.sidebar.multiselect(
            "Select city",
            options=df["city"].unique(),
            default=df["city"].unique()
            )

            filtered_df = df[
            (df["region"].isin(region)) &
            (df["retailer"].isin(retailer)) &
            (df["product"].isin(product)) &
            (df["sales_method"].isin(sales_method)) &
            (df["year"].isin(year)) &
            (df["state"].isin(state)) &
            (df["city"].isin(city))
            ]
            st.subheader("Filtered Data")
            st.dataframe(filtered_df)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Sales by Region")
                region_sales = (
                filtered_df
                .groupby("region")["total_sales"]
                .sum()
                )
                st.bar_chart(region_sales)

            with col2:
                st.subheader("Sales by Product")
                product_sales = (
                filtered_df
                .groupby("product")["total_sales"]
                .sum()
                )
                st.bar_chart(product_sales)
            st.subheader("Sales by Sale Method")
            region_sales = (
                filtered_df
                .groupby("sales_method")["total_sales"].sum()
            )
            st.bar_chart(region_sales)
            st.subheader("Sales Trends Over Time")
            sales_line = filtered_df.groupby("invoice_date")["total_sales"].sum().reset_index()
            fig_line = px.line(sales_line, x="invoice_date", y="total_sales", template="plotly_white")
            st.plotly_chart(fig_line, use_container_width=True)

            st.subheader("Top 5 and Bottom 5 Regions by Total Sales")

            region_sales = filtered_df.groupby("state")["total_sales"].sum().reset_index()
            region_sales = region_sales.sort_values(by = "total_sales",ascending = False).head(5)
            figqq = px.bar(
            region_sales,
            x= "state",
            y="total_sales",
            title="Top 5 States by Total Sales"
            )
            st.plotly_chart(figqq, use_container_width=True)

            region_sales1 = filtered_df.groupby("state")["total_sales"].sum().reset_index()
            region_sales1 = region_sales1.sort_values(by="total_sales", ascending=True).head(5)
            figqq1 = px.bar(
            region_sales1,
            x="state",
            y="total_sales",
            title="Bottom 5 States by Total Sales"
            )
            st.plotly_chart(figqq1, use_container_width=True)

            st.subheader("Total Sales by Month")
            month_plot = filtered_df.groupby("month_name")["total_sales"].sum()
            st.line_chart(month_plot)

            st.subheader("Total Units Sold by Month")
            units_sold_month_plot = filtered_df.groupby("month_name")["units_sold"].sum()
            st.line_chart(units_sold_month_plot)

            st.subheader("Total Sales by Retailer")
            retailer_plot = filtered_df.groupby("retailer")["total_sales"].sum()
            st.bar_chart(retailer_plot)

            st.subheader("Operating Profit by Retailer")
            operating_profit_plot = filtered_df.groupby("retailer")["operating_profit"].sum()
            st.bar_chart(operating_profit_plot)

            st.subheader("Operating Profit by Product")
            product_profit_plot = filtered_df.groupby("product")["operating_profit"].sum()
            st.bar_chart(product_profit_plot)
            st.subheader("Total Sales vs Operating Margin")

            fig_scatter = px.scatter(
                filtered_df,
                x="total_sales",
                y="operating_margin",
                color="region",
                size="units_sold",
                hover_data=["retailer", "product", "state"],
                labels={
                    "total_sales": "Total Sales ($)",
                    "operating_margin": "Operating Margin (%)"
                },
                title="Relationship between Total Sales and Operating Margin",
                template="plotly_white"
            )

            fig_scatter.update_layout(
                height=500
            )

            st.plotly_chart(fig_scatter, use_container_width=True)

        with tab2:
            st.subheader("Key Performance Indicators of Filtered Data")
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("Total Sales", f"${filtered_df['total_sales'].sum():,.0f}")
            kpi2.metric("Total Units Sold", f"{filtered_df['units_sold'].sum():,.0f}")
            kpi3.metric("Avg Margin", f"{filtered_df['operating_margin'].mean():.1f}%")