
# ShopSphere — E-commerce Sales Analysis
## Project Overview
ShopSphere is an end-to-end e-commerce data analytics project that analyzes sales, customers, products, categories, payments, deliveries, and customer reviews using SQL, Python, Pandas, and Power BI.

The goal is to transform raw e-commerce data into meaningful business insights and visualize key performance indicators through an interactive dashboard.

## Tools & Technologies
- **SQL / MySQL** — Database design, joins, aggregations, and business analysis
- **Python** — Data processing and analysis
- **Pandas & NumPy** — Data cleaning and manipulation
- **Power BI** — Interactive dashboard and KPI visualization
- **Git & GitHub** — Version control and project hosting

## Dataset Overview
The project uses a synthetic e-commerce dataset containing:

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

## Project Workflow
1. Designed a relational database in MySQL.
2. Generated and organized synthetic e-commerce data.
3. Analyzed business performance using SQL queries.
4. Processed and analyzed data using Python and Pandas.
5. Exported analysis results to CSV files.
6. Built a Power BI dashboard to monitor important business KPIs.

## Key Business Metrics
- Net Revenue: ₹693.91M
- Delivered Orders: 17,142
- Average Order Value (AOV): ₹40,480.14
- Delivered Customers: 2,437
- Cancellation Rate: 14.29%
- Average Delivery Time: 4.51 days

*Metrics are based on the current project dataset and dashboard.*

## Power BI Dashboard

![ShopSphere Power BI Dashboard](Dashboard%20%282%29.png)

The dashboard includes:
- Monthly Revenue Trend
- Net Revenue
- Delivered Orders
- Average Order Value
- Delivered Customers
- Cancellation Rate
- Average Delivery Time

Dashboard file: `powerbi/ShopSphere_Dashboard.pbix`

## Project Structure
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
└── .gitignore
```

##How to Run the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/sandeep-botche123/ShopSphere.git
   cd ShopSphere
   ```
2. Create and activate a Python virtual environment.
3. Install the required Python packages used by the project, including:
   ```bash
   pip install pandas numpy matplotlib mysql-connector-python python-dotenv
   ```
4. Create a local `.env` file in the project root with your own MySQL connection settings:
   ```text
   DB_HOST=localhost
   DB_USER=your_mysql_username
   DB_PASSWORD=your_mysql_password
   DB_NAME=shopsphere
   ```
5. Create the database and tables using the SQL scripts in the `DataBase/` folder, then load the data.
6. Run the Python scripts from the project root using your configured Python environment.
7. Open `powerbi/ShopSphere_Dashboard.pbix` in Power BI Desktop to explore the dashboard.

## Key Learnings
- Relational database design and SQL analysis
- Data cleaning and manipulation with Python
- Business KPI calculation and trend analysis
- Power BI dashboard development
- Organizing and publishing an analytics project with GitHub

## Author
**Botche Sandeep**

Aspiring Data Analyst | Python | SQL | Power BI
