import json
import requests
import re
from io import BytesIO, StringIO
from espn_api.football import League, Player, Team, BoxPlayer, box_score
from flask import Flask, request, jsonify, send_file
scoreboard = Flask(__name__)


year = 2024

# A welcome message to test our server
@scoreboard.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

def eligibleForPosition(position: str, playerPosition: str):
    if (position == playerPosition):
        return True

    if (position == "FLEX" and (playerPosition == "RB" or playerPosition == "WR" or playerPosition == "TE")):
        return True

    if (position == "OP" and playerPosition != "D/ST"):
        return True

    return False

def printPlayer(position: str, player: Player, longestNameLength: int, week: int):
    html = ""
    stats = player.stats[week]

    actual = 0
    if "points" in stats.keys():
        actual = stats["points"]

    html += "<tr>"
    html += "<td>" + position + "</td>"

    htmlTxt = "<td><span title='{}'>{}</span></td><td>{}</td>"
    html += htmlTxt.format(player.playerId, player.name, player.proTeam)

    txt = "{} {} {} ({})"
    txt = txt.format(position.ljust(4), player.name, player.proTeam, player.playerId).ljust(longestNameLength)


    txt += "{:10.2f} {:10.2f}"
    print(txt.format(stats["projected_points"], actual))

    htmlTxt = "<td style='text-align: right;'>{:10.2f}</td><td style='text-align: right;'>{:10.2f}</td>"
    html += htmlTxt.format(stats["projected_points"], actual)

    html += "</tr>"

    return html

def printTeam(team: Team, lineup: list[int], week: int):
    html = "<div style='border: 1px solid black;'>"
    html += "<h2>" + team.team_name + "</h2>"
    print(team.team_name)

    txt = ""
    txt = txt.ljust(len(team.team_name), "=")
    print(txt)
    print()

    longestNameLength = 0
    for player in team.roster:
        txt = "FLEX {} {} ({})"
        txt = txt.format(player.name, player.proTeam, player.playerId)

        if len(txt) > longestNameLength:
            longestNameLength = len(txt)

    html += "<table>"
    html += "<tr>"
    html += "<td colspan='10'>"
    html += "<h3>Lineup</h3>"
    html += "</td>"
    html += "</tr>"
    html += "<tr>"
    html += "<th>Pos.</th>"
    html += "<th>Player</th>"
    html += "<th>Team</th>"
    html += "<th style='text-align: right;'>Proj.</th>"
    html += "<th style='text-align: right;'>Act.</th>"
    html += "</tr>"
    txt = "Lineup"
    txt = txt.ljust(longestNameLength)
    txt += "     Proj.       Act."
    print(txt)

    width = len(txt)
    txt = ""
    txt = txt.ljust(width, "-")
    print(txt)

    printedLineup = []
    positions = ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX", "OP", "D/ST"]

    totalProjected = 0.0
    totalActual = 0.0
    for position in positions:
        for player in team.roster:
            if player.playerId in lineup and eligibleForPosition(position, player.position) and not(player.playerId in printedLineup):
                html += printPlayer(position, player, longestNameLength, week)
                stats = player.stats[week]

                totalProjected += stats["projected_points"]
                if "points" in stats.keys():
                    totalActual += stats["points"]

                printedLineup.append(player.playerId)
                break

    html += "<tr>"
    html += "<th colspan='3' style='text-align: right;'>Total</th>"
    htmlTxt = "<th style='text-align: right;'>{:10.2f}</th><th style='text-align: right;'>{:10.2f}</th>"
    html += htmlTxt.format(totalProjected, totalActual)
    html += "</tr>"
    txt = "Total:"
    txt = txt.rjust(longestNameLength)
    txt += "{:10.2f} {:10.2f}"
    print(txt.format(totalProjected, totalActual))

    html += "<tr>"
    html += "<td colspan='10'>"
    html += "<h3>Bench</h3>"
    html += "</td>"
    html += "</tr>"
    html += "<tr>"
    html += "<th>Pos.</th>"
    html += "<th>Player</th>"
    html += "<th>Team</th>"
    html += "<th style='text-align: right;'>Proj.</th>"
    html += "<th style='text-align: right;'>Act.</th>"
    html += "</tr>"
    print()
    txt = "Bench"
    txt = txt.ljust(longestNameLength)
    txt += "     Proj.       Act."
    print(txt)

    width = len(txt)
    txt = ""
    txt = txt.ljust(width, "-")
    print(txt)
    for player in team.roster:
        if not(player.playerId in lineup):
            html += printPlayer(player.position, player, longestNameLength, week)

    html += "</table>"
    html += "</div>"
    return html


@scoreboard.route('/finalsScoreboard', methods=['GET'])
def finalsScoreboard():
    week = 1

    rep = "<html>"
    rep += "<meta name='viewport' content='width=device-width'>"
    rep += "<body>"
    rep += "<h1>Boxes In, Boxes Out World Championship</h1>"

    rep += "<table>"
    rep += "<tr>"
    rep += "<td>"
    leagueDev = League(league_id=1020397, year=year)
    teamDrew = leagueDev.teams[3]
    lineupDrew = [3117251, 15847, 4242335, 4360310, 2577327, 4036378, 2576414,4428331,-16013]
    rep += printTeam(teamDrew, lineupDrew, week)
    rep += "</td>"
    rep += "</tr>"

    rep += "<tr>"
    rep += "<td>"
    leagueAna = League(league_id=1953587261, year=year)
    teamAlex = leagueAna.teams[4]
    lineupAlex = [3139477, 4697815, 4242431, 4374302, 4360438, 4361050, 4361741, 4361777, -16013]
    rep += printTeam(teamAlex, lineupAlex, week)
    rep += "</td>"
    rep += "</tr>"

    rep += "<tr>"
    rep += "<td>"
    leagueDSM = League(league_id=635993, year=year)
    teamByrd = leagueDSM.teams[3]
    lineupByrd = [4379399,3916387,3054850,3116406,4241478,3123076,4259545,4432577,-16021]
    rep += printTeam(teamByrd, lineupByrd, week)
    rep += "</td>"
    rep += "</tr>"

    rep += "<tr>"
    rep += "<td>"
    leagueMis = League(league_id=517497302, year=year)
    teamJeremy = leagueMis.teams[1]
    lineupJeremy = [2577417,3054850,4430737,4262921,4569618,4361307,3042519,4432577,-16021]
    rep += printTeam(teamJeremy, lineupJeremy, week)
    rep += "</td>"
    rep += "</tr>"
    rep += "</table>"

    rep += "</body>"
    rep += "<style>"
    rep += "table {"
    rep += "width: 100%;"
    rep += "}"
    rep += "td {"
    rep += "padding: 5px;"
    rep += "}"
    rep += "th {"
    rep += "padding: 5px;"
    rep += "text-align: left;"
    rep += "}"
    rep += "</style>"
    rep += "</html>"

    return rep

@scoreboard.route('/boxScores', methods=['GET'])
def boxScores():
    leagueDev = League(league_id=1020397, year=year)
    leagueAna = League(league_id=1953587261, year=year)
    leagueDSM = League(league_id=635993, year=year)
    leagueMis = League(league_id=517497302, year=year)

    week = leagueDev.current_week

    allBoxScores = leagueDev.box_scores(week=week)
    allBoxScores = allBoxScores + leagueAna.box_scores(week=week)
    allBoxScores = allBoxScores + leagueDSM.box_scores(week=week)
    allBoxScores = allBoxScores + leagueMis.box_scores(week=week)

    rep = "<html>"
    rep += "<meta name='viewport' content='width=device-width'>"
    rep += "<body>"
    rep += "<h1>Boxes In, Boxes Out<br/>League Scoreboard</h1>"

    i = 0
    for boxScore in allBoxScores:
        cls = "developer"
        leagueId = "1020397"
        if i>=6 and i<12:
            cls = "analyst"
            leagueId = "1953587261"
        elif i>=12 and i<18:
            cls = "dsm"
            leagueId = "635993"
        elif i>=18:
            cls = "misfit"
            leagueId = "517497302"

        rep += "<div class=\"boxScore " + cls + "\">"
        rep += "<table style=\"width: 100%;\">"
        rep += "<tr>"
        rep += "<td style=\"overflow: hidden;\">"
        rep += "<img src=\"" + boxScore.home_team.logo_url + "\" style=\"vertical-align:middle; height: 20px; width: 20px; overflow: hidden; margin-right: 5px;\" />"
        rep += "<span>" + boxScore.home_team.team_name + "</span> "
        rep += "<span>(" + boxScore.home_team.owners[0]["firstName"] + " " + boxScore.home_team.owners[0]["lastName"] + ")</span>"
        rep += "</td>"
        rep += "<td style=\"width: 40px;\">"
        rep += str(boxScore.home_score)
        rep += "</td>"
        rep += "<td style=\"width: 80px;\">"
        rep += "Proj. " + str(boxScore.home_projected)
        rep += "</td>"
        rep += "</tr>"

        rep += "<tr>"
        rep += "<td>"
        rep += "<img src=\"" + boxScore.away_team.logo_url + "\" style=\"vertical-align:middle; height: 20px; width: 20px; overflow: hidden; margin-right: 5px;\" />"
        rep += "<span>" + boxScore.away_team.team_name + "</span> "
        rep += "<span>(" + boxScore.away_team.owners[0]["firstName"] + " " + boxScore.away_team.owners[0]["lastName"] + ")</span>"
        rep += "</td>"
        rep += "<td>"
        rep += str(boxScore.away_score)
        rep += "</td>"
        rep += "<td>"
        rep += "Proj. " + str(boxScore.away_projected)
        rep += "</td>"
        rep += "</tr>"

        rep += "</table>"

        # rep += "<a href=\"https://fantasy.espn.com/football/boxscore?leagueId=" + leagueId + "&matchupPeriodId=" + str(week) + "&seasonId=" + str(year) + "&teamId=" + str(boxScore.home_team.team_id) + "\">View on ESPN</a>"

        rep += "</div>"

        i+=1


    rep += "</body>"
    rep += "<style>"
    rep += ".boxScore {"
    rep += "width: 100%;"
    rep += "border: 2px solid gray;"
    rep += "margin: 3px;"
    rep += "padding: 3px;"
    rep += "}"
    rep += ".developer"
    rep += "{"
    rep += "background-color: ef476f;"
    rep += "}"
    rep += ".analyst"
    rep += "{"
    rep += "background-color: ffd166"
    rep += "}"
    rep += ".dsm"
    rep += "{"
    rep += "background-color: 06d6a0"
    rep += "}"
    rep += ".misfit"
    rep += "{"
    rep += "background-color: 118ab2"
    rep += "}"
    rep += "</style>"
    rep += "</html>"

    return rep

def sortPoints(team: Team):
    return -1 * team.points_for

def sortWins(team: Team):
    return -1 * team.points_for

def sortPlayoff(team: Team):
    return -1 * team.playoff_pct

@scoreboard.route('/standings', methods=['GET'])
def standings():
    leagueDev = League(league_id=1020397, year=year)
    leagueAna = League(league_id=1953587261, year=year)
    leagueDSM = League(league_id=635993, year=year)
    leagueMis = League(league_id=517497302, year=year)

    allTeams = leagueDev.teams.copy()
    allTeams = allTeams + leagueAna.teams
    allTeams = allTeams + leagueDSM.teams
    allTeams = allTeams + leagueMis.teams

    allTeams.sort(key=sortPlayoff)
    allTeams.sort(key=sortPoints)
    allTeams.sort(key=sortWins)

    rep = "<html>"
    rep += "<meta name='viewport' content='width=device-width'>"
    rep += "<body>"
    rep += "<h1>Boxes In, Boxes Out<br/>Standings</h1>"

    rep += "<table>"
    rep += "<thead>"
    rep += "<tr>"
    rep += "<th></th>"
    rep += "<th>Team</th>"
    rep += "<th>W</th>"
    rep += "<th>L</th>"
    rep += "<th>T</th>"
    rep += "<th>Pts</th>"
    rep += "<th>PO%</th>"
    rep += "</tr>"
    rep += "</thead>"


    for (idx, team) in enumerate(allTeams):
        cls = "developer"
        if team in leagueAna.teams:
            cls = "analyst"
        elif team in leagueDSM.teams:
            cls = "dsm"
        elif team in leagueMis.teams:
            cls = "misfit"

        rep += "<tr class=\"" + cls + "\">"

        rep += "<td>"
        rep += str(idx + 1)
        rep += "</td>"

        rep += "<td>"
        rep += "<img src=\"" + team.logo_url + "\" style=\"vertical-align:middle; height: 20px; width: 20px; overflow: hidden; margin-right: 5px;\" />"
        rep += "<span>" + team.team_name + "</span> "
        rep += "<span>(" + team.owners[0]["firstName"] + " " + team.owners[0]["lastName"] + ")</span>"
        rep += "</td>"

        rep += "<td>"
        rep += str(team.wins)
        rep += "</td>"

        rep += "<td>"
        rep += str(team.losses)
        rep += "</td>"

        rep += "<td>"
        rep += str(team.ties)
        rep += "</td>"

        htmlTxt = "<td>{:10.1f}</td>"
        rep += htmlTxt.format(team.points_for)

        htmlTxt = "<td>{:10.0f}</td>"
        rep += htmlTxt.format(team.playoff_pct)

        rep += "</tr>"

    rep += "</table>"

    rep += "</body>"
    rep += "<style>"
    rep += "table {"
    rep += "width: 100%;"
    rep += "}"
    rep += "td {"
    rep += "padding: 5px;"
    rep += "}"
    rep += "th {"
    rep += "padding: 5px;"
    rep += "text-align: left;"
    rep += "font-weight: bold;"
    rep += "}"
    rep += ".developer"
    rep += "{"
    rep += "background-color: ef476f;"
    rep += "}"
    rep += ".analyst"
    rep += "{"
    rep += "background-color: ffd166"
    rep += "}"
    rep += ".dsm"
    rep += "{"
    rep += "background-color: 06d6a0"
    rep += "}"
    rep += ".misfit"
    rep += "{"
    rep += "background-color: 118ab2"
    rep += "}"
    rep += "</style>"
    rep += "</html>"

    return rep

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    scoreboard.run(threaded=True, port=5000)





