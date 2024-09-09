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

    allBoxScores = []

    scoresDev = []
    scoresAna = []
    scoresDSM = []
    scoresMis = []

    projScoresDev = []
    projScoresAna = []
    projScoresDSM = []
    projScoresMis = []

    for boxScore in leagueDev.box_scores(week=week):
        allBoxScores.append(boxScore)

        scoresDev.append(boxScore.home_score)
        scoresDev.append(boxScore.away_score)

        projScoresDev.append(boxScore.home_projected)
        projScoresDev.append(boxScore.away_projected)

    for boxScore in leagueAna.box_scores(week=week):
        allBoxScores.append(boxScore)

        scoresAna.append(boxScore.home_score)
        scoresAna.append(boxScore.away_score)

        projScoresAna.append(boxScore.home_projected)
        projScoresAna.append(boxScore.away_projected)

    for boxScore in leagueDSM.box_scores(week=week):
        allBoxScores.append(boxScore)

        scoresDSM.append(boxScore.home_score)
        scoresDSM.append(boxScore.away_score)

        projScoresDSM.append(boxScore.home_projected)
        projScoresDSM.append(boxScore.away_projected)

    for boxScore in leagueMis.box_scores(week=week):
        allBoxScores.append(boxScore)

        scoresMis.append(boxScore.home_score)
        scoresMis.append(boxScore.away_score)

        projScoresMis.append(boxScore.home_projected)
        projScoresMis.append(boxScore.away_projected)

    scoresDev.sort(reverse=True)
    scoresAna.sort(reverse=True)
    scoresDSM.sort(reverse=True)
    scoresMis.sort(reverse=True)

    projScoresDev.sort(reverse=True)
    projScoresAna.sort(reverse=True)
    projScoresDSM.sort(reverse=True)
    projScoresMis.sort(reverse=True)

    rep = "<html>"
    rep += "<meta name='viewport' content='width=device-width'>"
    rep += "<body>"
    rep += "<h1>Boxes In, Boxes Out<br/>Scoreboard</h1>"

    rep += "<a href=\"standings\">Standings</a><br/><br/>"

    i = 0
    for boxScore in allBoxScores:
        cls = "developer"
        leagueId = "1020397"
        homeRank = -1
        awayRank = -1
        homeProjectedRank = -1
        awayProjectedRank = -1
        if i < 6:
            homeRank = scoresDev.index(boxScore.home_score) + 1
            awayRank = scoresDev.index(boxScore.away_score) + 1

            homeProjectedRank = projScoresDev.index(boxScore.home_projected) + 1
            awayProjectedRank = projScoresDev.index(boxScore.away_projected) + 1
        if i>=6 and i<12:
            cls = "analyst"
            leagueId = "1953587261"

            homeRank = scoresAna.index(boxScore.home_score) + 1
            awayRank = scoresAna.index(boxScore.away_score) + 1

            homeProjectedRank = projScoresAna.index(boxScore.home_projected) + 1
            awayProjectedRank = projScoresAna.index(boxScore.away_projected) + 1
        elif i>=12 and i<18:
            cls = "dsm"
            leagueId = "635993"

            homeRank = scoresDSM.index(boxScore.home_score) + 1
            awayRank = scoresDSM.index(boxScore.away_score) + 1

            homeProjectedRank = projScoresDSM.index(boxScore.home_projected) + 1
            awayProjectedRank = projScoresDSM.index(boxScore.away_projected) + 1
        elif i>=18:
            cls = "misfit"
            leagueId = "517497302"

            homeRank = scoresMis.index(boxScore.home_score) + 1
            awayRank = scoresMis.index(boxScore.away_score) + 1

            homeProjectedRank = projScoresMis.index(boxScore.home_projected) + 1
            awayProjectedRank = projScoresMis.index(boxScore.away_projected) + 1

        rep += "<div class=\"boxScore " + cls + "\">"
        rep += "<table style=\"width: 100%;\">"
        rep += "<tr>"
        rep += "<td style=\"overflow: hidden;\">"
        rep += "<img src=\"" + boxScore.home_team.logo_url + "\" style=\"vertical-align:middle; height: 20px; width: 20px; overflow: hidden; margin-right: 5px;\" />"
        rep += "<a href=\"https://fantasy.espn.com/football/team?leagueId=" + leagueId + "&teamId=" + str(boxScore.home_team.team_id) + "\">" + boxScore.home_team.team_name + "</a> "
        rep += "<span>(" + boxScore.home_team.owners[0]["firstName"] + " " + boxScore.home_team.owners[0]["lastName"] + ")</span>"
        rep += "</td>"
        rep += "<td style=\"width: 80px;\">"
        rep += str(boxScore.home_score) + "&nbsp;(" + str(homeRank) + ")"
        rep += "</td>"
        rep += "<td style=\"width: 120px;\">"
        rep += "Proj.&nbsp;" + str(boxScore.home_projected) + "&nbsp;(" + str(homeProjectedRank) + ")"
        rep += "</td>"
        rep += "</tr>"

        rep += "<tr>"
        rep += "<td>"
        rep += "<img src=\"" + boxScore.away_team.logo_url + "\" style=\"vertical-align:middle; height: 20px; width: 20px; overflow: hidden; margin-right: 5px;\" />"
        rep += "<a href=\"https://fantasy.espn.com/football/team?leagueId=" + leagueId + "&teamId=" + str(boxScore.away_team.team_id) + "\">" + boxScore.away_team.team_name + "</a> "
        rep += "<span>(" + boxScore.away_team.owners[0]["firstName"] + " " + boxScore.away_team.owners[0]["lastName"] + ")</span>"
        rep += "</td>"
        rep += "<td>"
        rep += str(boxScore.away_score) + "&nbsp;(" + str(awayRank) + ")"
        rep += "</td>"
        rep += "<td>"
        rep += "Proj.&nbsp;" + str(boxScore.away_projected) + "&nbsp;(" + str(awayProjectedRank) + ")"
        rep += "</td>"
        rep += "</tr>"

        rep += "</table>"

        rep += "<a href=\"https://fantasy.espn.com/football/boxscore?leagueId=" + leagueId + "&matchupPeriodId=" + str(week) + "&seasonId=" + str(year) + "&teamId=" + str(boxScore.away_team.team_id) + "\">View Box Score on ESPN</a>"

        rep += "</div>"

        i+=1


    rep += "</body>"
    rep += "<style>"
    rep += ".boxScore {"
    rep += "max-width: 600px;"
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

    standingsDev = leagueDev.standings()
    standingsAna = leagueAna.standings()
    standingsDSM = leagueDSM.standings()
    standingsMis = leagueMis.standings()

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

    rep += "<a href=\"boxScores\">Box Scores</a><br/><br/>"

    rep += "<table>"
    rep += "<thead>"
    rep += "<tr>"
    rep += "<th style=\"width: 20px; text-align: center;\"></th>"
    rep += "<th style=\"width: 20px; text-align: center;\"></th>"
    rep += "<th>Team</th>"
    rep += "<th style=\"width: 20px; text-align: center;\">W</th>"
    rep += "<th style=\"width: 20px; text-align: center;\">L</th>"
    rep += "<th style=\"width: 20px; text-align: center;\">T</th>"
    rep += "<th style=\"width: 20px; text-align: center;\">Pts</th>"
    rep += "<th style=\"width: 20px; text-align: center;\">PO%</th>"
    rep += "</tr>"
    rep += "</thead>"


    for (idx, team) in enumerate(allTeams):
        placeInLeague = -1
        if team in leagueDev.teams:
            cls = "developer"
            leagueId = "1020397"
            placeInLeague = standingsDev.index(team) + 1
        if team in leagueAna.teams:
            cls = "analyst"
            leagueId = "1953587261"
            placeInLeague = standingsAna.index(team) + 1
        elif team in leagueDSM.teams:
            cls = "dsm"
            leagueId = "635993"
            placeInLeague = standingsDSM.index(team) + 1
        elif team in leagueMis.teams:
            cls = "misfit"
            leagueId = "517497302"
            placeInLeague = standingsMis.index(team) + 1

        rep += "<tr class=\"" + cls + "\">"

        rep += "<td style=\"text-align: center;\">"
        rep += str(idx + 1)
        rep += "</td>"

        rep += "<td style=\"text-align: center;\">"
        rep += str(placeInLeague)
        rep += "</td>"

        rep += "<td>"
        rep += "<img src=\"" + team.logo_url + "\" style=\"vertical-align:middle; height: 20px; width: 20px; overflow: hidden; margin-right: 5px;\" />"
        rep += "<a href=\"https://fantasy.espn.com/football/team?leagueId=" + leagueId + "&teamId=" + str(team.team_id) + "\">" + team.team_name + "</a> "
        rep += "<span>(" + team.owners[0]["firstName"] + " " + team.owners[0]["lastName"] + ")</span>"
        rep += "</td>"

        rep += "<td style=\"text-align: center;\">"
        rep += str(team.wins)
        rep += "</td>"

        rep += "<td style=\"text-align: center;\">"
        rep += str(team.losses)
        rep += "</td>"

        rep += "<td style=\"text-align: center;\">"
        rep += str(team.ties)
        rep += "</td>"

        htmlTxt = "<td style=\"text-align: center;\">{:10.1f}</td>"
        rep += htmlTxt.format(team.points_for)

        htmlTxt = "<td style=\"text-align: center;\">{:10.0f}</td>"
        rep += htmlTxt.format(team.playoff_pct)

        rep += "</tr>"

    rep += "</table>"

    rep += "</body>"
    rep += "<style>"
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





