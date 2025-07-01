import subprocess

bands = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
freqs = [9090e3, 9947.5e3, 11125e3, 11575e3, 13475e3, 13885e3, 16295e3, 18041e3, 19547.5e3, 19895e3]
rate = 301205
duration = 0.1

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

# Run RX scans on main array
filename_index = 0
for x in range (0,10):
    print("================= Band {} ==========================".format(x))
    for y in range (0, 16):
        cmd = "rx_samples_to_file --args addr={} --subdev A:A --ref external --freq {} --rate {} --duration {} --file {}.dat".format(addr[y], freqs[x], rate, duration, filenames[filename_index])
        print(cmd)
        returned_value = subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)  # returns the exit code in unix
        print('returned value:', returned_value)
        filename_index += 1
    # Run RX scans on interferometer array
    for y in range (0, 4):
        cmd = "rx_samples_to_file --args addr={} --subdev A:B --ref external --freq {} --rate {} --duration {} --file {}.dat".format(addr[y+4], freqs[x], rate, duration, filenames[filename_index])
        print(cmd)
        returned_value = subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)  # returns the exit code in unix
        print('returned value:', returned_value)
        filename_index += 1
        # Move files into UoL script path
    cmd = """mv -- "Clear_Scan"* /home/radar/UOL_scripts/Manual_Background_Scan/dat_files/"""
    print(cmd)
    returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
    print('returned value:', returned_value)

