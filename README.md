# wy-lanqiao-paths

作者署名：梧焰。

这个项目把我公开过的两份备赛笔记整理成可检索的 Markdown：Java 组方向、智能体开发方向。内容来自我从第一次参赛到后来拿到省一、国三的过程中，自己整理和踩过的坑。

> 文中出现的赛事名称仅用于说明学习内容来源。本项目是个人学习笔记，与赛事主办方无隶属、授权或官方背书关系。

## 这是什么

- [Java 组：从省一到国奖](docs/java-group/00-主文档.md)：认识赛项、环境准备、真题研究、Java 基础笔记、省一与国奖两个阶段的做法。
- [智能体开发：从 0 到国奖](docs/agent-dev/00-课程大纲.md)：赛项说明、官方文档解读、两届样题各跑一遍、赛题模板分析与备赛计划。

两份内容都保留了我原来的说话方式，没有改成书面语；同一套方法在两个场景里各写一遍，是为了对照差异，不是重复。

## 目录

```
docs/
├── java-group/       Java 组免费课程正文
├── agent-dev/        智能体开发免费课程正文
└── design/           配图风格配方（色值、坐标、风控红线）
scripts/
├── blue-tech-poster/ 蓝色科技风海报生成脚本
└── paper-learning-path/ 纸质学习路径图生成脚本
assets/               宣传图与封面
```

![海报-智能体开发](assets/海报-智能体开发.png)

![路径图-Java组](assets/路径图-Java组.png)

## 免费与付费

本仓库公开的是免费内容：课程正文、大纲、配图和绘图脚本。

整理版资料、系统课程、陪跑服务等付费产品**不在本仓库中**，只在这里留一个介绍：[付费版本说明](docs/付费版本说明.md)。购买入口：`TODO：填写你的付费课链接`。

## 本地生成配图

需要 Python 3 + `Pillow` + `numpy`，字体使用 Windows 自带的微软雅黑。

```bash
python scripts/blue-tech-poster/gen.py --out ./poster.png
python scripts/paper-learning-path/gen.py --out ./path.png
```

换课程标题、标签和数据，只改对应脚本同目录下的 `content.json`，不要改坐标。

## 许可

- 文档与配图（所有 Markdown 和 `assets/`）：[CC BY-NC-SA 4.0](LICENSE-DOCS)。可分享、可改编，需署名、禁止商用、衍生作品同协议。
- 代码（`scripts/`）：[MIT](LICENSE-CODE)。可用于商业项目。

他人不得把本仓库的免费文档直接拿去售卖或作为付费课程主体。作者本人保留全部著作权，并可另行提供商业授权。

## 交流

发现错别字、事实过期或链接失效，欢迎提 Issue。Pull Request 请只改一处问题，别顺手润色语气——这是原作者的表达习惯。
