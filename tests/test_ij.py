import unittest
from unittest.mock import patch, MagicMock
import datetime
import pathlib
import sys
import os
import shutil
import tempfile

# src ディレクトリをパスに追加してインポートできるようにする
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import ij

class TestIj(unittest.TestCase):
    def setUp(self):
        # テスト用の一時ディレクトリを作成
        self.test_dir = tempfile.mkdtemp()
        self.test_log_dir = pathlib.Path(self.test_dir)
        
        # ij.LOG_DIR をモック用のパスに差し替える
        self.patcher = patch('ij.LOG_DIR', self.test_log_dir)
        self.patcher.start()

    def tearDown(self):
        # パッチを解除
        self.patcher.stop()
        # 一時ディレクトリを削除
        shutil.rmtree(self.test_dir)

    def test_get_today_log_path(self):
        today = datetime.date.today()
        expected = self.test_log_dir / f"{today.isoformat()}.md"
        self.assertEqual(ij.get_today_log_path(), expected)

    def test_ensure_log_dir(self):
        # 一旦ディレクトリを削除
        os.rmdir(self.test_dir)
        self.assertFalse(self.test_log_dir.exists())
        
        ij.ensure_log_dir()
        self.assertTrue(self.test_log_dir.exists())

    def test_append_log(self):
        message = "Test log message"
        
        # 標準出力をキャプチャして余計な出力を抑制
        with patch('sys.stdout', new_callable=MagicMock):
            ij.append_log(message)
            
        log_path = ij.get_today_log_path()
        self.assertTrue(log_path.exists())
        
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn(message, content)
            # 時刻フォーマットの確認 (- HH:MM message)
            self.assertRegex(content, r'- \d{2}:\d{2} ' + message)

    @patch('ij.append_log')
    def test_main_multiple_args(self, mock_append_log):
        test_args = ['ij.py', 'Hello', 'World']
        with patch.object(sys, 'argv', test_args):
            ij.main()
            mock_append_log.assert_called_once_with('Hello World')

if __name__ == '__main__':
    unittest.main()
