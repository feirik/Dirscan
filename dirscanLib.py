import requests
import sys

NotFound = 0
NotAuthorised = 0
Found = 0
Forbidden = 0
Other = 0
CheckedLines = 0


# Check status code of a directory entry, output found and auth status code entries to stdout and file
def check_directory(directory, target, outfile, dir_len):
    # Use global variables to store and show status
    global NotFound, Found, Forbidden, Other, CheckedLines
    sys.stdout.write("%d Found, %d Forbidden, %d NotFound, %d Other, %d Percent Left\n"
                     % (Found, Forbidden, NotFound, Other, (dir_len - CheckedLines) * 100 / dir_len))
    sys.stdout.flush()

    try:
        response = requests.get(target + '/' + str(directory.rstrip()))

        status_code = response.status_code

        if status_code == 401:
            Other += 1
            CheckedLines += 1
            outfile.write("REQUIRES AUTH %s/%s" % (target, directory));
            sys.stdout.write("REQUIRES AUTH %s/%s" % (target, directory))
            sys.stdout.flush()

        elif status_code == 403:
            Forbidden = Forbidden + 1
            CheckedLines += 1
        elif status_code == 404:
            NotFound += 1
            CheckedLines += 1
        elif status_code == 200:
            Found += 1
            CheckedLines += 1
            outfile.write("FOUND %s/%s" % (target, directory))
            sys.stdout.write("FOUND %s/%s" % (target, directory))
            sys.stdout.flush()
        else:
            Other += 1
            CheckedLines += 1
    except requests.ConnectionError:
        outfile.write("Failed to connect to server.")
        outfile.close()
        print("Connection Error - Check target is correct")
        sys.exit()
