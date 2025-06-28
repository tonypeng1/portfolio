import pandas as pd
import os


def main():
    print("Hello from portfolio!\n")

    # Find the only file in the data/data_fidelity directory
    data_dir = "data/data_fidelity"
    files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
    if not files:
        print("No files found in data/data_fidelity.")
        return

    file_path = os.path.join(data_dir, files[0])
    df = pd.read_csv(file_path)
    # print(df.head())

    print(f"Loaded data from {file_path}\n")

    # Clean and sum all the values in the "Current Value" column
    df["Current Value"] = (
        df["Current Value"]
        .astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .replace("--", "0")
    )
    df["Current Value"] = pd.to_numeric(df["Current Value"], errors="coerce")
    total_current_value_fidelity = df["Current Value"].sum()
    print(f"Total Fidelity Current Value: ${round(total_current_value_fidelity):,}\n")

    # Filter rows where "Description" is in the specified cash list
    filter_list_cash_fidelity = ["HELD IN MONEY MARKET", "FDIC-INSURED DEPOSIT SWEEP"]
    filtered_df_cash_fidelity = df[df["Description"].isin(filter_list_cash_fidelity)]

    # Sum the "Current Value" for the filtered DataFrame
    value_cash_fidelity = filtered_df_cash_fidelity["Current Value"].sum()
    print(f"Total Current Value for {filter_list_cash_fidelity}: ${round(value_cash_fidelity):,}\n")

    # Calculate and print the percentage of value_cash_fidelity to total_current_value_fidelity
    if total_current_value_fidelity != 0:
        percent_cash = (value_cash_fidelity / total_current_value_fidelity) * 100
        print(f"Cash as percentage of total: {percent_cash:.1f}%\n")
    else:
        print("Total current value is zero, cannot compute percentage.")

    # Create a new 'Group' column: 'Cash' for cash descriptions, else use the original description
    df["Group"] = df["Description"].apply(
        lambda x: "Cash" if x in filter_list_cash_fidelity else x
    )

    # Group by 'Group', sum 'Current Value', and calculate percentage of total
    grouped = (
        df.groupby("Group")["Current Value"]
        .sum()
        .reset_index()
        .sort_values("Current Value", ascending=False)
    )
    grouped["Percentage of Total"] = (grouped["Current Value"] / total_current_value_fidelity) * 100

    # Add 'Symbol' to the grouped DataFrame (empty for 'Cash')
    def symbol_agg(x):
        if x.name == "Cash":
            return ""
        return x["Symbol"].dropna().unique()[0] if not x["Symbol"].dropna().empty else ""

    grouped_symbols = (
        df.groupby("Group").agg({'Symbol': lambda s: "" if s.name == "Cash" else (s.dropna().unique()[0] if not s.dropna().empty else "")}).reset_index()
    )

    # Merge symbols into grouped DataFrame
    grouped = grouped.merge(grouped_symbols, left_on="Group", right_on="Group")

    # Reorder columns for display
    grouped = grouped[["Group", "Symbol", "Current Value", "Percentage of Total"]]

    print("Current Value by Group as Percentage of Total:\n")
    print(grouped.to_string(index=False, formatters={
        "Current Value": "${:,.2f}".format,
        "Percentage of Total": "{:.2f}%".format
    }))
    print("")

if __name__ == "__main__":
    main()
