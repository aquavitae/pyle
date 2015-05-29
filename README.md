# pyle

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
    
# Commandline

    pyle [-h|--help] [-p|--search-parents] [-c|--create] <commands>
    
    optional arguments:
      -h, --help                Show this help message and exit
      -p, --search-parents      Traverse up the directory tree to find a venvrc.json
      -c, --create              Create a venv configuration in the local directory
                                with default configuration if none is found

    <commands> conform to the following pattern:
      py <args>                 
          Run python with <args>
        
      install|uninstall [--save] <args>   
          Run `pip [un]install <args>'.  If `--save' is used, then configuration file
          is updated to reflect the changes.
          
      <script> <args>
          Run an installed script with args
          
      ./<local-script> <args>
          Run a local python script with args.
  
#Configuration file

A configuration file named `venvrc.json` is expected.  This may contain the following structure:

    {
      venv_dir: 'relative/path/to/venv',
      requirements: [
        'list_of_requirements',
        'as_used_in_requirements.txt'
      ],
      requirements_file: 'requirements.txt
    }
    
