import json
import argparse
from datetime import datetime, timezone
import pathlib
import os
from util.queries.etherscan import *
from util.queries.daohaus import *
from util.analysis_functions import *


# generate path variable for arguments
def expand_path(string):
    if string:
        return pathlib.Path(os.path.expandvars(string))
    else:
        return None


# convert string input to a bool value
def str2bool(v):
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


if __name__ == "__main__":

    # get all arguments required for data and parsing
    dt = datetime.now()
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()

    parser = argparse.ArgumentParser()
    parser.add_argument("--block", type=str, help="block number for which to query data at")
    parser.add_argument("--timestamp", type=str, default=timestamp, help="timestamp for which to query data at")
    parser.add_argument(
        "--moloch_query_path",
        type=expand_path,
        default=expand_path("data/query_templates/metacartel-query.txt"),
        help="path to file containing moloch query template",
    )
    parser.add_argument(
        "--member_query_path",
        type=expand_path,
        default=expand_path("data/query_templates/member-query.txt"),
        help="path to file containing member query template",
    )
    parser.add_argument("--single_entry", type=str2bool, default=True, help="whether the query is for a single moloch")
    parser.add_argument(
        "--data_output_path", type=expand_path, default=None, help="path to file for storing data output",
    )
    args = parser.parse_args()

    if args.block:
        block = args.block
        timestamp = get_timestamp_from_block(block)
    else:
        timestamp = args.timestamp
        block = get_block_from_timestamp(timestamp)

    if not args.data_output_path:
        file_string_name = f"{block}-results.json"
        data_output_path = pathlib.Path("data") / file_string_name
    else:
        data_output_path = args.data_output_path

    # sanity check
    print({"block": block, "timestamp": timestamp, "output_path": data_output_path, "single_entry": args.single_entry})

    # load moloch query template and insert correct block number
    with open(args.moloch_query_path, "r") as file:
        moloch_template_list = file.readlines()

    moloch_query_string = "".join(moloch_template_list)
    moloch_query_string = moloch_query_string.replace("number: ", f"number: {block}")

    # run moloch query
    all_moloch_dict = run_moloch_query(moloch_query_string, single_entry=args.single_entry)

    # Load member query template and insert correct block number
    with open(args.member_query_path, "r") as file:
        member_template_list = file.readlines()

    member_query_string = "".join(member_template_list)
    member_query_string = member_query_string.replace("number: ", f"number: {block}")

    # generate member dictionary and create aggregated member info entry
    all_member_dict = run_member_query(member_query_string)
    all_member_dict = get_aggregated_member_info(all_member_dict)

    # loop through daos, generate relevant metrics, and create new entries to append to list
    final_moloch_info = []
    for idx, dao_info in enumerate(all_moloch_dict["data"]["moloches"]):
        dao = dao_info
        dao["aggregated_metrics"] = {}
        dao["aggregated_metrics"]["members"] = get_member_metrics(dao, all_member_dict)
        (
            dao["aggregated_metrics"]["decentralization"],
            dao["aggregated_metrics"]["proposals"],
        ) = get_decentralized_and_proposal_metrics(dao, timestamp)
        final_moloch_info.append(dao)

    final_dict = {"data": {"moloches": final_moloch_info, "block": block, "timestamp": timestamp}}
    with open(data_output_path, "w") as file:
        json.dump(final_dict, file)

