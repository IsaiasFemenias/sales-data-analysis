from pathlib import Path
import pandas as pd
#this is just a check to see if files are readable by the code itself, not much to see here.

# ubicar la ruta automáticamente
ruta = Path(__file__).resolve().parent.parent
Raws = ruta / "data" / "raw"

csv_files = sorted(Raws.glob("*.csv"))

if not csv_files:
    print(f"No CSVs found in: {Raws}")
else:
    print(f"CSVs Found: {len(csv_files)}\n") 
    for file_path in csv_files:
        print("=" * 70)
        print(f"File: {file_path.name}")
        print(f"Size: {file_path.stat().st_size / (1024**2):.2f} MB")
        try: # read only 5 rows to overview the csv
            try: sample = pd.read_csv(file_path,
                    nrows=5,
                    sep=None,
                    engine="python",
                    encoding="utf-8-sig",)
            except UnicodeDecodeError:
                sample = pd.read_csv(file_path,
                    nrows=5,
                    sep=None,
                    engine="python",
                    encoding="cp1252",)
            print(f"\nColumns ({len(sample.columns)}):")
            print(sample.columns.tolist())
            print("\nFirst five rows:")
            print(sample.to_string(index=False))
            print("\nDetected types:")
            print(sample.dtypes)
        except Exception as error:
            print(f"No se pudo inspeccionar el archivo: {error}") #this line only triggers if the csv cannot be read, so if everything is okay it will not be shown.
        print()