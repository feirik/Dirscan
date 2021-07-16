### Brief
Simple Python3 web directory scanner. Outputs found web site directories to file and console. Uses an OWASP directory list for scanning. The scripts are based on an [older python project](https://github.com/NoobieDog/Dir-Xcan).


#### Usage: python3 dirscan.py [-d, -n, -o] `<IP or domain name for target, http or https included>`

### Command line options
#### -d --directory `<directoryPath>` (optional)
Set path for the directory file you want to use. Default is directorylist.txt in the location of the script.

#### -n --threadnumber `<numberOfThreads>` (optional)
Sets number of threads for script to use. Default is set to 5.

#### -o --outfile `<outfilePath>` (optional)
Set path for where you want the output file to be stored. Default is dirscan_result.txt at the location of the script.

