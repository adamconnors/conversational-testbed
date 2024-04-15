class DebugLog:
    def __init__(self, filename):
        self.filename = filename

    def write_log(self, log_line):
        with open(self.filename, 'a') as file:
            file.write(log_line + '\n')