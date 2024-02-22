import psycopg2
from getpass import getpass
from psycopg2 import extras

def connect_to_db():
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
    return conn

def fetch_data(conn):
    cursor = conn.cursor()
    sql_query = "SELECT * FROM \"Sim Data\";"
    cursor.execute(sql_query)
    data = cursor.fetchall()
    cursor.close()
    return data

def calculate_total_views(data):
    # Assuming the total views are the sum of daily views for each variation
    baseline_total = sum(sum(row[1:8]) for row in data)
    variation_a_total = sum(sum(row[8:15]) for row in data)
    variation_b_total = sum(sum(row[15:22]) for row in data)
    return baseline_total, variation_a_total, variation_b_total

def calculate_daily_views(data):
    # Extract daily views for each variation
    baseline_daily = [sum([row[i] for row in data]) for i in range(1, 8)]
    variation_a_daily = [sum([row[i] for row in data]) for i in range(8, 15)]
    variation_b_daily = [sum([row[i] for row in data]) for i in range(15, 22)]
    return baseline_daily, variation_a_daily, variation_b_daily

def calculate_peak_views(data):
    baseline_daily, variation_a_daily, variation_b_daily = calculate_daily_views(data)
    return max(baseline_daily), max(variation_a_daily), max(variation_b_daily)

def calculate_average_views(data):
    baseline_daily, variation_a_daily, variation_b_daily = calculate_daily_views(data)
    return sum(baseline_daily)/7, sum(variation_a_daily)/7, sum(variation_b_daily)/7

def transform_data(data):
    transformed_data = []
    
    for row in data:
        run_id = row[0]  # Assuming the first column is the Run ID
        timestamp = row[-1]  # Assuming the last column is the Timestamp
        
        # Splitting the data into variations
        for variation_index, variation_name in enumerate(["Baseline", "Variation A", "Variation B"]):
            start_index = 1 + (7 * variation_index)
            end_index = start_index + 7
            
            variation_data = row[start_index:end_index]
            
            cumulative_views = 0
            peak_views = 0
            
            for day, views in enumerate(variation_data, start=1):
                cumulative_views += views
                peak_views = max(peak_views, views)
                average_views = cumulative_views / day
                
                transformed_data.append({
                    "run_id": run_id,
                    "Variation": variation_name,
                    "Day": day,
                    "Views": views,
                    "Cumulative_Views": cumulative_views,
                    "Peak_Views": peak_views,
                    "Average_Views": average_views,
                    "Timestamp": timestamp
                })
    
    return transformed_data

def insert_data_to_db(conn, transformed_data, table_name):
    """
    Insert the transformed data into the specified table in the PostgreSQL database.
    """
    cursor = conn.cursor()

    # Define the SQL query for inserting data
    insert_query = f"""
    INSERT INTO \"{table_name}\" ("run_id", "Variation", "Day", "Views", "Cumulative_Views", "Peak_Views", "Average_Views", "Timestamp")
    VALUES %s
    """
    
    # Insert each row of transformed data into the table
    values = [
            (
                row["run_id"],
                row["Variation"],
                row["Day"],
                row["Views"],
                row["Cumulative_Views"],
                row["Peak_Views"],
                row["Average_Views"],
                row["Timestamp"]
            )
            for row in transformed_data
        ]
    # Use the psycopg2 'extras' module for batch insertion
    extras.execute_values(cursor, insert_query, values)

    # Commit the changes to the database
    conn.commit()
    cursor.close()

if __name__ == "__main__":
    conn = connect_to_db()
    data = fetch_data(conn)

    structured_data = transform_data(data)
    
    # Insert the structured data into the desired table in the PostgreSQL database
    table_name = "Feature Variation Impact Analysis"
    insert_data_to_db(conn, structured_data, table_name)
    
    conn.close()
    print("Data insertion complete!")