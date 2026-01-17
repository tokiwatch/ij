# ij - Interstitial Journaling CLI Tool

`ij` is a CLI tool designed to record thoughts, achievements, and next actions during work transitions (interstitial) with minimal friction.

## Features

*   **Quick Logging:** Record notes with the current timestamp in a single command.
*   **Automatic Daily Log Generation:** Automatically creates Markdown files (`YYYY-MM-DD.md`) for each day.
*   **Fast Review:** Instantly display today's logs or past logs in the terminal.
*   **Search Function:** Keyword search across all log files.
*   **Editor Integration:** Directly edit log files using your favorite editor.

## Installation

1. Clone the repository.
   ```bash
   git clone https://github.com/username/ij.git
   cd ij
   ```

2. Grant execution permission to the script.
   ```bash
   chmod +x src/ij.py
   ```

3. (Recommended) Set up an alias or create a symbolic link in a directory included in your PATH for easier access.
   ```bash
   # Add to .bashrc or .zshrc
   alias ij='/path/to/ij/src/ij.py'
   ```

## Usage

### Logging
Pass a message as an argument to record it with the current timestamp.
```bash
ij "Drafted the project plan. Feeling a bit tired."
```
You can also type without quotes:
```bash
ij Drafted the project plan. Feeling a bit tired.
```
Output example:
```
Logged: 14:05 Drafted the project plan. Feeling a bit tired.
```

You can also use standard input (pipe) to record logs. This is useful for long messages or integrating with other commands.
```bash
echo "Long message..." | ij
```

### Interactive Mode
Launch an interactive prompt to enter your log. This is another way to avoid shell issues with long messages.
```bash
ij -i
```

### Show Today's Log
Run without arguments to list today's logs.
```bash
ij
```

### Search
Search for a keyword across all past logs.
```bash
ij -s "project plan"
```

### Edit Log
Open today's log file in your default editor.
```bash
ij -e
```

### Show History
Display logs for the recent `n` days.
```bash
ij -l 3
```

## Configuration

You can customize the behavior by setting environment variables.

| Environment Variable | Description | Default Value |
| --- | --- | --- |
| `IJ_LOG_DIR` | Directory path for saving log files | `~/.ij_logs` |
| `EDITOR` | Editor used with `ij -e` | `nano` |

Example (`.bashrc` / `.zshrc`):
```bash
export IJ_LOG_DIR="$HOME/Dropbox/Journal"
export EDITOR="vim"
```

## Development

### Running Tests
```bash
python3 -m unittest discover tests
```

## License

[MIT License](LICENSE)
