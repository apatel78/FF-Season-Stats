def get_user_points(league, user_id):
    points = 0
    for roster in league.get_rosters():
        if roster['owner_id'] == str(user_id):
            try:
                if not roster['settings']['fpts_decimal']:
                    decimal = 0
            except:
                continue
            else:
                decimal = roster['settings']['fpts_decimal']
            points = float(roster['settings']['fpts']) + (0.01 * float(decimal))
    return points

def get_user_transactions(league, user_id, playerTradesOnly, exludeDST):
    trades = 0
    waivers = 0
    free_agents = 0

    user_roster = 0

    for roster in league.get_rosters():
        if roster['owner_id'] == str(user_id):
            user_roster = roster['roster_id']

    for i in range(1, 18):
        for transaction in league.get_transactions(i):
            exclude = False
            # Trades
            if transaction['status'] == "complete" and transaction['type'] == "trade":
                for roster_id in transaction['roster_ids']:
                    if roster_id == user_roster:
                        if playerTradesOnly:
                            if (transaction["adds"] != None and transaction["drops"] != None):
                                for player in transaction['drops']:
                                    if exludeDST:
                                        if player.isalpha():
                                            exclude = True
                                for player in transaction['adds']:
                                    if exludeDST:
                                        if player.isalpha():
                                            exclude = True
                        if not exclude:
                            trades += 1

            # Waivers
            if transaction['type'] == 'waiver' and transaction['status'] == "complete":
                for roster_id in transaction['roster_ids']:
                    if roster_id == user_roster:
                        if transaction['drops']:
                            for player in transaction['drops']:
                                if exludeDST:
                                    if player.isalpha():
                                        exclude = True
                        if transaction['adds']:
                            for player in transaction['adds']:
                                if exludeDST:
                                    if player.isalpha():
                                        exclude = True
                        if not exclude:
                            waivers += 1

            # Free Agent
            if transaction['type'] == 'free_agent' and transaction['status'] == "complete":
                for roster_id in transaction['roster_ids']:
                    if roster_id == user_roster:
                        if transaction['drops']:
                            for player in transaction['drops']:
                                if exludeDST:
                                    if player.isalpha():
                                        exclude = True
                        if transaction['adds']:
                            for player in transaction['adds']:
                                if exludeDST:
                                    if player.isalpha():
                                        exclude = True
                        if not exclude:
                            free_agents += 1
    return (trades, waivers, free_agents)
