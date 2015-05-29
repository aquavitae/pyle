from unittest import TestCase
from unittest.mock import Mock, patch

import tempfile
import os.path

import pyle


class TestFindConfig(TestCase):

    def test_local_config_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, 'venvrc.py'), 'w') as fh:
                fh.write('pass')
            result = pyle.find_config(tmp, False)
            self.assertEqual(result, tmp)


class TestParseArgv(TestCase):

    def test_all_long_args(self):
        argv = ['--create', '--search-parents', 'python']
        args = pyle.parse_argv(argv)
        self.assertTrue(args.create)
        self.assertTrue(args.search_parents)
        self.assertEqual(args.args, ['python'])

    def test_all_short_args(self):
        argv = ['-c', '-p', 'python']
        args = pyle.parse_argv(argv)
        self.assertTrue(args.create)
        self.assertTrue(args.search_parents)
        self.assertEqual(args.args, ['python'])


class TestEnsureVenv(TestCase):

    def test_venv_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            venv_path = os.path.join(tmp, '.venv')
            os.mkdir(venv_path)
            result = pyle.ensure_venv(tmp, {'VENV_ROOT': '.venv'})
            self.assertEqual(result, venv_path)
