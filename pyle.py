#!/usr/bin/env python

"""
Pyle is an opinionated wrapper around pyvenv and pip, inspired by npm.

Programs run through pyle automatically use local venv based on the
configuration in a 'venvrc.json' config file.

Example use cases:

    # Run unittests
    pyle py -m unittest discover

    # Install simplejson, and save to requirements
    pyle install --save simplejson

    # Run the interactive interpeter, creating a venv if needed
    pyle -c py

    # Run pylint against a specific file in a subdirectory
    pyle -p pylint mymodule.py

    # Run a local script, creating a venv if necessary
    pyle -c ./myscript.py
"""

import argparse
import json
import os
import os.path
import subprocess
import sys
import venv

DESCRIPTION = __doc__


# The name of the expected configuration file.  It may be any python script and
# should set variables as in CONFIG_DEFAULTS
CONFIG_FILE_NAME = 'venvrc.json'

# Default configuration values
CONFIG_DEFAULTS = {
    'venv_root': '.venv',
    'requirements': [],
    'requirements_file': '',
}


class Pyle:

    def __init__(self):
        # Parse arguments from the command line
        self.args = self.parse_argv(sys.argv[1:])

        # Path to the config file
        self.config_path = self.find_config(os.getcwd())

        # Set the actual configuration
        if self.config_path:
            self.config = self.load_config()
        elif self.args.create:
            self.config_path = os.getcwd()
            self.config = CONFIG_DEFAULTS
            self.save_config()
        else:
            print('Config file not found')
            exit(1)

        # Path to the venv
        self.venv_path = os.path.join(self.config_path,
                                      self.config['venv_root'])

        # Run the program
        self.call_args(self.args.args)

    def parse_argv(self, argv):
        options = argparse.ArgumentParser(
            description=DESCRIPTION,
        )
        options.add_argument(
            '-p', '--search-parents',
            action='store_true',
            help='Traverse up the directory tree to find a venv'
        )
        options.add_argument(
            '-c', '--create',
            action='store_true',
            help='Create a venv configuration in the local directory with ' +
                 'default configuration if none is found'
        )
        options.add_argument('args', nargs=argparse.REMAINDER)
        return options.parse_args(argv)

    def find_config(self, cwd):
        """
        Find the config file and return its path.

        If `search_parents` is True, and the current directory does not contain
        a config file, the directory tree will be traversed upwards until a
        suitable config file is found.  None is returned if no config is found.
        """
        while os.path.exists(cwd):
            if os.path.exists(os.path.join(cwd, CONFIG_FILE_NAME)):
                return cwd
            elif not self.args.search_parents:
                return
            else:
                cwd = os.path.normpath(os.path.join(cwd, '..'))

    def load_config(self):
        """
        Find a configuration and load it.
        """
        path = os.path.join(self.config_path, CONFIG_FILE_NAME)
        config_set = {}
        with open(path, 'r') as cf:
            config_set = json.load(cf)
        config = CONFIG_DEFAULTS.copy()
        for key in config:
            if key in config_set:
                config[key] = config_set[key]
        return config

    def save_config(self):
        with open(os.path.join(self.config_path, CONFIG_FILE_NAME), 'w') as cf:
            json.dump(self.config, cf, indent=2,
                      separators=(', ', ': '), sort_keys=True)

    def get_requirements(self):
        """
        Return a list of requirements by consolidating REQUIREMENTS and
        REQUIREMENTS_FILE.
        """
        requirements = []
        if self.config['requirements_file']:
            req_path = os.path.join(self.config_path,
                                    self.config['requirements_file'])
            if os.path.exists(req_path):
                with open(req_path, 'r') as rh:
                    for line in rh.read():
                        requirements.append(line)
        for line in self.config['requirements']:
            requirements.append(line)
        return requirements

    def ensure_venv(self):
        """
        Find the local venv.

        If it does not exist, create it and install requirements.
        """
        if not os.path.exists(self.venv_path):
            os.mkdir(self.venv_path)
            venv.create(self.venv_path, with_pip=True)
            self.install_requirements()

    def install_requirements(self):
        """
        Install all requirements.
        """
        requirements = self.get_requirements()
        if requirements:
            self.run('pip', 'install', *requirements)

    def run(self, prog, *args):
        prog = os.path.join(self.venv_path, 'bin', prog)
        subprocess.call([prog] + list(args))

    def call_args(self, args):
        """
        Run the program described by args in the context of the virtual
        environment at venv_path
        """
        if args[0] in ['install', 'uninstall']:
            prog = 'pip'
            if '--save' in args:
                args.remove('--save')
                req = self.config.setdefault('requirements', [])
                for arg in args[1:]:
                    if not arg.startswith('-'):
                        if args[0] == 'install':
                            req.append(arg)
                        elif arg in req:
                            req.remove(arg)
                self.save_config()
            elif len(args) == 0:
                # Install all requirements
                self.install_requirements()
        elif args[0] == 'py':
            prog = 'python'
            args = args[1:]
        elif args[0].startswith('.'):
            prog = 'python'
        else:
            prog = args[0]
            args = args[1:]
        self.run(prog, *args)


if __name__ == '__main__':
    Pyle()
