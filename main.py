import pandas as pd
import os


def main():
    print("Hello from portfolio!\n")

    # Find the only file in the data/data_fidelity directory
    data_dir = "data/data_fidelity"
    files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f)) and f.lower().endswith(".csv")]
    if not files:
        print("No files found in data/data_fidelity.")
        return

    file_path = os.path.join(data_dir, files[0])
    df_fidelity = pd.read_csv(file_path, encoding='latin1', skip_blank_lines=True)
    # Remove non-ASCII characters from column names
    df_fidelity.columns = df_fidelity.columns.str.strip().str.replace(r"[^\x00-\x7F]+", "", regex=True)
    # print(df_fidelity.head())

    print(f"Load data from {file_path}\n")

    # Remove the row with Account Number == "32213"
    df_fidelity = df_fidelity[df_fidelity["Account Number"] != "32213"]
    # Remove the row with Account Number == "X77788987"
    df_fidelity = df_fidelity[df_fidelity["Account Number"] != "X77788987"]

    # Clean and sum all the values in the "Current Value" column
    df_fidelity["Current Value"] = (
        df_fidelity["Current Value"]
        .astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .replace("--", "0")
    )
    df_fidelity["Current Value"] = pd.to_numeric(df_fidelity["Current Value"], errors="coerce")
    total_current_value_fidelity = df_fidelity["Current Value"].sum()
    print(f"Total Fidelity Current Value: ${round(total_current_value_fidelity):,}\n")

    # # Filter rows where "Description" is in the specified cash list
    # filter_list_cash_fidelity = ["HELD IN MONEY MARKET", "FDIC-INSURED DEPOSIT SWEEP"]

    # Filter rows where "Symbol" is in the specified cash list
    filter_list_cash_fidelity = ["SPAXX**", "FDRXX**", "CORE**", "USD***", "Pending Activity"]

    filtered_df_cash_fidelity = df_fidelity[df_fidelity["Symbol"].isin(filter_list_cash_fidelity)]

    # Sum the "Current Value" for the filtered DataFrame
    value_cash_fidelity = filtered_df_cash_fidelity["Current Value"].sum()
    print(f"Total Current Value for {filter_list_cash_fidelity}: ${round(value_cash_fidelity):,}\n")

    # Calculate and print the percentage of value_cash_fidelity to total_current_value_fidelity
    if total_current_value_fidelity != 0:
        percent_cash = (value_cash_fidelity / total_current_value_fidelity) * 100
        print(f"Cash as percentage of total: {percent_cash:.2f}%\n")
    else:
        print("Total current value is zero, cannot compute percentage.")


    # Create a new 'Group' column: 'Cash' for cash descriptions, else use the original description
    df_fidelity["Group"] = df_fidelity["Symbol"].apply(
        lambda x: "Cash" if x in filter_list_cash_fidelity else x
    )

    # Group by 'Group', sum 'Current Value', and calculate percentage of total
    grouped_fidelity = (
        df_fidelity.groupby("Group")["Current Value"]
        .sum()
        .reset_index()
        .sort_values("Current Value", ascending=False)
    )
    grouped_fidelity["Percentage of Total"] = (grouped_fidelity["Current Value"] / total_current_value_fidelity) * 100

    # Add 'Symbol' to the grouped DataFrame: empty for 'Cash', else the group name (which is the Symbol)
    grouped_fidelity["Symbol"] = grouped_fidelity["Group"].apply(lambda x: "" if x == "Cash" else x)

    # Create a mapping from Symbol to Description
    symbol_to_description = df_fidelity.set_index("Symbol")["Description"].to_dict()

    # Add 'Description' to the grouped DataFrame: blank for 'Cash', else map from Symbol
    grouped_fidelity["Description"] = grouped_fidelity["Group"].apply(lambda x: "" if x == "Cash" else symbol_to_description.get(x, ""))

    # Reorder columns for display
    grouped_fidelity = grouped_fidelity[["Group", "Description", "Current Value", "Percentage of Total"]]

    # Remove rows where Percentage of Total is less than 0.10%
    grouped_fidelity = grouped_fidelity[grouped_fidelity["Percentage of Total"] >= 0.005]

    # Format columns for CSV output to match terminal print
    grouped_fidelity_formatted = grouped_fidelity.copy()
    grouped_fidelity_formatted["Current Value"] = grouped_fidelity_formatted["Current Value"].map("${:,.2f}".format)
    grouped_fidelity_formatted["Percentage of Total"] = grouped_fidelity_formatted["Percentage of Total"].map("{:.2f}%".format)

    # Save grouped_fidelity to CSV in the data/ folder
    grouped_fidelity_formatted.to_csv("data/grouped_fidelity.csv", index=False)

    print("Current Value by Group as Percentage of Total (Fidelity):\n")
    print(grouped_fidelity.to_string(index=False, formatters={
        "Current Value": "${:,.2f}".format,
        "Percentage of Total": "{:.2f}%".format
    }))



    # Find the only file in the data/data_fidelity_simon directory
    data_dir = "data/data_fidelity_simon"
    files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f)) and f.lower().endswith(".csv")]
    if not files:
        print("No files found in data/data_fidelity_simon.")
        return

    file_path = os.path.join(data_dir, files[0])
    df_fidelity = pd.read_csv(file_path, encoding='latin1', skip_blank_lines=True)
    # Remove non-ASCII characters from column names
    df_fidelity.columns = df_fidelity.columns.str.strip().str.replace(r"[^\x00-\x7F]+", "", regex=True)
    # print(df_fidelity.head())

    print(f"\nLoad data from {file_path}\n")

    # Remove the row with Account Number == "84479"
    df_fidelity = df_fidelity[df_fidelity["Account Number"] != "84479"]
    # Remove the row with Account Number == "X77788987"
    df_fidelity = df_fidelity[df_fidelity["Account Number"] != "X77788987"]

    # Clean and sum all the values in the "Current Value" column
    df_fidelity["Current Value"] = (
        df_fidelity["Current Value"]
        .astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .replace("--", "0")
    )
    df_fidelity["Current Value"] = pd.to_numeric(df_fidelity["Current Value"], errors="coerce")
    total_current_value_fidelity = df_fidelity["Current Value"].sum()
    print(f"Total Fidelity Current Value: ${round(total_current_value_fidelity):,}\n")

    # # Filter rows where "Description" is in the specified cash list
    # filter_list_cash_fidelity = ["HELD IN MONEY MARKET", "FDIC-INSURED DEPOSIT SWEEP"]

    # Filter rows where "Symbol" is in the specified cash list
    filter_list_cash_fidelity = ["SPAXX**", "FDRXX**", "CORE**", "USD***", "Pending Activity"]

    filtered_df_cash_fidelity = df_fidelity[df_fidelity["Symbol"].isin(filter_list_cash_fidelity)]

    # Sum the "Current Value" for the filtered DataFrame
    value_cash_fidelity = filtered_df_cash_fidelity["Current Value"].sum()
    print(f"Total Current Value for {filter_list_cash_fidelity}: ${round(value_cash_fidelity):,}\n")

    # Calculate and print the percentage of value_cash_fidelity to total_current_value_fidelity
    if total_current_value_fidelity != 0:
        percent_cash = (value_cash_fidelity / total_current_value_fidelity) * 100
        print(f"Cash as percentage of total: {percent_cash:.2f}%\n")
    else:
        print("Total current value is zero, cannot compute percentage.")


    # Create a new 'Group' column: 'Cash' for cash descriptions, else use the original description
    df_fidelity["Group"] = df_fidelity["Symbol"].apply(
        lambda x: "Cash" if x in filter_list_cash_fidelity else x
    )

    # Group by 'Group', sum 'Current Value', and calculate percentage of total
    grouped_fidelity_simon = (
        df_fidelity.groupby("Group")["Current Value"]
        .sum()
        .reset_index()
        .sort_values("Current Value", ascending=False)
    )
    grouped_fidelity_simon["Percentage of Total"] = (grouped_fidelity_simon["Current Value"] / total_current_value_fidelity) * 100

    # Add 'Symbol' to the grouped DataFrame: empty for 'Cash', else the group name (which is the Symbol)
    grouped_fidelity_simon["Symbol"] = grouped_fidelity_simon["Group"].apply(lambda x: "" if x == "Cash" else x)

    # Create a mapping from Symbol to Description
    symbol_to_description = df_fidelity.set_index("Symbol")["Description"].to_dict()

    # Add 'Description' to the grouped DataFrame: blank for 'Cash', else map from Symbol
    grouped_fidelity_simon["Description"] = grouped_fidelity_simon["Group"].apply(lambda x: "" if x == "Cash" else symbol_to_description.get(x, ""))

    # Reorder columns for display
    grouped_fidelity_simon = grouped_fidelity_simon[["Group", "Description", "Current Value", "Percentage of Total"]]

    # Remove rows where Percentage of Total is less than 0.10%
    grouped_fidelity_simon = grouped_fidelity_simon[grouped_fidelity_simon["Percentage of Total"] >= 0.005]

    # Format columns for CSV output to match terminal print
    grouped_fidelity_simon_formatted = grouped_fidelity_simon.copy()
    grouped_fidelity_simon_formatted["Current Value"] = grouped_fidelity_simon_formatted["Current Value"].map("${:,.2f}".format)
    grouped_fidelity_simon_formatted["Percentage of Total"] = grouped_fidelity_simon_formatted["Percentage of Total"].map("{:.2f}%".format)

    # Save grouped_fidelity_simon to CSV in the data/ folder
    grouped_fidelity_simon_formatted.to_csv("data/grouped_fidelity_simon.csv", index=False)

    print("Current Value by Group as Percentage of Total (Fidelity):\n")
    print(grouped_fidelity_simon.to_string(index=False, formatters={
        "Current Value": "${:,.2f}".format,
        "Percentage of Total": "{:.2f}%".format
    }))


    
    # Find the only file in the data/data_charles directory
    data_dir = "data/data_charles"
    files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f)) and f.lower().endswith(".csv")]
    if not files:
        print("No files found in data/data_charles.")
        return

    file_path = os.path.join(data_dir, files[0])
    df_charles = pd.read_csv(file_path, encoding='latin1', skip_blank_lines=True)
    # print(df_charles.head())

    print(f"\nLoad data from {file_path}")

    # --- Begin Charles block extraction ---
    blocks = []
    i = 0
    while i < len(df_charles):
        # Find the row with 'Symbol' in the first column
        if str(df_charles.iloc[i, 0]).strip() == "Symbol":
            # Account name is in the row above
            account_name = str(df_charles.iloc[i - 1, 0]).strip() if i > 0 else ""
            # Header row
            header = df_charles.iloc[i].tolist()
            # Find the next block or end of DataFrame
            j = i + 1
            while j < len(df_charles) and str(df_charles.iloc[j, 0]).strip() != "Symbol":
                # Skip empty rows
                if not df_charles.iloc[j].isnull().all() and not all(str(x).strip() == "" for x in df_charles.iloc[j]):
                    blocks.append([account_name] + df_charles.iloc[j].tolist())
                j += 1
            # Prepare for next block
            i = j
        else:
            i += 1

    # Build new DataFrame
    if blocks:
        # Add 'Account Name' to the header
        new_header = ["Account Name"] + header
        df_charles_clean = pd.DataFrame(blocks, columns=new_header)
        # Rename "Mkt Val (Market Value)" to "Current Value"
        if "Mkt Val (Market Value)" in df_charles_clean.columns:
            df_charles_clean = df_charles_clean.rename(columns={"Mkt Val (Market Value)": "Current Value"})
        # Remove rows where 'Symbol' is one of the distinct account names or "Account Total"
        account_names = set(df_charles_clean["Account Name"].dropna().unique())
        df_charles_clean = df_charles_clean[~df_charles_clean["Symbol"].isin(account_names.union({"Account Total"}))]
        # print("\nCleaned Charles DataFrame:\n")
        # print(df_charles_clean)

        # Clean and sum all the values in the "Current Value" column for Charles
        df_charles_clean["Current Value"] = (
            df_charles_clean["Current Value"]
            .astype(str)
            .str.replace(r"[\$,]", "", regex=True)
        )
        df_charles_clean["Current Value"] = pd.to_numeric(df_charles_clean["Current Value"], errors="coerce")
        total_current_value_charles = df_charles_clean["Current Value"].sum()
        print(f"\nTotal Charles Current Value: ${round(total_current_value_charles):,}\n")
    else:
        print("No valid blocks found in Charles data.")


    # Filter rows where "Symbol" is in the specified cash list
    filter_list_cash_charles = ["SGVT", "SGOV", "Cash & Cash Investments"]
    filtered_df_cash_charles = df_charles_clean[df_charles_clean["Symbol"].isin(filter_list_cash_charles)]

    # Sum the "Current Value" for the filtered DataFrame
    value_cash_charles = filtered_df_cash_charles["Current Value"].sum()
    print(f"Total Current Value for {filter_list_cash_charles}: ${round(value_cash_charles):,}\n")

    # Calculate and print the percentage of value_cash_charles to total_current_value_charles
    if total_current_value_charles != 0:
        percent_cash_charles = (value_cash_charles / total_current_value_charles) * 100
        print(f"Cash as percentage of total: {percent_cash_charles:.2f}%\n")
    else:
        print("Total current value is zero, cannot compute percentage.")


    # Create a new 'Group' column: 'Cash' for cash symbols, else use the original symbol
    df_charles_clean["Group"] = df_charles_clean["Symbol"].apply(
        lambda x: "Cash" if x in filter_list_cash_charles else x
    )

    # Group by 'Group', sum 'Current Value', and calculate percentage of total
    grouped_charles = (
        df_charles_clean.groupby("Group")["Current Value"]
        .sum()
        .reset_index()
        .sort_values("Current Value", ascending=False)
    )
    grouped_charles["Percentage of Total"] = (grouped_charles["Current Value"] / total_current_value_charles) * 100

    # Add 'Symbol' to the grouped DataFrame: empty for 'Cash', else the group name (which is the Symbol)
    grouped_charles["Symbol"] = grouped_charles["Group"].apply(lambda x: "" if x == "Cash" else x)

    # Create a mapping from Symbol to Description
    symbol_to_description_charles = df_charles_clean.set_index("Symbol")["Description"].to_dict() if "Description" in df_charles_clean.columns else {}

    # Add 'Description' to the grouped DataFrame: blank for 'Cash', else map from Symbol
    grouped_charles["Description"] = grouped_charles["Group"].apply(lambda x: "" if x == "Cash" else symbol_to_description_charles.get(x, ""))

    # Reorder columns for display
    grouped_charles = grouped_charles[["Group", "Description", "Current Value", "Percentage of Total"]]

    # Remove rows where Percentage of Total is less than 0.10%
    grouped_charles = grouped_charles[grouped_charles["Percentage of Total"] >= 0.005]

    # Format columns for CSV output to match terminal print
    grouped_charles_formatted = grouped_charles.copy()
    grouped_charles_formatted["Current Value"] = grouped_charles_formatted["Current Value"].map("${:,.2f}".format)
    grouped_charles_formatted["Percentage of Total"] = grouped_charles_formatted["Percentage of Total"].map("{:.2f}%".format)

    # Save grouped_charles to CSV in the data/ folder
    grouped_charles_formatted.to_csv("data/grouped_charles.csv", index=False)

    print("Current Value by Group as Percentage of Total (Charles):\n")
    print(grouped_charles.to_string(index=False, formatters={
        "Current Value": "${:,.2f}".format,
        "Percentage of Total": "{:.2f}%".format
    }))



    # Before merging, rename Description and Current Value columns in grouped_charles
    grouped_charles_renamed = grouped_charles.rename(
        columns={"Description": "Description_charles", "Current Value": "Current Value_charles"}
    )

    merged = pd.merge(
        grouped_fidelity[["Group", "Description", "Current Value"]],
        grouped_fidelity_simon[["Group", "Description", "Current Value"]],
        on="Group",
        how="outer",
        suffixes=("_fidelity", "_simon")
    )

    merged = pd.merge(
        merged,
        grouped_charles_renamed[["Group", "Description_charles", "Current Value_charles"]],
        on="Group",
        how="outer"
    )

    # Fill NaN with 0 for Current Value columns
    merged["Current Value_fidelity"] = merged["Current Value_fidelity"].fillna(0)
    merged["Current Value_simon"] = merged["Current Value_simon"].fillna(0)
    merged["Current Value_charles"] = merged["Current Value_charles"].fillna(0)

    # Sum the Current Value columns
    merged["Total Current Value"] = (
        merged["Current Value_fidelity"] +
        merged["Current Value_simon"] +
        merged["Current Value_charles"]
    )

    # Choose Description: Fidelity if present, else Simon, else Charles
    merged["Description"] = (
        merged["Description_fidelity"]
        .combine_first(merged["Description_simon"])
        .combine_first(merged["Description_charles"])
    )

    # Recalculate Percentage of Total
    total_merged = merged["Total Current Value"].sum()
    merged["Percentage of Total"] = (merged["Total Current Value"] / total_merged) * 100

    # Sort by Percentage of Total in descending order
    merged = merged.sort_values("Percentage of Total", ascending=False)

    # Reorder columns
    merged = merged[["Group", "Description", "Total Current Value", "Percentage of Total"]]

    # Remove rows where Percentage of Total is less than 0.10%
    merged = merged[merged["Percentage of Total"] >= 0.005]

    # Format for CSV output
    merged_formatted = merged.copy()
    merged_formatted["Total Current Value"] = merged_formatted["Total Current Value"].map("${:,.2f}".format)
    merged_formatted["Percentage of Total"] = merged_formatted["Percentage of Total"].map("{:.2f}%".format)

    # Save to CSV
    merged_formatted.to_csv("data/grouped_merged.csv", index=False)

    print(f"\nTotal Merged Current Value: ${round(total_merged):,}")
    # Calculate and print cash as percentage of total for merged
    cash_row = merged[merged["Group"] == "Cash"]
    if not cash_row.empty:
        cash_percent = cash_row["Percentage of Total"].values[0]
        print(f"\nCash as percentage of total: {cash_percent:.2f}%")
    else:
        print("\nCash as percentage of total: 0.00%")

    print("\nMerged Current Value by Group as Percentage of Total:\n")
    print(merged.to_string(index=False, formatters={
        "Total Current Value": "${:,.2f}".format,
        "Percentage of Total": "{:.2f}%".format
    }))

    print("")

if __name__ == "__main__":
    main()
