# Under construction
This repository is under construction.

# autorefactor
A script for automatic file movement.

# Description
This script automatically moves files from one directory or another.

When it detects that a specified file (start directory) exists, it moves it to another directory and renames it to match the name specified under end directory.

For example, if:

Start directory is ```C:\\Users\\User\\Downloads\\download.pdf```\
and end directory is ```E:\\Documents\\important.pdf```,\
the script will check for existence of ```download.pdf``` every second. If it exists, it will be moved to ```E:\\Documents``` and renamed to ```important.pdf```.\
If ```important.pdf``` already existed before the move, it will be overwritten.

# Commands and macros
This program can also be used as a command. Open command prompt and open the script with ```/?``` argument for more info, e.g.
```autorefactor /?```

You can also run the macro creator (which comes along with this program), create a macro and later import your settings easily.

Note that:
- The macro creator creates ```.bat``` files which are Windows exclusive, so they proabably won't work on another systems.
- If you want to run autorefactor from a Python script in a macro, you must add ```python.exe``` and/or ```pythonw.exe``` to system Path.
