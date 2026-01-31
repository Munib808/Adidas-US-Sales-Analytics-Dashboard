# Adidas US Sales Dashboard (2020–2021)
## Project Overview

This project presents a professional, interactive Streamlit dashboard for analyzing Adidas US sales data from 2020 to 2021.
The dashboard enables users to explore sales performance, profitability, and trends across regions, products, retailers, and time periods using dynamic filters and visual analytics.

The project covers the complete data analysis lifecycle, including preprocessing, exploratory analysis, univariate, bivariate, and multivariate analysis, and interactive visualization.

## Objectives

Analyze Adidas US sales performance across multiple business dimensions

Identify top and bottom performing regions, states, and products

Evaluate operating profit and operating margin behavior

Provide dynamic date-based insights for flexible time-period analysis

Build a clean, professional, and scalable Streamlit dashboard

## Project Structure
Adidas-US-Sales-Dashboard/
- │
- ├── Adidas US Sales Datasets.xlsx     # Raw dataset
- ├── adidas_cleaned.xls                # Cleaned and processed dataset
- ├── PreProcessing_Data.ipynb          # Data cleaning & preprocessing notebook
- ├── app.py                            # Streamlit dashboard application
- ├── logo.png                          # Dashboard logo
- └── README.md                         # Project documentation

## Dataset Description

The dataset contains Adidas sales transactions in the United States with the following key attributes:

"Retailer"	,"Retailer ID"	,"Invoice Date"	,"Region"	,"State"	,"City"	,"Product",	"Price per Unit"	,"Units Sold",	"Total Sales"	,"Operating Profit"	,"Operating Margin"	,"Sales Method"

## Dashboard Features
### 1. Dataset Overview

Description of the dataset

Column definitions

Preview of raw data

### 2. Univariate Analysis

Total Sales

Total Units Sold

Total Operating Profit

Average Operating Margin

Year-wise comparison (2020 vs 2021)

Fixed date insights

Dynamic date range analysis using start and end date selection

### 3. Bivariate & Multivariate Analysis

Sales by Region

Sales by Product

Sales by Sales Method

Sales Trends over Time

Top 5 and Bottom 5 States by Total Sales

Monthly Sales Trends

Monthly Units Sold Trends

Retailer-wise Sales and Profit Analysis

Product-wise Operating Profit

Relationship between Total Sales and Operating Margin

### 4. Interactive Filtering

Users can filter data by:

Region

Retailer

Product

Sales Method

Year

State

City

All charts and KPIs update dynamically based on selected filters.

## Technologies Used

Python

Streamlit – Interactive dashboard development

Pandas – Data manipulation and analysis

Plotly Express – Interactive visualizations

Pillow (PIL) – Image handling

## How to Run the Project

### 1. Install Required Libraries
pip install streamlit pandas plotly pillow

### 2. Run the Streamlit App
streamlit run app.py

## Key Insights Enabled

Identification of high-revenue and low-margin regions

Comparison of 2020 vs 2021 performance

Seasonal sales patterns

Retailer and product profitability analysis

Business-driven decision support through visual analytics

## Use Cases

Data Analytics Portfolio Project

Business Intelligence Demonstration

Sales Performance Analysis

Academic or Industrial Case Study

Interview-ready Streamlit Dashboard

## Future Enhancements

Year-over-Year growth analysis

Forecasting using time series models

Export filtered data functionality

KPI trend indicators

Deployment on Streamlit Cloud

## Author

## Munib Ahmad
Data Science | Machine Learning | Business Analytics
