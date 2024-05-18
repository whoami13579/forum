import sqlite3

con = sqlite3.connect("instance/database.db")
cur = con.cursor()

forums = [
    (1, "課業", "這是一個專門討論有關功課的地方"),
    (2, "選課", "有任何關於選課的東西都可以在這邊討論"),
    (3, "老師", "想知道哪些老師的課輕鬆好過分數又高嗎"),
    (4, "考古題", "加入這個討論區一起分享考古題吧"),
]
cur.executemany("INSERT INTO forums VALUES(?, ?, ?)", forums)
con.commit()
