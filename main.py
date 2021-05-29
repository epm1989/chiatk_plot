import subprocess
import platform
import datetime
import re
import os
if not os.path.exists('logs'):
    os.makedirs('logs')

command = ['/usr/lib/chia-blockchain/resources/app.asar.unpacked/daemon/chia',
           'plots', 'create', '-k', '32', '-b', '4000',
           '-t', '/home/epm1989c7/Pictures/chia/temp', '-d', '/home/epm1989c7/Pictures/chia/persistent',
           '-r', '2', '-u', '128',
           '-f', '8dd0a6848abc98b91721f8dc524b4264ef57fd53d9b651106b38d2299481d7eb3568dc0c1b578b85692964973ae4aa68',
           '-p', '83c107cf162c1b22f0fcdedb998e9da81229f8ba1ad058ec3f9411e939ab90b4a24732726ec793c6a27b2598ef171976']



kwargs = {}


def is_windows():
    return platform.system() == 'Windows'


if is_windows():
    flags = 0
    flags |= 0x00000008
    kwargs = {
        'creationflags': flags,
    }

unix_time = str(round(datetime.datetime.utcnow().timestamp()))


log_file_path = './logs/temp_{{datetime}}.log'
log_file_path = re.sub('{{datetime}}', unix_time, log_file_path)
log_file = open(log_file_path, 'a')


process = subprocess.Popen(command, stdout=log_file, stderr=log_file, shell=False, **kwargs)