from sleeper_wrapper import Players

def get_points_scored(league, user_dict):
    for roster in league.get_rosters():
        try:
            if not roster['settings']['fpts_decimal']:
                decimal = 0
        except:
            continue
        else:
            decimal = roster['settings']['fpts_decimal']
        points = float(roster['settings']['fpts']) + (0.01 * float(decimal))
        user_dict[roster['owner_id']].append(points)
    return user_dict

def get_init_transactions_dict(users_dict):
    transactions_dict = {}
    for user in users_dict:
        if len(users_dict[user]) > 1:
            transactions_dict[users_dict[user][1]] = [users_dict[user][0], 0, 0, 0]
    return transactions_dict

def get_user_and_player_transactions(league, transactions_dict, playerTradesOnly, exludeDST):
    player_transactions_dict = {}
    for i in range(1, 18):
        for transaction in league.get_transactions(i):
            # Trades
            if transaction['status'] == "complete" and transaction['type'] == "trade":
                if playerTradesOnly:
                    if (transaction["adds"] != None and transaction["drops"] != None):
                        player_transactions_dict, empty = update_player_count(transaction, player_transactions_dict, exludeDST)
                        if not empty:
                            for roster_id in transaction['roster_ids']:
                                transactions_dict[roster_id][1] += 1
                else:
                    player_transactions_dict, empty = update_player_count(transaction, player_transactions_dict, exludeDST)
                    if not empty:
                        for roster_id in transaction['roster_ids']:
                            transactions_dict[roster_id][1] += 1

            # Waivers
            if transaction['type'] == 'waiver' and transaction['status'] == "complete":
                player_transactions_dict, empty = update_player_count(transaction, player_transactions_dict, exludeDST)
                if not empty:
                    for roster_id in transaction['roster_ids']:
                        transactions_dict[roster_id][2] += 1

            # Free Agent
            if transaction['type'] == 'free_agent' and transaction['status'] == "complete":
                player_transactions_dict, empty = update_player_count(transaction, player_transactions_dict, exludeDST)
                if not empty:
                    for roster_id in transaction['roster_ids']:
                        transactions_dict[roster_id][3] += 1

    return (transactions_dict, player_transactions_dict)

def format_player_dict(player_dict, num_people_in_league, excludeDST):
    #Sort by num transactions
    players = list(sorted(player_dict.items(), key=lambda item: item[1], reverse=True))
    #Remove the un_needed players
    iterator = 0
    player_strings = []
    found_enough = True
    while found_enough:
        player, num = players[iterator]
        if not player.isalpha():
            player_strings.append(players[iterator])
        iterator += 1
        if len(player_strings) == num_people_in_league:
            found_enough = False

    return player_strings

def get_userDict(league):
    users_dict = {}
    for user in league.get_users():
        users_dict[user['user_id']] = [user['display_name']]

    for roster in league.get_rosters():
        users_dict[roster['owner_id']].append(roster['roster_id'])

    return users_dict

def update_player_count(transaction, player_transactions_dict, exludeDST):
    player_list = []
    if transaction['drops']:
        for player in transaction['drops']:
            if exludeDST:
                if not player.isalpha():
                    player_list.append(player)
            else:
                player_list.append(player)
    if transaction['adds']:
        for player in transaction['adds']:
            if exludeDST:
                if not player.isalpha():
                    player_list.append(player)
            else:
                player_list.append(player)
    player_list = list(set(player_list))
    for player in player_list:
        if not player in player_transactions_dict:
            player_transactions_dict[player] = 1
        else:
            player_transactions_dict[player] = player_transactions_dict[player] + 1

    empty = False
    if len(player_list) == 0:
        empty = True

    return (player_transactions_dict, empty)

def format_player_names(players_strings):
    player_names = {}
    players = Players()
    all_players = players.get_all_players()
    for player, value in players_strings:
        player_names[all_players[player]['full_name']] = value

    return player_names
