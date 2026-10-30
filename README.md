
# 🛒 ShopSphere — E-commerce Sales Analytics

An end-to-end data analytics project exploring e-commerce sales, customers, products, deliveries, and customer reviews using **MySQL, Python, Pandas, and Power BI**.

## 📊 Dashboard Preview

![ShopSphere Power BI Dashboard](Dashboard%20%282%29.png)

## 🎯 Project Overview

ShopSphere is an e-commerce analytics project built to transform raw transactional data into meaningful business insights. It combines SQL-based analysis, Python data processing, and Power BI visualizations to help understand sales performance and key business metrics.

**Project objectives:**
- Analyze revenue and monthly sales trends.
- Evaluate product and category performance.
- Understand customer purchasing behavior.
- Examine order cancellations and delivery performance.
- Explore customer ratings and product profitability.

## 🛠️ Tech Stack

- **MySQL** — Relational database design and SQL analysis
- **Python** — Data processing and analysis
- **Pandas & NumPy** — Data cleaning and manipulation
- **Power BI** — KPI visualization and dashboard development
- **Git & GitHub** — Version control and project hosting

## 📁 Dataset Overview

The project uses a synthetic e-commerce dataset with the following tables:

| Table | Records |
|---|---:|
| Customers | 2,500 |
| Categories | 5 |
| Products | 100 |
| Orders | 20,000 |
| Order Items | 49,889 |
| Payments | 20,000 |
| Deliveries | 17,142 |
| Reviews | 7,028 |

## 📈 Key Performance Indicators

| KPI | Dashboard Value |
|---|---:|
| Net Revenue | ₹693.91M |
| Delivered Orders | 17,142 |
| Average Order Value (AOV) | ₹40,480.14 |
| Delivered Customers | 2,437 |
| Cancellation Rate | 14.29% |
| Average Delivery Time | 4.51 days |

*Values reflect the current project dashboard and dataset.*

## 🔍 Analysis Performed

### SQL Analysis
- Revenue and monthly sales analysis
- Category and product performance
- Customer and city-level performance
- Product profitability and ratings
- Order and delivery status analysis

### Python Analysis
- Data processing and cleaning
- Aggregation and KPI calculations
- Analysis result generation
- Exporting processed results to CSV files

### Power BI Dashboard
- Monthly Revenue Trend
- Net Revenue
- Delivered Orders
- Average Order Value
- Delivered Customers
- Cancellation Rate
- Average Delivery Time

## 🔄 Project Workflow

1. Create the relational database and tables in MySQL.
2. Generate and organize the synthetic dataset.
3. Perform business analysis using SQL queries.
4. Process and analyze data using Python and Pandas.
5. Export analysis results into processed CSV files.
6. Build a Power BI dashboard to visualize key metrics.
7. Publish the project and documentation on GitHub.

## 🗂️ Repository Structure

```text
ShopSphere/
├── DataBase/
│   ├── 01_schema.sql
│   ├── 02_insert_data.sql
│   └── 03_analysis.sql
├── data/
│   ├── raw/
│   └── processed/
├── powerbi/
│   └── ShopSphere_Dashboard.pbix
├── scripts/
│   ├── generate_data.py
│   └── validation.py
├── src/
│   ├── Database.py
│   ├── analysis.py
│   ├── data_cleaning.py
│   └── load_delivery.py
├── Dashboard (2).png
├── .gitignore
└── README.md
```

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/sandeep-botche123/ShopSphere.git
cd ShopSphere
```

### 2. Set up Python

Create and activate a virtual environment, then install the required packages:

```bash
pip install pandas numpy matplotlib mysql-connector-python python-dotenv
```

### 3. Configure MySQL

- Ensure MySQL Server is installed and running.
- Create a local `.env` file in the project root with your own database credentials:

```text
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=shopsphere
```

- Execute the SQL scripts in the `DataBase/` folder in the appropriate order to create and populate the database.

### 4. Run the Python scripts

Use the configured Python environment to run the relevant scripts from the project root. Check each script for its execution requirements.

### 5. Open the dashboard

Open `powerbi/ShopSphere_Dashboard.pbix` using Power BI Desktop.

## 📚 Skills Demonstrated

- Relational database design
- SQL joins, aggregations, and business queries
- Python programming and data analysis
- Data cleaning and transformation
- KPI calculation and trend analysis
- Power BI dashboard development
- Git and GitHub project management

## 👨‍💻 Author

**Botche Sandeep**

Aspiring Data Analyst | Python | SQL | Power BI

[GitHub Repository](https://github.com/sandeep-botche123/ShopSphere)
