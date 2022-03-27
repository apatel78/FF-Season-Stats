from sleeper_wrapper import League
from sleeper_wrapper import User
import json
from utils.plot import *
from utils.user import *
from utils.league import *

#TODO
#README
def main():
    with open('config.json') as inputs:
        data = json.load(inputs)
    if data['Mode'] == "league":
        print("Running league mode")
        league_driver(League(data['League ID']), data['playerTradesOnly'], data['excludeDST'])
    elif data['Mode'] == "user":
        print("Running user mode")
        user_driver(data['User ID'], data['Year'], data['playerTradesOnly'], data['excludeDST'])
    elif data['Mode'] == "id":
        id_driver(League(data['League ID']), data['Username'])
    else:
        print("Incorrect usage for mode, please only use 'league' or 'user' or 'id'")
        exit(0)

def league_driver(league, playerTradesOnly, exludeDST):
    #Get Point Stats
    league_points_dict = get_points_scored(league, get_userDict(league))

    #Get Transaction Stats
    transactions_dict = get_init_transactions_dict(get_userDict(league))
    transactions_dict, player_dict = get_user_and_player_transactions(league, transactions_dict, playerTradesOnly, exludeDST)

    #Prepare the players to display
    players_strings = format_player_dict(player_dict, league.get_league()['total_rosters'], exludeDST)
    players_names = format_player_names(players_strings)

    #Prepare all three dicts for plotting and call plotting function
    league_points_x = []
    league_points_y = []
    for user in league_points_dict:
        if len(league_points_dict[user]) > 1:
            league_points_x.append(league_points_dict[user][0])
            league_points_y.append(league_points_dict[user][2])

    plot_single_bar(league_points_x, league_points_y, league.get_league()['name'] + "_points.jpg",
                "Points Scored", "Points scored in " + league.get_league()['name'], league.get_league()['name'])

    user_transactions_x = ['Waiver Moves', 'Free Agent Moves', 'Trades']
    user_transactions_y = {}
    for user in transactions_dict:
        user_transactions_y[transactions_dict[user][0]] = [transactions_dict[user][2], transactions_dict[user][3], transactions_dict[user][1]]

    plot_triple_bar(user_transactions_x, user_transactions_y, league.get_league()['name'] + "_transactions.jpg", league.get_league()['name'])

    player_transactions_x = []
    player_transactions_y = []
    for player in players_names:
        player_transactions_x.append(player)
        player_transactions_y.append(players_names[player])

    plot_single_bar(player_transactions_x, player_transactions_y, league.get_league()['name'] + "_players.jpg",
                "Number of Transactions", "Players involved in the most transactions in " + league.get_league()['name'], league.get_league()['name'])

def user_driver(user_id, year, playerTradesOnly, exludeDST):
    user = User(user_id)
    stats_dict = {}
    for league in user.get_all_leagues('nfl', year):
        league_name = league['name']
        league_struct = League(league['league_id'])
        num_points = get_user_points(league_struct, user_id)
        trades, waivers, free_agents = get_user_transactions(league_struct, user_id, playerTradesOnly, exludeDST)
        stats_dict[league_name] = [num_points, trades, waivers, free_agents]

    #Prepare for plotting and call plotting function
    #Find Username
    username = user.get_username()

    points_x = []
    points_y = []
    for league in stats_dict:
        points_x.append(league)
        points_y.append(stats_dict[league][0])

    plot_single_bar(points_x, points_y, username + "_points.jpg", "Points Scored", "Points scored by " + username, username)

    user_transactions_x = ['Waiver Moves', 'Free Agent Moves', 'Trades']
    user_transactions_y = {}
    for user in stats_dict:
        user_transactions_y[user] = [stats_dict[user][2], stats_dict[user][3], stats_dict[user][1]]

    plot_triple_bar(user_transactions_x, user_transactions_y, username + "_transactions.jpg", username)


def id_driver(league, username):
    for user in league.get_users():
        if user['display_name'] == username:
            print("Your Sleeper UserID is: " + user['user_id'])
            exit(0)
    print("No Sleeper UserID was found for: " + username)
    exit(0)

if __name__ == "__main__":
    main()