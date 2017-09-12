import sys
import time
import config
import server


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Please execute by run.bat')
        sys.exit()
    print()
    print("-" * 60)
    print("initializing start at ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    config.init(sys.argv[1], "base.prop")
    print("initializing end   at ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print("total history records are {}".format(len(config.history)))
    print("-" * 60)
    server.start()
    input()
