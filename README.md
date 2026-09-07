# E-commerce Customer Behavior Analysis

A comprehensive data cleaning and exploratory analysis of UK-based online retail transactions. This project demonstrates professional data analysis workflows including data quality assessment, cleaning, feature engineering, and insightful visualization.

## 📊 Project Overview

This project analyzes a real-world e-commerce dataset containing 541,909 transactions from a UK-based online retailer. The analysis focuses on:

- **Data Quality Assessment**: Identifying missing values, duplicates, and anomalies
- **Data Cleaning**: Handling invalid transactions while preserving business-critical data
- **Customer Analysis**: Understanding purchasing behavior and customer segmentation
- **Sales Trends**: Analyzing temporal patterns and product performance
- **Geographic Analysis**: Understanding market distribution across countries

## 🎯 Key Findings

- **Data Quality**: 24.9% of transactions have missing CustomerID (135,080 rows)
- **Returns**: Negative quantities represent valid return transactions
- **Top Markets**: UK dominates revenue, followed by European countries
- **Customer Behavior**: Highly skewed spending distribution typical of retail data

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.9-11557C?style=for-the-badge&logo=matplotlib&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-0.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

## 📁 Project Structure

```text
ecommerce-customer-analysis/
├── src/
│ └── ecommerce_analysis/
│ ├── init.py # Package initialization
│ ├── config.py # Configuration and paths
│ ├── logging_config.py # Logging setup with colors
│ ├── data_loader.py # Data loading functions
│ ├── data_profiling.py # Data quality assessment
│ ├── data_cleaning.py # Data cleaning pipeline
│ ├── analysis.py # Analysis functions
│ └── visualization.py # Plotting functions
├── tests/
│ ├── test_config.py # Configuration tests
│ ├── test_logging_config.py # Logging tests
│ └── test_data_cleaning.py # Cleaning tests
├── data/
│ ├── raw/ # Original dataset
│ └── processed/ # Cleaned data
├── reports/
│ └── figures/ # Generated visualizations
├── main.py # Main pipeline entry point
├── pyproject.toml # Project configuration
└── README.md
```

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/babaknikfar/ecommerce-customer-analysis.git
cd ecommerce-customer-behavior-analysis
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux
```

3. Install dependencies:
```bash 
pip install -e ".[dev]"
```

4. Download the dataset:\
Download Online Retail dataset from [UCI Repository](https://archive.ics.uci.edu/ml/datasets/online+retail)\
Place it in `data/raw/` as `online_retail.xlsx`

## 💻 Usage

Run the complete analysis pipeline:
```bash
python main.py
```

This will:
1. Load and profile the raw data
2. Clean the data (removing duplicates, handling missing values, fixing anomalies)
3. Perform analysis (sales trends, top products, country analysis, customer behavior)
4. Generate visualizations in reports/figures/

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v
```

## 📈 Data Quality Issues Handled

- Missing Values: CustomerID (24.9%), Description (0.3%)
- Duplicates: Multiple duplicate transactions
- Invalid Prices: Negative and zero unit prices
- Zero Quantities: Transactions with no items
- Returns: Negative quantities (kept as valid business events)

## 📊 Key Features

### Data Cleaning Pipeline

- Systematic removal of duplicates
- Intelligent handling of missing values
- Validation of transaction data
- Feature engineering (TotalPrice, YearMonth)

### Analysis

- Monthly sales trend analysis
- Top product identification
- Geographic revenue distribution
- Customer spending patterns

### Visualization

- Professional plots with clear labeling
- Dual-axis charts for correlated metrics
- Log-scale histograms for skewed distributions
- Consistent styling across all visualizations

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

Babak Nikfar
- Email: nikfar@nikintel.com
- GitHub: babaknikfar

## 🙏 Acknowledgments

- Dataset: [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/online+retail)
- Original data: Dr Daqing Chen, School of Engineering, London South Bank University




