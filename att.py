import psutil

CORE_LOAD_TEMPLATE = "core {0} -> {1}%\n\t"

TEMPLATES_CPU = {
    "cpu": {
        "loads": "CPU LOAD: \n\t{}",
        "times": "TIME OF WORK -> \n\tsystem - {system}\n\tuser - {user}"
    }
}

TEMPLATES_MEM = "MEMORY STATS ->\n\ttotal memory - {total}  \n\tavailable memory - {available}"

TEMPLATES_DISK = "DISK STATS ->\n\ttotal disk memory - {total}\n\tused disk memory - {used}\n\tfree disk memory - {free}\n\tdisk usage percent - {percent}%"

TEMPLATES_NET = "NET STATS ->\n\tbytes sent - {bytes_sent}\n\tbytes received - {bytes_recv}\n\tpackets sent - {packets_sent}\n\tpackets received - {packets_recv}\n\terrors in - {errin}\n\terrors out - {errout}\n\tdropps in - {dropin}\n\tdropps out - {dropout} "

TEMPLATES_BATTERY = "BATTERY STATS ->\n\tbattery percent - {}%\n\tbattery power plugged - {}"

TEMPLATE_PROC = "\tPID:: {pid}\t Name:: {name}\t Memory percent:: {memory_percent}\t CPU percent:: {cpu_percent}\n"

def get_cpu():
    times = psutil.cpu_times(percpu=False)
    load = psutil.cpu_percent(interval=1, percpu=True)
    res_cpu = {
        "times": {"user": times.user, "system": times.system},
        "load": {"values": load}
    }
    return res_cpu

def get_mem():
    mem = psutil.virtual_memory()
    res_mem = {
        "memory":
        {
        "total": mem.total,
        "available": mem.available
        }
    }
    return res_mem

def get_disk():
    disk = psutil.disk_usage('/')
    res_disk = {
        "disk": {
            "total": disk.total, "used": disk.used,"free": disk.free,
            "percent": disk.percent
         }
    }
    return res_disk

def get_net_stats ():
    net = psutil.net_io_counters()
    res_net = {
        "net": {
             "bytes_sent": net.bytes_sent, "bytes_recv": net.bytes_recv,
             "packets_sent": net.packets_sent, "packets_recv": net.packets_recv,
             "errin": net.errin, "errout": net.errout,
             "dropin": net.dropin, "dropout": net.dropout
            }
    }
    return res_net

def get_sensors():
    batt = psutil.sensors_battery()
    return batt
    
def get_proc():
    listofproc = list()
    for proc in psutil.process_iter():
        pInfoDict = proc.as_dict(attrs=['pid', 'memory_percent', 'name', 'cpu_percent'])
        listofproc.append(pInfoDict)
    return listofproc

def show():
    cpu = get_cpu()
    template_load = ""
    for i,value in enumerate (cpu["load"]["values"]):
        template_load += CORE_LOAD_TEMPLATE.format (i,value)
    cpu_load_info = TEMPLATES_CPU["cpu"]["loads"].format(template_load)
    print (cpu_load_info)
    work_time_cpu = TEMPLATES_CPU["cpu"]["times"].format (**cpu["times"])
    print (work_time_cpu)
    print ("\n\n\t__________________________\n\n")
    mem = get_mem()
    memory_usage = TEMPLATES_MEM.format (**mem["memory"])
    print (memory_usage)
    print ("\n\n\t__________________________\n\n")
    disk = get_disk()
    disk_usage = TEMPLATES_DISK.format (**disk["disk"])
    print (disk_usage)
    print ("\n\n\t__________________________\n\n")
    net = get_net_stats()
    net_stats = TEMPLATES_NET.format(**net["net"])
    print (net_stats)
    print ("\n\n\t__________________________\n\n")
    battery = get_sensors()
    battery_cond = TEMPLATES_BATTERY.format (battery.percent, battery.power_plugged)
    print (battery_cond)
    print ("\n\n\t__________________________\n\n")
    proces = get_proc()
    proc_info = ""
    for i in proces:
        proc_info += TEMPLATE_PROC.format(**i)
    beginning_proc = "PROCESS STATS ->\n"
    proc_info = beginning_proc + proc_info
    print (proc_info)

if __name__ == "__main__":
    show()
