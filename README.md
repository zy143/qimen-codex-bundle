# 奇门 Skill · Codex 一体化交付包 v3.1

**唯一执行方法：时家转盘奇门拆补法。**

从 [START_HERE.md](START_HERE.md) 开始；首次提示词：[prompts/01_START.md](prompts/01_START.md)。

| 入口 | 用途 |
|---|---|
| [CODEX_PROMPTS.md](CODEX_PROMPTS.md) | 首次执行、续跑、独立审查三种提示词 |
| [taskpack/FIRST_BATCH.md](taskpack/FIRST_BATCH.md) | 首批6组19卡 |
| [taskpack/TASKS.md](taskpack/TASKS.md) | 68个父任务、204张子卡，196必做/8可选 |
| [taskpack/reference/v3/PLAN.md](taskpack/reference/v3/PLAN.md) | 当前完整开发计划 |
| [taskpack/reference/v3/CHAIBU_SPEC.md](taskpack/reference/v3/CHAIBU_SPEC.md) | 拆补法研究规范与边界 |
| [BUNDLE_CONTENTS.md](BUNDLE_CONTENTS.md) | 全部输入文件的整理位置 |
| [bundle_checks/REPORT.md](bundle_checks/REPORT.md) | 本轮实际交付复验结果 |

最新执行资料已解压到taskpack，不必再解开历史ZIP。原始附件在sources，既往所有交付按原文件名保留在archive/deliverables。
这是资料与任务执行环境的交接包：不含完整生产排盘引擎、不含完整五批典籍，不代表204张卡已经实施。任务定义和原文件未改；新增入口只解决目录、指令和交付完整性。

```bash
python verify_bundle.py
python taskpack/taskctl.py --project-root . validate
python taskpack/taskctl.py --project-root . next --limit 10
```
本包没有安装或自动运行外部程序，没有替你提交远程仓库。后续产品开发在本根目录进行，详情见START_HERE。
