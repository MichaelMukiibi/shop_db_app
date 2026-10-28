import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import pymysql

# Load environment configuration
load_dotenv()

app = Flask(__name__)

def get_db_connection():
    """Helper function to create a database connection."""
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/orders', methods=['GET'])
def view_orders():
    # Read the status parameter from the URL (e.g. /orders?status=Pending)
    selected_status = request.args.get('status', 'ALL')

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            if selected_status and selected_status != 'ALL':
                # Parameterized query filtering by specific status
                sql = """
                    SELECT o.order_id, c.name AS customer_name, o.order_date, o.total_amount, o.status
                    FROM orders o
                    INNER JOIN customers c ON o.customer_id = c.customer_id
                    WHERE o.status = %s
                    ORDER BY o.order_id ASC;
                """
                cursor.execute(sql, (selected_status,))
            else:
                # Query all orders when 'ALL' is selected or page first loads
                sql = """
                    SELECT o.order_id, c.name AS customer_name, o.order_date, o.total_amount, o.status
                    FROM orders o
                    INNER JOIN customers c ON o.customer_id = c.customer_id
                    ORDER BY o.order_id ASC;
                """
                cursor.execute(sql)

            orders_data = cursor.fetchall()
    finally:
        connection.close()

    # Render template with database results
    return render_template('orders.html', orders=orders_data, selected_status=selected_status)

if __name__ == '__main__':
    app.run(debug=True)