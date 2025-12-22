import json
from espn_api.football import League, Player, Team, BoxPlayer, box_score
from flask import Flask, request, jsonify, send_file, render_template
scoreboard = Flask(__name__)


year = 2025

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

# @scoreboard.route('/finalsScoreboardV2', methods=['GET'])
# def finalsScoreboardV2():
#     return render_template('finalsScoreboard.html')


@scoreboard.route('/finalsScoreboard', methods=['GET'])
def finalsScoreboard():
    week = 16

    rep = "<html>"
    rep += "<meta name='viewport' content='width=device-width'>"
    rep += "<body>"
    rep += "<h1>Boxes In, Boxes Out World Championship</h1>"

    rep += "<table>"
    rep += "<tr>"
    rep += "<td>"
    leagueNFCEast = League(league_id=653771400, year=year)
    teamEast = leagueNFCEast.teams[2]
    lineupEast = [3046779, 4047365, 4360516, 4258173, 4430878, 3046439, 4567048, 4432577, -16034]
    rep += printTeam(teamEast, lineupEast, week)
    rep += "</td>"
    rep += "</tr>"

    rep += "<tr>"
    rep += "<td>"
    leagueAFCWest = League(league_id=1020397, year=year)
    teamWest = leagueAFCWest.teams[2]
    lineupWest = [3046779, 4239996, 4596448, 4426515, 4361370, 4361307, 4567048, 4038941, -16007]
    rep += printTeam(teamWest, lineupWest, week)
    rep += "</td>"
    rep += "</tr>"

    rep += "<tr>"
    rep += "<td>"
    leagueAFCSouth = League(league_id=517497302, year=year)
    teamSouth = leagueAFCSouth.teams[7]
    lineupSouth = [2578570, 3043078, 4379399, 4430878, 3886598, 3929645, 4568490, 4361741, -16021]
    rep += printTeam(teamSouth, lineupSouth, week)
    rep += "</td>"
    rep += "</tr>"

    rep += "<tr>"
    rep += "<td>"
    leagueNFCNorth = League(league_id=1953587261, year=year)
    teamNorth = leagueNFCNorth.teams[0]
    lineupNorth = [4431452, 4596448, 4038815, 4430878, 3915416, 4432665, 3886598, 4431611, -16007]
    rep += printTeam(teamNorth, lineupNorth, week)
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
    leagueNFCEast = League(league_id=653771400, year=year)
    leagueAFCWest = League(league_id=1020397, year=year)
    leagueAFCSouth = League(league_id=517497302, year=year)
    leagueNFCNorth = League(league_id=1953587261, year=year)

    week = leagueNFCEast.current_week

    allBoxScores = []

    scoresNFCEast = []
    scoresAFCWest = []
    scoresAFCSouth = []
    scoresNFCNorth = []

    projScoresNFCEast = []
    projScoresAFCWest = []
    projScoresAFCSouth = []
    projScoresNFCNorth = []

    for boxScore in leagueNFCEast.box_scores(week=week):
        allBoxScores.append(boxScore)

        scoresNFCEast.append(boxScore.home_score)
        scoresNFCEast.append(boxScore.away_score)

        projScoresNFCEast.append(boxScore.home_projected)
        projScoresNFCEast.append(boxScore.away_projected)

    for boxScore in leagueAFCWest.box_scores(week=week):
        allBoxScores.append(boxScore)

        scoresAFCWest.append(boxScore.home_score)
        scoresAFCWest.append(boxScore.away_score)

        projScoresAFCWest.append(boxScore.home_projected)
        projScoresAFCWest.append(boxScore.away_projected)

    for boxScore in leagueAFCSouth.box_scores(week=week):
        allBoxScores.append(boxScore)

        scoresAFCSouth.append(boxScore.home_score)
        scoresAFCSouth.append(boxScore.away_score)

        projScoresAFCSouth.append(boxScore.home_projected)
        projScoresAFCSouth.append(boxScore.away_projected)

    for boxScore in leagueNFCNorth.box_scores(week=week):
        allBoxScores.append(boxScore)

        scoresNFCNorth.append(boxScore.home_score)
        scoresNFCNorth.append(boxScore.away_score)

        projScoresNFCNorth.append(boxScore.home_projected)
        projScoresNFCNorth.append(boxScore.away_projected)

    scoresNFCEast.sort(reverse=True)
    scoresAFCWest.sort(reverse=True)
    scoresAFCSouth.sort(reverse=True)
    scoresNFCNorth.sort(reverse=True)

    projScoresNFCEast.sort(reverse=True)
    projScoresAFCWest.sort(reverse=True)
    projScoresAFCSouth.sort(reverse=True)
    projScoresNFCNorth.sort(reverse=True)

    rep = "<html>"
    rep += "<meta name='viewport' content='width=device-width'>"
    rep += "<body>"
    rep += "<h1>Boxes In, Boxes Out<br/>Scoreboard</h1>"

    rep += "<a href=\"standings\">Standings</a><br/><br/>"

    i = 0
    for boxScore in allBoxScores:
        cls = "NFCEast"
        leagueId = "653771400"
        homeRank = -1
        awayRank = -1
        homeProjectedRank = -1
        awayProjectedRank = -1
        if i < 6:
            homeRank = scoresNFCEast.index(boxScore.home_score) + 1
            awayRank = scoresNFCEast.index(boxScore.away_score) + 1

            homeProjectedRank = projScoresNFCEast.index(boxScore.home_projected) + 1
            awayProjectedRank = projScoresNFCEast.index(boxScore.away_projected) + 1
        if i>=6 and i<12:
            cls = "AFCWest"
            leagueId = "1020397"

            homeRank = scoresAFCWest.index(boxScore.home_score) + 1
            awayRank = scoresAFCWest.index(boxScore.away_score) + 1

            homeProjectedRank = projScoresAFCWest.index(boxScore.home_projected) + 1
            awayProjectedRank = projScoresAFCWest.index(boxScore.away_projected) + 1
        elif i>=12 and i<18:
            cls = "AFCSouth"
            leagueId = "517497302"

            homeRank = scoresAFCSouth.index(boxScore.home_score) + 1
            awayRank = scoresAFCSouth.index(boxScore.away_score) + 1

            homeProjectedRank = projScoresAFCSouth.index(boxScore.home_projected) + 1
            awayProjectedRank = projScoresAFCSouth.index(boxScore.away_projected) + 1
        elif i>=18:
            cls = "NFCNorth"
            leagueId = "1953587261"

            homeRank = scoresNFCNorth.index(boxScore.home_score) + 1
            awayRank = scoresNFCNorth.index(boxScore.away_score) + 1

            homeProjectedRank = projScoresNFCNorth.index(boxScore.home_projected) + 1
            awayProjectedRank = projScoresNFCNorth.index(boxScore.away_projected) + 1

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
    rep += ".NFCEast"
    rep += "{"
    rep += "background-color: ef476f;"
    rep += "}"
    rep += ".AFCWest"
    rep += "{"
    rep += "background-color: ffd166"
    rep += "}"
    rep += ".AFCSouth"
    rep += "{"
    rep += "background-color: 06d6a0"
    rep += "}"
    rep += ".NFCNorth"
    rep += "{"
    rep += "background-color: 118ab2"
    rep += "}"
    rep += "</style>"
    rep += "</html>"

    return rep

def sortPoints(team: Team):
    return -1 * team.points_for

def sortWins(team: Team):
    return -1 * team.wins

def sortPlayoff(team: Team):
    return -1 * team.playoff_pct

@scoreboard.route('/standings', methods=['GET'])
def standings():
    leagueNFCEast = League(league_id=653771400, year=year)
    leagueAFCWest = League(league_id=1020397, year=year)
    leagueAFCSouth = League(league_id=517497302, year=year)
    leagueNFCNorth = League(league_id=1953587261, year=year)

    standingsNFCEast = leagueNFCEast.standings()
    standingsAFCWest = leagueAFCWest.standings()
    standingsAFCSouth = leagueAFCSouth.standings()
    standingsNFCNorth = leagueNFCNorth.standings()

    allTeams = leagueNFCEast.teams.copy()
    allTeams = allTeams + leagueAFCWest.teams
    allTeams = allTeams + leagueAFCSouth.teams
    allTeams = allTeams + leagueNFCNorth.teams

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
        if team in leagueNFCEast.teams:
            cls = "NFCEast"
            leagueId = "653771400"
            placeInLeague = standingsNFCEast.index(team) + 1
        if team in leagueAFCWest.teams:
            cls = "AFCWest"
            leagueId = "1020397"
            placeInLeague = standingsAFCWest.index(team) + 1
        elif team in leagueAFCSouth.teams:
            cls = "AFCSouth"
            leagueId = "517497302"
            placeInLeague = standingsAFCSouth.index(team) + 1
        elif team in leagueNFCNorth.teams:
            cls = "NFCNorth"
            leagueId = "1953587261"
            placeInLeague = standingsNFCNorth.index(team) + 1

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
    rep += ".NFCEast"
    rep += "{"
    rep += "background-color: ef476f;"
    rep += "}"
    rep += ".AFCWest"
    rep += "{"
    rep += "background-color: ffd166"
    rep += "}"
    rep += ".AFCSouth"
    rep += "{"
    rep += "background-color: 06d6a0"
    rep += "}"
    rep += ".NFCNorth"
    rep += "{"
    rep += "background-color: 118ab2"
    rep += "}"
    rep += "</style>"
    rep += "</html>"

    return rep

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    scoreboard.run(threaded=True, port=5000)





