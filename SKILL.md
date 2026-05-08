---
name: community-llm-wiki
description: "Community AI-OS (社区土地神): Event-driven community knowledge graph with co-presence, emergence, and structural freedom metrics."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [community, knowledge-graph, event-driven, wiki, collaboration, social-network]
    category: community
    related_skills: [llm-wiki, obsidian, notion]
---

# Community AI-OS (社区土地神)

基于「共在 / 涌现 / 逍遥 / 因作而是」哲学，Community AI-OS 是一个以 **Event 为唯一事实源**、以 **Graph 为呈现方式**、以 **Person 为结构化节点**，并通过 Agent 提供解释与导航的「因作而是」的关系网络型社区操作系统。

受 [Karpathy 的 LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 启发，但面向社区协作场景重新设计：
- **LLM Wiki** 是知识积累系统（信息→理解→关联）
- **CAiOS** 是关系生成系统（行动→关系→涌现）

## 系统哲学（四象世界观）

| 概念 | 含义 | 在系统中的体现 |
|------|------|---------------|
| **共在 (Co-presence)** | 社区的基础不是个体，而是关系。人在关系中被定义。 | 关系图谱（Graph） |
| **涌现 (Emergence)** | 社区的价值来自协作，而非预设设计。作品/项目来自关系互动。 | Event → Artifact 转化率 |
| **逍遥 (Structural Freedom)** | 个体在网络中具备自由生成关系与切换角色的能力。 | 角色熵 + 发起能力 + 网络扩展 |
| **因作而是 (Becoming-through-Action)** | 人不是身份，而是在持续行动（Event）中被生成的结构。 | Event 先于身份 |

## 系统结构

```
输入（群聊/私聊/H5/外部工具）
    ↓
Event Parser（解析为结构化 Event）
    ↓
Event（唯一事实源）
    ↓
Person + Relationship（计算生成）
    ↓
Graph + CommunityState（计算生成）
    ↓
Agent（解释 + 导航）
    ↓
Text + Links（输出给用户）
    ↓
用户行动 → 新 Event（循环）
```

## 核心数据结构

### 本体层（Ontology）—— 只存三类实体

**Community（社区）** — 意义容器
- `id`, `name`, `values[]`, `manifesto`, `tags[]`, `founders[]`, `links{}`

**Person（成员）** — 节点
- `id`, `profile{}`, `skills[]`, `interests[]`, `links{}`, `works_input[]`
- `event_refs[]` — 参与事实（引用 Event，不存 Event 本体）
- `external_inputs[]` — 外部输入记录

**Event（事件协作）** — 关系发生器
- `id`, `timestamp`, `type` (activity|project)
- `metadata{title, description}`
- `initiator`, `co_creators[]`, `participants[]`
- `artifacts[]` — 协作产出（photo/video/doc/report/link）
- `external{}` — 外部来源
- `source{}` — 数据来源

### 不存在于本体层（计算生成）

- Relationship（关系密度）
- Graph（关系网络）
- State（社区状态）
- Reputation（声誉）
- Cohesion（凝聚力）

## 关系密度计算

### 单次 Event 贡献值

| 关系类型 | 含义 | 单次贡献 |
|---------|------|---------|
| initiator ↔ co_creator | 共同建构事件结构 | +3.0 |
| co_creator ↔ co_creator | 核心协作执行 | +2.5 |
| initiator ↔ participant | 场域创建 + 进入 | +1.5 |
| co_creator ↔ participant | 局部协作接触 | +1.2 |
| participant ↔ participant | 共在出现 | +1.0 |

### 累积规则

```
density(A, B) = Σ(Event contribution across all shared events)
```

### 关系类型划分

| density 区间 | 类型 |
|-------------|------|
| < 3 | weak |
| 3–10 | normal |
| > 10 | strong |

## 社区状态指标（三指标）

### 1. 共在 (Co-presence) — 社区是否「连起来了」

```
co_presence = (E / N) + C

E = relationship edges 总数
N = person 数量
C = clustering_factor = number_of_clusters / N
```

### 2. 涌现 (Emergence) — 社区是否「产生了东西」

```
emergence = A / E

A = artifacts 总数（来自 Event.artifacts）
E = events 总数
```

### 3. 逍遥 (Xiaoyao) — 个体能否自由生成关系

个体级：
```
xiaoyao(person) = 0.4 * IR + 0.3 * RE + 0.3 * NR

IR = initiator_events / total_events          （发起能力）
RE = entropy(initiator, co_creator, participant) （角色多样性）
NR = new_connections / total_connections      （网络扩展）
```

社区级：
```
community_xiaoyao = average(xiaoyao(person))
```

## 使用方式

### 初始化社区

```bash
# 创建社区数据目录
mkdir -p ./my-community/{events,people,community,state,graph}

# 使用脚本初始化
python scripts/community_wiki_init.py --name "我的社区" --values "共在,涌现,逍遥" --output ./my-community
```

### 录入 Event

```bash
# 从 JSON 文件批量导入 Events
python scripts/community_wiki_ingest.py --community ./my-community --events events.jsonl

# 或单条录入
python scripts/community_wiki_ingest.py --community ./my-community --event '{
  "type": "activity",
  "initiator": "alice",
  "co_creators": ["bob"],
  "participants": ["carol", "dave"],
  "metadata": {"title": "周末共创会"}
}'
```

### 计算图谱与状态

```bash
# 计算关系图谱和社区状态
python scripts/community_wiki_compute.py --community ./my-community --output ./my-community/state

# 输出：graph.json + state.json
```

### 查询与导航（Agent 层）

```bash
# 查询社区状态
python scripts/community_wiki_query.py --community ./my-community --query "state"

# 查询个人档案
python scripts/community_wiki_query.py --community ./my-community --query "person" --id alice

# 查询关系网络
python scripts/community_wiki_query.py --community ./my-community --query "graph" --depth 2

# 推荐连接
python scripts/community_wiki_query.py --community ./my-community --query "recommend" --for alice
```

## 目录结构

```
my-community/
├── community.json          # Community 本体
├── events/
│   ├── event_001.json      # Event 原始数据
│   ├── event_002.json
│   └── ...
├── people/
│   ├── alice.json          # Person 数据（含 event_refs）
│   ├── bob.json
│   └── ...
├── state/
│   ├── graph.json          # 计算出的关系图谱
│   └── state.json          # 社区三指标状态
└── log.md                  # 操作日志（append-only）
```

## 与 LLM Wiki 的对比

| 维度 | LLM Wiki | CAiOS |
|------|----------|-------|
| 核心单元 | Source（信息源） | Event（行动/协作） |
| 连接逻辑 | 语义关联（概念相似） | 关系密度（协作事实） |
| 时间性 | 可静态积累 | 必须持续更新（Event 驱动） |
| 主体 | 知识（客观） | 人（在关系中生成） |
| 产出 | 理解、洞察 | 作品、项目、关系网络 |
| 哲学 | 认知论 | 存在论（因作而是） |

## 脚本工具

- `scripts/community_wiki_init.py` — 初始化社区目录结构
- `scripts/community_wiki_ingest.py` — 导入 Event 数据
- `scripts/community_wiki_compute.py` — 计算关系图谱与社区状态
- `scripts/community_wiki_generate.py` — **生成 Markdown Wiki**（核心输出）
- `scripts/community_wiki_query.py` — 查询接口：state / person / graph / recommend
- `scripts/community_wiki_export.py` — 导出：GEXF / Cytoscape / Markdown / CSV
详见各脚本的 `--help` 输出。

## 最终输出：Markdown Wiki

`community_wiki_generate.py` 是核心输出脚本，它将社区数据生成为一组互相关联的 **Markdown 文件**，形成完整的社区知识图谱 Wiki：

```
wiki/
├── index.md              # 索引页（总目录）
├── community.md          # 社区主页（价值观 + 三指标 + 活跃成员）
├── graph.md              # 关系图谱（所有关系边 + 密度 + 共同 Event）
├── log.md                # 操作日志
├── people/
│   ├── alice.md          # 个人页（逍遥指数 + Event 记录 + 关系网络）
│   ├── bob.md
│   └── ...
└── events/
    ├── evt_001.md        # Event 页（参与者 + 角色 + 协作产出）
    ├── evt_002.md
    └── ...
```

### 特性

- **[[wikilinks]] 互相关联**：所有页面通过 `[[page|title]]` 互相链接
- **YAML frontmatter**：每页都有结构化元数据，支持 Obsidian Dataview 查询
- **表格化指标**：社区状态、个人逍遥指数、关系密度全部用表格呈现
- **Obsidian 原生兼容**：直接作为 Obsidian vault 打开，Graph View 可视化关系网络
- **GitHub 友好**：标准 Markdown，GitHub 可渲染
- **纯文本、无数据库**：任何文本编辑器均可阅读和编辑

## 扩展建议

1. **数据源接入**：接入微信群聊、Discord、Notion、GitHub 等，通过 Webhook 或 API 自动解析为 Event
2. **可视化**：使用 D3.js / Cytoscape.js 渲染 Graph，颜色编码关系密度
3. **Agent 增强**：接入 LLM，实现自然语言查询、智能推荐、社区诊断
4. **H5/App 入口**：将 Graph、Person、Community State 封装为移动端产品

## 设计原则

1. **Event 是唯一事实源** — 一切从 Event 推导，不预设关系
2. **只存 Raw Data，不存计算结果** — Relationship/Graph/State 实时计算
3. **关系先于身份** — 人是在 Event 中生成的，不是预先定义的
4. **涌现不设计** — 系统只记录生成，不控制产出
5. **开放系统** — 外部工具产生的协作也应映射为 Event

## 参考

- [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- 社区土地神 CAiOS V1.0 完整设计文档
