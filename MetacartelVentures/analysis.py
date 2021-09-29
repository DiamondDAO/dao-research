import json

# Load data
with open("./data/10884668-results.json", "r") as f:
    results_09182020 = json.load(f)
f.close()

with open("./data/13316507-results.json", "r") as f:
    results_09282021 = json.load(f)
f.close()

if __name__ == "__main__":
    # Metrics to calculate
# Decentralization
# - Minimum winning coalition (minimum % of wallets needed to affect a vote)
# - % of total wallets that published a proposal  (y)
# - Voter participation rate (y)
# - MoM change

# Proposals
# - # of proposals this month
#     - Pass
#     - Fail
# - Value distributed through proposals (tribute, loot, shares | priority tribute)
# - Value received through proposals
# - MoM change

# Contributors
# - # of wallets that put in money
#     - Average amount put in
# - # of wallets that received money
#     - Average amount taken
# - MoM change
# - Voting coalitions
#     - Choose like top 3 
#     - Define however
# - Connected members
#     - Choose like top3
#     - Define however

# Members
# - Number of members
# - Number of active members
# - Members that belong to other DAOhaus DAOs
# - Average DAOs per member 

    pass