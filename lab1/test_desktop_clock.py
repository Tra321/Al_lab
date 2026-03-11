import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from desktop_clock import get_current_time, get_current_date, DesktopClock


class TestDesktopClock(unittest.TestCase):
    
    def test_get_current_time_format(self):
        result = get_current_time()
        self.assertRegex(result, r"^\d{2}:\d{2}:\d{2}$")
    
    def test_get_current_date_format(self):
        result = get_current_date()
        parts = result.split()
        self.assertEqual(len(parts), 2)
        self.assertRegex(parts[0], r"^\d{4}-\d{2}-\d{2}$")
    
    @patch('desktop_clock._strftime')
    def test_get_current_time_with_mock(self, mock_strftime):
        mock_strftime.return_value = "12:30:45"
        result = get_current_time()
        self.assertEqual(result, "12:30:45")
    
    @patch('desktop_clock._strftime')
    def test_get_current_date_with_mock(self, mock_strftime):
        mock_strftime.return_value = "2026-03-08 Sunday"
        result = get_current_date()
        self.assertEqual(result, "2026-03-08 Sunday")
    
    def test_desktop_clock_init(self):
        root = tk.Tk()
        root.withdraw()
        clock = DesktopClock(root)
        self.assertEqual(clock.root.title(), "Desktop Clock")
        self.assertEqual(clock.root.geometry(), "400x250")
        root.destroy()
    
    def test_desktop_clock_labels_exist(self):
        root = tk.Tk()
        root.withdraw()
        clock = DesktopClock(root)
        self.assertIsNotNone(clock.time_label)
        self.assertIsNotNone(clock.date_label)
        root.destroy()


if __name__ == '__main__':
    unittest.main()
