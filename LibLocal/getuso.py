import psutil
from LibLocal import config

def getCpu():
    cpu_percent = psutil.cpu_percent(interval=1)
    return cpu_percent

def getRam():
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    return ram_percent

def getDisco():
    disk = psutil.disk_usage(config.configDB['disco'])
    disk_percent = disk.percent
    return disk_percent