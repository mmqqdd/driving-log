# 我的驾考笔记

> 练完、刷完、听完教练一句话，对着 Cursor 说出来就行。

- 仓库：[Gitee](https://gitee.com/mengqiangding/driving-log) · [GitHub](https://github.com/mmqqdd/driving-log)
- 线上：https://driving-log-d25.pages.dev

## 本地运行

```bash
npm install
npm run dev
```

打开 http://localhost:5173

## 怎么用

在 Cursor 里打开这个仓库，直接说话：

| 说什么 | 会发生什么 |
|---|---|
| 今天练倒车入库，右库后视镜对上线就打方向 | 在 `journal/` 记练车日志，并回写到科目二笔记 |
| 科目一这题又错了：黄灯亮时已过停止线可以继续 | 记进科目一易错 |
| 教练说坡道起步离合抬到半联动停三秒再给油 | 写进对应科目的要点 |
| 下周三约了科目二 | 更新档案里的考试日期 |

第一次使用前，先说清楚：在哪考、C1 还是 C2、现在到哪一科。档案在 `system/profile.md`。

## 结构

```
system/     档案、怎么用这套笔记
subjects/   科目一到四，易错 + 口诀 + 失败点
journal/    练车 / 刷题日志
.cursor/skills/   drive-log（说一句就记下来）
```

新增 markdown 文件后侧边栏会自动更新，不需要改配置。

## 部署

线上在 [Cloudflare Pages](https://driving-log-d25.pages.dev)，练车场上用手机翻笔记。

代码在两个远端：Gitee（`origin`）给国内看仓库，GitHub（`github`）备用。一次推两个：

```bash
git push all main
```

站点目前是直接上传。记完新笔记后可以说「部署一下」，会重新构建并发布。
