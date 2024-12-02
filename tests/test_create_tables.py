import pytest
import psycopg
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

# Test for reviews table
def test_reviews_table(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='reviews';")
        columns = cursor.fetchall()
    expected_columns = {'id', 'user_id', 'product_id', 'rating', 'comment'}
    actual_columns = {column[0] for column in columns}
    assert expected_columns.issubset(actual_columns), f"Expected columns {expected_columns} but got {actual_columns}"

# Test for user count
def test_user_count(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
    assert user_count == 3, f"Expected 3 users, found {user_count}"

# Test for product count
def test_product_count(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
    assert product_count == 5, f"Expected 5 products, found {product_count}"

# Test for order count
def test_order_count(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM orders")
        order_count = cursor.fetchone()[0]
    assert order_count == 3, f"Expected 3 orders, found {order_count}"

# Test for items count
def test_order_items_count(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM order_items")
        order_items_count = cursor.fetchone()[0]
    assert order_items_count == 5, f"Expected 5 order items, found {order_items_count}"

# Test for review count
def test_review_count(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM reviews")
        review_count = cursor.fetchone()[0]
    assert review_count == 5, f"Expected 5 reviews, found {review_count}"

# Test for alices order
def test_alice_order(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("""
            SELECT oi.product_id, oi.quantity
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            WHERE o.user_id = 1
        """)
        alice_order = cursor.fetchall()
    expected_items = [(1, 1), (2, 2)]
    assert alice_order == expected_items, f"Expected {expected_items}, found {alice_order}"

# Test for charlies reviews
def test_charlie_reviews(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.product_id, r.rating, r.comment
            FROM reviews r
            WHERE r.user_id = 3
        """)
        charlie_reviews = cursor.fetchall()
        expected_reviews = [
        (4, 5, 'Love the monitor! Crystal clear.'),
        (5, 4, 'Headphones are solid.')
        ]
        assert charlie_reviews == expected_reviews, f"Expected {expected_reviews}, found {charlie_reviews}"

