import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style of seaborn for better visualization
sns.set_style("whitegrid")
sns.set_palette("pastel")

# P1. Initial Conditions
initial_connection_distribution = stats.norm.rvs(loc=500, scale=100, size=1000)
first_degree_distribution = stats.norm.rvs(loc=300, scale=50, size=1000)
second_degree_distribution = stats.norm.rvs(loc=200, scale=40, size=1000)
third_degree_distribution = stats.norm.rvs(loc=100, scale=20, size=1000)
initial_view_percentage = 0.05

# Subscription tiers and associated ad counts
subscriptions = ["Free", "Premium Career", "Premium Business", "Sales Navigator", "Recruiter Lite", "Learning"]
ad_counts = [3, 1, 1, 0, 0, 2]
user_subscriptions = np.random.choice(subscriptions, size=1000, p=[0.6, 0.1, 0.1, 0.05, 0.05, 0.1])  # Example distribution

# P2. Agent Behavior
def view_probability(user_connections, user_subscription, influence_factor=0.19):
    ad_factor = 1 - 0.01 * ad_counts[subscriptions.index(user_subscription)]  # 1% reduction per ad
    return min(1, influence_factor * user_connections / 1000 * ad_factor)

# P3. Time Dynamics and other parameters remain the same
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
plt.title('Views by Subscription Tier Over Time', fontsize=16)
plt.xlabel('Subscription Tier', fontsize=14)
plt.ylabel('Number of Views', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()

print(f"Total views after {simulation_duration} days: {sum(views_by_subscription.values())}")