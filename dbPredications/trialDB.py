import psycopg2

class DatabaseConnection:
	def __init__(self):
		try:
			self.connection = psycopg2.connect(
				"dbname='super_awesome_application' user='nschumacher' host='localhost' password='12' port='5432'")
			self.connection.autocommit = True
			self.cursor = self.connection.cursor()
		except:
			print("Did not connect to database")


	def create_table(self):
		create_table_command = "CREATE TABLE pet(id serial PRIMARY KEY, name varchar(100), age integer NOT NULL)"
		self.cursor.execute(create_table_command)

	def insert_new_record(self):
		new_record = ("misa meo3", "88")
		inset_command = "INSERT INTO pet(name, age) VALUES('" + new_record[0] + "','" + new_record[1] + "')"
		print(inset_command)
		self.cursor.execute(inset_command)

	def query_all(self):

		self.cursor.execute("SELECT * FROM pet")
		cats = self.cursor.fetchall()

		# Cycling through rows in cats table
		for cat in cats:

			# Converting cat tuple into array
			catArray = []
			for item in cat:
				catArray.append(item)
			print("each pet :", cat)
			print("each pet :", catArray)

	def update_record(self):
		# Changes any age set that is 88 to 10
		update_command = "UPDATE pet SET age=10 WHERE age=88"
		self.cursor.execute(update_command)

	def drop_table(self):
		drop_table_command = "DROP TABLE pet"
		self.cursor.execute(drop_table_command)

if __name__ == '__main__':
	database_connection = DatabaseConnection()
	#database_connection.create_table()
	#database_connection.insert_new_record()
	database_connection.query_all()
	database_connection.update_record()
	database_connection.query_all()
	#database_connection.drop_table()



