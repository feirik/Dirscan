import requests
import sys
import threading

NotFound = 0
NotAuthorised = 0
Found = 0
Forbidden = 0
Other = 0
CheckedLines = 0


# Threading class to get work from global queue to check directories
class Dirscan(threading.Thread):
    def __init__(self, queue, target, outfile, directory_len):
        threading.Thread.__init__(self)
        self.queue = queue
        self.target = target
        self.outfile = outfile
        self.dir_len = directory_len

    def run(self):
        while True:
            try:
                # Process task
                directory = self.queue.get()
                self.check_directory(directory)
                self.queue.task_done()
            except SystemExit:
                print("Shutting down")

    # Check status code of a directory entry, output found and auth status code entries to stdout and file
    def check_directory(self, directory):
        # Use global variables to store and show status
        global NotFound, Found, Forbidden, Other, CheckedLines
        sys.stdout.write("%d Found, %d Forbidden, %d NotFound, %d Other, %d Percent Left\n"
                         % (Found, Forbidden, NotFound, Other, (self.dir_len - CheckedLines) * 100 / self.dir_len))
        sys.stdout.flush()

        try:
            response = requests.get(self.target + '/' + str(directory.rstrip()))

            status_code = response.status_code

            if status_code == 401:
                Other += 1
                CheckedLines += 1
                self.outfile.write("REQUIRES AUTH %s/%s" % (self.target, directory));
                sys.stdout.write("REQUIRES AUTH %s/%s" % (self.target, directory))
                sys.stdout.flush()

            elif status_code == 403:
                Forbidden = Forbidden + 1
                CheckedLines += 1
                self.outfile.write("FORBIDDEN %s/%s" % (self.target, directory))
                sys.stdout.write("FORBIDDEN %s/%s" % (self.target, directory))
                sys.stdout.flush()
            elif status_code == 404:
                NotFound += 1
                CheckedLines += 1
            elif status_code == 200:
                Found += 1
                CheckedLines += 1
                self.outfile.write("FOUND %s/%s" % (self.target, directory))
                sys.stdout.write("FOUND %s/%s" % (self.target, directory))
                sys.stdout.flush()
            else:
                Other += 1
                CheckedLines += 1
        except requests.ConnectionError:
            self.outfile.write("Failed to connect to server.")
            self.outfile.close()
            print("Connection Error - Check target is correct")
            sys.exit()
