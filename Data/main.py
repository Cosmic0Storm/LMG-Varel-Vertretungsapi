import sys
import update

if sys.argv[1]=="-D":
    if sys.argv[2]=="heute":
        update.Update_Thread("heute").start()
    elif sys.argv[3]=="morgen":
        update.Update_Thread("morgen").start()
    else:
        print("Error: Wrong Argument")
else:
    print("Error: No Argument \n -D {heute:morgen}")

    