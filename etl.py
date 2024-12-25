# Importing the required libraries
import requests
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup
import logging

# Configure logging
def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    logging.basicConfig(
        filename="code_log.txt",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info(message)

def extract(url, table_attribs):
    log_progress("Starting data extraction")  
    # Fetch the webpage content
    response = requests.get(url)
    if response.status_code != 200:
        log_progress("Failed to fetch the webpage")
        raise Exception("Failed to fetch the webpage")   
    # Parse the webpage content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')   
    # Locate the table containing the required information
    table = soup.find("table", table_attribs)
    if not table:
        log_progress("Failed to find the specified table on the webpage")
        raise Exception("Table not found on the webpage with the provided attributes")    
    rows = table.find_all("tr")
    log_progress(f"Found {len(rows)} rows in the table")
    # Extract data for all banks (verify structure manually)
    data = []
    for row in rows[1:]:  # Skip header row
        cols = row.find_all("td")
        if len(cols) > 2:  # Ensure there are enough columns
            # Extract the bank name and market capitalization
            name = cols[1].text.strip()  # Adjust column index if needed
            mc_text = cols[2].text.strip().replace(",", "").split("[")[0]
            try:
                mc_usd = float(mc_text)  # Convert market cap to float
                data.append({"Name": name, "Market_Cap_USD_Billion": mc_usd})
            except ValueError:
                log_progress(f"Invalid market capitalization value for {name}")
                continue
    # Log the number of valid rows extracted
    log_progress(f"Extracted {len(data)} rows successfully")
    # Convert the extracted data into a DataFrame
    df = pd.DataFrame(data)
    log_progress("Data extraction completed successfully")
    return df

def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    try:
        rates = pd.read_csv(csv_path)
        rates.set_index("Currency", inplace=True)
        df["Market_Cap_GBP_Billion"] = df["Market_Cap_USD_Billion"] * rates.loc["GBP", "Rate"]
        df["Market_Cap_EUR_Billion"] = df["Market_Cap_USD_Billion"] * rates.loc["EUR", "Rate"]
        df["Market_Cap_INR_Billion"] = df["Market_Cap_USD_Billion"] * rates.loc["INR", "Rate"]
        log_progress("Data transformation successful.")
        return df
    except Exception as e:
        log_progress(f"Error during transformation: {e}")
        raise

def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''
    try:
        df.to_csv(output_path, index=False)
        log_progress(f"Data saved to CSV at {output_path}.")
    except Exception as e:
        log_progress(f"Error saving data to CSV: {e}")
        raise

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
    try:
        conn = sqlite3.connect(sql_connection)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        log_progress(f"Data saved to database table {table_name}.")
    except Exception as e:
        log_progress(f"Error saving data to database: {e}")
        raise

def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    try:
        conn = sqlite3.connect(sql_connection)
        cursor = conn.cursor()
        cursor.execute(query_statement)
        results = cursor.fetchall()
        for row in results:
            print(row)
        conn.close()
        log_progress("Query executed successfully.")
    except Exception as e:
        log_progress(f"Error running query: {e}")
        raise

# Main script execution
if __name__ == "__main__":
    # Define parameters
    data_url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
    exchange_rate_csv = "./exchange_rate.csv"
    output_csv = "./Largest_banks_data.csv"
    db_name = "Banks.db"
    table_name = "Largest_banks"

    # Call functions in sequence
    try:
        df = extract(data_url, {"class": "wikitable"})
        print(df.head())  # Debugging: Check extracted data
        transformed_df = transform(df, exchange_rate_csv)
        print(transformed_df.head())  # Debugging: Check transformed data
        load_to_csv(transformed_df, output_csv)
        load_to_db(transformed_df, db_name, table_name)

        print("\nContents of the entire table:")
        query = f"SELECT * FROM {table_name};"
        run_query(query, db_name)

        print("\nAverage market capitalization in GBP:")
        query = f"SELECT AVG(Market_Cap_GBP_Billion) FROM {table_name};"
        run_query(query, db_name)

        print("\nTop 5 banks by name:")
        query = f"SELECT Name FROM {table_name} LIMIT 5;"
        run_query(query, db_name)

    except Exception as e:
        log_progress(f"Workflow execution failed: {e}")
