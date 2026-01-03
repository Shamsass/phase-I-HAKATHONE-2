import unittest
from unittest.mock import patch
from main import main

class TestMain(unittest.TestCase):
    @patch("main.CLI")
    @patch("main.TaskManager")
    def test_main(self, mock_task_manager, mock_cli):
        """Test that the main function instantiates TaskManager and CLI and calls run."""
        main()
        mock_task_manager.assert_called_once()
        mock_cli.assert_called_once_with(mock_task_manager.return_value)
        mock_cli.return_value.run.assert_called_once()

if __name__ == "__main__":
    unittest.main()
