import _io
import os
import json
import random
from pathlib import Path
from argparse import ArgumentParser, Namespace, SUPPRESS
from datetime import datetime
from zoneinfo import ZoneInfo
from faker import Faker


def create_logs_dir():
    os.makedirs(PATH.joinpath('logs'),exist_ok = True)

def persist_employee_data():
    with open(PATH.joinpath('employees.json'),'w') as f:
        json.dump(EMPLOYEES, f,indent = 2)

def cleanse():
    if not PATH.joinpath("logs").exists():
        print('\033[38;5;10mNo logs exist.\033[0m')
        return 
    files = PATH.joinpath('logs').iterdir()
    total_files = 0
    for file in files:
        file_path = os.path.join('logs',file)
        os.remove(file_path)
        print(f'\033[38;5;9mRemoved: {file_path}\033[0m')
        total_files += 1
    
    print(f'\033[38;5;14mCleansed logs of {total_files} file(s)\033[0m')


def log_gen(lines):
    tz = ZoneInfo('EST')
    for line in range(lines):
        dep = random.choice(list(LOG.keys()))
        level =  random.choice(["DEBUG","INFO","WARNING","ERROR","CRITICAL"])
        resource = random.choice(LOG[dep]["resources"])
        message: str = random.choice(LOG[dep]["log"][level])
        person = random.choice(EMPLOYEES[dep])["emp_id"]

        yield {
            "id": faker.uuid4(),
            "dt": datetime.now(tz = tz).strftime("%Y-%m-%d %H:%M:%S %z"),
            'level':level,
            'dep': dep,
            'ip': faker.ipv4(),
            'msg': message.format(resource = resource, name = person)
        }


parser = ArgumentParser(description = "log_genrator")
parser.add_argument('-t',"--total-lines",type = int, default = 5_000)
parser.add_argument('-p',"--per-file",type = int, default = 1_000)
parser.add_argument("-c","--cleanse",action = "store_true")
parser.add_argument('-r','--randomness', action = 'store_false')
parser.add_argument('-s','--random-seed', type = int, default = 4, help = SUPPRESS)
parser.add_argument('-e','--persist-employees', action = "store_true")

args: Namespace = parser.parse_args()





PATH = Path(__file__).parents[1].joinpath('log_gen') 
print(PATH)
MAX_LINES_PER_FILE = args.per_file
TOTAL_LOG_LINES = args.total_lines
file: _io.TextIOWrapper = None 
current_line = 0
faker: Faker = Faker()
total_files = 0

print(f'\033[38;5;10m[DEFAULTS]: [total_lines = {TOTAL_LOG_LINES}], [max_lines = {MAX_LINES_PER_FILE}], [cleanse = {"yes" if args.cleanse else "no"!r}]\033[0m')


if not  args.randomness:
    print('\033[38;5;14mNo RANDOMENESS\033[0m')
    random.seed(args.random_seed)
    Faker.seed(args.random_seed)
if args.cleanse:
    cleanse()

LOG = {
    "Network": {
        "resources": ["Router", "Switch", "Firewall", "Load Balancer"],
        "log": {
            "DEBUG": [
                "{name} traced packet flow through {resource}, noting unexpected header flags",
                "{name} toggled debug mode on {resource} for detailed heartbeat logs",
                "{name} captured a malformed ARP request from {resource}",
                "{name} ran a traceroute via {resource} to isolate a 120 ms hop delay",
                "{name} compared baseline throughput against live data on {resource}"
            ],
            "INFO": [
                "{name} successfully established BGP peering with {resource}",
                "{name} pushed a configuration snapshot to {resource}",
                "{name} verified VLAN segmentation on {resource}",
                "{name} confirmed firmware v2.3 rollout to {resource}",
                "{name} observed seamless failover on {resource} during maintenance"
            ],
            "WARNING": [
                "{name} detected 85% CPU load spike on {resource}",
                "{name} noticed sporadic packet drops on {resource}",
                "{name} flagged a mismatched MTU on {resource}",
                "{name} saw high retransmission rates via {resource}",
                "{name} recorded a transient link flapping event on {resource}"
            ],
            "ERROR": [
                "{name} failed to authenticate SSH session on {resource}",
                "{name} experienced kernel panic crash on {resource}",
                "{name} couldn’t resolve DNS lookup through {resource}",
                "{name} lost SNMP polling responses from {resource}",
                "{name} found inconsistent ACL rules on {resource}"
            ],
            "CRITICAL": [
                "{name} emergency‑rebooted {resource} after memory overflow",
                "{name} observed complete routing table corruption on {resource}",
                "{name} triggered disaster recovery via {resource} cluster",
                "{name} fail‑safe protocol activated for {resource} overheating",
                "{name} unreachable standby node detected on {resource}"
            ]
        }
    },
    "Storage": {
        "resources": ["SAN", "NAS", "Disk Array", "Tape Library"],
        "log": {
            "DEBUG": [
                "{name} logged raw I/O metrics from {resource} during stress test",
                "{name} performed block‑level checksum on {resource}",
                "{name} profiled read/write latencies on {resource}",
                "{name} captured firmware debug trace from {resource}",
                "{name} compared SMART attributes against historical baseline for {resource}"
            ],
            "INFO": [
                "{name} provisioned a 2 TB volume on {resource}",
                "{name} successfully completed snapshot of {resource}",
                "{name} rotated backup tapes in {resource}",
                "{name} mounted {resource} to database cluster",
                "{name} reclaimed 500 GB free space on {resource}"
            ],
            "WARNING": [
                "{name} noted elevated read error rates on {resource}",
                "{name} observed RAID rebuild running slower than usual on {resource}",
                "{name} low cache hit ratio detected on {resource}",
                "{name} temperature threshold nearing limit on {resource}",
                "{name} detected pending sector remap events on {resource}"
            ],
            "ERROR": [
                "{name} I/O timeout while writing to {resource}",
                "{name} metadata corruption found on {resource}",
                "{name} replication lag exceeded SLA for {resource}",
                "{name} failed to decrypt volume on {resource}",
                "{name} manual intervention required: rebuild error on {resource}"
            ],
            "CRITICAL": [
                "{name} catastrophic disk failure in {resource} array",
                "{name} all redundant controllers lost in {resource}",
                "{name} data integrity violation alarm from {resource}",
                "{name} emergency switchover activated for {resource}",
                "{name} complete loss of access to {resource}"
            ]
        }
    },
    "Database": {
        "resources": ["MySQL", "PostgreSQL", "MongoDB", "Redis"],
        "log": {
            "DEBUG": [
                "{name} enabled slow‑query tracing on {resource}",
                "{name} captured query execution plan from {resource}",
                "{name} profiled index usage statistics on {resource}",
                "{name} ran consistency check on {resource} cluster",
                "{name} instrumented transaction lock metrics on {resource}"
            ],
            "INFO": [
                "{name} completed full backup of {resource}",
                "{name} applied schema migration to {resource}",
                "{name} rotated logs for {resource}",
                "{name} promoted replica to primary in {resource} cluster",
                "{name} cleared cache entries in {resource}"
            ],
            "WARNING": [
                "{name} slow replication detected on {resource}",
                "{name} connection pool exhaustion approaching in {resource}",
                "{name} temporary deadlock resolved on {resource}",
                "{name} high rollback rate observed in {resource}",
                "{name} table bloat exceeding threshold in {resource}"
            ],
            "ERROR": [
                "{name} connection timeout on {resource} under heavy load",
                "{name} failed to commit transaction in {resource}",
                "{name} integrity constraint violation in {resource}",
                "{name} unexpected null value in critical column of {resource}",
                "{name} lost quorum in {resource} cluster"
            ],
            "CRITICAL": [
                "{name} primary node down in {resource} cluster",
                "{name} unrecoverable corruption detected in {resource}",
                "{name} emergency failover to disaster‑recovery site for {resource}",
                "{name} data loss suspected on {resource}",
                "{name} manual intervention required: cluster split‑brain on {resource}"
            ]
        }
    },
    "Application": {
        "resources": ["API Server", "Web Frontend", "Auth Service", "Cache Layer"],
        "log": {
            "DEBUG": [
                "{name} traced HTTP headers on {resource} request",
                "{name} dumped thread stack from {resource} for analysis",
                "{name} toggled verbose logging on {resource}",
                "{name} captured raw payload on {resource}",
                "{name} profiled endpoint latency on {resource}"
            ],
            "INFO": [
                "{name} deployed v4.2.0 to {resource}",
                "{name} health check passed on {resource}",
                "{name} gracefully restarted {resource}",
                "{name} scaled out an instance of {resource}",
                "{name} rotated API credentials in {resource}"
            ],
            "WARNING": [
                "{name} memory usage at 78% on {resource}",
                "{name} slow database response impacting {resource}",
                "{name} session store nearing capacity in {resource}",
                "{name} high error rate observed in {resource}",
                "{name} latency spike detected on {resource}"
            ],
            "ERROR": [
                "{name} unhandled exception in {resource} handler",
                "{name} failed OAuth handshake in {resource}",
                "{name} downstream service timeout for {resource}",
                "{name} cache miss storm on {resource}",
                "{name} deployment rollback triggered for {resource}"
            ],
            "CRITICAL": [
                "{name} whole {resource} cluster unresponsive",
                "{name} security breach detected via {resource}",
                "{name} emergency shutdown of {resource} to protect data",
                "{name} cascading failure from {resource} to other services",
                "{name} manual failover initiated for {resource}"
            ]
        }
    }
}
EMPLOYEES = {dep: [{"gender": (gender := random.choice(["female","male"])),
                   'first_name': (fname := getattr(faker,f'first_name_{gender}')()),
                   "last_name": (lname := getattr(faker,f'last_name_{gender}')()),
                   'emp_id': f'{lname[:3]}{fname[-3:]}'.upper()} 
            for i in range(random.randint(3,6))]
            for dep in LOG.keys()
            }

create_logs_dir()
if args.persist_employees:
    persist_employee_data()

try:
    for idx,log_dct in enumerate(log_gen(TOTAL_LOG_LINES), start = 1):
        
        if current_line == MAX_LINES_PER_FILE:
            file.close()
            current_line = 0 
        if current_line == 0:
            total_files += 1
            
            file_name = PATH.joinpath('logs',f'log_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}_{total_files:03d}.jsonl')
            print(F'{total_files}: {file_name}')
            file = open(file_name, mode = 'w',encoding = 'utf-8')

        current_line += 1 
        file.write(json.dumps(log_dct)+'\n')
except KeyboardInterrupt:
    print(f'caught keyboardinteerupt')
    if file is not None or not file.closed:
        file.close()
print(f'total_log_lines_generated : {idx}')

    
    
