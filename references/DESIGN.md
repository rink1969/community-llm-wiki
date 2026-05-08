# CAiOS V1.0 设计文档参考

## 系统定位

基于「共在 / 涌现 / 逍遥 / 因作而是」的个人和社区世界观，Community OS 是一个生成式社区操作系统，以 Event 为唯一事实源，通过关系网络（Graph）呈现社区网络结构，并以 Agent 提供解释与导航能力，并以 H5 或 App 提供 Tools。这是一款为零代码基础的社区主理人准备的社区操作系统产品。

## 系统哲学

### 共在（Relation-first）
- 社区的基础不是个体，而是关系
- 人在关系中被定义
- 社区是关系网络，而非人集合

### 涌现（Emergence）
- 社区的价值来自协作，而非预设设计
- 作品 / 项目 / 内容来自关系互动
- 系统不预设结果，只记录生成

### 逍遥（Structural Freedom）
- 个体在网络中具备自由生成关系与切换角色的能力

### 因作而是（Becoming-through-Action）
- 人不是身份，而是在持续行动（Event）中被生成的结构
- Event 先于身份
- 做什么，成为什么

## 系统结构图

```
输入（群聊/私聊/H5）
    ↓
Event Parser
    ↓
Event
    ↓
Person + Relationship
    ↓
Graph + State
    ↓
Agent
    ↓
Text + Links
    ↓
用户
    ↓
Event（循环）
```

## 核心数据结构

### 本体层（Ontology）

只有三类实体：Community / Person / Event

- Community → 意义容器
- Person → 节点
- Event → 关系发生器

### 不存在的东西（非常重要）

以下全部不属于本体层：
- Relationship（计算出来）
- Graph（计算出来）
- State（计算出来）
- reputation（计算出来）
- cohesion（计算出来）

## 关系密度计算

| 关系类型 | 含义 | 单次 Event 贡献 |
|---------|------|----------------|
| initiator ↔ co_creator | 共同建构事件结构 | +3.0 |
| co_creator ↔ co_creator | 核心协作执行 | +2.5 |
| initiator ↔ participant | 场域创建 + 进入 | +1.5 |
| co_creator ↔ participant | 局部协作接触 | +1.2 |
| participant ↔ participant | 共在出现 | +1.0 |

累积规则：`density(A,B) = Σ(Event contribution)`

关系类型划分：
- < 3: weak
- 3–10: normal
- > 10: strong

## 社区状态指标

### 共在（Co-presence）
```
co_presence = (E / N) + C
E = relationship edges 总数
N = person 数量
C = clustering_factor = number_of_clusters / N
```

### 涌现（Emergence）
```
emergence = A / E
A = artifacts 数量
E = events 总数
```

### 逍遥（Xiaoyao）
个体级：
```
xiaoyao(person) = 0.4 * IR + 0.3 * RE + 0.3 * NR
IR = initiator_events / total_events
RE = entropy(initiator, co_creator, participant)
NR = new_connections / total_connections
```

社区级：`community_xiaoyao = average(xiaoyao(person))`

## H5 产品结构

1. Graph（首页）— 关系图谱
2. Person（核心页）— Event 轨迹、关系网络、作品
3. Community（公共页）— 三指标状态、Event 流、活跃成员
4. Tools（工具集）— 活动记录、项目记录、文档/wiki、作品上传
5. Personal Space（个人空间）— 我的 Event、我的关系网络、私聊 Agent

## Agent 层

定位：Community OS 的「认知与入口层」

功能：
1. 解释 — 关系、人、状态、Event
2. 引导 — 推荐人、推荐活动、推荐共创
3. 入口生成 — Person link、Event link、Graph link、Tool link

不做：
- 不运营社区
- 不决策
- 不控制系统

输出：text、link（H5 跳转）

## 系统本质总结

❌ 不是：社交平台、活动系统、CRM、AI 运营工具
✔ 是：「以 Event（作）为本体的关系网络型社区操作系统」

## 最终一句话定义

Community OS 是一个以 Event 为唯一事实源、以 Graph 为呈现方式、以 Person 为结构化节点，并通过 Agent 提供解释与导航的「因作而是」的关系网络型社区操作系统。
