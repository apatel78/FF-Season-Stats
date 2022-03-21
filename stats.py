from sleeper_wrapper import League
import json

with open('info.json') as inputs:
    data = json.load(inputs)


league = League(data['League ID'])

users_dict = {}

for user in league.get_users():
    users_dict[user['user_id']] = user['display_name']

#Have to hard-code since the user gets removed from the team when they get chopped
rosters_dict = {
    11 : "Apatel892",
    3 : "DKLocksCoInc",
    15 : "Smelscifi",
    4 : "Peltron3030",
    7 : "HerbalFFB",
    1 : "christhrowrocks",
    14 : "jnmaniac1",
    2 : "Bootzay",
    13 : "BustyDullard",
    17 : "foolstp",
    10 : "Noro",
    8 : "ikyn",
    5 : "OfficerBrando25",
    12 : "Bakron",
    16 : "Derriphan",
    18 : "tanay002",
    9 : "PartyWolff",
    6 : "Moose17"
}

temp_transaction = []
faab_dict = {}
num_trades_dict = {}

#Player involved in most transactions
player_transactions_dict = {}

cursed_player_dict = {}

'''
for transactoins in league.get_transactions(5):
    print(transactoins)
    print("--------------")
'''

for i in range(1, 18):
    for transaction in league.get_transactions(i):

        #Used for FABB calculations
        if transaction['status'] == "complete" and transaction['type'] == "trade" and transaction['waiver_budget'] != None and (transaction["adds"] != None and transaction["drops"] != None):
            for faab_transaction in transaction['waiver_budget']:
                if faab_transaction['sender'] not in faab_dict:
                    faab_dict[faab_transaction['sender']] = 0
                else:
                    faab_dict[faab_transaction['sender']] = faab_dict[faab_transaction['sender']] + faab_transaction['amount']
                
                if faab_transaction['receiver'] not in faab_dict:
                    faab_dict[faab_transaction['receiver']] = 0
                else:
                    faab_dict[faab_transaction['receiver']] = faab_dict[faab_transaction['receiver']] - faab_transaction['amount']
        
        #Used to determine number of trades
        if transaction['status'] == "complete" and transaction['type'] == "trade" and (transaction["adds"] != None and transaction["drops"] != None):
            for roster_id in transaction['roster_ids']:
                if roster_id not in num_trades_dict:
                    num_trades_dict[roster_id] = 1
                else:
                    num_trades_dict[roster_id] = num_trades_dict[roster_id] + 1

        #Used to determine player involved in most transactions
        if transaction['type'] != "commissioner":
            #If waiver
            if transaction['type'] == 'waiver' and transaction['status'] == "complete":
                if transaction['drops']:
                    for player in transaction['drops']:
                        if not player in player_transactions_dict:
                            player_transactions_dict[player] = 1
                        else:
                            player_transactions_dict[player] = player_transactions_dict[player] + 1
                if transaction['drops']:
                    for player in transaction['adds']:
                        if not player in player_transactions_dict:
                            player_transactions_dict[player] = 1
                        else:
                            player_transactions_dict[player] = player_transactions_dict[player] + 1
            #If Free Agent
            if transaction['type'] == 'free_agent' and transaction['status'] == "complete":
                if transaction['drops']:
                    for player in transaction['drops']:
                        if not player in player_transactions_dict:
                            player_transactions_dict[player] = 1
                        else:
                            player_transactions_dict[player] = player_transactions_dict[player] + 1
                if transaction['adds']:
                    for player in transaction['adds']:
                        if not player in player_transactions_dict:
                            player_transactions_dict[player] = 1
                        else:
                            player_transactions_dict[player] = player_transactions_dict[player] + 1
            #If trade
            if transaction['type'] == 'trade' and transaction['status'] == "complete":
                temp_player_list = []
                if transaction['drops']:
                    for player in transaction['drops']:
                        if not player in temp_player_list:
                            temp_player_list.append(player)
                if transaction['adds']:
                    for player in transaction['adds']:
                        if not player in temp_player_list:
                            temp_player_list.append(player)
                if temp_player_list:
                    for player in temp_player_list:
                        if not player in player_transactions_dict:
                            player_transactions_dict[player] = 1
                        else:
                            player_transactions_dict[player] = player_transactions_dict[player] + 1
        
        #Used to determine the most cursed player
        if transaction['type'] == "commissioner":
            if transaction['drops']:
                for player in transaction['drops']:
                    if not player in cursed_player_dict:
                        cursed_player_dict[player] = 1
                    else:
                        cursed_player_dict[player] = cursed_player_dict[player] + 1


#Fix Faab_dict structure
faab_whore = {}
for user1 in rosters_dict:
    for user2 in faab_dict:
        if user1 == user2:
            faab_whore[rosters_dict[user1]] = faab_dict[user2]
        else:
            continue

faab_whore = dict(sorted(faab_whore.items(), key=lambda item: item[1]))
# print(faab_whore)

num_trades = {}
for user1 in rosters_dict:
    for user2 in num_trades_dict:
        if user1 == user2:
            num_trades[rosters_dict[user1]] = num_trades_dict[user2]
        else:
            continue

num_trades = dict(sorted(num_trades.items(), key=lambda item: item[1]))
# print(num_trades)

# most_transaction_player = {}
max_key = max(player_transactions_dict, key=player_transactions_dict.get)
# most_transaction_player = dict(sorted(player_transactions_dict.items(), key=lambda item: item[1],reverse=True))
print(max_key)
# print(most_transaction_player)
# print(len(most_transaction_player))


# most_cursed_player = {}
# most_cursed_player = dict(sorted(cursed_player_dict.items(), key=lambda item: item[1],reverse=True))
cursed_player = max(cursed_player_dict, key=cursed_player_dict.get)
print(cursed_player)
# print(most_cursed_player)

'''
Statistics to track:
Player involved in most transactions (Adding the player counts, Dropping the player counts, trading the player counts,
    Cutting the player (commish) does NOT count)
-Track number of transactions for every player

Most Cursed player (player that was on the most rosters that got chopped)
-Find which user got cut every week, find similarity in players

'''

'''
Most FAAB gained: Derriphan (814)

Most FAAB traded away: 

Most Trades: Moose (15)

Least Trades: Herbal/Brando (1)

Alexander Mattison was involved in the most transactions (10)
Amari Cooper was the most cursed player (5)
309 unique players rostered at some point

--------------
{'waiver_budget': [], 'type': 'free_agent', 'transaction_id': '751736532364312576', 'status_updated': 1633590465206, 'status': 'complete', 'settings': None, 'roster_ids': [12], 'metadata': None, 'leg': 5, 'drops': None, 'draft_picks': [], 'creator': '376640431687127040', 'created': 1633590465206, 'consenter_ids': [12], 'adds': {'4531': 12}}
--------------

--------------
{'waiver_budget': [{'sender': 15, 'receiver': 3, 'amount': 250}], 'type': 'trade', 'transaction_id': '751922492389613568', 'status_updated': 1633634816265, 'status': 'complete', 'settings': None, 'roster_ids': [15, 3], 'metadata': None, 'leg': 5, 'drops': {'6955': 3, '6789': 15}, 'draft_picks': [], 'creator': '431201599533088768', 'created': 1633634801531, 'consenter_ids': [15, 3], 'adds': {'6955': 15, '6789': 3}}
--------------

--------------
{'waiver_budget': [], 'type': 'waiver', 'transaction_id': '754264272544120832', 'status_updated': 1634195166452, 'status': 'complete', 'settings': {'waiver_bid': 46, 'seq': 32}, 'roster_ids': [1], 'metadata': {'notes': 'Your waiver claim was processed successfully!'}, 'leg': 5, 'drops': {'4040': 1}, 'draft_picks': [], 'creator': '202517573990879232', 'created': 1634193125428, 'consenter_ids': [1], 'adds': {'7526': 1}}
--------------


--------------------
{'waiver_budget': [], 'type': 'commissioner', 'transaction_id': '776693604260413440', 'status_updated': 1639540694826, 'status': 'complete', 'settings': None, 'roster_ids': [10], 'metadata': None, 'leg': 14, 'drops': {'6819': 10}, 'draft_picks': [], 'creator': '202517573990879232', 'created': 1639540694826, 'consenter_ids': None, 'adds': None}
--------------------
'''