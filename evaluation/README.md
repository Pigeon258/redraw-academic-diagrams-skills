# 正式使用双 Skill 对照

本目录用于比较：

- `redraw-academic-diagrams`：质量基线；
- `redraw-academic-diagrams-fast`：效率优先。

不为评分额外构造测试图。每个真实任务只使用用户自然选择或轮换分配的一个 Skill，并记录：

- 首个可用 PPTX 时间；
- 接受结果的总时间；
- 用户自行修改时间；
- AI 反馈轮次与追加时间；
- 正式和实际交付状态；
- fixlist 数量；
- 最终是否接受；
- 重复或高影响缺陷。

## 记录

```powershell
python record_field_run.py `
  --store runs.jsonl `
  --task-id task-001 `
  --skill redraw-academic-diagrams-fast `
  --version 0.1.0 `
  --diagram-class architecture `
  --builder artifact-tool+powerpoint `
  --first-minutes 18 `
  --total-minutes 24 `
  --user-edit-minutes 2 `
  --ai-revision-minutes 4 `
  --feedback-rounds 1 `
  --practical-state "FAST PASS WITH FIXLIST" `
  --formal-state "NEEDS REVISION" `
  --fixlist-count 1 `
  --final-accepted
```

任务 ID 必须匿名化；不要写入姓名、论文标题、聊天账号、绝对路径或原图内容。

## 汇总

```powershell
python summarize_field_runs.py --store runs.jsonl --output summary.json
```

至少积累若干真实任务后再比较。工具链、图复杂度、网络和用户等待时间均是混杂因素，不能只看平均首轮时间。
