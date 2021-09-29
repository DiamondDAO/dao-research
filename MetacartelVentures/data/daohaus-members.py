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
    'https://api.thegraph.com/subgraphs/name/odyssy-automaton/daohaus',
    '',
    json={"query": new_str}
    )
    while json.loads(response.text)['data']['members']:
      if response.status_code == 200:
        all_members.extend(json.loads(response.text)['data']['members'])
        print(len(all_members))
      else:
          raise Exception("Query failed. Return code is {}.   {}".format(response.status_code, q))
      new_str = q.replace("lastID", '"' + all_members[-1]['id'] + '"')
      response = requests.post(
      'https://api.thegraph.com/subgraphs/name/odyssy-automaton/daohaus',
      '',
      json={"query": new_str}
      )
      print(json.loads(response.text))
      with open("./MetacartelVentures/data/" + str(len(all_members)) + "-daohaus.json", "w", encoding="utf-8") as f:
          json.dump(json.loads(response.text), f)
      f.close()

# Diamond DAO contract address: 0x4fe53f216b432c8f604e35ccfeaf7534bc728b0d
query = """
{
    members(first: 1000, where: {id_gt: lastID}) {
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
run_member_query(query)