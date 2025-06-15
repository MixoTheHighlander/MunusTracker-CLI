# MunusTracker 🕐

> **Track your time. Honor your work.**

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-red.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightblue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-yellow.svg)
![Status](https://img.shields.io/badge/status-active-lightgreen.svg)

A powerful command-line time tracking tool that helps you monitor and log your tasks with precision and elegance.

## 🧠 What Does "Munus" Mean?

"Munus" is a Latin word with several related meanings:
- **Duty or obligation**
- **Service, gift, or offering**
- **Something one performs for the benefit of others or as a responsibility**

It's the root of modern words like:
- **Municipal** (related to civic duty)
- **Remuneration** (payment for service)
- **Communal** (shared responsibilities)

## 📖 A bit of poetry

A tool to log and honor the work you do — your time as a gift. <br>
A quiet record of purpose true, in moments you uplift.

## 🚀 Features

- 🔄 **Multi-Task Support** - Track multiple concurrent tasks
- 📝 **Comprehensive Logging** - Detailed logs with duration calculations
- ⏱️ **Precise Time Tracking** - Start and stop tasks with accurate timing
- 📊 **Multiple Time Formats** - Choose from 12 different time display formats
- ⚙️ **Configurable Settings** - Customize display preferences and limits
- 📋 **Task Management** - View active tasks and completed logs
- 🔍 **Advanced Sorting** - Sort logs by ID, name, time, or duration

## 📦 Installation

1. Ensure you have Python 3 installed (tested on python 3.12)

2. Clone the repository:
```bash
git clone https://github.com/MixoTheHighlander/MunusTracker-CLI.git
cd MunusTracker-CLI
```

## 🎯 Quick Start

### Start a Task
```bash
python MunusTracker.py start "Working on documentation"
```

### View Active Tasks
```bash
python MunusTracker.py active
```

### Stop a Task
```bash
# If only one task is active
python MunusTracker.py stop

# If multiple tasks are active, specify ID
python MunusTracker.py stop 1
```

### View Recent Logs
```bash
python MunusTracker.py log
python MunusTracker.py log 5  # Show last 5 entries
```

## 📖 Commands Reference

## Task Management
- `start <task_name>` - Start tracking a new task
- `stop [task_id]` - Stop an active task
- `active` - Display all currently running tasks

## Log Viewing
- `log [count]` - Show recent log entries (default: 10)
- `all` - Display all log entries (max: 4 294 967 296)
- `sort <criteria> [--reverse]` - Sort logs by:
  - `id` - Task ID
  - `name` - Task name
  - `start` / `time_started` - Start time
  - `stop` / `time_stopped` - Stop time
  - `duration` - Task duration

## Configuration
- `config show` - Display current settings
- `config set <setting> <value>` - Update a setting


### Settings
- `time_format` - Time display format (see table above)
- `logs_display_count` - Default number of logs to show
- `active_tasks_count_limit` - Maximum concurrent tasks ("inf" for unlimited)

### Time Formats
Choose from multiple time display formats:

| Format | Example |
|--------|---------|
| `iso_space` | `2024-01-15 14:30:00` |
| `iso_t` | `2024-01-15T14:30:00` |
| `iso_z` | `2024-01-15T14:30:00+0000` |
| `iso_utc_z` | `2024-01-15T14:30:00Z` |
| `rfc_3339` | `2024-01-15T14:30:00+00:00` |
| `rfc_3339_millis` | `2024-01-15T14:30:00.123456+00:00` |
| `rfc_2822` | `Mon, 15 Jan 2024 14:30:00 +0000` |
| `us_slash` | `01/15/2024 14:30:00` |
| `eu_dot` | `15.01.2024 14:30:00` |
| `friendly_12` | `January 15, 2024 at 2:30:00 PM` |
| `friendly_24` | `January 15, 2024 at 14:30:00` |
| `compact` | `20240115143000` |

### Examples
```bash
# Change time format to friendly 24-hour
python MunusTracker.py config set time_format friendly_24

# Set default log display count
python MunusTracker.py config set logs_display_count 15

# Limit active tasks
python MunusTracker.py config set active_tasks_count_limit 5
```

## 📁 File Structure

```
MunusTracker/
├── MunusTracker.py          # Main application
├── data/
│   ├── settings.json        # User preferences and data
│   └── tasks.log            # Plain text log file
├── README.md
└── LICENSE
```

## 📊 Data Storage

MunusTracker uses two storage methods:
- **JSON** ([data/settings.json](data/settings.json)) - Structured data for active tasks, completed logs, and settings
- **Plain Text** ([data/tasks.log](data/tasks.log)) - Human-readable log entries

## 🔧 Example Workflow

```bash
# Start working on a project
python MunusTracker.py start "Implementing user authentication"

# Check what's running
python MunusTracker.py active
# Output: Active tasks (1):
#   ID 1: 'Implementing user authentication' (running for 1:15:24)

# Start another task
python MunusTracker.py start "Code review"

# Stop the first task
python MunusTracker.py stop 1

# View recent activity
python MunusTracker.py log 3

# Sort logs by duration to see longest tasks
python MunusTracker.py sort duration --reverse
```

## 🛠️ Development

### Todo List
- Multiple log format exports (JSON, XML, YAML, CSV)
- Log format converter
- Data reset commands
- Enhanced help system
- Counting how much total time you spent on your tasks
- Version information
- Bug fixes
- And a few more ideas...

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💝 Credits

Made with love for every CLI tool enthusiast by [Michael Newcomer](https://github.com/MixoTheHighlander).

---

*MunusTracker - Because your time matters, and every moment deserves to be honored.*