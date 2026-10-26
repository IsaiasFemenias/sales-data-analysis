
# this entire file is just for visualization: graphs, bars, etc., using Matplotlib and Seaborn.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_loader import figures_dir

sns.set_theme(style="whitegrid", context="notebook")

def plot_monthly_revenue(monthly):
    for currency, data in monthly.groupby("Currency"):
        data = data.sort_values("Month")
        fig, ax = plt.subplots(figsize=(11, 5))
        sns.lineplot(
            data=data,
            x="Month",
            y="revenue",
            marker="o",
            ax=ax,)

        ax.set_title(f"Monthly Recorded Amount ({currency})")
        ax.set_xlabel("Month")
        ax.set_ylabel(f"Recorded amount ({currency})")
        ax.tick_params(axis="x", rotation=45)

        fig.tight_layout()
        fig.savefig(figures_dir / f"monthly_revenue_{currency}.png",
            dpi=150,
            bbox_inches="tight",)
        plt.close(fig)

def plot_top_products(products, top_n=10):
    for currency, data in products.groupby("Currency"):
        top = (data.sort_values("revenue", ascending=False).head(top_n).copy())
        top["Product"] = top["Product ID"].astype(str)
        fig, ax = plt.subplots(figsize=(10, 6))

        sns.barplot( data=top, x="revenue", y="Product", hue="Product", legend=False, ax=ax,)
        ax.set_title(f"Top {top_n} Products by Recorded Amount ({currency})")
        ax.set_xlabel(f"Recorded amount ({currency})")
        ax.set_ylabel("Product ID")

        fig.tight_layout()
        fig.savefig(figures_dir / f"top_products_{currency}.png",dpi=150,bbox_inches="tight",)
        plt.close(fig)

def plot_category_revenue(products):
    if "Category" not in products.columns:
        return
    category_data = (products.dropna(subset=["Category"])
        .groupby(["Currency", "Category"], as_index=False,)["revenue"].sum())

    for currency, data in category_data.groupby("Currency"):
        data = data.sort_values("revenue", ascending=False)

        fig, ax = plt.subplots(figsize=(10, 5))

        sns.barplot(data=data, x="revenue", y="Category", hue="Category", legend=False, ax=ax,)
        ax.set_title(f"Recorded Amount by Category ({currency})")
        ax.set_xlabel(f"Recorded amount ({currency})")
        ax.set_ylabel("Category")

        fig.tight_layout()
        fig.savefig(figures_dir / f"category_revenue_{currency}.png",dpi=150,bbox_inches="tight",)
        plt.close(fig)

def plot_store_revenue(stores, top_n=10):
    for currency, data in stores.groupby("Currency"):
        top = (data.sort_values("revenue", ascending=False) .head(top_n).copy())
        top["Store"] = top["Store Name"].fillna(
            top["Store ID"].astype(str))

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=top, x="revenue", y="Store", hue="Store", legend=False, ax=ax,)
        ax.set_title(f"Top {top_n} Stores by Recorded Amount ({currency})")
        ax.set_xlabel(f"Recorded amount ({currency})")
        ax.set_ylabel("Store")

        fig.tight_layout()
        fig.savefig(figures_dir / f"top_stores_{currency}.png", dpi=150, bbox_inches="tight", )
        plt.close(fig)

def plot_transaction_types(transaction_types):
    for currency, data in transaction_types.groupby("Currency"):
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.barplot(data=data, x="Transaction Type", y="line_count", hue="Transaction Type", legend=False, ax=ax,)
        ax.set_title(f"Transaction Lines by Type ({currency})")
        ax.set_xlabel("Transaction type")
        ax.set_ylabel("Number of lines")
        ax.tick_params(axis="x", rotation=25)
        fig.tight_layout()
        fig.savefig(figures_dir / f"transaction_types_{currency}.png",
            dpi=150,bbox_inches="tight", )
        plt.close(fig)
