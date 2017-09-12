import os
import sys
import time

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

i = 268435456/100
for x in range(int(i)):
    pass

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


if len(sys.argv) > 1:
    print(os.path.abspath(sys.argv[1]))
else:
    print('Please execute by run.bat')
    sys.exit()

input()
