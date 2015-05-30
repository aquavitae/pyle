from unittest import TestCase
from unittest.mock import Mock, patch

import tempfile
import os.path

from pyle import Pyle


class TestCase(TestCase):

    def setUp(self):
        self.mself = Mock()


class TestFindConfig(TestCase):

    def test_local_config_file(self):
        self.mself.args.search_parents = False
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, 'venvrc.json'), 'w') as fh:
                fh.write('pass')
            result = Pyle.find_config(self.mself, tmp)
            self.assertEqual(result, tmp)


class TestParseArgv(TestCase):

    def test_all_long_args(self):
        argv = ['--create', '--search-parents', 'python']
        args = Pyle.parse_argv(self.mself, argv)
        self.assertTrue(args.create)
        self.assertTrue(args.search_parents)
        self.assertEqual(args.args, ['python'])

    def test_all_short_args(self):
        argv = ['-c', '-p', 'python']
        args = Pyle.parse_argv(self.mself, argv)
        self.assertTrue(args.create)
        self.assertTrue(args.search_parents)
        self.assertEqual(args.args, ['python'])


class TestEnsureVenv(TestCase):

    def test_venv_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            venv_path = os.path.join(tmp, '.venv')
            self.mself.venv_path = venv_path
            os.mkdir(venv_path)
            # Should run withing error
            Pyle.ensure_venv(self.mself)
