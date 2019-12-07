import sqlite3

conn = sqlite3.connect('players.db')
cur = conn.cursor()

data = cur.execute('SELECT * From Player')
ratings = dict()
for player in data:
    id = player[0]
    name = player[1]
    yrds = player[2]
    completed = player[3]
    intercepted = player[4]
    attempted = player[5]
    tds = player[6]
    if attempted > 0:
        yrds_per_attempt = yrds/attempted
        percentage = (completed/attempted)*100
    else:
        yrds_per_attempt = 0
        percentage = 0



    rating = 20*yrds + 1500 * tds - 200*intercepted + yrds_per_attempt*500 + percentage * 500 + 50*completed
    ratings[id] = rating
for player_id in ratings:
    cur.execute('INSERT OR IGNORE INTO Rating(player_id, rating) VALUES(?,?)',(player_id, ratings[player_id]))
conn.commit()

orderedData = cur.execute('SELECT Player.name, Rating.rating FROM Player JOIN Rating ON Player.player_id = Rating.player_id ORDER BY Rating.rating DESC')
for row in orderedData:
    print(row)
