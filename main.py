import os
from dotenv import load_dotenv
import pymysql

# Load environment variables from .env file
load_dotenv()

config = {
  'host': os.getenv('DB_HOST'),
  'user': os.getenv('DB_USER'),
  'password': os.getenv('DB_PASSWORD'),
  'database': os.getenv('DB_NAME'),
  'cursorclass': pymysql.cursors.DictCursor
}

def connect_db():
  try:
    # Establish connection
    connection = pymysql.connect(**config)
    print("Successfully connected to the shop_db!")

    with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM customers;")

      results = cursor.fetchall()
      print("Customers in the database:")
      for result in results:
        print(result['name'])

    connection.close()

  except pymysql.MySQLError as e:
    print(f"Connection failed: {e}")

if __name__ == "__main__":
  connect_db()