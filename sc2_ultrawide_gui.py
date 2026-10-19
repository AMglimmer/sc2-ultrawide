"""Self-contained GUI entry; only an explicit action opens the game process."""
import contextlib
import ctypes
import io
import os
from pathlib import Path
import queue
import sys
import threading
import traceback
from datetime import datetime

import sc2_ultrawide
from ultrawide.ui import APP_DIRECTORY, HELPER_FLAG, helper_log


def run_command(command):
    output = io.StringIO()
    previous = sys.argv
    code = 0
    try:
        sys.argv = [previous[0], command]
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            try:
                sc2_ultrawide.main()
            except SystemExit as error:
                code = error.code if isinstance(error.code, int) else 1
                if error.code and not isinstance(error.code, int):
                    print(error.code)
            except Exception:
                code = 1
                traceback.print_exc()
    finally:
        sys.argv = previous
    text = output.getvalue()
    directory = Path(os.environ.get("SC2_ULTRAWIDE_LOG_DIR", str(Path(APP_DIRECTORY) / "logs")))
    try:
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "last-command.txt").write_text(
            f"{datetime.now().astimezone().isoformat()} {command} exit={code}\n{text}", encoding="utf-8")
    except OSError as error:
        code = 1
        text += f"\n无法保存日志：{error}\n"
    return code, text


def main():
    if sys.argv[1:] == [HELPER_FLAG]:
        try:
            sc2_ultrawide.main()
            return 0
        except (Exception, SystemExit) as error:
            helper_log(f"helper failed: {type(error).__name__}: {error}")
            return 1
    if sys.argv[1:] == ["--status"]:
        return run_command("status")[0]
    if sys.argv[1:]:
        return 2
    ctypes.windll.user32.SetProcessDPIAware()
    import tkinter as tk
    from tkinter import ttk
    from tkinter.scrolledtext import ScrolledText

    root = tk.Tk()
    root.title("星际 II 超宽工具 · Portable")
    root.geometry("860x540")
    root.minsize(720, 450)
    panel = ttk.Frame(root, padding=16)
    panel.pack(fill="both", expand=True)
    ttk.Label(panel, text="国服 build 98370 · 单人战役 · 自带 Python 运行时").pack(anchor="w")
    ttk.Label(panel, text="先通过 Battle.net 启动游戏，设为窗口化全屏；进入战役后启用。").pack(anchor="w", pady=(8, 0))
    ttk.Label(panel, text="启用会修改客户端内存，存在账号和崩溃风险。关闭本窗口不停止 HUD 助手；游戏退出后助手结束。").pack(anchor="w", pady=8)
    bar = ttk.Frame(panel)
    bar.pack(fill="x", pady=8)
    state = tk.StringVar(value="等待操作（尚未访问游戏）")
    output = ScrolledText(panel, wrap="word", font=("Consolas", 10))
    output.pack(fill="both", expand=True)
    ttk.Label(panel, textvariable=state).pack(anchor="w", pady=(8, 0))
    results = queue.Queue()
    buttons = []
    busy = False

    def execute(command):
        nonlocal busy
        if busy:
            return
        busy = True
        for button in buttons:
            button.configure(state="disabled")
        state.set("正在执行，请稍候……")
        threading.Thread(target=lambda: results.put(run_command(command)), daemon=True).start()

    for label, command in (("只读查看状态", "status"), ("启用超宽 + 自动修复 HUD", "apply"), ("恢复 16:9", "revert")):
        button = ttk.Button(bar, text=label, command=lambda cmd=command: execute(cmd))
        button.pack(side="left", padx=(0, 10))
        buttons.append(button)

    def poll():
        nonlocal busy
        try:
            code, text = results.get_nowait()
        except queue.Empty:
            pass
        else:
            busy = False
            output.delete("1.0", "end")
            output.insert("end", text)
            state.set("操作完成" if code == 0 else "操作失败，请查看上方详情")
            for button in buttons:
                button.configure(state="normal")
        root.after(100, poll)

    root.protocol("WM_DELETE_WINDOW", lambda: state.set("操作执行中，请等完成后关闭。") if busy else root.destroy())
    poll()
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
