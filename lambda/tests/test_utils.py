import unittest
from unittest.mock import patch, MagicMock
from src.utils import get_db_connection

class TestGetDbConnection(unittest.TestCase):
    @patch("psycopg.connect")
    def test_get_db_connection_success(self, mock_connect):
        db_credentials = {
            "host": "localhost",
            "port": 5432,
            "dbname": "testdb",
            "user": "testuser",
            "password": "testpass",
        }
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        connection = get_db_connection(db_credentials)

        mock_connect.assert_called_once_with(
            host="localhost",
            port=5432,
            dbname="testdb",
            user="testuser",
            password="testpass",
        )
        self.assertEqual(connection, mock_conn)

    @patch("psycopg.connect")
    def test_get_db_connection_failure(self, mock_connect):
        db_credentials = {
            "host": "localhost",
            "port": 5432,
            "dbname": "testdb",
            "user": "testuser",
            "password": "testpass",
        }
        mock_connect.side_effect = Exception("Database not found")

        with self.assertRaises(Exception) as context:
            get_db_connection(db_credentials)

        self.assertEqual(str(context.exception), 'Failed to connect: Database not found')

if __name__ == "__main__":
    unittest.main()