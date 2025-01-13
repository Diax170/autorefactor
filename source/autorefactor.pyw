import sys

def show_cmd_help():
    print("""
Usage: autorefactor [[/? | -h | --help] | --start-dir <dir> --end-dir <dir> [--logs-dir <path> | --no-logs] [--show-successes] [--hide-errors]]

Options:
  /?, -h, --help           Show this help message.
  --start-dir <dir>        Specify the starting directory (required).
  --end-dir <dir>          Specify the ending directory (required).
  --logs-path <path>       Specify the path for logs (default is .\\).
  --no-logs                Do not generate logs (mutually exclusive with --logs-dir).
  --show-successes         Display successes.
  --hide-errors            Suppress error messages.

Notes:
  If neither --logs-dir nor --no-logs is provided, logs are saved in the current directory (.\\).
  If no options are specified, prompts the user for all necessary info.
""")
    sys.exit()

# Check for custom help
if '/?' in sys.argv or '-h' in sys.argv or '--help' in sys.argv:
    show_cmd_help()

import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from tkinter import font as tmp_font
from datetime import datetime
from time import sleep
import os
import shutil


tk.font = tmp_font
del tmp_font

__title__ = 'autorefactor'
__author__ = 'Diax170'
__version__ = 'alpha v1.0.1'


def help_():
    messagebox.showinfo(__title__, f"""
Info label
Title: {__title__}
Author: {__author__}
Version: {__version__}

This script automatically moves files from one directory to another.
When it detects that a specified file (start directory) exists, it moves it to another directory and renames it to match the name specified under end directory.

For example, if:
Start directory is C:\\Users\\User\\Downloads\\download.pdf
and end directory is E:\\Documents\\important.pdf
the script will check for existence of download.pdf every second. If it exists, it will be moved to E:\\Documents and renamed to important.pdf
If important.pdf already existed before the move, it will be overwritten.

This program can also be used as a command. Open command prompt and open the script with /? argument for more info.

You can also run the macro creator (which comes along with this program), create a macro and later import your settings easily.

If you're having trouble using this program, try running it as an administrator.
""".strip('\n'))

def press_to_quit():
    try:
        root.after_cancel(refact_id)
    except:
        pass
    messagebox.showinfo(__title__, 'Press OK to exit')
    try:
        log_info('User quit the script')
    except:
        pass
    sys.exit()

def refactor():
    if os.path.exists(start_dir):
        try:
            shutil.move(start_dir, end_dir)
            log_info('Refactored successfully')
            if successes_var.get():  # If user checked 'Show successes'
                messagebox.showinfo(__title__, 'Refactored successfully')
        except Exception as e:
            if errors_var.get():  # If user checked 'Show errors'
                messagebox.showerror(__title__, str(e))
            log_info(f'Error while refactoring: {e}')
    global refact_id
    refact_id = root.after(1000, refactor)

def pause_resume():
    if pause_btn.cget('text') == 'Pause':  # If not paused
        root.after_cancel(refact_id)
        pause_btn.configure(text='Resume')
        top_label.configure(text=top_label_pause)
    else:
        root.after(1000, refactor)
        pause_btn.configure(text='Pause')
        top_label.configure(text=top_label_def)

def btn_quit_cmd():
    press_to_quit()
    root.destroy()

def log_info(msg):
    full_msg = f'{datetime.now().ctime()}: {msg}'
    print(full_msg)

    if logs_dir:
        try:
            with open(logs_dir, 'a') as logs:
                logs.write(full_msg + '\n')
        except Exception as e:
            print(f"Couldn't log data: {e}")


# Arguments
if len(sys.argv) > 1:  # If arguments were provided
    # I admit that I can't really use argparse so this part of the script is AI-generated
    import argparse

    # Custom argument parser to override the error behavior
    class CustomArgumentParser(argparse.ArgumentParser):
        def error(self, message):
            print(f'\nError: {message}\n')
            sleep(1.5)
            show_cmd_help()

    # Initialize the argument parser
    parser = CustomArgumentParser(
        description='A script for automatic file moving with customizable logging and display options.',
        add_help=False  # Disable default help to handle custom commands
    )

    # Required arguments
    parser.add_argument('--start-dir', type=str, help='Specify the starting directory.', required=True)
    parser.add_argument('--end-dir', type=str, help='Specify the ending directory.', required=True)

    # Mutually exclusive group for logging
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument('--logs-path', type=str, help='Specify the path for logs (default is .\\).')
    log_group.add_argument('--no-logs', action='store_true', help='Disable logging.')

    # Optional flags
    parser.add_argument('--show-successes', action='store_true', help='Display successes.')
    parser.add_argument('--hide-errors', action='store_true', help='Suppress error messages.')

    # Parse the arguments
    args = parser.parse_args()

    # Default logs directory if no-logs and logs-path are not specified
    logs_path = args.logs_path if args.logs_path else (None if args.no_logs else ".\\")

    # Rest of arguments (not AI generated)
    start_dir = args.start_dir
    end_dir = args.end_dir
    successes_val = args.show_successes  # Show successes
    errors_val = not args.hide_errors  # Show errors
else:
    # Welcome user to the program
    match messagebox.askyesnocancel(__title__, f'Welcome to {__title__} by {__author__} version {__version__}. Would you like to get some help?'):
        case True:
            help_()
        case None:
            press_to_quit()

    # Prompt for some info
    start_dir = simpledialog.askstring(__title__, 'Enter start directory:                    ')
    if start_dir is None:
        press_to_quit()
    else:
        start_dir = start_dir.strip('"')

    end_dir = simpledialog.askstring(__title__, 'Enter end directory:                        ')
    if end_dir is None:
        press_to_quit()
    else:
        start_dir = start_dir.strip('"')

    successes_val = False  # Show successes
    errors_val = True  # Show errors

    if messagebox.askyesno(__title__, 'Would you like to save logs to the same location where the script/executable is? (.\\)\n'
                                      'Click No to choose another location or disable logs'):
        logs_path = '.\\'
    else:
        if messagebox.askokcancel(__title__, 'In the next window, please specify logs path (or click Cancel to disable logs)'):
            logs_path = filedialog.askdirectory()
            if not logs_path:  # If cancelled
                logs_path = None
        else:
            logs_path = None

# Set up logs
if logs_path:  # If logs path is not None and not empty ('')
    logs_dir = os.path.join(logs_path, 'log.log')
    with open(logs_dir, 'w'):
        pass  # Delete previous logs (or create a new log file)
else:
    logs_dir = None
    log_info("Warning: These logs aren't being saved to any file")

# Log some info
log_info(f'Start directory = {start_dir}')
log_info(f'End directory = {end_dir}')

end_path = os.path.dirname(end_dir)
end_name = os.path.basename(end_dir)


# Basic window configuration
root = tk.Tk()
root.title(__title__)

# Set the default font size
default_font = tk.font.nametofont('TkDefaultFont')
default_font.configure(size=13)

# Add some UI
top_label_def = 'Refactoring... Closing this window will quit the script'
top_label_pause = 'Script paused.'
top_label = tk.Label(root, text=top_label_def, anchor='w')
top_label.pack(anchor='w', padx=5, pady=(5, 3))

label = (f'Start directory: {start_dir}\n'
         f'End directory: {end_dir}')
tk.Label(root, text=label, anchor='w', justify='left').pack(anchor='w', padx=5, pady=(0, 5))

btn_frame = tk.Frame(root)

successes_var = tk.BooleanVar(value=successes_val)
tk.Checkbutton(btn_frame, text='Show successes', variable=successes_var).pack(side=tk.LEFT, padx=5)

errors_var = tk.BooleanVar(value=errors_val)
tk.Checkbutton(btn_frame, text='Show errors', variable=errors_var).pack(side=tk.LEFT, padx=(0, 10))

pause_btn = tk.Button(btn_frame, text='Pause', width=6, command=pause_resume)
pause_btn.pack(side=tk.LEFT)

tk.Button(btn_frame, text='Exit', command=btn_quit_cmd).pack(side=tk.LEFT)

btn_frame.pack(side=tk.BOTTOM, padx=5, pady=5)


refact_id = root.after(1000, refactor)  # Start refactoring
log_info('Started refactoring')
root.mainloop()
log_info('User quit the script')
