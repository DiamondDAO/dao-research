import json
import requests
from datetime import datetime, timezone
import time
from pprint import pprint

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


def get_aggregated_member_info(member_dict):
    cleaned_member_dict = {}
    for memberAddress in member_dict.keys():
        currentDaos = []
        kickedFromDaos = []
        rageQuitFromDaos = []
        for entry in member_dict[memberAddress]["dao_information"]:
            if entry["kicked"]:
                kickedFromDaos.append(entry["molochAddress"])
            if entry["didRagequit"]:
                rageQuitFromDaos.append(entry["molochAddress"])
            if not entry["kicked"] and not entry["didRagequit"]:
                currentDaos.append(entry["molochAddress"])
        aggregated_information_dict = {}
        aggregated_information_dict["current_daos"] = currentDaos
        aggregated_information_dict["kicked_from"] = kickedFromDaos
        aggregated_information_dict["rage_quit_from"] = rageQuitFromDaos
        cleaned_member_dict[memberAddress] = member_dict[memberAddress]
        cleaned_member_dict[memberAddress]["aggregated_information"] = aggregated_information_dict

    return cleaned_member_dict


if __name__ == "__main__":
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
    print(cleaned_member_dict)
