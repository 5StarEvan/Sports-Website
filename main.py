import BasketballPlayer
import numpy as np
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo, leaguedashplayerstats
from nba_api.stats.static import players
from datetime import datetime
#import AIChoices

def read_favourite_players(filename='FavouritePlayers.txt'):
    favourite_players = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                name = line.strip()
                if name:
                    favourite_players.append(name)
    except FileNotFoundError:
        print(f"{filename} not found.")
    return favourite_players

def get_player_id_by_name(player_name):
    player_list = players.find_players_by_full_name(player_name)
    if player_list:
        return player_list[0]['id']
    return None

def get_player_current_age(player_id):
    info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    info_dict = info.get_dict()
    birth_date_str = info_dict['resultSets'][0]['rowSet'][0][info_dict['resultSets'][0]['headers'].index('BIRTHDATE')]
    dob = datetime.strptime(birth_date_str.split('T')[0], '%Y-%m-%d')
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def get_player_stats(player_name):
    player_id = get_player_id_by_name(player_name)
    if not player_id:
        print(f"Player not found: {player_name}")
        return None
    try:
        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        career_dict = career.get_dict()
        career_stats = None
        for result_set in career_dict['resultSets']:
            if result_set['name'] == 'CareerTotalsRegularSeason':
                career_stats = result_set
                break
        if not career_stats:
            print(f"Career stats not found for {player_name}.")
            return None
        headers = career_stats['headers']
        stats = career_stats['rowSet'][0]
        stats_dict = dict(zip(headers, stats))
        player_age = get_player_current_age(player_id)
        # Team
        recent_team = None
        for result_set_team in career_dict['resultSets']:
            if result_set_team['name'] == 'SeasonTotalsRegularSeason':
                if result_set_team['rowSet']:
                    last_season_row = result_set_team['rowSet'][-1]
                    if 'TEAM_ABBREVIATION' in result_set_team['headers']:
                        team_index = result_set_team['headers'].index('TEAM_ABBREVIATION')
                        recent_team = last_season_row[team_index]
                    elif 'TEAM_NAME' in result_set_team['headers']:
                        team_index = result_set_team['headers'].index('TEAM_NAME')
                        recent_team = last_season_row[team_index]
                break
        team = recent_team
        sport = "Basketball"
        position = None
        gp = stats_dict['GP'] if stats_dict['GP'] else 1
        ppg = round(stats_dict['PTS'] / gp, 2)
        apg = round(stats_dict['AST'] / gp, 2)
        rpg = round(stats_dict['REB'] / gp, 2)
        spg = round(stats_dict['STL'] / gp, 2)
        bpg = round(stats_dict['BLK'] / gp, 2)
        tpg = round(stats_dict['TOV'] / gp, 2)
        fpg = round(stats_dict['PF'] / gp, 2)
        fgptc = round(stats_dict['FG_PCT'] * 100 if stats_dict['FG_PCT'] is not None else 0, 2)
        player_obj = BasketballPlayer.BasketballPlayer(
            player_name, player_age, team, sport, position,
            ppg, apg, rpg, spg, bpg, tpg, fpg, fgptc
        )
        return player_obj
    except Exception as e:
        print(f"An error occurred while fetching stats for {player_name}: {e}")
        return None

def get_top_nba_players_by_stat(stat, top_n=10):
    """
    Returns the top_n NBA players for a given stat (e.g., 'PTS', 'AST', 'REB', 'FG_PCT', etc.).
    Usage: get_top_nba_players_by_stat('PTS', 10) for top 10 points per game scorers.
    """

    if stat == 'ppg':
        stat = 'PTS'
    elif stat == 'apg':
        stat = 'AST'
    elif stat == 'rpg':
        stat = 'REB'
    elif stat == 'fgptc':
        stat = 'FG_PCT'
    elif stat == 'spg':
        stat = 'STL'
    elif stat == 'bpg':
        stat = 'BLK'
    elif stat == 'tpg':
        stat = 'TOV'
    elif stat == 'fpg':
        stat = 'PF'

    stats = leaguedashplayerstats.LeagueDashPlayerStats(season_type_all_star='Regular Season').get_dict()
    headers = stats['resultSets'][0]['headers']
    rows = stats['resultSets'][0]['rowSet']
    if stat not in headers:
        print(f"Stat '{stat}' not found. Valid stats: {headers}")
        return []
    stat_index = headers.index(stat)
    player_name_index = headers.index('PLAYER_NAME')
    gp_index = headers.index('GP')
    # Calculate per-game value for each player
    rows_with_per_game = [
        (x, round(x[stat_index]/x[gp_index], 2) if x[gp_index] else 0)
        for x in rows
    ]
    # Sort by per-game value
    top_rows = sorted(rows_with_per_game, key=lambda tup: tup[1], reverse=True)[:top_n]
    return [{
        'name': x[player_name_index],
        'value': per_game
    } for x, per_game in top_rows]


def get_player_stats_by_id(player_id, player_name=None):
    try:
        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        career_dict = career.get_dict()
        career_stats = None
        for result_set in career_dict['resultSets']:
            if result_set['name'] == 'CareerTotalsRegularSeason':
                career_stats = result_set
                break
        if not career_stats:
            return None
        headers = career_stats['headers']
        stats = career_stats['rowSet'][0]
        stats_dict = dict(zip(headers, stats))
        player_age = get_player_current_age(player_id)
        recent_team = None
        for result_set_team in career_dict['resultSets']:
            if result_set_team['name'] == 'SeasonTotalsRegularSeason':
                if result_set_team['rowSet']:
                    last_season_row = result_set_team['rowSet'][-1]
                    if 'TEAM_ABBREVIATION' in result_set_team['headers']:
                        team_index = result_set_team['headers'].index('TEAM_ABBREVIATION')
                        recent_team = last_season_row[team_index]
                    elif 'TEAM_NAME' in result_set_team['headers']:
                        team_index = result_set_team['headers'].index('TEAM_NAME')
                        recent_team = last_season_row[team_index]
                break
        team = recent_team
        sport = "Basketball"
        position = None
        gp = stats_dict['GP'] if stats_dict['GP'] else 1
        ppg = round(stats_dict['PTS'] / gp, 2)
        apg = round(stats_dict['AST'] / gp, 2)
        rpg = round(stats_dict['REB'] / gp, 2)
        spg = round(stats_dict['STL'] / gp, 2)
        bpg = round(stats_dict['BLK'] / gp, 2)
        tpg = round(stats_dict['TOV'] / gp, 2)
        fpg = round(stats_dict['PF'] / gp, 2)
        fgptc = round(stats_dict['FG_PCT'] * 100 if stats_dict['FG_PCT'] is not None else 0, 2)
        player_obj = BasketballPlayer.BasketballPlayer(
            player_name if player_name else "NBA Top Player", player_age, team, sport, position,
            ppg, apg, rpg, spg, bpg, tpg, fpg, fgptc
        )
        return player_obj
    except Exception as e:
        return None

def print_top_nba_players_by_stat(stat, top_n=10):
    topArray =get_top_nba_players_by_stat(stat, top_n)
    for player in topArray:
        print(player['name'], player['value'])

# Main execution
if __name__ == "__main__":
    favouritePlayers = read_favourite_players()
    player_objects = []
    for player in favouritePlayers:
        obj = get_player_stats(player)
        if obj:
            player_objects.append(obj)

    print_top_nba_players_by_stat('bpg', 10)
    #topList = AIChoices.getAIPicks()

    # for name in topList:
    #     print(name)


