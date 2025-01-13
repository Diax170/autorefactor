# autorefactor
A script for automatic file movement.

# Attention
This script is version alpha, so it hasn't beem fully tested yet.\
Any bug reports would be very helpful.

# Description
This script automatically moves files from one directory or another.

When it detects that a specified file (start directory) exists, it moves it to another directory and renames it to match the name specified under end directory.

For example, if:

Start directory is ```C:\Users\User\Downloads\download.pdf```\
and end directory is ```E:\Documents\important.pdf```,\
the script will check for existence of ```download.pdf``` every second. If it exists, it will be moved to ```E:\Documents``` and renamed to ```important.pdf```.\
If ```important.pdf``` already existed before the move, it will be overwritten.

# How to run
You can either open:
- The ```autorefactor.pyw``` file if you have Python on your computer (recommended), you should have version 3.10 or newer,
- or the ```autorefactor.exe``` executable (in releases).

# Commands and macros
This program can also be used as a command. Open command prompt and open the script with ```/?``` argument for more info, e.g.
```autorefactor /?```

You can also run the macro creator (which comes along with this program), create a macro and later import your settings easily.\
Its Python script file is ```macrocreator.pyw``` (located in the branch main) and the executable is ```macrocreator.pyw``` (can be found in releases).

Note that:
- The macro creator creates ```.bat``` files which are Windows exclusive, so they proabably won't work on another systems.
- If you want to run autorefactor from a Python script in a macro, you must add ```python.exe``` and/or ```pythonw.exe``` to system Path.
