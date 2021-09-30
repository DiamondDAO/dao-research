import json
from data.daohaus_members import run_member_query, get_aggregated_member_info
from util.analysis_functions import *

# Load data
with open("./MetacartelVentures/data/10884668-results.json", "r") as f:
    results_09182020 = json.load(f)

with open("./MetacartelVentures/data/13316507-results.json", "r") as f:
    results_09282021 = json.load(f)

if __name__ == "__main__":

    # get member information and clean to create an easily accessible dictionary
    member_query_string = """
    {
      members(
        block: {number: 13316507}
        first: 1000, where: {id_gt: lastID}) {
            id
            createdAt
            molochAddress
            memberAddress
            shares
            loot
            exists
            didRagequit
            kicked
            jailed
        }
    }
    """
    all_member_dict = run_member_query(member_query_string)
    all_member_dict = get_aggregated_member_info(all_member_dict)
    print(all_member_dict)

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

    block_number = "13316507"

    for idx, dao_info in enumerate(results_09282021["data"]["moloches"]):
        dao = dao_info
        dao["aggregated_metrics"] = {}
        dao["aggregated_metrics"]["members"] = get_member_metrics(dao, all_member_dict)
        (
            dao["aggregated_metrics"]["decentralization"],
            dao["aggregated_metrics"]["proposals"],
        ) = get_decentralized_and_proposal_metrics(dao, block_number)

