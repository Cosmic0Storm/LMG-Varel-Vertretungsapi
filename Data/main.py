#! /usr/bin/python3
import sys
import update
from Database import Database
if "-t" in sys.argv:
    i = sys.argv.index("-t")
    if sys.argv[i+1]=="heute":
        update.Update_Thread("heute").start()
    elif sys.argv[i+1]=="morgen":
        update.Update_Thread("morgen").start()
    else:
        print("Error: Wrong Argument")
elif "-DB" in sys.argv:
    i=sys.argv.index("-DB")
    if sys.argv[i+1]=="setup":
        D=Database()
        D.setup()
    else:
        print("Only setup interface is available")
else:
    print("Error: No Argument \n -t {heute:morgen}#define type of script \n -DB setup#Setup DB")

    
