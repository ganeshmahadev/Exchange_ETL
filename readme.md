# Banks Project: Extract, Transform, and Load (ETL) for Largest Banks by Market Capitalization

## Overview
This project automates the process of extracting data on the world's largest banks by market capitalization, transforming the data into different currencies (GBP, EUR, INR), and storing it in both CSV and SQLite database formats. It also includes functionality to run queries for analysis.

---

## Features
1. **Data Extraction**
   - Extracts data from a webpage listing the top 10 largest banks in the world.
   - Parses HTML tables using `BeautifulSoup` to retrieve the name and market capitalization of each bank.

2. **Data Transformation**
   - Converts market capitalization from USD to GBP, EUR, and INR using exchange rates from a provided CSV file.

3. **Data Storage**
   - Saves the transformed data into a CSV file.
   - Loads the data into an SQLite database for easy querying.

4. **Query Execution**
   - Provides query examples to:
     - Print the entire contents of the database table.
     - Calculate the average market capitalization in GBP.
     - Retrieve the names of the top 5 banks.

---

## Requirements

The project requires the following Python libraries:
- `requests`: For fetching the webpage data.
- `pandas`: For data manipulation and transformation.
- `sqlite3`: For database storage and query execution.
- `beautifulsoup4`: For parsing HTML tables.
- `logging`: For tracking the execution flow and debugging errors.

### Installation
To install the required libraries, use:
```bash
pip install requests pandas beautifulsoup4
```

---

## Project Structure

```plaintext
banks_project.py       # Main ETL script
exchange_rate.csv      # Exchange rates file
Largest_banks_data.csv # Transformed data in CSV format
Banks.db               # SQLite database file
code_log.txt           # Log file for tracking execution
```

---

## How to Run the Project

1. Clone or download the project files.
2. Ensure `exchange_rate.csv` is present in the working directory.
3. Run the script using:
```bash
python banks_project.py
```
4. The script will:
   - Extract data from the webpage.
   - Transform market capitalization to GBP, EUR, and INR.
   - Save the results to a CSV file and an SQLite database.
   - Execute predefined SQL queries.

---

## Output
### Generated Files
- **CSV File:** The transformed data is saved as `Largest_banks_data.csv`.
- **Database File:** The transformed data is stored in `Banks.db` under the `Largest_banks` table.

### Query Results
1. **Entire Table Contents:**
   ```sql
   SELECT * FROM Largest_banks;
   ```
   Prints the entire table.

2. **Average Market Capitalization (GBP):**
   ```sql
   SELECT AVG(Market_Cap_GBP_Billion) FROM Largest_banks;
   ```
   Prints the average market capitalization in GBP.

3. **Top 5 Bank Names:**
   ```sql
   SELECT Name FROM Largest_banks LIMIT 5;
   ```
   Prints the names of the top 5 banks.

---

## Logging
All key execution steps, errors, and debug messages are logged in the `code_log.txt` file. This helps in tracking progress and troubleshooting issues.

---

## Example Queries
To interact with the database, you can modify the SQL queries in the script or run your own queries using an SQLite client.

### Sample Queries:
1. **Print All Data:**
   ```sql
   SELECT * FROM Largest_banks;
   ```
2. **Calculate Average Market Cap in EUR:**
   ```sql
   SELECT AVG(Market_Cap_EUR_Billion) FROM Largest_banks;
   ```
3. **Retrieve Bank Names with Market Cap > 200 Billion USD:**
   ```sql
   SELECT Name FROM Largest_banks WHERE Market_Cap_USD_Billion > 200;
   ```






