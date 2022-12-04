import psutil
from datetime import datetime
from pathlib import Path
import sched, time
timer=3599
my_file = Path("usage_log.csv")
if my_file.is_file():
    # file exists
    print("File exists")
else:
    with open('usage_log.csv', 'w') as f:
        f.writelines('Time,Cpu_Usage,Used_memory,Total_memory(GB)')



s = sched.scheduler(time.time, time.sleep)
def log_save(sc): 
    print("Saving....")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    memory=psutil.virtual_memory()
    #print(memory)
    memoryp=memory.percent
    memory_total=round((memory.total)/(1024*1024*1024),2)
    cpu_usage=psutil.cpu_percent(interval=1, percpu=True)
    avg_cpu_usage=round((sum(cpu_usage)/len(cpu_usage)),2)
    #print('CPU Usage',cpu_usage)
    #print('Average CPU Usage',avg_cpu_usage)
    print('\n'+str(time)+','+str(avg_cpu_usage)+','+str(memoryp)+','+str(memory_total))
    with open('usage_log.csv', 'a') as f:
        f.writelines('\n'+str(time)+','+str(avg_cpu_usage)+','+str(memoryp)+','+str(memory_total))
    # do your stuff
    sc.enter(timer, 1, log_save, (sc,))

s.enter(1, 1, log_save, (s,))
s.run()