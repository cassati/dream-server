import os
import sys
import config
import server


if __name__ == "__main__":
    config_file_name = "base.config"
    if len(sys.argv) <= 1:
        work_dir = os.getcwd()
    else:
        work_dir = sys.argv[1]

    try:
        print()
        print("-" * 60)
        config.init(work_dir, config_file_name)
        print("total history records are {}".format(len(config.history)))
        host, port = config.host, config.port
        server.start(host, port)
    except Exception as e:
        print(e)

    input()
