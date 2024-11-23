import pytest
import psycopg
from psycopg import sql
from dotenv import load_dotenv
import os

# Load environment variables from .env.test file
load_dotenv('.env.test')

# Database connection setup using environment variables
@pytest.fixture(scope='module')
def db_connection():
    conn = psycopg.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    yield conn
    conn.close()

# Test for users table
def test_users_table(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users';")
        columns = cursor.fetchall()
        expected_columns = {'id', 'name', 'email'}
        actual_columns = {column[0] for column in columns}
        assert expected_columns.issubset(actual_columns), f"Expected columns {expected_columns} but got {actual_columns}"

# Test for products table
def test_products_table(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='products';")
        columns = cursor.fetchall()
        expected_columns = {'id', 'name', 'price'}
        actual_columns = {column[0] for column in columns}
        assert expected_columns.issubset(actual_columns), f"Expected columns {expected_columns} but got {actual_columns}"

# Test for orders table
def test_orders_table(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='orders';")
        columns = cursor.fetchall()
        expected_columns = {'id', 'user_id', 'order_date'}
        actual_columns = {column[0] for column in columns}
        assert expected_columns.issubset(actual_columns), f"Expected columns {expected_columns} but got {actual_columns}"

# Test for order_items table
def test_order_items_table(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='order_items';")
        columns = cursor.fetchall()
        expected_columns = {'id', 'order_id', 'product_id', 'quantity'}
        actual_columns = {column[0] for column in columns}
        assert expected_columns.issubset(actual_columns), f"Expected columns {expected_columns} but got {actual_columns}"

# # Test for reviews table
# def test_reviews_table(db_connection):
#     with db_connection.cursor() as cursor:
#         cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='reviews';")
#         columns = cursor.fetchall()
#         expected_columns = {'id', 'user_id', 'product_id', 'rating', 'comment'}
#         actual_columns = {column[0] for column in columns}
#         assert expected_columns.issubset(actual_columns), f"Expected columns {expected_columns} but got {actual_columns}"
