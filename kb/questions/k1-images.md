---
title: 科目一课程配图账
updated: 2026-09-04
---

# 科目一课程配图账

课里用的图在 `public/images/k1/`，网页写成 `/images/k1/文件名`。  
标准标是按国标样子画的矢量图，进 git。交警手势从电子技巧 PDF 第 20–22 页（印「第20/35」到「第22/35」）整行两帧一起裁，进 git。

完整图标扫描件仍在 `kb/raw/…/最新驾考图标.pdf`（约 465 张），不上站、不进 git。模拟考 134 张情景图在 `kb/raw/bank/k1/images/`，不进课。

| 文件 | 节 | 图上是什么 | 来源 |
|---|---|---|---|
| `stop.svg` | 05 | 八边形停车让行 | 自绘 |
| `yield.svg` | 05 | 倒三角减速让行 | 自绘 |
| `no-pass.svg` | 05 | 红圈禁止通行 | 自绘 |
| `no-entry.svg` | 05 | 红圈白杠禁止驶入 | 自绘 |
| `no-long-park.svg` | 04 · 05 | 一杠禁止长停 | 自绘 |
| `no-park.svg` | 04 · 05 | 叉禁止停车 | 自绘 |
| `speed-max.svg` | 04 | 红圈最高时速 | 自绘 |
| `speed-min.svg` | 04 | 蓝圈最低时速 | 自绘 |
| `speed-end.svg` | 04 | 黑杠解除限速 | 自绘 |
| `warn-triangle.svg` | 04 | 故障车警告三角 | 自绘 |
| `curve-1.svg` | 05 | 急弯 | 自绘 |
| `curve-2.svg` | 05 | 反向弯 | 自绘 |
| `curve-3.svg` | 05 | 连续弯 | 自绘 |
| `warn-ped.svg` | 05 · 07 | 注意行人 | 自绘 |
| `warn-child.svg` | 05 | 注意儿童 | 自绘 |
| `warn-bike.svg` | 05 | 注意非机动车 | 自绘 |
| `lane-bike.svg` | 05 | 非机动车道 | 自绘 |
| `crosswalk.svg` | 05 · 07 | 蓝底人行横道 | 自绘 |
| `hump.svg` | 05 | 驼峰桥 | 自绘 |
| `uneven.svg` | 05 | 路面不平 | 自绘 |
| `work.svg` | 05 | 施工 | 自绘 |
| `rail.svg` | 05 · 07 | 铁路道口 | 自绘 |
| `mountain-road.svg` | 05 | 傍山险路 | 自绘 |
| `rocks.svg` | 05 | 注意落石 | 自绘 |
| `embankment.svg` | 05 | 堤坝路 | 自绘 |
| `ferry.svg` | 05 | 渡口 | 自绘 |
| `meet.svg` | 05 · 07 | 会车让行（粗箭头先走） | 自绘 |
| `high-beam.svg` | 06 | 远光（平射） | 自绘 |
| `low-beam.svg` | 06 · 07 | 近光（斜下） | 自绘 |
| `fog-front.svg` | 06 | 前雾灯绿 | 自绘 |
| `fog-rear.svg` | 06 | 后雾灯黄 | 自绘 |
| `master-light.svg` | 06 | 灯光总开关 | 自绘 |
| `position-light.svg` | 06 | 示廓灯成对 | 自绘 |
| `brake.svg` | 06 | 制动 `(!)` | 自绘 |
| `park-brake.svg` | 06 | 手刹 `(P)` | 自绘 |
| `police-stop.jpg` | 06 | 停止一组：正面 + 侧面，左臂向上直伸 | 电子技巧 p21（第20/35）上行两帧 |
| `police-straight.jpg` | 06 | 直行一组：两臂平伸 → 右臂向左摆 | 电子技巧 p21 中行两帧 |
| `police-slow.jpg` | 06 | 减速一组：右臂平伸掌心向下 → 往下摆 | 电子技巧 p21 下行两帧 |
| `police-wait-turn.jpg` | 06 | 待转一组：左臂靠近伞杆，再向下摆 | 电子技巧 p22（第21/35）上行两帧 |
| `police-change.jpg` | 06 | 变道一组：右臂前伸 → 摆到胸口 | 电子技巧 p22 中行两帧 |
| `police-left.jpg` | 06 | 左转一组：右臂平伸，左臂再摆 | 电子技巧 p22 下行两帧 |
| `police-right.jpg` | 06 | 右转一组：左臂平伸，右臂再摆 | 电子技巧 p23（第22/35）中行两帧 |
| `signs-warn-1.jpg`–`4.jpg` | 05 | 警告标志汇总 | `最新驾考图标.pdf` 第 5–8 页 |
| `signs-ban-1.jpg`–`3.jpg` | 05 | 禁令标志汇总 | 同上第 1–3 页 |
| `signs-guide.jpg` | 05 | 指示标志汇总 | 电子技巧第 27/35 页 |

没有 `police-pull-over.jpg`。电子技巧第 20–22 页只有停 / 直 / 减速 / 待转 / 变道 / 左转 / 右转，靠边停车只写文字。

重出图：`python3 scripts/publish-k1-course-images.py`（手势裁图要能读到电子技巧 PDF，或已有 `/tmp/k1-tips/p21.png`–`p23.png`）。
