# FF Season Stats

FF Season Stats is a Python script for visually representing how active users were in their fantasy football league on Sleeper.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required dependencies for this script.

```bash
pip install -r requirements.txt
```

## Usage

In order to use the script, please update the Config.json file with the appropriate data to reflect the mode. Then, run 
```commandline
python main.py
```

### League Mode (requires Mode, League ID, playerTradesOnly, excludeDST):
The primary purpose of this mode is to determine the activity of every user within a certain league. 
* Mode should be set to league
* League ID can be found on desktop in the URL while viewing a league on Sleeper
* playerTradesOnly should be true if all trades counted should include at least one player
* excludeDST should be true if all transactions should exclude DST

This mode will output 3 bar graphs: a graph showing the total points scored, a graph showing user total transactions, and a graph showing player total transactions.

### User Mode (requires Mode, User ID, Year, playerTradesOnly, excludeDST):
The primary purpose of this mode is to determine the activity of one user in every league. 
* Mode should be set to user
* User ID can be found using the ID Mode
* Year should be the year for the fantasy season
* playerTradesOnly should be true if all trades counted should include at least one player
* excludeDST should be true if all transactions should exclude DST

This mode will output 2 bar graphs: a graph showing the user's total points scored in every league and a graph showing the user's total transactions in every league.

### ID Mode (requires Mode, League ID, Username):
The primary purpose of this mode is to find a user id
* Mode should be set to id
* League ID can be any league the user is in
* Username can be found on the bottom left of the Sleeper website

This mode will output the userID in the terminal.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)