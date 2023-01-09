import os
from threading import Thread
import subprocess
from sgleft import iswinl
from sgright import iswinr, func2

t1 = Thread(target=subprocess.run, args=(["python", "sgleft.py"],))
t2 = Thread(target=subprocess.run, args=(["python", "sgright.py"],))


t1.start()
t2.start()
while True:
    print(iswinr())
    if iswinl():
        print('LEFT WON!')
        break
    if iswinr():
        print('RIGHT WON!')
        break





'''
os.system('python sgleft.py && python sgright.py')

os.system('python sgright.py')
'''


