import os
from threading import Thread
import subprocess

t1 = Thread(target=subprocess.run, args=(["python", "sg-left.py"],))
t2 = Thread(target=subprocess.run, args=(["python", "sg-right.py"],))

t1.start()
t2.start()






'''
os.system('python sg-left.py && python sg-right.py')

os.system('python sg-right.py')
'''


