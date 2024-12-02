import unittest
from unittest.mock import patch, MagicMock
from src.utils import get_db_connection

class TestDatabaseConnection(unittest.TestCase):

    @patch('psycopg.connect')
    def test_successful_connection(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        db_credentials = {
            'host': 'localhost',
            'port': 5432,
            'dbname': 'testdb',
            'user': 'testuser',
            'password': 'testpass'
        }

        connection = get_db_connection(db_credentials)

        mock_connect.assert_called_with(
            host=db_credentials['host'],
            port=db_credentials['port'],
            dbname=db_credentials['dbname'],
            user=db_credentials['user'],
            password=db_credentials['password']
        )

        self.assertEqual(connection, mock_conn)

    @patch('psycopg.connect')
    def test_connection_failure(self, mock_connect):
        mock_connect.side_effect = Exception('Database not found')

        db_credentials = {
            'host': 'localhost',
            'port': 5432,
            'dbname': 'testdb',
            'user': 'testuser',
            'password': 'testpass'
        }

        with self.assertRaises(Exception) as context:
            get_db_connection(db_credentials)

        self.assertEqual(str(context.exception), 'Failed to connect: Database not found')

if __name__ == '__main__':
    unittest.main()