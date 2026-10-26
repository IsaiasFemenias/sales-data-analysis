from pathlib import Path
import pandas as pd
ruta = Path(__file__).resolve().parent.parent
ruta_raw = ruta / "data" / "raw"
procesado = ruta / "data" / "processed"
figures_dir = ruta / "outputs" / "figures"
reports_dir = ruta / "outputs" / "reports"

def ensure_output_dirs(): #creating output dirs if they dont exist
    for directory in (procesado,
        figures_dir,
        reports_dir,):
        directory.mkdir(parents=True, exist_ok=True)
def load_reference_data(): #here I am just loading smaller csvs for product and store analysis
    products_path = ruta_raw / "products.csv"
    stores_path = ruta_raw / "stores.csv"
    if not products_path.exists():
        raise FileNotFoundError(
            f"Products file not found: {products_path}")
    if not stores_path.exists():
        raise FileNotFoundError(
            f"Stores file not found: {stores_path}")
    products = pd.read_csv(products_path)
    stores = pd.read_csv(stores_path)
    return products, stores

def iter_transaction_chunks(chunksize=100_000): #yield transaction data in manageable chunks (100k as I said)
    transactions_path = ruta_raw / "transactions.csv"
    if not transactions_path.exists():
        raise FileNotFoundError(
            f"Transactions file not found: {transactions_path}")
    required_columns = ["Invoice ID","Customer ID","Product ID","Unit Price","Quantity","Date","Discount","Line Total","Store ID","Currency","Transaction Type","Payment Method",]
    header = pd.read_csv(transactions_path,nrows=0, encoding="utf-8-sig",)
    missing = set(required_columns) - set(header.columns)
    if missing:
        raise ValueError(
            f"Missing transaction columns: {sorted(missing)}")
    yield from pd.read_csv(
        transactions_path,
        usecols=required_columns,
        chunksize=chunksize,
        encoding="utf-8-sig",
        low_memory=True,)