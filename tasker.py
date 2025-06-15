import argparse
import json
import os
from datetime import datetime

active_tasks_file = 'data/active_tasks.json'
old_tasks_file = 'data/tasks.log'
time_format = '%Y-%m-%d %H:%M:%S'
start_time = 0
stop_time = 0

def get_time(t_format) -> str:
    return datetime.now().strftime(t_format)

def load_json(path):
    if not os.path.exists(path):
        return None
    with open (path) as f:
        return json.load(f)

def save_json(path, data):
    with open (path, 'w') as f:
        return json.dump(data, f, indent=2)

def save_log(path, entry):
    with open (path, "a") as f:
        f.write(entry + '\n')

def start_task(task, time: str):
    # if not os.path.exists(active_tasks_file):
    #     return
    data = {
        "task": task,
        "start": time
    }
    save_json(active_tasks_file, data)
    entry = f"[{time}] STARTED: {task}"
    save_log(old_tasks_file, entry)
    print(f"Successfully started task {task} at {time}")

def stop_task(time: str):
    stop_time = datetime.strptime(time, time_format)
    data = load_json(active_tasks_file)
    if not data:
        print("You have 0 active tasks")
        return
    task = data["task"]
    task_start = data["start"]
    start_time = datetime.strptime(task_start, time_format)
    entry = f"[{time}] STOPPED: {task}; (Duration: {stop_time-start_time})"
    save_log(old_tasks_file, entry)
    os.remove(active_tasks_file)
    print(f"Successfully ended task {task} in {stop_time-start_time}")
    print("Task got saved into logs")

def display_logs(path):
    with open (path, 'r') as f:
        print(*[x for x in f])

def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest = "cmd")
    startParser = subparser.add_parser("start", help = "Starts counting time of your task")
    startParser.add_argument("task_name", type=str, help="name of your task")
    subparser.add_parser("stop", help="Stops and saves your task")
    subparser.add_parser("log", help="Dispalys logs of all tasks")
    args = parser.parse_args()
    
    if args.cmd == "start":
        start_task(args.task_name, get_time(time_format))
    if args.cmd == "stop":
        stop_task(get_time(time_format))
    if args.cmd == "log":
        display_logs(old_tasks_file)


if __name__ == "__main__":
    main()