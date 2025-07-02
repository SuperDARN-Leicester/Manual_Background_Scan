"""
Man_Bkgrd_Scan
~~~~~~~~~~~~~~~~~~
This script uses the USRP 'rx_samples_to_file' utility to listen on all 20 off receive channels (16 off main, 4 off interferometer) accross all 10 licenced bands.
It produces 200 binary files which are saved to the /home/radar/UOL_scripts/Manual_Background_Scan/dat_files/ directory.
NOTE: The 'rx_samples_to_file' calls are made in series and are fairly time consuming. So this script takes a while to run.

:copyright: 2020-2025 University of Leicester
"""

import subprocess

bands = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
freqs = [9090e3, 9947.5e3, 11125e3, 11575e3, 13475e3, 13885e3, 16295e3, 18041e3, 19547.5e3, 19895e3] # Centre frequency of licenced bands, Hz
rate = 301205 # sample rate (samples per second)
duration = 1 # RX duration, s (beware - this is done 200 times + some overhead for each 'rx_samples_to_file' call!)

# Generate list of N200 IP addresses
addr = []
for x in range(100, 116):
    addr.append("192.168.10.{}".format(x))

# Generate list of file names
filenames = []
for x in range (0,10):
    for y in range (0, 16):
        filenames.append("Clear_Scan_Main{}_Band{}".format(y, x))
    for y in range (0, 4):
        filenames.append("Clear_Scan_Intf{}_Band{}".format(y, x))

filename_index = 0 # Index used to to extract filename from list for each 'rx_samples_to_file' call
for x in range (0,10): # loop through each TX band
    print("================= Band {} ==========================".format(x))

    # Run scans on 16 off main array RX channels
    for y in range (0, 16):
        cmd = "rx_samples_to_file --args addr={} --subdev A:A --ref external --freq {} --rate {} --duration {} --file {}.dat".format(addr[y], freqs[x], rate, duration, filenames[filename_index])
        print(cmd)
        returned_value = subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # Run 'rx_samples_to_file' command and surpress output
        print('returned value:', returned_value) # returns the exit code in unix
        filename_index += 1

    # Run scans on 4 off interferometer RX channels
    for y in range (0, 4):
        cmd = "rx_samples_to_file --args addr={} --subdev A:B --ref external --freq {} --rate {} --duration {} --file {}.dat".format(addr[y+4], freqs[x], rate, duration, filenames[filename_index])
        print(cmd)
        returned_value = subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)  # Run 'rx_samples_to_file' command and surpress output
        print('returned value:', returned_value) # returns the exit code in unix
        filename_index += 1

    # Move files into UoL script path
    cmd = """mv -- "Clear_Scan"* /home/radar/UOL_scripts/Manual_Background_Scan/dat_files/"""
    print(cmd)
    returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
    print('returned value:', returned_value)

