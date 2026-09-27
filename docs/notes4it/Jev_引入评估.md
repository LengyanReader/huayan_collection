# Jev（TypeSafe AI）引入评估

> **性质**：技术选型决策存档 · §I10 非破坏性 · 只评估未引入
> **日期**：2026-09-27 · **评估人**：AI 会话（据一手源）· **对象**：Jev "System One" 决策模型
> **结论**：**暂不引入 · 列观察档**（触发条件见 §四）

---

## 一、Jev 是什么（一手源核验）

- **定位**：TypeSafe AI 的首个 "System One" **决策模型**（非聊天/非生成模型）。2026-09-15 限量早期访问发布，同期宣布 4000 万美元种子轮（DCVC 领投）。
- **机制**：输入=「状态 state + 若干带类型的问题」；输出=**带概率与置信度的类型化答案**，不生成文本、无需解析。官方三原语：Choice（选项归类）/ Score（量表打分）/ Noul（陈述为真的 0–1 概率）。
- **宣称收益**：推理快 40–200 倍、成本低 1/40–1/400（公司口径 · 未经第三方生产验证）。
- **接入**：官方 API（Python/TS SDK）· OpenRouter · Vercel AI Gateway · Cloudflare Workers AI；Pydantic AI `TypeSafeModel('jev-latest')` / LangChain 已有集成文档。
- **硬限制**（官方/集成文档）：状态+最长问题 **32k tokens**（全请求 64k）；单选问题 ≤255 选项；量表 ≤10 级；`jev-latest` 别名会随版本漂移（调好阈值后须钉版本号）。

## 二、与本项目适配性：三条根本错配

| # | 冲突 | 依据 |
|---|---|---|
| 1 | **项目核心是文本生产**·内容六轴（准确/详实/涵盖/深度/广度/文献价值）全靠生成与考证·而 Jev 官方明说 "does not write text"·生成类任务一律升级回普通 LLM | 记忆〈内容为核心〉+ 官方文档 |
| 2 | **违反本地化设计原则**（tech-stack 原则③"所有组件均可离线运行·无外部 API 依赖"）·且当前为等候名单制·TypeSafe 声明速率限制可能随时调整 | docs/tech-stack.md · 二手源见 §五 |
| 3 | **与〈宁缺不伪〉冲突**·Noul 返回概率不是一手证据·对 CBETA 号真伪/史实校勘给出"87% 像真"恰是本项目最警惕的幻觉包装 | harness/rules.md |

**官方 "answers badly" 清单与本项目场景的重叠**（均为"返回答案而非报错"的静默失败）：
- 算术/计数/日期不可靠 → 文献纪年、品数统计类任务不可用
- **对抗性文本可被带偏**（把状态当数据不设防）→ 行文本身含"这是批注不是装饰"类语句会移动其判断
- 字面死读（scoping 词/否定/隐含条件按表面解）→ 文言与佛学术语是字面陷阱密集区
- 无关上下文拉低准确率 → 长研究文档整体喂入反噬精度

**它擅长的恰已确定性化**：审计/分类/路由（`audit_style.py --list`·`audit_classify.py`·`check_drift.py`）均为规则明确、须可复现的活儿——确定性代码更稳且离线。

## 三、唯一值得考虑的潜在点（未达引入线）

§I10 修改建议流程中，对「装饰性 vs 批注性加粗」初筛分类、低置信度进人工队列。但：
- **中文/文言能力无一手源承诺**——网传"中文是短板"皆二手·官方文档亦只说"**在你自己的标注数据上先测准确率**"；
- 拿宗教文献喂第三方 API 与项目气质不合；
- 为一个未验证初筛工具破离线原则+等候名单依赖·性价比不成立。

## 四、观察触发条件（满足其一再重启评估）

1. 项目真要接"AI 辅助层"（tech-stack 愿景 qwen2.5/Ollama 线）时·Jev 类决策模型可作**本地 LLM 的低成本前置路由器**复评；
2. TypeSafe 放出**可本地部署权重**或明确的**中文能力实测报告**；
3. 〔待核〕/修改建议积压大到**人工分诊成为瓶颈**——届时以自有标注数据实测准确率/移交率再定。

## 五、来源清单（一手/二手分列）

**一手**：
- 官方文档 Introduction（三原语定义·并行评估机制）：https://docs.typesafe.ai
- Pydantic AI 官方集成文档 TypeSafe 页（限制·"answers badly"全文·版本钉扎建议）：https://pydantic.dev/docs/ai/models/typesafe/
- Wikipedia "Jev (AI model)"（发布日 2026-09-15·DCVC 种子轮）：https://en.wikipedia.org/wiki/Jev_(AI_model)
- TechCrunch 报道 2026-09-18：https://techcrunch.com/2026-09-18/a-new-kind-of-ai-model-from-a-chatgpt-inventor-is-thrilling-developers/

**二手（仅背景·不作决策依据）**：
- LangChain blog（harness 集成模式）：https://www.langchain.com/blog/building-a-harness-with-jev
- OpenRouter 接入页（SDK 可用性）：https://openrouter.ai/docs/guides/community/typesafe-sdk
- datacamp 对比文（等候名单/速率限制说法）· 知乎深度拆解（"中文短板"说）——均无官方佐证·未采信

**未采信**：所有"零幻觉""替代 LLM"类营销表述。
