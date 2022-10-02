import re
import requests as req
from bs4 import BeautifulSoup
import os
import matplotlib.pyplot as plt
from requesting_urls import get_html
from filter_urls import find_urls

class Stats:
    """
    The class finds the each team in the semifinals, finds the players in each team, finds the player statistics
    for each player and plots the statistics for the three best players from each team.

    """
    def __init__(self):
        """
        Defines class variables,
        teams_dict (dictionary): used to store lists of players and url
        player_dict (dictionary): used to store a dictionary of ppg, bpg and rpg values
        teams (list): used to store the names of teams
        team_urls (list): used to store the urls of teams
        """
        self.teams_dict = {}
        self.players_dict = {}

        self.teams = []
        self.team_urls = []


    def _read_url(self, url):
        html = get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def find_teams(self, url = "https://en.wikipedia.org/wiki/2021_NBA_playoffs"):
        """
        Finds the each team that plays in the semifinals with their respective urls

        Arguments
        ----------
        url (str): default argument is a string of the url for 2021 NBA playoffs

        Returns
        -------
        self.team (list): a list of all team names
        self.url (list): a list of all team urls
        """
        soup = self._read_url(url)
        bracket_header = soup.find(id = "Bracket")
        bracket_table = bracket_header.find_next("table")
        headers = bracket_table.find_all("th")
        rows = bracket_table.find_all("tr")
        rows = rows[1:]

        for row in rows:
            cells = row.find_all("td")
            if len(cells) == 1 or len(cells) == 2:
                continue
            for cell in cells:
                semi_cell = cell.find_all("b")   #lists with 1 element
                if len(semi_cell)==0:
                    continue
                cell = semi_cell[0].text.strip() #takes the 0-th element to remove the list structure

                if cell == "Eastern Conference" or cell == "Western Conference":
                    continue

                regex = r"\D{2,20}[^*]"
                match = re.findall(regex, cell)  #list of 0 or 1 elements
                if len(match) == 0:
                    continue
                if match[0] in self.teams:            #takes the 0-th element to remove the list structure
                    continue
                self.teams = self.teams + match


        base_url = "https://en.wikipedia.org"
        add_base = r"^\/.*"

        str_table = str(bracket_table)           #turning bs4 element to a string
        all_urls = find_urls(str_table, base_url)

        for team in self.teams:
            if "LA" in team:
                team = team[2:]
                team = "Los Angeles" + team
            team = team.split(" ")
            team = "_".join(team)
            for url in all_urls:
                if url in self.team_urls:
                    continue
                if team in url:
                    self.team_urls.append(url)
                    break
        return self.teams, self.team_urls


    def _extract_player_help_func(self, html): #To avoid duplicate code
        soup = BeautifulSoup(html, "html.parser")
        Roster = soup.find(id = "Roster")
        Players =  Roster.find_all_next("table")[1]
        rows = Players.find_all("tr")[1:]

        players = []
        player_urls = []

        regex = r"\w*, \w*[-.']?[ ]?\w*[-.]?"

        for row in rows:
            cells = row.find_all("td")
            cell_name = cells[2].text.strip()
            matches = re.findall(regex, cell_name)
            name_split = matches[0].split(", ")
            last_name, first_name = name_split
            name_split = [first_name] + [last_name]
            name = " ".join(name_split)
            players.append(name)

            base_url = "https://en.wikipedia.org"
            name_cell_str = str(cells[2])
            url = find_urls(name_cell_str, base_url)
            player_urls += url
        return players, player_urls


    def extract_player(self, team_url = None):
        """
        Either finds all player and accompaning url from each team or finds players and accompaning url from one team,
        if a team is given as an argument.
        The methode uses a helper function _extract_player_help_func(), to avoid duplicating code. The helper function takes in
        a string of html-code and returns two lists, one containing player names and the other containing player urls

        Arguments
        ---------
        team_url (str): default is None

        Returns
        -------
        If team_url != None:
            players (list): names of players
            player_url (list): urls for players
        If team_url == None:
            self.teams_dict (dictionary): a dictionary with team names as keys and the lists players and player_url as values
        """
        if team_url != None:
            html = get_html(team_url)
            return self._extract_player_help_func(html)

        if len(self.teams) == 0:
            self.teams,  self.teams = self.find_teams()

        for url, team in zip(self.team_urls, self.teams):
            html = get_html(url)
            self.teams_dict[team] = self._extract_player_help_func(html)
        return self.teams_dict

    def extract_player_statistics(self, player_url):
        """
        Find the statistics for each player

        Arguments
        ---------
        player_url (str): a string spesifying the url for one specific player

        Returns
        -------
        ppg (float): the point per game for a given player
        bpg (float): the blocks per game for a given player
        rpg (float): the rebounds per game for a given player
        """
        html = get_html(player_url)
        soup = BeautifulSoup(html, "html.parser")
        nba_header = soup.find(id="NBA_career_statistics")

        ppg, bpg, rpg = 0, 0, 0

        if nba_header is None :
            nba_header = soup.find(id="NBA")
        try:
            regular_season_header = nba_header.find_next(id="Regular_season")
            nba_table = regular_season_header.find_next("table")
        except:
            try:
                nba_table = nba_header.find_next("table")
            except:
                return ppg, bpg, rpg
        table_header = nba_table.find_all("th")


        for idx, headers in enumerate(table_header):
            if headers.text.strip() == "PPG":
                ppg_idx = idx
            if headers.text.strip() == "RPG":
                rpg_idx = idx
            if headers.text.strip() == "BPG":
                bpg_idx = idx


        table_rows = nba_table.find_all("tr")
        for row in table_rows:
            find_row = row.find("a")
            if find_row is None:
                continue

            if "title" not in str(find_row):
                continue

            cells = row.find_all("td")
            if "2020–21 NBA season" in find_row["title"]:
                rpg = cells[rpg_idx].text.strip()
                bpg = cells[bpg_idx].text.strip()
                ppg = cells[ppg_idx].text.strip()
                if "*" in rpg:
                    rpg = rpg[:-1]
                if "*" in bpg:
                    bpg = bpg[:-1]
                if "*" in ppg:
                    ppg = ppg[:-1]
            else:
                continue

            scores = [rpg, bpg, ppg]
            for i in range(len(scores)):
                try:
                    scores[i] = float(scores[i])
                except:
                    scores[i] = 0

            rpg, bpg, ppg = scores
        return ppg, bpg, rpg


    def player_compare(self, team):
        """
        Compares the point per game for each player in a given team and finds the top three players

        Arguments
        ---------
        team (str): the name of a team

        Returns
        -------
        three lists containing the name and the value of points per game for three best players
        """
        if len(self.teams_dict)==0: #we need the team_dict to find the players and urls for each team
            self.extract_player()
        players = self.teams_dict[team][0]
        player_urls = self.teams_dict[team][1]
        nr1, nr2, nr3 = 0, 0, 0                          #ppg values set to 0
        nr1_name, nr2_name, nr3_name = None, None, None  #player names set to None
        for player, url in zip(players, player_urls):
            player_dict = {}                             #dictionary stores ppg, bpg and rpg values
            ppg, bpg, rpg = self.extract_player_statistics(url)

            player_dict["ppg"], player_dict["bpg"], player_dict["rpg"] = ppg, bpg, rpg
            self.players_dict[player] = player_dict      #dictionary that has player name as keys and the dict containing ppg, bpg and rpg as values

            if ppg > nr1: #updates all three best players
                nr3, nr3_name = nr2, nr2_name
                nr2, nr2_name = nr1, nr1_name
                nr1, nr1_name = ppg, player
            elif ppg > nr2: #updates only the nr. 2 and nr. 3
                nr3, nr3_name = nr2, nr2_name
                nr2, nr2_name = ppg, player
            elif ppg > nr3: #updates only nr. 3
                nr3, nr3_name = ppg, player

        return [nr1_name, nr1], [nr2_name, nr2], [nr3_name, nr3]


    def comparison_pool(self, teams=None):
        """
        Collects the three best players from each team into one dictionary

        Arguments
        ---------
        teams (list): default is set to None

        Returns
        -------
        best_players_per_team_dict (dictionary): a dictionary with team name as keys and dictionary containing the three best players
            from that a given team
        """
        if teams == None:
            teams = self.teams
        best_players_per_team_dict = {}
        for team in teams:
            nr1, nr2, nr3 = self.player_compare(team) # nr1, nr2 and nr3 is here lists of a name and a value
            best_players_dict = {}                    # dictionary with player name as keys and ppg, bpg and rpg as values
            best_players_dict[nr1[0]] = self.players_dict[nr1[0]]
            best_players_dict[nr2[0]] = self.players_dict[nr2[0]]
            best_players_dict[nr3[0]] = self.players_dict[nr3[0]]

            best_players_per_team_dict[team] = best_players_dict
        return best_players_per_team_dict


    def _color_table(self):
        color_table = {}
        color_list = ["lightcoral", "brown", "mediumaquamarine", "pink", "paleturquoise", "indianred", "palegreen", "orange"]
        for team, color in zip(self.teams, color_list):
            color_table[team] = color
        return color_table


    def _plot_players(self, xpg = "ppg"):
        """
        Saves an image of the player statistics plottes against either ppg, bpg or rpg.
        Uses a helper function _color_table() to define the colors of the plot, which return a dictionary with
        team names as keys and colors as values

        Arguments
        ---------
        xpg (str): defines which unit of messurment to plot against

        Returns
        -------
        None
        """
        point_name_dict = {"ppg": "Points", "bpg": "Blocks", "rpg": "Rebounds"}
        if xpg not in point_name_dict:
            print("Input need to be either 'ppg', 'bpg' or 'rpg'")
            return
        if len(self.teams) == 0:
            self.find_teams()

        color_table = self._color_table()
        dict = self.comparison_pool(self.teams)
        count_so_far = 0
        all_names = []

        plt.figure(figsize=(9, 6))
        for team in self.teams:
            xpg_list = []
            names = []
            for player in dict[team]:
                names.append(player)
                xpg_list.append(dict[team][player][xpg])
            all_names.extend(names)
            x = range(count_so_far, count_so_far + len(dict[team]))
            count_so_far += len(dict[team])


            bars = plt.bar(x, xpg_list, color = color_table[team], label = team)

        dir = os.getcwd()
        path = dir + "\\NBA_player_statistics"

        plt.ylabel(f"{point_name_dict[xpg]} per game")
        plt.xlabel("Players")
        plt.xticks(range(len(all_names)), all_names, rotation = 90)
        plt.legend(loc = 0)
        plt.grid(False)
        plt.title(f"{point_name_dict[xpg]} per game")
        plt.subplots_adjust(left=0.09, right=0.9, top=0.95, bottom=0.37)
        plt.savefig(f"{path}\\players_over_{xpg}.png")
        print(f"image for {xpg} had been saved to {path}")

    def plot(self):
        """
        Plots the statistics for the three best players from each team, with regard to ppg, bbg and rpg.
        """
        self._plot_players("ppg")
        self._plot_players("bpg")
        self._plot_players("rpg")





if __name__ == '__main__':
    stat = Stats()
    stat.plot()
