import pandas as pd
import matplotlib.pyplot as plt

# Sample Election Data
data = {
    "Constituency": ["A", "A", "B", "B", "C", "C"],
    "Party": ["Party X", "Party Y", "Party X", "Party Z", "Party Y", "Party Z"],
    "Candidate": ["Candidate 1", "Candidate 2", "Candidate 3", "Candidate 4", "Candidate 5", "Candidate 6"],
    "Votes": [12000, 11000, 15000, 14000, 17000, 16000]
}

df = pd.DataFrame(data)

# Calculate total votes for each party
total_votes_by_party = df.groupby("Party")["Votes"].sum()
print("\nTotal Votes per Party:\n", total_votes_by_party)

# Function to determine the winning party in each constituency
def get_winning_party(sub_df):
    return sub_df.loc[sub_df["Votes"].idxmax(), "Party"]

# Determine winning party in each constituency
winning_party_by_constituency = df.groupby("Constituency").apply(get_winning_party)
print("\nWinning Party by Constituency:\n", winning_party_by_constituency)

# Determine overall election winner (party with most total votes)
overall_winner = total_votes_by_party.idxmax()
print("\nOverall Election Winner:", overall_winner)

# Calculate vote share percentage for each candidate
df["Vote Share (%)"] = (df["Votes"] / df["Votes"].sum()) * 100

# Identify close contests (margin < 5%)
df_sorted = df.sort_values(["Constituency", "Votes"], ascending=[True, False])
df_sorted["Rank"] = df_sorted.groupby("Constituency")["Votes"].rank(method="dense", ascending=False)

# Select top two candidates per constituency
top_two = df_sorted[df_sorted["Rank"] <= 2].copy()
top_two["Vote Difference"] = top_two.groupby("Constituency")["Votes"].diff().abs().fillna(0)

# Check if vote difference is less than 5% of the highest votes in that constituency
close_contests = top_two[top_two["Vote Difference"] < 0.05 * top_two.groupby("Constituency")["Votes"].transform("max")]

print("\nClose Contests (Margin < 5%):\n", close_contests[["Constituency", "Candidate", "Party", "Votes", "Vote Difference"]])

# ----------------- Visualization -----------------

# 1. Bar Chart: Winning Votes by Constituency
plt.figure(figsize=(8, 5))
plt.bar(winning_party_by_constituency.index, df.groupby("Constituency")["Votes"].max(), color='skyblue', edgecolor='black')
plt.xlabel("Constituency")
plt.ylabel("Votes")
plt.title("Winning Votes by Constituency")
plt.show()

# 2. Pie Chart: Vote Share by Party (Enhanced)
plt.figure(figsize=(8, 6))
colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"]
plt.pie(total_votes_by_party, labels=total_votes_by_party.index, autopct="%1.1f%%", startangle=140, colors=colors, wedgeprops={'edgecolor': 'black'})
plt.title("Vote Share by Party")
plt.show()