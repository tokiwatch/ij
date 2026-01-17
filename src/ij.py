#!/usr/bin/env python3
import argparse
import datetime
import os
import pathlib
import subprocess
import sys

# 定数設定
# 環境変数 IJ_LOG_DIR があればそれを使い、なければホームディレクトリ配下を使用
env_log_dir = os.environ.get("IJ_LOG_DIR")
if env_log_dir:
    LOG_DIR = pathlib.Path(env_log_dir)
else:
    LOG_DIR = pathlib.Path.home() / ".ij_logs"

def get_today_log_path():
    """今日のログファイルのパスを取得する"""
    today = datetime.date.today()
    filename = f"{today.isoformat()}.md"
    return LOG_DIR / filename

def ensure_log_dir():
    """ログディレクトリが存在することを確認し、なければ作成する"""
    if not LOG_DIR.exists():
        LOG_DIR.mkdir(parents=True, exist_ok=True)

def append_log(message):
    """メッセージをログに追記する"""
    ensure_log_dir()
    log_path = get_today_log_path()
    now = datetime.datetime.now().strftime("%H:%M")
    
    # ファイルが新規作成の場合は日付を見出しとして入れるなどの考慮もありうるが、
    # 仕様書には明記されていないため、仕様書の形式通り "- HH:MM メッセージ" とする。
    
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"- {now} {message}\n")
    
    print(f"Logged: {now} {message}")

def show_today_log():
    """今日のログを表示する"""
    log_path = get_today_log_path()
    if log_path.exists():
        print(f"--- Log for {datetime.date.today()} ---")
        with open(log_path, "r", encoding="utf-8") as f:
            print(f.read(), end="")
    else:
        print("No logs for today.")

def search_logs(keyword):
    """全ログファイルからキーワードを検索する"""
    if not LOG_DIR.exists():
        print("No log directory found.")
        return

    found = False
    # 日付順にソートして検索
    log_files = sorted(LOG_DIR.glob("*.md"))
    
    for log_file in log_files:
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                file_matches = []
                for line in lines:
                    if keyword.lower() in line.lower():
                        file_matches.append(line.strip())
                
                if file_matches:
                    print(f"[{log_file.stem}]")
                    for match in file_matches:
                        print(f"  {match}")
                    print("")
                    found = True
        except Exception as e:
            print(f"Error reading {log_file}: {e}")

    if not found:
        print(f"No matches found for '{keyword}'.")

def run_interactive_mode():
    """インタラクティブモードでログを入力する"""
    print("Enter your log message (Press Ctrl+C to cancel):")
    try:
        message = input("> ")
        if message.strip():
            append_log(message.strip())
        else:
            print("Empty message, nothing logged.")
    except KeyboardInterrupt:
        print("\nCancelled.")

def open_editor():
    """今日のログファイルをエディタで開く"""
    ensure_log_dir()
    log_path = get_today_log_path()
    
    # ファイルが存在しない場合は空のファイルを作成しておく
    if not log_path.exists():
        log_path.touch()

    editor = os.environ.get("EDITOR", "nano")  # デフォルトは nano (macOS/Linux向け)
    # Windowsの場合はメモ帳などをフォールバックにする考慮も必要だが、今回はdarwin環境なのでnanoで良しとする
    
    try:
        subprocess.call([editor, str(log_path)])
    except FileNotFoundError:
        print(f"Editor '{editor}' not found. Please set $EDITOR environment variable.")

def show_recent_logs(days):
    """直近 n 日分のログを表示する"""
    if not LOG_DIR.exists():
        print("No log directory found.")
        return

    today = datetime.date.today()
    target_dates = [today - datetime.timedelta(days=i) for i in range(days)]
    # リストを過去 -> 現在の順にする
    target_dates.reverse()

    for date_obj in target_dates:
        filename = f"{date_obj.isoformat()}.md"
        log_path = LOG_DIR / filename
        
        if log_path.exists():
            print(f"--- {date_obj} ---")
            with open(log_path, "r", encoding="utf-8") as f:
                print(f.read(), end="")
            print("") # 空行で見やすく

def main():
    parser = argparse.ArgumentParser(description="Interstitial Journaling CLI Tool")
    
    # メッセージ引数 (位置引数、オプショナル)
    # nargs='?' とすると、引数がない場合は None になる
    # しかし、他のオプションとの兼ね合いが難しいため、
    # メッセージがある場合とない場合（一覧表示）の分岐が必要
    
    # ここでは、サブコマンドを使わずに、引数の組み合わせで分岐させる設計とする
    # 仕様:
    # ij -> 今日のログ一覧
    # ij "msg" -> ログ記録
    # ij -s keyword -> 検索
    # ij -e -> 編集
    # ij -l n -> 履歴
    
    parser.add_argument("message", nargs="*", help="Log message to append")
    parser.add_argument("-s", "--search", help="Search keyword in all logs")
    parser.add_argument("-e", "--edit", action="store_true", help="Open today's log in editor")
    parser.add_argument("-l", "--list-recent", type=int, metavar="N", help="Show logs for the recent N days")
    parser.add_argument("-i", "--interactive", action="store_true", help="Run in interactive mode")

    args = parser.parse_args()

    # 優先順位の処理
    if args.interactive:
        run_interactive_mode()
    elif args.edit:
        open_editor()
    elif args.search:
        search_logs(args.search)
    elif args.list_recent is not None:
        show_recent_logs(args.list_recent)
    elif args.message:
        append_log(" ".join(args.message))
    else:
        # 引数がなく、標準入力がパイプなどの場合（TTYでない場合）は標準入力を読み込む
        if not sys.stdin.isatty():
            # 標準入力からの読み込み
            # strip() で前後の空白を除去し、空文字でない場合のみログ記録
            stdin_message = sys.stdin.read().strip()
            if stdin_message:
                append_log(stdin_message)
                return

        # 引数も標準入力もない場合は今日のログを表示
        show_today_log()

if __name__ == "__main__":
    main()
