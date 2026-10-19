# 星际争霸 II 超宽屏工具 · 国服 98370 Portable 预览版

简体中文 | [English / 上游原文](README.en.md)

这是基于上游项目的本地适配分支 `codex/cn-build-98370`，并非 Blizzard 官方补丁。
适用验证环境：Windows 11、64 位客户端、国服 Battle.net、build 98370、3440×1440、窗口化全屏。
exe 文件元数据为 5.0.15.98370，用户报告启动器版本为 5.0.17.98370；目前仅据运行 build 描述适配范围。

## 下载 Portable 版

- [下载免 Python 的便携版（preview.3）](https://github.com/AMglimmer/sc2-ultrawide/releases/download/cn-98370-portable-preview.3/sc2-ultrawide-cn-98370-portable-preview.3.zip)
- [发布说明与 SHA-256 校验文件](https://github.com/AMglimmer/sc2-ultrawide/releases/tag/cn-98370-portable-preview.3)
- [国服适配及 Portable 源码](https://github.com/AMglimmer/sc2-ultrawide/tree/codex/cn-build-98370)

解压后双击 `SC2-Ultrawide-Portable.exe`，无需安装 Python。请放在可写目录。
国服适配代码位于上述分支；`main` 保留上游程序代码，请使用发布包或适配分支。

## 运行

### 双击启动器

Portable 版解压后，双击 `SC2-Ultrawide-Portable.exe`，再点“启用超宽 + 自动修复 HUD”。
先通过 Battle.net 启动游戏，保持窗口化全屏。无需输入 PowerShell 命令。
Portable EXE 包含 64 位 Python、Tk 和程序源码，不需要安装 Python、`py.exe` 或 pip。
只复制此 EXE 也能运行。单文件启动会在 Windows 临时目录解压运行时，正常退出后清理。
较早的 preview.2 中 `SC2-Ultrawide.exe` 是 C# 启动器，仍需要外部 Python 和同目录源码；请勿混淆。
“只读查看状态”不写游戏内存；“恢复 16:9”会调整窗口并可能写 HUD。
关闭启动器窗口不会停止助手；退出游戏后助手自动结束。没有开机启动项或服务。
日志保存在同目录 `logs`，记录命令结果、助手启动/退出、HUD 修复和异常，不每秒刷日志。
请放在可写目录。关闭图形窗口后助手独立运行；下次重新启动游戏后需要再次点击启用。

旧版 C# 图形版实测：只读状态和启用按钮均由用户点击验证无报错；一次换关后助手自动修复通过，重复 apply 未产生第二个助手。
Portable 版通过 17 项离线测试，以及移除 Python 环境路径、仅放置 EXE 的启动检查。
打包检查时未发现游戏进程，状态和助手入口按预期提示游戏未启动；新界面进程响应正常。随后用户反馈 Portable 已能运行；新版的换关、关闭 GUI 后助手存活与完整退出流程尚未完成专项实机复测。
真实退出游戏后的清理尚未打断用户游戏进行实测，退出与异常停止逻辑有模拟测试覆盖。

### 命令行

源码用户请先获取适配分支：

```powershell
git clone --branch codex/cn-build-98370 https://github.com/AMglimmer/sc2-ultrawide.git
cd sc2-ultrawide
```

需要 64 位 Python 3；仅使用标准库，不需要 pip 安装。
通过国服 Battle.net 启动游戏，选择 Windowed (Fullscreen)，在主菜单或单人战役中运行：

```powershell
python -B sc2_ultrawide.py status
python -B sc2_ultrawide.py apply --no-helper
```

`status` 只读。`apply --no-helper` 修改当前进程内存与窗口，HUD 仅处理一次，不启动助手。
换任务后若 HUD 恢复默认，可再次执行该命令。不要并行运行多个游戏实例或多个补丁命令。

上游的 `apply`（不带参数）会启动独立后台助手，在每次任务加载后重设 HUD；
它不是开机服务，随游戏退出或宽屏状态结束而停止。一次实际换关自动修复已验证，其他皮肤和长期运行仍需更多测试。

```powershell
python -B sc2_ultrawide.py revert
```

`revert` 会调整窗口并可能写 HUD；重启游戏也可撤销本工具的内存修改。
本工具不修改游戏 exe、存档或配置，不修改 Windows 桌面分辨率，不自动提权。

## 验证范围与限制

- 增加 98370 的窗口比例常量模板，拒绝旧模板误命中的 -1.0。
- HUD 虚表扫描兼容实际观察到的一条插入指令，新增节范围与方法指针校验。
- 已验证标准 CLI 的单次 HUD 修复；窗口已为全屏时不重设窗口或 client API 标志。
- 任务内观察到上游用于检查尺寸接受情况的字段为 0×0；其语义尚需核实。仅当窗口已占满超宽显示器且当前 HUD 实例通过校验时，允许跳过窗口调整、直接修复 HUD 或启动助手；其他情况下仍拒绝异常尺寸。
- 已在一个神族战役场景实测 3440×1440，用户反馈整体效果可用。
- 血条偏宽尚未修复。后续只读调查找到相关类型与单位对象，但未确认可验证的宽度字段，因此没有进行血条缩宽试写；也未做相同场景的 16:9/21:9 对照。
- 上游的 HUD 公式仅横向拉伸底部中间模型，不能视为所有 UI 元素均已适配。
- 已实测一次跨任务自动修复；其他种族皮肤、重新启动游戏和长期稳定性尚未验证；未对 build 97563 重新实机回归。

## 风险

程序修改运行中的客户端内存，单人内容也不能保证账号安全，可能导致崩溃或封禁。
不要用于多人对战。项目不检查当前玩法、不规避反作弊，也不承诺官方许可。

## 开发验证

### 打包自带 Python 的 Portable EXE

以下步骤只供开发者使用，玩家无需安装打包依赖：

```powershell
python -m venv .venv-build
.\.venv-build\Scripts\python.exe -m pip install -r requirements-build.txt
.\build-portable.ps1
```

输出为 `dist/onefile/SC2-Ultrawide-Portable.exe`。`-Mode onedir` 可生成文件夹版本供排查。
打包使用 PyInstaller，不请求管理员权限，不创建服务或自启动项。源码命令行的用法不变。

```powershell
python -B -m unittest test_compatibility -v
```

测试仅使用合成字节和模拟对象，不连接游戏。实测记录不包含在源码仓库中，避免提交本机内存地址和路径日志。

## 上游与贡献

感谢 [PKDT-93/sc2-ultrawide](https://github.com/PKDT-93/sc2-ultrawide) 的实现与研究。[国服适配草稿 PR](https://github.com/PKDT-93/sc2-ultrawide/pull/1) 尚未合并，本仓库预览发布不代表原作者或 Blizzard 官方认可。
