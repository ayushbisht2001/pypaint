import sys
import os
from cx_Freeze import setup, Executable

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

# Dependencies are automatically detected, but it might need fine tuning.
additional_modules = []

build_exe_options = {"includes": additional_modules,
                     "packages": ["tkinter","math","Image","sys","os","speech_recognition","pyttsx3","pyautogui","gtts","playsound"],
                     "excludes": [],
                     "include_files": [
                                       os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                                       os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')
                                       ]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="LetterDrawer",
      version="1.0",
      description="U hoe!",
      options={"build_exe": build_exe_options},
      executables=[Executable("hybridnotepad.py", base=base)]) #change workspace.py to your file name