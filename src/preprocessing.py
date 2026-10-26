import pandas as pd
numericos = ["Customer ID","Product ID","Unit Price","Quantity","Discount","Line Total","Store ID",] #Numéricos in spanish means numeric (referring to the columns here)
# here Ill normalize data types and log potential issues without automatically removing returns.
def clean_transactions(df):
    df = df.copy()
    original_rows = len(df)
    df = df.drop_duplicates().copy()
    duplicates_removed = original_rows - len(df)
    for column in numericos:
        df[column] = pd.to_numeric(df[column],
            errors="coerce",)
    df["Date"] = pd.to_datetime(df["Date"],errors="coerce",) # Parse dates.
    # Normalize text columns.
    for column in ["Invoice ID","Currency", "Transaction Type","Payment Method",]:
        df[column] = df[column].astype("string").str.strip()
    # A row is usable for basic analysis only if its key fields exist, so:
    required = ["Invoice ID","Product ID","Date","Quantity","Unit Price","Line Total",]
    valid_mask = df[required].notna().all(axis=1)
    invalid_rows = int((~valid_mask).sum())
    df = df.loc[valid_mask].copy()
    quality = {
        "rows_before_cleaning": original_rows,
        "exact_duplicates_removed": duplicates_removed,
        "rows_missing_required_fields": invalid_rows,
        "rows_after_cleaning": len(df),
        "negative_quantity_rows": int(
            (df["Quantity"] < 0).sum() ),
        "nonpositive_price_rows": int(
            (df["Unit Price"] <= 0).sum()),
        "negative_line_total_rows": int(
            (df["Line Total"] < 0).sum()),
        "missing_customer_id_rows": int(
            df["Customer ID"].isna().sum()),}
    #I do not discard negative quantities or amounts automatically, as they may represent returns or adjustments.
    return df, quality