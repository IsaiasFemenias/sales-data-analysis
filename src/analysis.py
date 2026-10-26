#you found gold! This is where the core data transformation actually happens.
from collections import defaultdict
import pandas as pd
from src.preprocessing import clean_transactions

#this func analyzes chunks and returns aggregated tables
def analyze_transactions(chunks, products, stores): 
    monthly_parts = []
    product_parts = []
    store_parts = []
    payment_parts = []
    type_parts = []
    customer_parts = []
    quality_records = []
    invoice_ids = set()
    transaction_types = set()
    currencies = set()
    rows_processed = 0

    for chunk_number, chunk in enumerate(chunks, start=1):
        df, quality = clean_transactions(chunk)
        quality["chunk"] = chunk_number
        quality_records.append(quality)
        rows_processed += len(df)

        df = df.loc[df["Currency"].notna()].copy() #excluding rows with no usable currency from monetary metrics.
        invoice_ids.update(df["Invoice ID"].dropna().unique())
        transaction_types.update(df["Transaction Type"].dropna().unique())
        currencies.update(df["Currency"].dropna().unique())
        df["Revenue"] = df["Line Total"]
        df["Month"] = (
            df["Date"].dt.to_period("M").astype(str))
        
        monthly_parts.append(
            df.groupby(["Currency", "Month"],
                as_index=False,
                observed=True,).agg(revenue=("Revenue", "sum"),
                units=("Quantity", "sum"),
                line_count=("Invoice ID", "size"),))

        product_parts.append(
            df.groupby(["Currency", "Product ID"],
                as_index=False,
                observed=True,).agg(revenue=("Revenue", "sum"),
                units=("Quantity", "sum"),
                line_count=("Invoice ID", "size"),))

        store_parts.append(
            df.groupby(["Currency", "Store ID"],
                as_index=False,
                observed=True,).agg(
                revenue=("Revenue", "sum"),
                units=("Quantity", "sum"),
                line_count=("Invoice ID", "size"),))

        payment_parts.append(
            df.groupby(["Currency", "Payment Method"],
                as_index=False,
                observed=True,
                dropna=False,).agg(revenue=("Revenue", "sum"),
                line_count=("Invoice ID", "size"),))

        type_parts.append(
            df.groupby(["Currency", "Transaction Type"],
                as_index=False,
                observed=True,
                dropna=False,).agg(revenue=("Revenue", "sum"),
                units=("Quantity", "sum"),
                line_count=("Invoice ID", "size"),))

        # customer IDs are pseudonymous identifiers for aggregation; I will not load names, emails, and telephone numbers.
        customer_data = df.dropna(subset=["Customer ID"])
        customer_parts.append(
            customer_data.groupby(["Currency", "Customer ID"],
                as_index=False,
                observed=True,).agg(revenue=("Revenue", "sum"),
                units=("Quantity", "sum"),
                line_count=("Invoice ID", "size"),))

        print( f"Processed chunk {chunk_number:,} | "f"Rows analyzed: {rows_processed:,}" )

    if not monthly_parts:raise ValueError("No valid transaction rows were found.")

    def combine(parts, keys):
        """Combine partial aggregates into final aggregates."""
        combined = pd.concat(parts, ignore_index=True)
        return (combined.groupby(keys,as_index=False,dropna=False, ).sum(numeric_only=True) )

    monthly = combine(monthly_parts,["Currency", "Month"],)

    product_sales = combine(product_parts,["Currency", "Product ID"],)

    store_sales = combine(store_parts,["Currency", "Store ID"],)

    payment_sales = combine(payment_parts,["Currency", "Payment Method"],)

    type_sales = combine(type_parts,["Currency", "Transaction Type"],)

    customer_sales = combine(customer_parts,["Currency", "Customer ID"],)

    # Add descriptive product and store attributes.
    product_columns = ["Product ID",
        "Category",
        "Sub Category",
        "Description EN",
        "Production Cost",]

    product_sales = product_sales.merge(products[product_columns].drop_duplicates("Product ID"),
        on="Product ID",
        how="left",
        validate="many_to_one",)

    store_columns = ["Store ID","Country","City","Store Name",]

    store_sales = store_sales.merge( stores[store_columns].drop_duplicates("Store ID"),on="Store ID",how="left",validate="many_to_one",)

    quality = pd.DataFrame(quality_records)
    metadata = {"rows_processed": rows_processed,"unique_invoices": len(invoice_ids),"currencies": sorted(currencies),"transaction_types": sorted(transaction_types),}
    return {"monthly": monthly,
        "products": product_sales,
        "stores": store_sales,
        "payments": payment_sales,
        "transaction_types": type_sales,
        "customers": customer_sales,
        "quality": quality,
        "metadata": metadata,}

# this func builds a concise summary, keeping currencies separate.
def create_summary(results): 
    monthly = results["monthly"]
    summary = (monthly.groupby("Currency", as_index=False)
        .agg(total_recorded_amount=("revenue", "sum"),
            total_units=("units", "sum"),
            transaction_lines=("line_count", "sum"),
            months_observed=("Month", "nunique"),))
    return summary