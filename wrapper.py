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
    "baseline": "path_to_baseline_script.py",
    "variation_a": "path_to_variation_a_script.py",
    "variation_b": "path_to_variation_b_script.py"
}

# Number of runs
num_runs = 1000

for run in range(num_runs):
    # Dictionary to store results for this run
    results = {}

    for variation, script_path in scripts.items():
        # Execute the script and capture the output
        output = os.popen(f"python {script_path}").read()
        
        # Extract the total views from the output
        total_views = int(output.split(":")[-1].strip())
        
        # Store the total views in the results dictionary
        results[variation] = total_views

    # Construct the SQL query
    sql_query = """
    INSERT INTO "Sim Data" (ID, baseline_views, variation_a_views, variation_b_views, baseline_plot, variation_a_plot, variation_b_plot)
    VALUES (DEFAULT, %s, %s, %s, %s, %s, %s);
    """

    # Define paths to the saved plots
    plot_paths = {
        "baseline": "path_to_baseline_plot_directory",
        "variation_a": "path_to_variation_a_plot_directory",
        "variation_b": "path_to_variation_b_plot_directory"
    }

    # Fetch the latest saved plots for each variation
    latest_plots = {}
    for variation, plot_dir in plot_paths.items():
        latest_plot = max(os.listdir(plot_dir), key=lambda x: os.path.getctime(os.path.join(plot_dir, x)))
        latest_plots[variation] = os.path.join(plot_dir, latest_plot)

    # Insert data into the database
    cursor.execute(sql_query, (results["baseline"], results["variation_a"], results["variation_b"], latest_plots["baseline"], latest_plots["variation_a"], latest_plots["variation_b"]))
    conn.commit()

cursor.close()
conn.close()