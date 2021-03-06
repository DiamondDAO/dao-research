# clean raw members query data into a dictionary organized by wallet address (id)
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


# generate metrics on members of a specific dao
def get_member_metrics(dao_info, member_dict):

    kicked_member_count = 0
    rage_quit_member_count = 0
    members_in_multiple_daos = 0
    total_dao_count = 0
    current_member_count = 0

    member_metrics_dict = {}

    for member in dao_info["members"]:
        memberAddress = member["id"].split("-")[2]
        if member["kicked"]:
            kicked_member_count += 1
            continue
        if member["didRagequit"]:
            rage_quit_member_count += 1
            continue
        else:
            current_member_count += 1

        current_info = member_dict[memberAddress]
        if len(current_info["aggregated_information"]["current_daos"]) > 1:
            members_in_multiple_daos += 1
        total_dao_count += len(current_info["aggregated_information"]["current_daos"]) - 1

    # metrics (keys) that are being generated
    member_metrics_dict["all_time_member_count"] = len(dao_info["members"])
    member_metrics_dict["current_member_count"] = current_member_count
    member_metrics_dict["members_in_multiple_daos"] = members_in_multiple_daos
    member_metrics_dict["average_daos_per_member"] = total_dao_count / current_member_count
    member_metrics_dict["kicked_member_count"] = kicked_member_count
    member_metrics_dict["rage_quit_member_count"] = rage_quit_member_count

    return member_metrics_dict


# generate metrics on proposals and decentralization for a given dao
def get_decentralized_and_proposal_metrics(dao_info, timestamp):

    reference_timestamp = int(timestamp)
    month_timestamp = reference_timestamp - (60 * 60 * 24 * 30)

    total_proposals = 0
    total_votes = 0
    total_proposals_passed = 0
    total_shares_given = 0
    total_tribute_dict = {}
    total_payment_dict = {}
    member_proposal_dict = {}

    proposal_metrics_dict = {}

    proposer_wallets = set()
    voter_wallets = set()

    decentralization_metrics_dict = {}

    for proposal in dao_info["proposals"]:
        if proposal["cancelled"]:
            continue
        total_proposals += 1
        proposer_wallets.add(proposal["applicant"])
        for vote in proposal["votes"]:
            memberAddress = vote["id"].split("-")[2]
            voter_wallets.add(memberAddress)
        total_votes += int(proposal["yesVotes"]) + int(proposal["noVotes"])
        if proposal["didPass"]:
            total_proposals_passed += 1
        else:
            continue
        total_shares_given += int(proposal["sharesRequested"])
        if proposal["tributeTokenSymbol"]:
            if proposal["tributeTokenSymbol"] not in total_tribute_dict.keys():
                total_tribute_dict[proposal["tributeTokenSymbol"]] = {
                    "decimal": int(proposal["tributeTokenDecimals"]),
                    "token_address": proposal["tributeToken"],
                    "value": float(proposal["tributeOffered"]),
                }
            else:
                total_tribute_dict[proposal["tributeTokenSymbol"]]["value"] = total_tribute_dict[
                    proposal["tributeTokenSymbol"]
                ]["value"] + float(proposal["tributeOffered"])
        if proposal["paymentTokenSymbol"]:
            if proposal["paymentTokenSymbol"] not in total_payment_dict.keys():
                total_tribute_dict[proposal["paymentTokenSymbol"]] = {
                    "decimal": int(proposal["paymentTokenDecimals"]),
                    "token_address": proposal["paymentToken"],
                    "value": float(proposal["paymentRequested"]),
                }
            else:
                total_tribute_dict[proposal["paymentTokenSymbol"]]["value"] = total_tribute_dict[
                    proposal["paymentTokenSymbol"]
                ]["value"] + float(proposal["paymentToken"])

    proposal_metrics_dict["total_proposals"] = total_proposals
    proposal_metrics_dict["total_votes"] = total_votes
    proposal_metrics_dict["total_proposals_passed"] = total_proposals_passed
    proposal_metrics_dict["total_shares_given"] = total_shares_given
    proposal_metrics_dict["total_tribute_information"] = total_tribute_dict
    proposal_metrics_dict["total_payment_information"] = total_payment_dict

    decentralization_metrics_dict["voter_participation_rate"] = (
        len(voter_wallets) * 100 / dao_info["aggregated_metrics"]["members"]["current_member_count"]
    )

    decentralization_metrics_dict["proposal_rate"] = (
        len(proposer_wallets) * 100 / dao_info["aggregated_metrics"]["members"]["current_member_count"]
    )

    return decentralization_metrics_dict, proposal_metrics_dict
