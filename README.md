# 星际争霸 II 超宽屏工具 · 国服 98370

简体中文 | [上游项目 / English](https://github.com/PKDT-93/sc2-ultrawide)

基于 PKDT-93/sc2-ultrawide 的国服适配与便携预览分支，非 Blizzard 官方补丁。

## 下载

- [血条修复 Portable 预览版 1：便携 ZIP](https://github.com/AMglimmer/sc2-ultrawide/releases/download/cn-98370-healthbars-preview.1/sc2-ultrawide-cn-98370-healthbars-preview.1.zip)
- [EXE、源码、校验值及完整发布说明](https://github.com/AMglimmer/sc2-ultrawide/releases/tag/cn-98370-healthbars-preview.1)
- [保留旧 Portable preview.3（不包含血条修复）](https://github.com/AMglimmer/sc2-ultrawide/releases/tag/cn-98370-portable-preview.3)

预览版自带 Python/Tk，解压后双击 `SC2-Ultrawide-Healthbars-Preview.exe`，无需安装 Python。

**已知问题：运输装载格仍有比例问题，例如折跃棱镜血条下方的载客格子。本版未修复装载格，不代表全部头顶 UI 都已适配。**

## 使用

验证环境为 Windows x64、国服加载 build 98370、3440×1440、窗口化全屏、单人战役。

1. 通过国服 Battle.net 启动游戏并设置窗口化全屏。
2. 打开工具，根据需要点击“启用超宽 + 自动修复 HUD”。
3. 进入战役，让单位状态条可见，再单独点击“启用血条比例修复（实验）”。
4. 保持工具窗口打开，血条修复会跟随任务切换；点击停止或正常关闭窗口会撤回这项修复。原有 HUD 助手仍按旧机制运行到游戏退出。重启游戏后需重新启用。

只打开窗口不访问游戏内存。血条修复保留格数、颜色和纵向位置，并把已识别普通/组合分段条的格体、黑边和间距一起横向缩到约 74.42%。装载格、未分段条及未知绘制路径未修复，其他 build/分辨率/渲染器未验证。

## 验证与风险

28 项离线测试通过，含不连接游戏的隔离原生测试子进程；实际测试包含受伤变色、换关、普通/组合状态条和 GUI 启停。打包 EXE 一次 15 秒测试处理 1408 帧、41667 条状态组、跳过 0 次，结束后恢复校验通过。用户确认启停正常、组合条比例自然；长期稳定性和所有内容仍未全面验证。

血条功能使用临时原生绘制回调，比原有 HUD 参数修改更深入。游戏原有 EXE、配置、存档和 Battle.net 文件不修改，不自动提权、不创建服务或开机启动、不绕过反作弊，但仍存在崩溃及账号风险。请勿用于多人对战，单人内容也不能保证账号安全。

## 源码与贡献

本仓库 `main` 是中文文档入口，适配源码位于下列分支/标签，请勿把 main 中的上游程序当成预览版适配源码。

- [国服适配与血条源码分支](https://github.com/AMglimmer/sc2-ultrawide/tree/codex/cn-build-98370)
- [本次发布标签源码](https://github.com/AMglimmer/sc2-ultrawide/tree/cn-98370-healthbars-preview.1)
- [中文使用说明](https://github.com/AMglimmer/sc2-ultrawide/blob/cn-98370-healthbars-preview.1/README.healthbars-preview.zh-CN.md)
- [原生回调审阅说明](https://github.com/AMglimmer/sc2-ultrawide/blob/cn-98370-healthbars-preview.1/NATIVE_HEALTHBARS.md)
- [提交给原作者的 PR #1](https://github.com/PKDT-93/sc2-ultrawide/pull/1)（尚未合并）

感谢原作者的实现与研究。Fork 预览发布不代表原作者或 Blizzard 官方认可。
