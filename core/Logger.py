import os

LOGFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/suspicious_domains.log")

class Logger:
    def __init__(self, print_logs: bool = False):
        self.print_logs = print_logs

    def alert(self, msg):
        #msg = f"[{level.upper()}] {','.join([f'{d[0]}({d[1]})' for d in domains])} ({issuer})"
        with open(LOGFILE, "a") as f:
            f.write(msg + "\n")
        if self.print_logs:
            print(msg)
