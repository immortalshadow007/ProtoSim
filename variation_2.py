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
dir_name = "variation_b_plot"

# Check if directory exists, if not, create it
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

# P1. Initial Conditions for 10,000 users
# Generate random numbers for initial connections, first, second, and third-degree distributions
initial_connection_distribution = stats.norm.rvs(loc=500, scale=100, size=10000)
first_degree_distribution = stats.norm.rvs(loc=300, scale=50, size=10000)
second_degree_distribution = stats.norm.rvs(loc=200, scale=40, size=10000)
third_degree_distribution = stats.norm.rvs(loc=100, scale=20, size=10000)
initial_view_percentage = 0.05

# Define subscription tiers and associated ad counts
subscriptions = ["Free", "Premium Career", "Premium Business", "Sales Navigator", "Recruiter Lite", "Learning"]
ad_counts = [5, 2, 2, 0, 0, 3]  # Increased ad impact
# Assign a subscription tier to each user based on the provided probabilities
user_subscriptions = np.random.choice(subscriptions, size=10000, p=[0.4, 0.2, 0.2, 0.05, 0.05, 0.1])  # Modified distribution

# P2. Agent Behavior with tweaked influence factor
def view_probability(user_connections, user_subscription, influence_factor=0.18):
    # Calculate the reduction in view probability due to ads
    ad_factor = 1 - 0.02 * ad_counts[subscriptions.index(user_subscription)]  # 2% reduction per ad for increased impact
    return min(1, influence_factor * user_connections / 1000 * ad_factor)

# P3. Time Dynamics remain the same
simulation_duration = 7  # in days
check_frequency = 3  # times per day

# Simulation
views_by_subscription = {sub: 0 for sub in subscriptions}
for day in range(simulation_duration):
    for check in range(check_frequency):
        for user in range(len(initial_connection_distribution)):
            if np.random.rand() < view_probability(initial_connection_distribution[user], user_subscriptions[user]):
                views_by_subscription[user_subscriptions[user]] += 1

# Visualization using seaborn and matplotlib
plt.figure(figsize=(12, 7))
sns.barplot(x=list(views_by_subscription.keys()), y=list(views_by_subscription.values()), palette="viridis")
plt.title('Views by Subscription Tier Over Time (Variation C)', fontsize=16)
plt.xlabel('Subscription Tier', fontsize=14)
plt.ylabel('Number of Views', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
plot_filename = os.path.join(dir_name, f"variation_b_plot_{current_time}.png")
plt.savefig(plot_filename)

print(f"Total views after {simulation_duration} days: {sum(views_by_subscription.values())}")