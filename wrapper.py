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

for run in range(num_runs):
    # Dictionary to store results for this run
    results = {}

    for variation, script_path in scripts.items():
        # Execute the script and capture the output
        output = os.popen(f'python "{script_path}"').read()
        
        # Extract the total views from the output
        try:
            total_views = int(output.split(":")[-1].strip())
        except ValueError:
            print(f"Unexpected output from {script_path}: {output}")
            continue

        
        # Store the total views in the results dictionary
        results[variation] = total_views

    # Construct the SQL query
    sql_query = """
    INSERT INTO "Sim Data" (baseline_views, variation_a_views, variation_b_views, baseline_plot, variation_a_plot, variation_b_plot, timestamp)
    VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, DEFAULT);
    """

    sql_query = """
    INSERT INTO "Sim Data" (run_id, baseline_views, variation_a_views, variation_b_views, baseline_plot, variation_a_plot, variation_b_plot, "timestamp")
    VALUES (%s, %s, %s, %s, %s, %s, %s, DEFAULT);
"""

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

    # Insert data into the database
    # Execute the SQL query
    # Execute the SQL query
    cursor.execute(sql_query, (run, results["baseline"], results["variation_a"], results["variation_b"], latest_plots["baseline"], latest_plots["variation_a"], latest_plots["variation_b"]))
    conn.commit()

cursor.close()
conn.close()