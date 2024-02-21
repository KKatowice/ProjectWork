import mysql.connector

timeout = 10
connection = mysql.connector.connect(
    host="team2-proj-project-work.a.aivencloud.com",
    user="avnadmin",
    password="sta su trello su database creation",#FIXME
    database="defaultdb",
    port=19066,
    charset="utf8mb4",
    connect_timeout=timeout,
)

cursor = connection.cursor()
r = cursor.execute("SHOW DATABASES")
print(r)
connection.close()
