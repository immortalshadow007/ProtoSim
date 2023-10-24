import os
import psycopg2
from getpass import getpass

# Request user input for database connection details
db_name = input("Enter the database name: ")
host = input("Enter the host (e.g., localhost): ")
port = input("Enter the port (usually 5432 for PostgreSQL): ")
username = input("Enter the username: ")
password = getpass("Enter the password (input will be hidden): ")

# Establish a connection to the database
conn = psycopg2.connect(
    dbname=db_name,
    host=host,
    port=port,
    user=username,
    password=password
)
cursor = conn.cursor()

# Define paths to the scripts
scripts = {
    "baseline": "C:\\Users\\HP Pavilion\\Sims-and-Proto\\baseline.py",
    "variation_a": "C:\\Users\\HP Pavilion\\Sims-and-Proto\\variation_1.py",
    "variation_b": "C:\\Users\\HP Pavilion\\Sims-and-Proto\\variation_2.py"
}

# Number of runs
num_runs = 1000

# List to accumulate the rows
data_to_insert = []

for run in range(num_runs):
    # Dictionary to store results for this run
    daily_results = {}

    for variation, script_path in scripts.items():
        # Execute the script and capture the output
        output = os.popen(f'python "{script_path}"').read().split("\n")
        
        # Extract the daily views from the output
        daily_views = []
        for line in output:
            if line.startswith("Day"):
                day_views = int(line.split(":")[1].strip().split(" ")[0])  # Extracting view count from "Day X: Y views"
                daily_views.append(day_views)

        # Store the daily views in the daily_results dictionary
        daily_results[variation] = daily_views

    # Define paths to the saved plots
    plot_paths = {
        "baseline": "C:\\Users\\HP Pavilion\\Sims-and-Proto\\baseline_plot",
        "variation_a": "C:\\Users\\HP Pavilion\\Sims-and-Proto\\variation_a_plot",
        "variation_b": "C:\\Users\\HP Pavilion\\Sims-and-Proto\\variation_b_plot"
    }

    # Fetch the latest saved plots for each variation
    latest_plots = {}
    for variation, plot_dir in plot_paths.items():
        latest_plot = max(os.listdir(plot_dir), key=lambda x: os.path.getctime(os.path.join(plot_dir, x)))
        latest_plots[variation] = os.path.join(plot_dir, latest_plot)

    # Append the data to the list
    row_data = [run] + daily_results["baseline"] + daily_results["variation_a"] + daily_results["variation_b"] + [latest_plots["baseline"], latest_plots["variation_a"], latest_plots["variation_b"]]
    data_to_insert.append(tuple(row_data))

# Construct the SQL query for bulk insert
sql_query = """
INSERT INTO "Sim Data" (run_id, baseline_views_day_1, baseline_views_day_2, baseline_views_day_3, baseline_views_day_4, 
baseline_views_day_5, baseline_views_day_6, baseline_views_day_7, variation_a_views_day_1, variation_a_views_day_2, 
variation_a_views_day_3, variation_a_views_day_4, variation_a_views_day_5, variation_a_views_day_6, variation_a_views_day_7, 
variation_b_views_day_1, variation_b_views_day_2, variation_b_views_day_3, variation_b_views_day_4, variation_b_views_day_5, 
variation_b_views_day_6, variation_b_views_day_7, baseline_plot, variation_a_plot, variation_b_plot, "timestamp")
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, DEFAULT);
"""

# Bulk insert data into the database
cursor.executemany(sql_query, data_to_insert)
conn.commit()

cursor.close()
conn.close()