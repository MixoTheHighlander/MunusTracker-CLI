import argparse
import json
import os
from datetime import datetime

SETTINGS_FILE = 'data/settings.json'
LOG_FILE = 'data/tasks.log'

TIME_FORMATS = {
    'iso_space': '%Y-%m-%d %H:%M:%S',
    'iso_t': '%Y-%m-%dT%H:%M:%S',
    'iso_z': '%Y-%m-%dT%H:%M:%S%z',
    'iso_utc_z': '%Y-%m-%dT%H:%M:%SZ',
    
    'rfc_3339': '%Y-%m-%dT%H:%M:%S%z',
    'rfc_3339_millis': '%Y-%m-%dT%H:%M:%S.%f%z',
    'rfc_2822': '%a, %d %b %Y %H:%M:%S %z',
    'us_slash': '%m/%d/%Y %H:%M:%S',
    'eu_dot': '%d.%m.%Y %H:%M:%S',

    'friendly_12': '%B %d, %Y at %I:%M:%S %p',
    'friendly_24': '%B %d, %Y at %H:%M:%S',
    
    'compact': '%Y%m%d%H%M%S',
}

time_format = TIME_FORMATS['iso_space']
logs_display_count: int = 10
active_tasks_count_limit: int = 2**32

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

def log_builder():
    # Builds log files based on selected extension in settings
    pass

def start_task(task, time: str):
    settings = load_json(SETTINGS_FILE)
    if not settings:
        print("Error: Could not load settings")
        return
    
    ID = generate_id()
    
    task_data = {
        "id": ID,
        "task": task,
        "start": time
    }
    
    if 'Data' not in settings:
        settings['Data'] = {}
    if 'tasks' not in settings['Data']:
        settings['Data']['tasks'] = {}
    if 'active_tasks' not in settings['Data']['tasks']:
        settings['Data']['tasks']['active_tasks'] = {"count": 0, "items": []}
    
    settings['Data']['tasks']['active_tasks']['items'].append(task_data)
    settings['Data']['tasks']['active_tasks']['count'] = len(settings['Data']['tasks']['active_tasks']['items'])
    
    if 'logs' not in settings['Data']:
        settings['Data']['logs'] = {"count": 0, "items": [], "last_id": 0}
    settings['Data']['logs']['last_id'] = ID
    
    save_json(SETTINGS_FILE, settings)
    
    entry = f"[{ID}] [{time}] STARTED: {task}"
    save_log(LOG_FILE, entry)
    
    print(f"Successfully started task '{task}' with ID {ID} at {time}")

def stop_task(time: str, task_id: int = None):
    settings = load_json(SETTINGS_FILE)
    if not settings:
        print("Error: Could not load settings")
        return
    
    active_tasks = settings.get('Data', {}).get('tasks', {}).get('active_tasks', {}).get('items', [])
    
    if not active_tasks:
        print("You have 0 active tasks")
        return
    
    task_data = None
    if task_id is not None:
        for task in active_tasks:
            if task['id'] == task_id:
                task_data = task
                break
        if task_data is None:
            print(f"No active task found with ID {task_id}")
            print("Active tasks:")
            for task in active_tasks:
                print(f"  ID {task['id']}: '{task['task']}'")
            return
    elif len(active_tasks) == 1:
        task_data = active_tasks[0]
    else:
        print(f"You have {len(active_tasks)} active tasks:")
        for task in active_tasks:
            print(f"  ID {task['id']}: '{task['task']}'")
        print("Please specify which task to stop by running: tasker.py stop <task_id>")
        return
    
    stop_time = datetime.strptime(time, time_format)
    task = task_data["task"]
    task_start = task_data["start"]
    ID = task_data["id"]
    
    start_time = None
    for fmt_name, fmt_string in TIME_FORMATS.items():
        try:
            start_time = datetime.strptime(task_start, fmt_string)
            break
        except ValueError:
            continue
    
    if start_time is None:
        print(f"Warning: Could not parse start time '{task_start}', using current time for duration calculation")
        start_time = stop_time
    
    duration = stop_time - start_time
    
    active_tasks.remove(task_data)
    settings['Data']['tasks']['active_tasks']['items'] = active_tasks
    settings['Data']['tasks']['active_tasks']['count'] = len(active_tasks)
    
    if 'logs' not in settings['Data']:
        settings['Data']['logs'] = {"count": 0, "items": []}
    
    log_entry = {
        "id": ID,
        "task": task,
        "start": task_start,
        "stop": time,
        "duration": str(duration)
    }
    
    settings['Data']['logs']['items'].append(log_entry)
    settings['Data']['logs']['count'] = len(settings['Data']['logs']['items'])
    
    save_json(SETTINGS_FILE, settings)
    
    entry = f"[{ID}] [{time}] STOPPED: {task}; (Duration: {duration})"
    save_log(LOG_FILE, entry)
    
    print(f"Successfully stopped task '{task}' (ID: {ID}) after {duration}")
    print("Task has been saved to logs")

def display_x_logs(path, num):
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
            if not lines:
                print("Log file is empty")
                return
            lines_to_display = lines[-num:]
            for line in lines_to_display:
                print(line.strip())
    except FileNotFoundError:
        print(f"Error: Log file not found at {path}; Use help command to see possible solutions.")
    except Exception as e:
        print(f"An error occurred: {e}")

def load_settings():
    settings = load_json(SETTINGS_FILE)
    if not settings:
        settings = {
            "Preferences": {
                "time_format": "iso_space",
                "logs_display_count": 10,
                "active_tasks_count_limit": "inf"
            },
            "Data": {
                "tasks": {
                    "active_tasks": {
                        "count": 0,
                        "items": []
                    }
                },
                "logs": {
                    "count": 0,
                    "items": [],
                    "last_id": 0
                }
            }
        }
        save_json(SETTINGS_FILE, settings)
    
    global time_format, logs_display_count, active_tasks_count_limit
    prefs = settings.get('Preferences', {})
    time_format = TIME_FORMATS.get(prefs.get('time_format', 'iso_space'), TIME_FORMATS['iso_space'])
    logs_display_count = int(prefs.get('logs_display_count', 10))
    active_tasks_count_limit = float(prefs.get('active_tasks_count_limit', float('inf')))
    return settings

def generate_id():
    settings = load_json(SETTINGS_FILE)
    if not settings:
        return 1
    
    last_id = settings.get('Data', {}).get('logs', {}).get('last_id', 0)
    new_id = last_id + 1
    
    return new_id

def display_active_tasks():
    settings = load_json(SETTINGS_FILE)
    if not settings:
        print("Error: Could not load settings")
        return
    
    active_tasks = settings.get('Data', {}).get('tasks', {}).get('active_tasks', {}).get('items', [])
    
    if not active_tasks:
        print("No active tasks")
        return
    
    print(f"Active tasks ({len(active_tasks)}):")
    for task in active_tasks:
        task_id = task.get('id', '?')
        task_name = task.get('task', 'Unknown')
        start_time = task.get('start', 'Unknown')

        try:
            start_dt = None
            for fmt_name, fmt_string in TIME_FORMATS.items():
                try:
                    start_dt = datetime.strptime(start_time, fmt_string)
                    break
                except ValueError:
                    continue
            
            if start_dt:
                current_dt = datetime.now()
                duration = current_dt - start_dt
                print(f"  ID {task_id}: '{task_name}' (running for {duration})")
            else:
                print(f"  ID {task_id}: '{task_name}' (started at {start_time})")
        except:
            print(f"  ID {task_id}: '{task_name}' (started at {start_time})")

def display_settings():
    settings = load_json(SETTINGS_FILE)
    if not settings:
        print("Error: Could not load settings")
        return
    
    prefs = settings.get('Preferences', {})
    print("Current Settings:")
    print(f"  Time Format: {prefs.get('time_format', 'iso_space')}")
    print(f"  Logs Display Count: {prefs.get('logs_display_count', 10)}")
    print(f"  Active Tasks Limit: {prefs.get('active_tasks_count_limit', 'inf')}")
    
    print("\nAvailable Time Formats:")
    for format_name in TIME_FORMATS.keys():
        print(f"  - {format_name}")

def update_setting(setting_name, setting_value):
    settings = load_json(SETTINGS_FILE)
    if not settings:
        print("Error: Could not load settings")
        return
    
    if 'Preferences' not in settings:
        settings['Preferences'] = {}
    
    if setting_name == "time_format":
        if setting_value not in TIME_FORMATS:
            print(f"Invalid time format '{setting_value}'")
            print("Available formats:", ", ".join(TIME_FORMATS.keys()))
            return
        settings['Preferences']['time_format'] = setting_value
        print(f"Time format updated to: {setting_value}")
    
    elif setting_name == "logs_display_count":
        try:
            count = int(setting_value)
            if count <= 0:
                print("Logs display count must be a positive integer")
                return
            settings['Preferences']['logs_display_count'] = count
            print(f"Logs display count updated to: {count}")
        except ValueError:
            print("Logs display count must be a valid integer")
            return
    
    elif setting_name == "active_tasks_count_limit":
        if setting_value.lower() == "inf":
            settings['Preferences']['active_tasks_count_limit'] = "inf"
            print("Active tasks limit updated to: unlimited")
        else:
            try:
                limit = int(setting_value)
                if limit <= 0:
                    print("Active tasks limit must be a positive integer or 'inf'")
                    return
                settings['Preferences']['active_tasks_count_limit'] = str(limit)
                print(f"Active tasks limit updated to: {limit}")
            except ValueError:
                print("Active tasks limit must be a valid integer or 'inf'")
                return
    
    else:
        print(f"Unknown setting: {setting_name}")
        print("Available settings: time_format, logs_display_count, active_tasks_count_limit")
        return
    
    save_json(SETTINGS_FILE, settings)
    load_settings()

def sort_logs(sort_by="id", reverse=False):
    settings = load_json(SETTINGS_FILE)
    if not settings:
        print("Error: Could not load settings")
        return
    
    logs = settings.get('Data', {}).get('logs', {}).get('items', [])
    
    if not logs:
        print("No completed tasks found in logs")
        return
    
    def get_sort_key(log_entry):
        if sort_by == "id":
            return log_entry.get('id', 0)
        elif sort_by == "name":
            return log_entry.get('task', '').lower()
        elif sort_by == "start" or sort_by == "time_started":
            try:
                start_time = log_entry.get('start', '')
                return datetime.strptime(start_time, time_format)
            except:
                return datetime.min
        elif sort_by == "stop" or sort_by == "time_stopped":
            try:
                stop_time = log_entry.get('stop', '')
                return datetime.strptime(stop_time, time_format)
            except:
                return datetime.min
        elif sort_by == "duration":
            try:
                duration_str = log_entry.get('duration', '0:00:00')
                if '.' in duration_str:
                    duration_str = duration_str.split('.')[0]
                parts = duration_str.split(':')
                if len(parts) == 3:
                    hours, minutes, seconds = map(int, parts)
                    return hours * 3600 + minutes * 60 + seconds
                else:
                    return 0
            except:
                return 0
        else:
            return 0
    
    try:
        sorted_logs = sorted(logs, key=get_sort_key, reverse=reverse)
    except Exception as e:
        print(f"Error sorting logs: {e}")
        return
    
    print(f"Logs sorted by {sort_by} ({'descending' if reverse else 'ascending'}):")
    print("-" * 80)
    
    for log in sorted_logs:
        task_id = log.get('id', '?')
        task_name = log.get('task', 'Unknown')
        start_time = log.get('start', 'Unknown')
        stop_time = log.get('stop', 'Unknown')
        duration = log.get('duration', 'Unknown')
        
        print(f"ID {task_id}: '{task_name}'")
        print(f"  Started:  {start_time}")
        print(f"  Stopped:  {stop_time}")
        print(f"  Duration: {duration}")
        print()

def main():
    load_settings()
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="cmd")
    startParser = subparser.add_parser("start", help="Starts counting time of your task")
    startParser.add_argument("task_name", nargs='+', help="name of your task (can contain spaces)")
    stopParser = subparser.add_parser("stop", help="Stops and saves your task")
    stopParser.add_argument("task_id", type=int, nargs="?", help="ID of the task to stop (optional, if not provided and multiple tasks are active, you'll be prompted)")
    subparser.add_parser("active", help="Displays all currently active tasks")
    logParser = subparser.add_parser("log", help="Displays logs of all tasks")
    logParser.add_argument("log_count", type=int, nargs="?", default=logs_display_count, help="Number of logs to display (default from settings)")
    subparser.add_parser("all", help="Displays all logs")
    sortParser = subparser.add_parser("sort", help="Sort and display logs by specified criteria")
    sortParser.add_argument("sort_by", choices=["id", "name", "start", "time_started", "stop", "time_stopped", "duration"], help="Criteria to sort by")
    sortParser.add_argument("--reverse", "-r", action="store_true", help="Sort in descending order")
    configParser = subparser.add_parser("config", help="Manage application settings")
    configSubparser = configParser.add_subparsers(dest="config_cmd")
    configSubparser.add_parser("show", help="Display current settings")
    setParser = configSubparser.add_parser("set", help="Update a setting")
    setParser.add_argument("setting_name", help="Name of the setting to update")
    setParser.add_argument("setting_value", help="New value for the setting")
    args = parser.parse_args()

    if args.cmd == "start":
        start_task(' '.join(args.task_name), get_time(time_format))
    elif args.cmd == "stop":
        stop_task(get_time(time_format), getattr(args, 'task_id', None))
    elif args.cmd == "active":
        display_active_tasks()
    elif args.cmd == "log":
        display_x_logs(LOG_FILE, args.log_count)
    elif args.cmd == "all":
        display_x_logs(LOG_FILE, 2**32)
    elif args.cmd == "sort":
        sort_logs(args.sort_by, args.reverse)
    elif args.cmd == "config":
        if args.config_cmd == "show":
            display_settings()
        elif args.config_cmd == "set":
            update_setting(args.setting_name, args.setting_value)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()