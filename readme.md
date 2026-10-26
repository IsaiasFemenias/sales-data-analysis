**Author:** IF

This project explores a global fashion retail dataset using Python to analyze sales performance, product demand, transaction patterns, and data quality.
The analysis processes more than 6 million transaction records in manageable chunks, generates summary tables, and produces visualizations to explore sales trends across different currencies, products, and stores.
The goal is to demonstrate practical skills in data processing, data cleaning, exploratory data analysis (EDA), and data visualization.

My Objectives

- Assess data quality and identify potential inconsistencies.
- Calculate key sales and transaction metrics.
- Analyze monthly sales trends.
- Identify top-performing products, categories, and stores.
- Explore transaction types and payment methods.
- Summarize customer purchasing activity.
- Communicate results through clear, informative visualizations.

Tools used

- Python
- pandas
- NumPy
- Matplotlib
- Seaborn

Source

This project uses the "Global Fashion Retail Stores Dataset" (https://www.kaggle.com/datasets/ricgomes/global-fashion-retail-stores-dataset), published on Kaggle by Ric. G.

The dataset includes transaction records and supporting information about customers, products, stores, employees, and discounts.

The original CSV files are expected to be placed in "data/raw/". For data privacy, repository size, and distribution considerations, the raw dataset files are not included in this repository.

Project Structure

sales-data-analysis/
├── data/
│   ├── raw/              # Original dataset files (Also available on the previously shared Kaggle Repository)
│   └── processed/        # Processed data
├── src/
│   ├── data_loader.py    # Data loading
│   ├── preprocessing.py  # Data cleaning
│   ├── analysis.py       # Aggregation and analysis
│   ├── visualization.py  # Chart generation
│   └── main.py           # Main execution script
├── outputs/
│   ├── figures/          # Generated charts
│   └── reports/          # Generated CSV summaries
├── requirements.txt      # Tools previously mentioned (pandas, MatPlotLib, SeaBorn, etc...)
├── .gitignore
└── README.md


How to Run
1. Clone the repository
git clone https://github.com/if0001/sales-data-analysis
cd sales-data-analysis

2. Install dependencies
Install the required packages (requirements.txt file):
pip install -r requirements.txt

3. Add the dataset
Download the dataset from Kaggle and place the original CSV files in "data/raw/", preserving their filenames.

4. Run the analysis
From the project root directory, execute:
python -m src.main
The script processes transaction data in chunks and generates summary reports and charts in the "outputs/" directory.

Final Outputs

The analysis made generates CSV reports covering:

- Overall sales summaries by currency
- Monthly sales trends
- Product performance
- Store performance
- Payment methods
- Transaction types
- Customer-level metrics
- Data quality checks by processing chunk

It also generates charts showing monthly recorded amounts, top products, category performance, store performance, and transaction types.

Scope

This is an independent portfolio project intended to demonstrate practical data analysis skills. The findings describe the dataset analyzed and should not be interpreted as a representation of current retail market conditions or as a guarantee of future performance.
Amounts are analyzed separately by currency and should not be combined without a suitable currency conversion method. Sales and returns should also be interpreted in the context of the dataset's transaction definitions.

Disclaimer:
This project uses historical, publicly available data. The analysis is for educational and portfolio purposes only.

