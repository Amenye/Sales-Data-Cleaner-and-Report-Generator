# 🛒Sales-Data-Cleaner-and-Report-Generator

## 📋 Project Overview
This project is a Data Engineering solution designed to repair a corrupted retail transaction dataset. Simulating a real-world software failure, the input logs contained systematic errors including missing financial totals, lost item metadata, and inconsistent boolean flags.

Instead of standard data cleaning methods (like filling missing values with averages), this pipeline implements a **Logic-Based Reconstruction** strategy. It builds a knowledge base from valid rows to mathematically restore missing data, ensuring 100% integrity before generating business insights.

## 🚀 Key Features
* **Self-Healing Data Logic:** Dynamically builds a "Truth Dictionary" from valid transactions to recover missing Item names based on `(Category, Price)` combinations.
* **Vectorized Reconstruction:** Utilizes Pandas index mapping for high-performance logical imputation, restoring missing `Total Spent` and `Price Per Unit` values without slow loops.
* **Integrity Validation:** Implements strict automated assertions (using `assert`) to verify that `Price * Quantity == Total` for every single row after cleaning.
* **Outlier Detection:** Automatically identifies and filters erroneous transactions (e.g., impossible quantities) based on business rules.
* **Business Intelligence:** Aggregates cleaned data to report on Revenue by Channel, Top Categories, and Discount Effectiveness.

## 🛠️ Tech Stack
* **Python 3.10+**
* **Pandas** (Vectorized Operations & Data Cleaning)
* **NumPy** (Mathematical Validation)
* **Matplotlib** (Visual Analytics)

## 📊 Sample Output
When the pipeline runs, it processes the raw CSV, performs the repair, and outputs a verification report.

**Console Report:**
```text
Loading the Dataset...

======== RETAIL PERFORMANCE REPORT ========
Original Rows:  12575
Cleaned Rows:   11362 (Dropped 1213 unrecoverable)
-------------------------------------------
Total Revenue:  R1472998.5
    - Online:   R749431.0
    - In-Store: R723567.5
-------------------------------------------
Average Spent:
    -Full Price: R 129.10
    -Discounted: R 130.72
-------------------------------------------
Top Category:   "Furniture"
-------------------------------------------
Validation: PASSED (Total == Price * Qty)
===========================================
Files saved: 'retail_sales_clean.csv', 'retail_report.txt'
```

## ⚙️ How to Run

### 1. Clone the Repository
Open your terminal or command prompt and run:
```bash
git clone [https://github.com/YOUR_USERNAME/Sales-Data-Cleaner-and-Report-Generator.git](https://github.com/YOUR_USERNAME/Sales-Data-Cleaner-and-Report-Generator.git)
cd Sales-Data-Cleaner-and-Report-Generator
```
### 2. Install Dependencies
```bash
pip install pandas numpy matplotlib
```
### 3. Setup Data
#### Ensure the raw dataset file retail_store_sales.csv is located in the root directory of the project.
Note: If you are using your own dataset, ensure it matches the schema (Transaction ID, Category, Price, Quantity, etc.).
### 4. Execute the Pipeline
```bash
python retail_pipeline.py
```
### 5. Check Results
**After execution, the script will generate two files in the same directory:**
* retail_sales_clean.csv: The fully reconstructed and cleaned dataset.
* retail_report.txt: A text summary of the key performance indicators.
