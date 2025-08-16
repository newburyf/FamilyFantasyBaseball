import statsapi
# Links
# Stats API Python wrapper
# https://github.com/toddrob99/MLB-StatsAPI/wiki
# Official MLB Stats API Docs
# https://github.com/MajorLeagueBaseball/google-cloud-mlb-hackathon/tree/main/datasets/mlb-statsapi-docs

# Getting box score data:
# 1. Call schedule on the team id for the current date to check if team played, if they did take note of the 'game_id'
# 2. Call boxscore_data with the 'game_id'
# 3. Access the all player data in the 'homeBatters', 'awayBatters', 'homePitchers', and 'awayPitchers' categories
# 4. Access individual player data by searching by 'personId' and the MLB personId number OR by 'name' and player last name (and sometimes initial it seems)
#    Seems like I should really use the personID field for player lookups, may need to manually find this for every player though

# td = statsapi.get('teams',{'sportIds':1, 'fields':'teams,name,id'})
# # print(td)
# for t in td['teams']:
#     print("Name: " + t['name'] + " ID: " + str(t['id']))


# gameID = statsapi.schedule(team=119, date='10/25/2024')[0]['game_id']
# gameID = statsapi.schedule(team=119, date='2024-10-25')[0]['game_id']
# boxscoreData = statsapi.boxscore_data(gameID)

# for p in boxscoreData['homeBatters']:
#     if p['name'] == "Freeman, F":
#         print(p)

# players = statsapi.lookup_player('freeman,', season=2025)
# for p in players:
#     print(f"{p['fullName'], p['id']}")

# print(statsapi.boxscore(776747, True, True, True, True, True))
# with open("test.txt", "w") as f:
#     f.write(str(statsapi.boxscore_data(776747)))
# data = statsapi.boxscore_data(776747)
# print(data['homeBatters'])
# for p in data['homeBatters']:
#     if p['name'] == "Schneider":
#         print(p['r'])

