import psycopg
import boto3
from botocore.exceptions import ClientError
import json
import base64

def get_db_connection(db_credentials):
    """
    Get a database connection based on the provided credentials.

    :param db_credentials: A dictionary containing the database credentials.
    :return: A database connection object.
    """
    try:
        connection = psycopg.connect(
            host=db_credentials['host'],
            port=db_credentials['port'],
            dbname=db_credentials['dbname'],
            user=db_credentials['user'],
            password=db_credentials['password']
        )
        print("Database connected.")
        return connection
    except Exception as e:
        raise Exception(f"Failed to connect: {e}")