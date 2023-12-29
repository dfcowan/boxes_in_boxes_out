import requests
import re
from io import BytesIO, StringIO
from espn_api.football import League
from flask import Flask, request, jsonify, send_file
scoreboard = Flask(__name__)



# A welcome message to test our server
@scoreboard.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

week = 17

def eligibleForPosition(position, playerPosition):
    if (position == playerPosition):
        return True
    
    if (position == "FLEX" and (playerPosition == "RB" or playerPosition == "WR" or playerPosition == "TE")):
        return True

    if (position == "OP" and playerPosition != "D/ST"):
        return True

    return False

def printPlayer(position, player, longestNameLength):
    html = ""
    stats = player.stats[week]

    actual = 0
    if "points" in stats.keys():
        actual = stats["points"]

    html += "<tr>"
    html += "<td>" + position + "</td>"
    
    htmlTxt = "<td>{}</td><td>{}</td>"
    html += htmlTxt.format(player.name, player.proTeam)

    txt = "{} {} {} ({})"
    txt = txt.format(position.ljust(4), player.name, player.proTeam, player.playerId).ljust(longestNameLength)


    txt += "{:10.2f} {:10.2f}"
    print(txt.format(stats["projected_points"], actual))

    htmlTxt = "<td style='text-align: right;'>{:10.2f}</td><td style='text-align: right;'>{:10.2f}</td>"
    html += htmlTxt.format(stats["projected_points"], actual)

    html += "</tr>"

    return html

def printTeam(team, lineup):
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
                html += printPlayer(position, player, longestNameLength)            
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
            html += printPlayer(player.position, player, longestNameLength)

    html += "</table>"
    html += "</div>"
    return html


@scoreboard.route('/finalsScoreboard', methods=['GET'])
def respond():
    rep = "<html>"
    rep += "<meta name='viewport' content='width=device-width'>"
    rep += "<body>"
    rep += "<h1>Boxes In, Boxes Out World Championship</h1>"

    rep += "<table>"
    rep += "<tr>"
    rep += "<td>"
    leagueDev = League(league_id=1020397, year=2023)
    teamDrew = leagueDev.teams[3]
    lineupDrew = [3117251, 15847, 4242335, 4360310, 2577327, 4036378, 2576414,4428331,-16013]
    rep += printTeam(teamDrew, lineupDrew)
    rep += "</td>"
    rep += "</tr>"

    rep += "<tr>"
    rep += "<td>"
    leagueAna = League(league_id=1953587261, year=2023)
    teamAlex = leagueAna.teams[4]
    lineupAlex = [3139477, 4697815, 4379399, 4374302, 4360438, 4361050, 2576414, 4361741, -16014]
    rep += printTeam(teamAlex, lineupAlex)
    rep += "</td>"
    rep += "</tr>"

    rep += "<tr>"
    rep += "<td>"
    leagueDSM = League(league_id=635993, year=2023)
    teamByrd = leagueDSM.teams[3]
    lineupByrd = [3916387,3068267,3054850,3116406,4241478,3123076,4259545,4432577,-16021]
    rep += printTeam(teamByrd, lineupByrd)
    rep += "</td>"
    rep += "</tr>"

    rep += "<tr>"
    rep += "<td>"
    leagueMis = League(league_id=517497302, year=2023)
    teamJeremy = leagueMis.teams[1]
    lineupJeremy = [2577417,3054850,4430737,4262921,4569618,4361307,3042519,4432577,-16021]
    rep += printTeam(teamJeremy, lineupJeremy)
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

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    scoreboard.run(threaded=True, port=5000)





