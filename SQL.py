import sqlite3
import vals

def masterSQL():
    master = sqlite3.connect(vals.path + "master/master.db")
    charaQ = master.execute('SELECT "index", text FROM text_data WHERE category = 170')
    songQ = master.execute('SELECT "index", text FROM text_data WHERE category = 16')
    charaQ = list(charaQ)
    songQ = list(songQ)
    return charaQ, songQ

def func(query):
    twoStrList = []
    for i in query:
        query = list(query)
        twoStrList.append(query[i][1][0:2])
        query[i][1] = vals.path + "dat/" + query[i][1][0:2] + "/" + query[i][1]
        return query, twoStrList

def metaSQL():
    meta = sqlite3.connect(vals.path + "meta")
    soundsrcQ = meta.execute("SELECT  n ,h FROM a where n like 'sound/l/%chara%awb'")
    okesrcQ = meta.execute("SELECT  n ,h FROM a where n like 'sound/l/%oke_01.awb'")
    return func(soundsrcQ)[0], func(okesrcQ)[0], func(soundsrcQ)[1], func(okesrcQ)[1]

