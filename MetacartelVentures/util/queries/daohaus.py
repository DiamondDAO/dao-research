import json
import requests
from datetime import datetime, timezone
import time
from pprint import pprint
import sys

# TO DO: Need to add endpoint as argument. Right now data is only mainnet DAO members.
def run_member_query(q):

    # The Graph DAOhaus Mainnet endpoint
    # https://api.thegraph.com/subgraphs/name/odyssy-automaton/daohaus
    # The Graph DAOhaus xDAI endpoint
    # https://api.thegraph.com/subgraphs/name/odyssy-automaton/daohaus-xdai

    all_members = []
    new_str = q.replace("lastID", '""')
    response = requests.post(
        "https://api.thegraph.com/subgraphs/name/odyssy-automaton/daohaus", "", json={"query": new_str}
    )
    while json.loads(response.text)["data"]["members"]:
        if response.status_code == 200:
            all_members.extend(json.loads(response.text)["data"]["members"])
        else:
            raise Exception("Query failed. Return code is {}.   {}".format(response.status_code, q))
        new_str = q.replace("lastID", '"' + all_members[-1]["id"] + '"')
        response = requests.post(
            "https://api.thegraph.com/subgraphs/name/odyssy-automaton/daohaus", "", json={"query": new_str}
        )
    print(f"Total Member Entries: {len(all_members)}")

    # Get unique members by creating a member dictionary
    member_dict = {}
    for entry in all_members:
        copy_entry = entry
        memberAddress = copy_entry.pop("memberAddress")

        if memberAddress not in member_dict.keys():
            member_dict[memberAddress] = {}
            member_dict[memberAddress]["dao_information"] = [copy_entry]
        else:
            member_dict[memberAddress]["dao_information"] = member_dict[memberAddress]["dao_information"] + [copy_entry]
    print(f"Unique Members: {len(member_dict)}")

    return member_dict

    # TO DO: Need to add endpoint as argument. Right now data is only mainnet DAO members.


def run_moloch_query(q, single_entry=True):

    # The Graph DAOhaus Mainnet endpoint
    # https://api.thegraph.com/subgraphs/name/odyssy-automaton/daohaus
    # The Graph DAOhaus xDAI endpoint
    # https://api.thegraph.com/subgraphs/name/odyssy-automaton/daohaus-xdai

    all_moloches = []
    if single_entry:
        new_str = q
    else:
        new_str = q.replace("lastID", '""')

    response = requests.post(
        "https://api.thegraph.com/subgraphs/name/odyssy-automaton/daohaus", "", json={"query": new_str}
    )
    while json.loads(response.text)["data"]["moloches"]:
        if response.status_code == 200:
            all_moloches.extend(json.loads(response.text)["data"]["moloches"])
        else:
            raise Exception("Query failed. Return code is {}.   {}".format(response.status_code, q))
        if single_entry:
            break
        new_str = q.replace("lastID", '"' + all_moloches[-1]["id"] + '"')
        response = requests.post(
            "https://api.thegraph.com/subgraphs/name/odyssy-automaton/daohaus", "", json={"query": new_str}
        )

    print(f"Total Moloches Returned: {len(all_moloches)}")
    final_dict = {}
    final_dict["data"] = {"moloches": all_moloches}
    return final_dict


if __name__ == "__main__":

    sys.path.append("../")
    from util.analysis_functions import get_aggregated_member_info

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
    cleaned_member_dict = get_aggregated_member_info(all_member_dict)

    with open("13316507-query.txt", "r") as file:
        all_lines = file.readlines()

    moloch_query_string = "".join(all_lines)
    moloch_result = run_moloch_query(moloch_query_string, single_entry=True)

    with open("13316507-results.json", "w") as file:
        json.dump(moloch_result, file)

    with open("10884668-query.txt", "r") as file:
        all_lines = file.readlines()

    moloch_query_string = "".join(all_lines)
    moloch_result = run_moloch_query(moloch_query_string, single_entry=True)

    with open("10884668-results.json", "w") as file:
        json.dump(moloch_result, file)
