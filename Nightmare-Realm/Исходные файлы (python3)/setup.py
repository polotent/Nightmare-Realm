import cx_Freeze, os

exe = [cx_Freeze.Executable("realm.py", base = "Win32GUI")]

os.environ['TCL_LIBRARY'] = r'C:\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Python36\tcl\tk8.6'

cx_Freeze.setup(
    name = "Nightmare Realm",
    options = {"build_exe" : {"packages":["pygame"],
                              "include_files":["images/"]}

    },
    executables = exe
)
