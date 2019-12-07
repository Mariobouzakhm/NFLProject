import openpyxl as xl
import sqlite3

conn = sqlite3.connect('players.db')
cur = conn.cursor()

names = ['data-1.xlsx','data-2.xlsx','data-3.xlsx','data-4.xlsx','data-5.xlsx','data-6.xlsx','data-7.xlsx','data-8.xlsx','data-9.xlsx']

dic = dict()

for fname in names:
    print('Working with '+fname)
    workbook = xl.load_workbook(fname)
    sheet = workbook['data']

    for i in range(2, sheet.max_row + 1):
        play_type = sheet['Z'+str(i)].value
        if play_type == 'pass':
            id = sheet['FF'+str(i)].value
            name = sheet['FG'+str(i)].value
            if id in dic:
                continue
            else:
                dic[id] = name
    for key in dic:
        cur.execute('INSERT OR IGNORE INTO Player(player_id, name, pass_yrds, pass_completed, pass_intercepted, pass_attempted, pass_tds) VALUES(?,?, ?, ?, ?, ?, ?)', (key, dic[key],0,0,0,0,0))
conn.commit()
