# main execution entry point.
from src.analysis import analyze_transactions, create_summary
from src.data_loader import ( figures_dir, reports_dir, ensure_output_dirs, iter_transaction_chunks, load_reference_data,)
from src.visualization import (plot_category_revenue, plot_monthly_revenue, plot_top_products, plot_store_revenue, plot_transaction_types,)

def main():
    ensure_output_dirs()
    print("=" * 70)
    print("SALES DATA ANALYSIS")
    print("=" * 70)
    print("\nLoading product and store reference data...") #obviamente se puede proceder sin hacer este print, simplemente queda mas "profesional"
    products, stores = load_reference_data()
    print(f"Products loaded: {len(products):,}")
    print(f"Stores loaded: {len(stores):,}")
    print("\nProcessing transactions in chunks...")
    results = analyze_transactions(iter_transaction_chunks(chunksize=100_000), products, stores,)
    print("\nCreating summary...")
    summary = create_summary(results)

    # saved aggregated tables, not raw customer information.
    tables = {"sales_summary.csv": summary,
        "monthly_sales.csv": results["monthly"],
        "product_sales.csv": results["products"],
        "store_sales.csv": results["stores"],
        "payment_methods.csv": results["payments"],
        "transaction_types.csv": results["transaction_types"],
        "customer_metrics.csv": results["customers"],
        "data_quality_by_chunk.csv": results["quality"],}

    for filename, table in tables.items():
        output_path = reports_dir / filename
        table.to_csv(output_path, index=False)
        print(f"Saved: {output_path.name}")

    # generate visualizations.
    plot_monthly_revenue(results["monthly"])
    plot_top_products(results["products"])
    plot_category_revenue(results["products"])
    plot_store_revenue(results["stores"])
    plot_transaction_types(results["transaction_types"])
    metadata = results["metadata"]

# Just for showcase purposes, I decided to print key stats summarizing the work done.
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETED")
    print("=" * 70)
    print(f"Rows processed: {metadata['rows_processed']:,}")
    print(f"Unique invoice IDs: {metadata['unique_invoices']:,}")
    print(f"Currencies: {metadata['currencies']}")
    print(f"Transaction types: {metadata['transaction_types']}")
    print(f"\nReports directory: {reports_dir}")
    print(f"Figures directory: {figures_dir}")

    print("\nSummary:")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()