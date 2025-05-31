# Chocolate Sales Data Analysis

## Introduction
This project analyzes chocolate sales data through data exploration, cleaning, feature engineering, and exploratory data analysis (EDA). The goal is to uncover insights into sales trends, product performance, and relationships between different variables.

## Data Overview
The dataset contains the following columns:
- **Sales Person**: Name of the salesperson
- **Product**: Type of chocolate product
- **Country**: Market location
- **Boxes Shipped**: Number of chocolate boxes sold
- **Amount**: Total sales revenue
- **Date**: Date of sale

## Data Cleaning
- Checked for missing and duplicate values (none found)
- Ensured consistency in the 'Amount' column to maintain numerical accuracy

## Feature Engineering
- Converted 'Date' into datetime format
- Created a new feature: **Per_box_price** = Amount / Boxes Shipped

## Exploratory Data Analysis (EDA)
- **Sales Person Analysis**: Bar plots to compare individual sales performance
- **Country-wise Sales Distribution**: Pie chart to highlight major markets
- **Product Performance**: Bar plots to visualize top-selling chocolates
- **Boxes Shipped vs. Amount**: Scatter plot to analyze the correlation
- **Time Trends**: Line plot tracking the shipment trends over time
- **Product Pricing Analysis**: Violin plots to explore pricing variations across regions

## Key Findings
- Some products have significantly higher demand
- Sales trends vary across different countries and salespeople
- Per box pricing differs based on the product category
