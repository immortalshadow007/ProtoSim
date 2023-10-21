import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Set the style of seaborn for better visualization
sns.set_style("whitegrid")
sns.set_palette("pastel")

# Define the directory name
dir_name = "baseline_plot"

# Check if directory exists, if not, create it
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

# P1. Initial Conditions
initial_connection_distribution = stats.norm.rvs(loc=500, scale=100, size=1000)
first_degree_distribution = stats.norm.rvs(loc=300, scale=50, size=1000)
second_degree_distribution = stats.norm.rvs(loc=200, scale=40, size=1000)
third_degree_distribution = stats.norm.rvs(loc=100, scale=20, size=1000)
initial_view_percentage = 0.05

# P2. Agent Behavior
def view_probability(user_connections, influence_factor=0.1):
    return min(1, influence_factor * user_connections / 1000)

# P3. Time Dynamics
simulation_duration = 7
check_frequency = 3

# P4. External Factors
external_influence_factor = 0.05

# P5. Constraints
max_daily_views = 10000

# Simulation
daily_views = []
for day in range(simulation_duration):
    daily_view_count = 0
    for check in range(check_frequency):
        for user in range(len(initial_connection_distribution)):
            if np.random.rand() < view_probability(initial_connection_distribution[user]):
                daily_view_count += 1
        daily_view_count = min(daily_view_count, max_daily_views)
    daily_view_count += int(daily_view_count * external_influence_factor)
    daily_views.append(daily_view_count)

# Visualization using seaborn and matplotlib
plt.figure(figsize=(10, 6))
sns.lineplot(x=range(simulation_duration), y=daily_views, marker='o', linewidth=2.5)
plt.title('Daily Views Over Time', fontsize=16)
plt.xlabel('Day', fontsize=14)
plt.ylabel('Number of Views', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
plot_filename = os.path.join(dir_name, f"plot_{current_time}.png")
plt.savefig(plot_filename)

print(f"Total views after {simulation_duration} days: {sum(daily_views)}")