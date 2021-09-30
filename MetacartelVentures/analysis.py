import json
import pandas as pd

# Load data
with open("./MetacartelVentures/data/10884668-results.json", "r") as f:
    results_09182020 = json.load(f)
f.close()

with open("./MetacartelVentures/data/13316507-results.json", "r") as f:
    results_09282021 = json.load(f)
f.close()

if __name__ == "__main__":
    # Metrics to calculate
# Decentralization
# - Minimum winning coalition (minimum % of wallets needed to affect a vote)
# - % of total wallets that published a proposal  (y)
# Number of wallets that published proposal / total number of wallets
# Total number of wallets: 
    df_09182020_members = pd.DataFrame.from_dict(results_09182020["data"]["moloches"][0]["members"])
    
    # Clean up member id by deleting the DAO id that's tagged on.
    df_09182020_members["id"] = df_09182020_members.apply(lambda row: row["id"].split('-')[2], axis=1)

    df_09182020_proposals = pd.DataFrame.from_dict(results_09182020["data"]["moloches"][0]["proposals"])
# - Voter participation rate (y)
    print('hello')
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