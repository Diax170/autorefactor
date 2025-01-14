from tkinter import messagebox, filedialog, simpledialog
import sys


__title__ = 'Macro creator'
__version__ = 'alpha v1.0.2'
__author__ = 'Diax170'


def press_to_quit():
    messagebox.showinfo(__title__, 'Press OK to exit')
    sys.exit()


if not messagebox.askyesno(__title__, f'Welcome to {__title__} for autorefactor version {__version__} by {__author__}\n'
                                      'Please note that this program creates macros which are dedicated for Windows.\n'
                                      'If you run them on other operating systems, they might not work.\n'
                                      'Do you want to continue?'):  press_to_quit()

def get_step_msg(): return f'Step {step}/8'

step = 1
if not messagebox.askokcancel(get_step_msg(), 'In the next window, please select autorefactor script or executable file.\n'
                                              'Warning: if you later rename, move or delete that file, the macro will stop working'):
    press_to_quit()
program_dir = filedialog.askopenfilename(
    title=f'{get_step_msg()} Target the autorefactor script/executable file',
    defaultextension='.exe',
    filetypes=[
        ('Python scripts and executable files', '*.py *.pyw *.exe'),
        ('All files', '*.*'),
    ]
)
if not program_dir:  # If cancelled
    press_to_quit()

step = 2
match messagebox.askyesnocancel(get_step_msg(), 'Would you like for the macro to run with admin privileges? (not recommended)'):
    case True:
        run_as_admin = True
    case False:
        run_as_admin = False
    case None:
        press_to_quit()

step = 3
start_dir = simpledialog.askstring(get_step_msg(), 'Enter start directory:                    ')
if start_dir is None:
    press_to_quit()
else:
    start_dir = start_dir.strip('"')

step = 4
end_dir = simpledialog.askstring(get_step_msg(), 'Enter end directory:                        ')
if end_dir is None:
    press_to_quit()
else:
    end_dir = end_dir.strip('"')

step = 5
match messagebox.askyesnocancel(get_step_msg(), 'Would you like to save logs to the same location where the script/executable is? (.\\)\n'
                                                'Click No to choose another location or disable logs'):
    case True:
        logs_path = '.\\'
    case False:
        if messagebox.askokcancel(get_step_msg(), 'In the next window, please specify logs path (or click Cancel to disable logs)'):
            logs_path = filedialog.askdirectory()
            if not logs_path:  # If cancelled
                logs_path = None
        else:
            logs_path = None
    case None:
        press_to_quit()

step = 6
show_successes = messagebox.askyesnocancel(get_step_msg(), 'Would you like to display success messages?')
if show_successes is None:
    press_to_quit()

step = 7
hide_errors = messagebox.askyesnocancel(get_step_msg(), 'Would you like to hide error messages?')
if hide_errors is None:
    press_to_quit()

step = 8
if not messagebox.askokcancel(get_step_msg(), 'Last step\n'
                                              'In the next window, please specify directory and name of the macro'):
    press_to_quit()
macro_dir = filedialog.asksaveasfilename(
    title=f'{get_step_msg()} Save as',
    defaultextension='.bat',
    filetypes=[
        ('Batch files', '*.bat'),
        ('All files', '*.*')
    ]
)
if not macro_dir:  # If cancelled
    press_to_quit()


# Create the macro (batch) file
try:
    # Form the command
    command = f'start "autorefactor" '
    if program_dir.endswith('.py'):  command += 'python '
    elif program_dir.endswith('.pyw'):  command += 'pythonw '
    command += f'"{program_dir.replace('/', '\\')}" '
    command += f'--start-dir "{start_dir.replace('/', '\\')}" '
    command += f'--end-dir "{end_dir.replace('/', '\\')}" '
    if logs_path != '.\\':
        if logs_path is None:  command += '--no-logs '
        else:  command += f'--logs-path "{logs_path}" '
    if show_successes:  command += '--show-successes '
    if hide_errors:  command += '--hide-errors'
    command = command.rstrip()

    # Save the command to a batch file
    with open(macro_dir, 'w') as file:
        file.write('@echo off\n')
        if run_as_admin:
            file.write('net session >nul 2>&1\n')
            file.write('if %errorlevel% neq 0 (\n')
            file.write('echo This macro requires administrative privileges.\n')
            file.write('echo Restarting with elevated permissions...\n')
            file.write('timeout /t 1 /nobreak >nul\n')
            file.write('powershell -Command "Start-Process \'%~f0\' -Verb runAs"\n')
            file.write('exit /b\n')
            file.write(')\n')
        file.write(command + '\n')

    # Display a success message and warn user to add Python to Path (if required)
    is_script = program_dir.endswith('.py') or program_dir.endswith('.pyw')
    messagebox.showinfo('Success', f'The macro has been successfully saved as {macro_dir}{'' if is_script else '\nPress OK to exit'}')
    if is_script:
        messagebox.showwarning('Warning', 'Before you run this macro, ensure that python.exe and pythonw.exe are added to system Path or the macro won\'t work!\nPress OK to exit')
except Exception as e:
    messagebox.showerror('Unable to save the macro', str(e) + '\nPress OK to exit')
