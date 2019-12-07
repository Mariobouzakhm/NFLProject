import openpyxl as xl
import sqlite3

conn = sqlite3.connect('players.db')
cur = conn.cursor()

names = ['data-1.xlsx','data-2.xlsx','data-3.xlsx','data-4.xlsx','data-5.xlsx','data-6.xlsx','data-7.xlsx','data-8.xlsx','data-9.xlsx']

dicYrds = dict()
dicAttempted = dict()
dicCompleted = dict()
dicIntercepted = dict()
dicTds = dict()

for fname in names:
    print('Working with '+fname)
    workbook = xl.load_workbook(fname)
    sheet = workbook['data']

    for i in range(2, sheet.max_row + 1):
        print(i)
        play_type = sheet['Z'+str(i)].value
        if play_type == 'pass':
            id = sheet['FF'+str(i)].value
            pass_yrds = sheet['AA'+str(i)].value
            dicAttempted[id] = 1 + dicAttempted.get(id, 0)
            if pass_yrds > 0:
                dicCompleted[id] = 1 + dicCompleted.get(id, 0)
                dicYrds[id] = pass_yrds + dicYrds.get(id, 0)
            if sheet['FR'+str(i)].value != 'NA':
                dicIntercepted[id] = 1 + dicIntercepted.get(id, 0)
            if sheet['EP'+str(i)].value == 1:
                dicTds[id] = 1 + dicTds.get(id, 0)



for player_id in dicYrds:
    cur.execute('UPDATE Player SET pass_yrds = ? where player_id = ?', (dicYrds[player_id], player_id))
    cur.execute('UPDATE Player SET pass_completed = ? where player_id = ?', (dicCompleted[player_id], player_id))
    cur.execute('UPDATE Player SET pass_attempted = ? where player_id = ?', (dicAttempted[player_id], player_id))
    if player_id in dicIntercepted and dicIntercepted[player_id] > 0:
        cur.execute('UPDATE Player SET pass_intercepted = ? where player_id = ?', (dicIntercepted[player_id], player_id))
    if player_id in dicTds and dicTds[player_id] > 0:
        cur.execute('UPDATE Player SET pass_tds = ? where player_id = ?', (dicTds[player_id], player_id))
conn.commit()
