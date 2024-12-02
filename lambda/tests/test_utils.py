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
        mock_connect.side_effect = Exception("Connection failed")

        with self.assertRaises(Exception) as context:
            get_db_connection(db_credentials)

        self.assertTrue(
            "Failed to connect: Connection failed" in str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
