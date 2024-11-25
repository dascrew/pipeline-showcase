import unittest
from unittest.mock import patch, mock_open
import os
from src.utils import local_db_config

class TestDBConfig(unittest.TestCase):

    @patch.dict(os.environ, {
        'DB_HOST': 'localhost',
        'DB_PORT': '5432',
        'DB_NAME': 'testdb',
        'DB_USER': 'testuser',
        'DB_PASSWORD': 'testpass'
    })
    @patch('builtins.open', new_callable=mock_open, read_data='')
    @patch('src.utils.load_dotenv', side_effect=lambda *args, **kwargs: None)
    def test_load_env_variables(self, mock_load_dotenv, mock_file):
        config = local_db_config('.env.test')
        expected_config = {
            'host': 'localhost',
            'port': '5432',
            'dbname': 'testdb',
            'user': 'testuser',
            'password': 'testpass'
        }
        self.assertEqual(config, expected_config)

    @patch.dict(os.environ, {}, clear=True)
    @patch('builtins.open', new_callable=mock_open, read_data='')
    @patch('src.utils.load_dotenv', side_effect=lambda *args, **kwargs: None)
    def test_missing_env_variables(self, mock_load_dotenv, mock_file):
        config = local_db_config('.env.test')
        expected_config = {
            'host': None,
            'port': None,
            'dbname': None,
            'user': None,
            'password': None
        }
        self.assertEqual(config, expected_config)

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('src.utils.load_dotenv', side_effect=lambda *args, **kwargs: None)
    def test_file_not_found(self, mock_load_dotenv, mock_file):
        with patch.dict(os.environ, {}, clear=True):
            config = local_db_config('.env.test')
            expected_config = {
                'host': None,
                'port': None,
                'dbname': None,
                'user': None,
                'password': None
            }
            self.assertEqual(config, expected_config)

if __name__ == '__main__':
    unittest.main()