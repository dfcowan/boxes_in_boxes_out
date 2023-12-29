from espn_api.football import League

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
    stats = player.stats[week]

    actual = 0
    if "points" in stats.keys():
        actual = stats["points"]

    txt = "{} {} {} ({})"
    txt = txt.format(position.ljust(4), player.name, player.proTeam, player.playerId).ljust(longestNameLength)

    txt += "{:10.2f} {:10.2f}"
    print(txt.format(stats["projected_points"], actual))

def printTeam(team, lineup):
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
                printPlayer(position, player, longestNameLength)            
                stats = player.stats[week]

                totalProjected += stats["projected_points"]
                if "points" in stats.keys():
                    totalActual += stats["points"]

                printedLineup.append(player.playerId)
                break


    txt = "Total:"
    txt = txt.rjust(longestNameLength)
    txt += "{:10.2f} {:10.2f}"
    print(txt.format(totalProjected, totalActual))


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
            printPlayer(player.position, player, longestNameLength)


leagueDev = League(league_id=1020397, year=2023)
teamDrew = leagueDev.teams[3]
lineupDrew = [3117251, 15847, 4242335, 4360310, 2577327, 4036378, 2576414,4428331,-16013]
printTeam(teamDrew, lineupDrew)

print()
print()
print()

leagueAna = League(league_id=1953587261, year=2023)
teamAlex = leagueAna.teams[4]
lineupAlex = [3139477, 4697815, 4379399, 4374302, 4360438, 4361050, 2576414, 4361741, -16014]
printTeam(teamAlex, lineupAlex)

print()
print()
print()

leagueDSM = League(league_id=635993, year=2023)
teamByrd = leagueDSM.teams[3]
lineupByrd = [3916387,3068267,3054850,3116406,4241478,3123076,4259545,4432577,-16021]
printTeam(teamByrd, lineupByrd)

print()
print()
print()

leagueMis = League(league_id=517497302, year=2023)
teamJeremy = leagueMis.teams[1]
lineupJeremy = [2577417,3054850,4430737,4262921,4569618,4361307,3042519,4432577,-16021]
printTeam(teamJeremy, lineupJeremy)



