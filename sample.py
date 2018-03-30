import pymysql

db = pymysql.connect("localhost", 'root', 'mars', 'test1')
cursor = db.cursor()
cursor.execute("select car_no from car where available='no';")
data = list(cursor.fetchall())
numbers = [x[0] for x in data]
print(data)
print(numbers)
db.close()




