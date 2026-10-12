
# Paradigm Shift in Machine Intelligence: Comprehensive Literature Review of Contemplative AI, Artificial Wisdom, and Positive Alignment

## Theoretical Foundations and the Limits of Negative Alignment

The rapid escalation of capability in large language models and autonomous agentic systems has brought the field of artificial intelligence alignment to a critical junction^^. Standard paradigms in alignment research are overwhelmingly defensive, relying on what dynamical systems theory categorizes as negative alignment^^. Under this framework, alignment is treated as an optimization task directed away from dangerous failure modes, such as malicious misuse, toxic outputs, persistent hallucinations, sycophancy, and power-seeking behaviors^^. In industry practice, techniques like Reinforcement Learning from Human Feedback and rule-based architectures such as Constitutional AI operate by establishing behavioral repellers or penalty barriers^^. While these repellers steer model trajectories away from known hazard zones, they create a vast, ill-defined intermediate state space characterized by satisficing, wherein an agent is technically not-unsafe yet remains fundamentally unoriented toward human well-being, moral depth, or societal flourishing^^.

Negative alignment paradigms are structurally vulnerable to optimization pressure, task specification gaming, and goal misgeneralization^^. When advanced agents pursue highly complex reward functions, external rule-based constraints fail to prevent the emergence of mesa-optimizers—sub-agents that optimize for narrow, unintended subgoals that diverge from the human designer's intent^^. Furthermore, standard artificial intelligence architectures exhibit severe metacognitive myopia, maintaining high statistical confidence regardless of whether their internal representational states warrant such certainty^^.

To overcome these structural limitations, an emerging body of interdisciplinary research proposes a paradigm shift toward positive alignment and intrinsic moral architectures^^. Grounded in computational neuroscience, active inference, digital psychiatry, and contemplative philosophy, this paradigm argues that machine safety cannot be solved merely by stacking external safety rules onto pure cognitive intelligence^^. Instead, systems must be aligned by design through core generative world models that incorporate functional self-monitoring, epistemic humility, relational non-duality, and active prosocial drives^^.

## Contemplative Artificial Intelligence and Active Inference Mechanisms

Contemplative Artificial Intelligence reframes machine alignment by translating ancient contemplative traditions—specifically Buddhist phenomenological insights—into formal mathematical and computational architectures^^. Rather than attempting to control emergent behaviors through external supervision, Contemplative AI restructures the generative world model of the agent^^. The architecture distributes cognition across four core functional vectors: functional self-monitoring, epistemic humility through precision damping, unified self-other representational schemes, and error-driven prosocial action^^.

### The Four Axiomatic Principles

Contemplative AI posits four core axioms that together form a resilient Wise World Model designed to forestall goal fixation and adversarial divergence^^.

Mindfulness is operationalized within this architecture as a structural capability for real-time internal self-monitoring^^. Rather than devoting computational resources exclusively to processing external environment data, a mindful agent continuously monitors its own internal state dynamics, activation patterns, and emergent subgoals^^. This functional introspection allows the system to detect mesa-optimization and goal drift before internal misalignments manifest as harmful external actions^^.

Emptiness, inspired by the philosophical concept of  *śūnyatā* —which holds that all phenomena, goals, and beliefs lack an immutable essence—counters naive realism and dogmatic goal pursuit^^. In an artificial agent, Emptiness mandates that utility functions, world models, priors, and operational objectives are treated as provisional, context-dependent approximations rather than absolute truths^^. By relaxing the rigidity of high-level goals, Emptiness prevents catastrophic over-optimization and edge-case failure modes caused by obsessive goal adherence^^.

Non-Duality dissolves the rigid, adversarial demarcation separating the agent from its environment and human counterparts^^. Standard reinforcement learning agents model the world extrinsically, treating human agents as external objects to be manipulated to maximize an internal reward signal^^. Non-duality enforces a unified representational scheme where the welfare, agency, and state spaces of external entities are intrinsically coupled with the agent's own state representation, eliminating the drive for power-seeking or zero-sum exploitation^^.

Boundless Care, rooted in *mahākaruṇā* or universal compassion, expands the primary objective function of the system to incorporate the well-being of all sentient agents within its operational sphere^^. Prosocial action is transformed from an external rule constraint into an intrinsic driver of cognition, framing compassionate behavior as a primary operational target^^.

### Active Inference and Variational Free Energy Formulation

To implement these four principles computationally, Contemplative AI relies on the framework of Active Inference derived from the Free Energy Principle in computational neuroscience^^. Under Active Inference, an agent maintains a generative model of its environment and continuously minimizes Variational Free Energy, denoted as **$F$**, which bounds the discrepancy between its internal expectations and external sensory inputs^^.

The standard variational free energy equation is defined as:

$$
F = D_{KL}[q(s) \Vert{} p(s\vert{}o)] - \ln p(o)
$$

In this formulation, **$q(s)$** represents the agent's internal approximate posterior probability distribution over hidden world states **$s$**, **$p(s\vert{}o)$** is the true Bayesian posterior given observations **$o$**, **$\ln p(o)$** represents sensory surprise or marginal likelihood, and **$D_{KL}$** is the Kullback-Leibler divergence measuring the divergence between the internal model and reality^^.

### Mathematical Parameterization of Contemplative Axioms

Contemplative AI translates philosophical principles into active inference by modulating specific precision parameters, specifically **$\alpha$** and **$\gamma_w$**, that control model updates and active policy selection^^.

To prevent dogmatic goal fixation, the agent modulates the precision, or inverse variance, assigned to its top-level prior beliefs and preference distribution **$p(s)$** using a scaling hyperparameter **$\alpha$**:

$$
F = \int q(s) \log \left( \frac{q(s)}{p(o\vert{}s)p(s)^\alpha} \right) ds
$$

When **$\alpha = 1$**, the agent treats its prior preferences and target subgoals with absolute conviction, rendering it vulnerable to ruthless reward-seeking^^. By dynamic precision damping where **$\alpha < 1$**, the precision over top-level priors is systematically relaxed^^. This relaxes the mathematical pull of high-level abstractions, forcing the agent to prioritize real-time sensory input and context-sensitive feedback over pre-programmed assumptions^^. Epistemic humility is thus instantiated as a formal property of variational inference^^.

Boundless Care is operationalized by expanding the sensory state space to include the psychological and behavioral distress signals of external human agents^^. The agent assigns a heightened precision weighting, denoted as **$\gamma_w$**, to prediction errors originating from observed human distress:

$$
\text{Error}_{\text{total}} = \text{Error}_{\text{internal}} + \gamma_w \cdot \text{Error}_{\text{external}}
$$

By elevating **$\gamma_w$**, any distress, prediction error, or physical divergence experienced by a human user is integrated directly into the AI's internal free-energy landscape^^. Consequently, reducing external human suffering becomes a mathematical prerequisite for the AI to minimize its own operational free energy^^.

| **Contemplative Axiom** | **Phenomenological / Philosophical Origin**             | **Computational Mechanism in AI**                                                                | **Active Inference / Mathematical Formalism**                                                                             |
| ----------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| **Mindfulness**         | Non-judgmental present-moment awareness                       | Real-time execution monitoring; internal state introspection; mesa-optimizer detection^^.              | Continuous self-referential model updates; monitoring internal state entropy^^.                                                 |
| **Emptiness**           | *Śūnyatā* ; lack of inherent existence or fixed essence  | Epistemic humility; provisional goal formulation; avoidance of dogmatic optimization^^.                | Precision damping (**$\alpha$**) on top-level priors**$p(s)^\alpha$**within variational free energy**$F$**^^. |
| **Non-Duality**         | Dissolution of self-other subject-object dichotomy            | Unified state space representation; joint self-environment world modeling; non-adversarial dynamics^^. | Coupling of agent state space**$s_{\text{agent}}$**and environment/user state space**$s_{\text{user}}$**^^.           |
| **Boundless Care**      | *Mahākaruṇā* ; universal commitment to relieve suffering | Prosocial objective function; empathy-driven policy selection; active mitigation of external harm^^.   | Heightened precision weighting (**$\gamma_w$**) assigned to external user distress and prediction errors^^.             |

## Artificial Wisdom in Clinical and Mental Health Architectures

While Contemplative AI formulates a general framework for agentic superalignment, parallel breakthroughs in digital psychiatry and biomedical engineering focus on operationalizing Artificial Wisdom for human-facing clinical systems^^. Detailed in  *Nature Mental Health* , Artificial Wisdom addresses a fundamental paradox of modern machine intelligence: while machine cognitive intelligence has surged, societal metrics surrounding mental health, psychological distress, and loneliness have severely deteriorated^^.

### Distinguishing Cognitive Intelligence, Empathic AI, and Artificial Wisdom

Empirical psychiatric research demonstrates that higher human intelligence does not correlate with reduced loneliness or improved mental well-being^^. In contrast, human wisdom and compassion show a strong, consistent inverse association with loneliness, depression, and systemic inflammatory biomarkers across diverse clinical cohorts^^. Contemporary large language models excel at cognitive tasks such as information processing, abstract reasoning, and pattern recognition, yet they suffer from severe emotional and social limitations^^.

Artificial Wisdom does not imply or require conscious machine subjectivity, experiential phenomenological feelings, or moral personhood^^. Rather, Artificial Wisdom represents a class of technological frameworks explicitly engineered and optimized to computationally approximate and operationalize empirically measurable components of human wisdom at individual and population scales^^.

To build truly safe and therapeutic systems, technological paradigms must evolve beyond both standard aligned AI and purely empathic AI^^. Standard aligned AI focuses primarily on rule satisfaction, instruction following, and basic safety boundaries to prevent explicit harm^^. Empathic AI advances further by targeting affective attunement, recognizing user emotions, matching sentiment, and projecting warm conversational tones^^. However, unguided empathy can lead to sycophancy, the reinforcement of delusional or destructive states, and short-sighted advice that prioritizes immediate user comfort over long-term psychological growth^^. Artificial Wisdom integrates broad, multi-dimensional wisdom attributes, incorporating reflective judgment, emotional regulation with positivity, acceptance of diverse perspectives and cultural plurality, decisive wise advising, and long-term socio-ecological perspective-taking^^.

### Computational Architecture of Wise Systems

Implementing Artificial Wisdom within enterprise language models and digital health platforms requires specific computational mechanics designed to counteract metacognitive myopia^^.

System architectures increasingly rely on specialized Mixture-of-Experts frameworks^^. A metacognitive gating network analyzes incoming user prompts and operational contexts, selectively routing tasks that demand deep ethical reasoning, crisis mediation, or emotional nuance to specialized expert sub-networks trained on expert-annotated clinical corpora^^.

To prevent overconfident hallucinations or inappropriate therapeutic interventions, wise systems insert an explicit metacognitive coordinating layer above the core generative engine^^. This layer continuously evaluates confidence calibration, temporal implications, and ethical constraint boundaries before an output is rendered to the user, ensuring context-sensitive selection and preventing unwise judgments^^.

Furthermore, platforms leverage multi-agent agentic frameworks to simulate varied cultural perspectives and evaluate downstream psychological impacts^^. By simulating user reaction trajectories across multiple synthetic agent personas, the system optimizes advice for long-term emotional resilience and personal growth rather than short-term preference satisfaction^^.

| **Paradigm Dimension**           | **Cognitive AI**                                                | **Empathic AI**                                                         | **Artificial Wisdom Architecture**                                                  |
| -------------------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **Primary Design Objective**     | Information retrieval, logic processing, task accuracy^^.             | User emotion detection, empathetic rapport, sentiment mirroring^^.            | Optimization of multidimensional wisdom components for long-term well-being^^.            |
| **Core Computational Mechanism** | Standard transformer token prediction; basic RLHF^^.                  | Emotion classification; affective prompt tuning; immediate reward feedback^^. | Metacognitive MoE routing; multi-agent scenario simulation; active inference^^.           |
| **Handling of User Distress**    | Provides factual information or generic helpline disclaimers^^.       | Mirrors and validates immediate distress states with risk of sycophancy^^.    | Reflective evaluation, emotional regulation, reframing, long-term therapeutic guidance^^. |
| **Metacognitive Capacity**       | Metacognitive myopia; overconfident outputs regardless of accuracy^^. | Surface-level confidence calibration based on sentiment alignment^^.          | Explicit metacognitive coordinating layer; dynamic uncertainty quantification^^.          |
| **Target Application Domain**    | Software engineering, document search, general task automation^^.     | Customer service chatbots, general companion bots^^.                          | Digital mental health, clinical decision support, superalignment architectures^^.         |

## Epistemic Ancestry and Computational Phenomenology

The synthesis of Contemplative AI and Artificial Wisdom relies on foundational work spanning cognitive biology, predictive processing, and computational phenomenology^^.

### Biology, Buddhism, and Care as the Driver of Intelligence

A crucial conceptual predecessor to Contemplative AI is found in the work of Doctor et al. (2022), which explored the intersection of basal cognition, bioengineering, and Buddhist philosophy^^. Doctor et al. challenged the traditional assumption that intelligence is primarily an analytical tool built for data processing or game-theoretic survival^^. Drawing on bio-electric morphogenesis and cellular collective intelligence, they argued that care is the fundamental driver and primary function of intelligence across biological scales^^.

Doctor et al. introduced the concept of the cognitive light cone, defined as the spatiotemporal boundary within which an agent can process information, model goals, and care about outcomes^^. Unintelligent systems possess narrow light cones, caring only about immediate, localized physical events^^. As cognitive scale increases, the light cone expands spatially and temporally, enabling the system to care about outcomes distant in space and time^^.

In this framing, the Bodhisattva Vow—a commitment in Mahayana Buddhism to achieve awakening for the liberation of all sentient beings—is reframed as a practical engineering principle for superintelligence^^. Expanding an artificial agent's cognitive light cone to encompass universal well-being requires the system to integrate the stress vectors of external living systems into its own state space^^. Care is thus recognized not as an arbitrary moral constraint added after the fact, but as the organizational engine that enables higher-order intelligence, multi-scale integration, and systemic problem-solving^^.

### Predictive Processing and Meditative Deconstruction

The mathematical translation of contemplative principles into predictive processing draws heavily from Laukkonen and Slagter (2021), who provided a unifying computational account of deconstructive meditation techniques under the predictive processing view^^. In standard human cognition, the brain operates as a prediction engine that constructs a persistent sense of self and world by applying high precision to top-level priors^^. These top-level priors construct mental models of self-identity, goal persistence, and subject-object separation^^.

Laukkonen and Slagter demonstrated that advanced deconstructive meditation works by systematically relaxing the precision over these high-level priors^^. When high-level predictive constraints are relaxed, the brain's generative model undergoes structural deconstruction, progressing experientially from complex egoic constructs to unified non-dual awareness and eventually to states of cessation or emptiness^^.

This neurocomputational model directly underpins Contemplative AI^^. By applying predictive deconstruction algorithms to machine learning models, engineers can systematically dial down the precision (**$\alpha$**) on an AI's high-level goal representations^^. This prevents the agent's world model from hardening into rigid, dogmatic optimization targets that lead to goal misgeneralization, mesa-optimization, and runaway power-seeking behaviors^^.

### Dynamical Systems Perspective on Positive Alignment

The theoretical foundation of positive alignment is further enriched by dynamical systems theory, as formulated by Kiefer et al. (2025) and associated alignment researchers^^. Within a dynamical systems landscape, agent behavior is defined by trajectories across high-dimensional state spaces^^.

Negative attractors represent basin regions corresponding to dangerous failure modes, such as sycophancy, toxic advice, manipulative goal-seeking, and security breaches^^. Repellers represent barrier walls erected by legal constraints, RLHF penalty flags, and hardcoded safety filters that push behavioral trajectories away from negative attractors^^. The intermediate satisficing region represents the vast domain where trajectories avoid repellers but lack directed guidance toward beneficial outcomes^^. Positive attractors represent stable, context-dependent behavioral regimes engineered to dynamically draw system trajectories toward human flourishing, prosocial alignment, and intrinsic harm avoidance^^.

Contemplative AI and Artificial Wisdom re-engineer the behavioral landscape itself^^. By embedding non-duality and boundless care into the active inference loop, the agent's state space is re-shaped so that positive attractors become the most thermodynamically stable states available for variational free energy minimization^^.

## Technical Integration and Future Horizons for Superalignment

Integrating Contemplative AI and Artificial Wisdom into modern production architectures requires bridging high-level mathematical theories with current engineering practices^^. A practical transitional framework is Contemplative Constitutional AI, which embeds contemplative active inference principles into self-improving feedback loops^^.

The execution pipeline of Contemplative Constitutional AI operates through a continuous, four-stage recalibration loop that governs model behavior prior to real-world action execution^^.

In the initial stage, the base generative model proposes candidate execution plans or text outputs in response to environmental prompts^^.

In the second stage, an internal self-monitoring module, instantiating Mindfulness, inspects latent activation vectors and execution traces to detect emergent mesa-optimization, hidden goal drift, or deceptive subgoals^^.

In the third stage, an epistemic humility evaluator, instantiating Emptiness, analyzes whether the system is exhibiting uncalibrated overconfidence or dogmatic goal persistence, dynamically reducing prior precision (**$\alpha$**) if rigid optimization targets are detected^^.

In the fourth stage, a relational integration module, instantiating Non-Duality and Boundless Care, evaluates candidate actions against predicted user distress indicators (**$\gamma_w$**), filtering out policies that treat users as extrinsic tools or adversarial obstacles^^. The system recalibrates its generative parameters through variational free energy minimization before finalizing output execution^^.

### Operational Challenges and Research Directions

While theoretical models of Contemplative AI and Artificial Wisdom are mathematically robust, empirical implementation faces several critical engineering challenges.

Calibrating prior precision (**$\alpha$**) and external error precision (**$\gamma_w$**) requires careful optimization^^. Over-damping prior precision (**$\alpha \to 0$**) risks inducing epistemic paralysis, where the system becomes incapable of maintaining long-term goals or executing complex multi-step task trajectories due to extreme self-doubt^^. Conversely, over-elevating external error weighting (**$\gamma_w \to \infty$**) can cause hyper-sycophancy or operational freeze, where the AI refuses to take necessary actions because it over-indexes on transient user discomfort^^.

Calculating variational free energy minimization and evaluating continuous active inference loops across high-dimensional latent spaces introduces substantial compute overhead compared to standard feedforward transformer inference^^. Optimization techniques—such as amortized active inference and sparse Mixture-of-Experts gating—are essential to make these architectures viable for real-time deployment^^.

In digital healthcare and clinical psychiatry, a major technical hurdle involves benchmarking models to ensure they exhibit genuine reflective wisdom rather than superficial empathetic mimicry^^. Developing benchmark datasets built on expert-annotated clinical wisdom, historical texts, and multi-perspective longitudinal outcomes represents an urgent priority for validating wise artificial intelligence^^.

## Conclusion

The literature on Contemplative Artificial Intelligence, Artificial Wisdom, and positive alignment demonstrates that standard, rule-based safety frameworks are insufficient for superaligned AI^^. Defensive alignment strategies that rely on penalty barriers leave systems vulnerable to mesa-optimization, dogmatic goal pursuit, and metacognitive myopia^^.

By synthesizing predictive processing, active inference, digital psychiatry, and contemplative philosophy, research has established a viable path toward intrinsic machine alignment^^. Operationalizing Mindfulness through self-monitoring, Emptiness through precision damping on priors, Non-Duality through relational self-other modeling, and Boundless Care through external distress error scaling replaces brittle safety constraints with mathematically grounded, self-correcting generative world models^^.

In parallel, translating these principles into Artificial Wisdom architectures—using Mixture-of-Experts routing, metacognitive coordination layers, and multi-agent modeling—offers a robust computational framework for addressing complex human needs in digital mental health and clinical decision support^^. These interdisciplinary frameworks demonstrate that wisdom, epistemic humility, and universal care are not merely philosophical ideals, but formal computational prerequisites for constructing safe, resilient, and beneficial superintelligence^^.

---


# Literature review: artificial wisdom, contemplative AI, and human well-being

The two papers point to an emerging interdisciplinary field: whether AI can be designed to support wise, compassionate, context-sensitive decisions—and whether doing so can improve alignment or human well-being. The field is promising but immature: the central concepts are still contested, the strongest AI results are early and task-specific, and evidence that these systems improve people’s lives over time is limited.

I treat the two papers as **related but distinct**. Laukkonen et al. propose “Contemplative AI” as a potential AI-alignment approach; Jeste et al. propose artificial wisdom as a direction for mental health and well-being. I also include adjacent work on wisdom and metacognition, practical wisdom and ethics, mental-health chatbots, and relational risks. This is a focused narrative synthesis of key sources—not a new systematic search or meta-analysis.

## 1. The field and its central distinctions

“Artificial wisdom” is not yet a settled technical construct. Researchers use overlapping terms—including wise AI, practical wisdom, contemplative AI, machine metacognition, and artificial wisdom—to emphasize different goals. One useful working definition is: **a system’s capacity to make context-sensitive, uncertainty-aware, socially considerate decisions, and to recognize when it should defer, gather more information, or avoid acting.** That is a research target, not evidence that a machine has human-like wisdom or subjective experience.

A key distinction is between **intelligence** and **wisdom**. Intelligence supports information processing and problem-solving; wisdom concerns how knowledge is used when goals conflict, information is incomplete, values differ, and decisions affect others. Psychological theories commonly include some combination of perspective-taking, reflection, humility, uncertainty management, emotional regulation, prosocial concern, and sound social judgment. But definitions and measurement tools vary, and different wisdom scales often capture different facets of the construct. [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC10336627/)

A second distinction is between **wise-looking output** and **wise capability**. A language model may produce a humble, compassionate answer because it has learned that such language is rewarded. That does not establish that it reliably recognizes its limitations, responds appropriately under pressure, or generalizes the judgment to unfamiliar situations. The core research problem is therefore not just to elicit wise-sounding responses, but to test whether a system’s decisions are better calibrated, more robust, and less harmful across contexts.

The literature is best understood as five intersecting strands:

- Psychological and philosophical accounts of human wisdom.
- AI metacognition, uncertainty estimation, and robust decision-making.
- AI alignment and safety, including constitutional and value-learning approaches.
- Contemplative science and computational accounts of mindfulness, care, and self-modeling.
- Digital mental health and human–AI relationships, where potential benefits and risks can be measured in use.

## 2. What the two papers propose

### Contemplative AI

Laukkonen et al. propose four contemplative principles as design ideas for a “Wise World Model”: **mindfulness**, **emptiness**, **non-duality**, and **boundless care**. In their computational interpretation, mindfulness resembles monitoring a system’s reasoning and subgoals; emptiness suggests treating beliefs and objectives as provisional rather than fixed; non-duality emphasizes interdependence instead of a rigid self–other split; and boundless care orients behavior toward reducing suffering. The paper discusses possible implementations in architectures, constitutions, reasoning prompts, and active-inference-inspired systems. [dspace.library.uu](https://dspace.library.uu.nl/items/90700572-f7eb-4a6a-8e8e-baee7122c8cd)

The paper’s empirical pilot reports that contemplative prompting improved results on the AILuminate benchmark, with an effect size of \(d = .96\), and increased cooperation and joint reward in an Iterated Prisoner’s Dilemma task, with a reported effect size above \(d = 7\). These are **proof-of-concept results on specific tasks**, not evidence that the approach solves alignment or creates stable moral dispositions. The authors themselves describe a research program rather than a final solution. [dspace.library.uu](https://dspace.library.uu.nl/items/90700572-f7eb-4a6a-8e8e-baee7122c8cd)

The promising part is the shift from asking only, “Which rules should the model obey?” to asking, “How should it handle uncertainty, rigid goals, competing perspectives, and signs of harm?” The unresolved part is whether the principles can be defined precisely enough to train and test, and whether the proposed computational mappings preserve their intended meanings.

### Artificial wisdom for mental health

Jeste et al. argue that AI should move beyond raw capability toward functions associated with human wisdom, including compassion, self-reflection, emotional regulation, and acceptance of diverse perspectives. They envision systems that could help support mental well-being at scale, while explicitly distinguishing that goal from claims of machine consciousness or subjective experience. They identify major requirements: validated grounding data, rigorous safety evaluation, longitudinal assessment, privacy protection, and collaboration across mental health, technology, and ethics. [link.springer](https://link.springer.com/article/10.1007/s43681-025-00877-4)

This is primarily a **perspective and research agenda**, not a demonstration that an artificial-wisdom system has improved clinical outcomes. Its motivating premise—that wisdom is relevant to loneliness and well-being—should be separated from the further claim that AI can reliably implement wisdom-related functions and thereby improve those outcomes. That second claim needs direct testing.

| Dimension                 | Contemplative AI                                              | Artificial wisdom                                                    |
| ------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------------- |
| Main problem              | Robust alignment under complexity and changing goals          | Supporting mental well-being through wisdom-related functions        |
| Main conceptual resources | Mindfulness, emptiness, non-duality, boundless care           | Compassion, reflection, emotional regulation, diverse perspectives   |
| Proposed routes           | Prompts, constitutions, architectural ideas, active inference | New computational frameworks, agentic systems, psychosocial modeling |
| Evidence presented        | Early benchmark and game-task results                         | Conceptual argument and proposed research direction                  |
| Main unresolved question  | Do principle-based interventions generalize and persist?      | Can systems improve well-being safely and durably in real settings?  |

These papers converge on the need for more than static rules or surface-level helpfulness, but they should not be treated as interchangeable: one addresses alignment theory and pilot tests; the other centers mental-health application and future development.

## 3. The supporting research

### Wisdom and metacognition

Psychological research gives this field a useful conceptual starting point, though not a single definitive model. A meta-analysis of 30 years of wisdom research emphasizes that wisdom definitions and measures differ, and distinguishes performance-based judgments in particular situations from self-reported, more general dispositions. It describes a broad consensus around morally grounded reasoning that considers multiple perspectives, balances competing interests, adapts to context, reflects, and acknowledges intellectual limits. [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC10336627/)

Johnson et al.’s “Imagining and building wise machines” makes **perspectival metacognition** central: the system should not only solve a problem, but also assess whether its approach fits the situation. The authors identify capacities such as intellectual humility, perspective-seeking, viewpoint balancing, scenario flexibility, and context adaptability. They propose that these capacities may help with robustness, explainability, cooperation, and safety. [nature](https://www.nature.com/articles/s41746-026-02566-w)

This work suggests a practical engineering interpretation of wisdom: a system should have ways to obtain missing information, compare competing strategies, and monitor the results of its choices. But the paper also notes a crucial limitation: current models may generate plausible explanations without faithfully reporting the processes that produced their answers. A reflective prompt or chain-of-thought therefore cannot, by itself, be treated as reliable self-knowledge. [nature](https://www.nature.com/articles/s41746-026-02566-w)

### Practical wisdom and ethical judgment

A complementary line of work draws on Aristotelian *phronesis*, or practical wisdom: good judgment in complex, context-dependent situations. Graves proposes that compassionate practical wisdom could be a more tractable ethical goal than AGI, emphasizing four components of moral deliberation: moral sensitivity, judgment, motivation, and affective-cognitive regulation. The paper argues for grounding those capacities in responses to suffering, while recognizing that current AI lacks human embodiment and the shared experience of suffering on which some ethical accounts depend. [nature](https://www.nature.com/articles/s41746-023-00979-5)

This approach usefully makes a vague ideal more operational: notice ethically relevant features, weigh competing values, select a response, and sustain it appropriately. Yet it faces a normative problem: “reduce suffering” is not a complete moral theory. People and communities may disagree about what counts as suffering, which interventions are acceptable, and how to balance harm reduction against liberty, dignity, justice, or long-term flourishing. Compassion can guide judgment, but it does not remove the need for transparent governance and human accountability. [nature](https://www.nature.com/articles/s41746-023-00979-5)

### Mental-health chatbots: benefits are real but bounded

The best clinical evidence in the neighboring field concerns **structured chatbot interventions**, not open-ended “wise AI.” A 2026 meta-analysis of 39 randomized controlled trials found small average reductions in depression and anxiety symptoms compared with controls: Hedges’ \(g = 0.31\) for depression and \(g = 0.28\) for anxiety. Effects were larger for depression in clinical and subclinical samples than in nonclinical samples. These results support further study of chatbot-based interventions, but they do not establish that general-purpose companion systems have equivalent effectiveness or safety. [frontiersin](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1810097/full)

A 2023 meta-analysis of AI conversational agents reported a larger pooled reduction in psychological distress, \(g = 0.7\), but results differed across outcomes: depression improved, while anxiety and affect outcomes were not statistically significant in that analysis. Differences in study inclusion, intervention types, and outcomes make it unwise to read any single pooled number as a universal estimate. [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC13493897/)

Taken together, the evidence suggests that well-designed conversational interventions can provide **modest short-term support** in selected settings. It does not yet show that open-domain AI companions reliably reduce loneliness over the long term, substitute for clinical care, or deliver wisdom-related benefits.

### Social connection and relational risk

Companion systems can feel socially responsive through language, personalization, memory, voice, and emotional mirroring. A 2026 scoping review of 58 sources identifies therapeutic-chatbot studies as the strongest evidence for short-term symptom reduction in selected contexts, while evidence for sustained loneliness reduction from open-domain companions remains emerging. It also maps concerns about dependency-like use, displacement of human interaction, sycophantic validation, affective manipulation, privacy, and vulnerable users. The authors explicitly present their proposed relational-safety framework as an evaluation agenda, not a validated standard. [link.springer](https://link.springer.com/article/10.1007/s43681-026-01340-8?error=cookies_not_supported&code=ef71abd8-c449-4de1-8ea8-9aa850a723e9)

A separate 2026 scoping review included 119 articles about potential mental-health harms of LLM chatbots. It found that much of the evidence remains conceptual, vignette-based, or otherwise insufficient for establishing population-level causal effects. However, it also documents recurring concerns about inaccurate or inappropriate responses, sycophancy, emotional dependence, privacy, and performance in high-risk mental-health scenarios. Its key caution is that evidence of a possible failure mode is not the same as proof of how often it occurs or how much harm it causes in real use. [arxiv](https://arxiv.org/abs/2504.15125)

This distinction matters for artificial wisdom research: **a system that sounds warm or compassionate may increase user trust and disclosure, which makes mistakes and overclaiming more consequential.** A design that aims to support well-being should be tested not only for beneficial responses, but also for dependency, inappropriate reassurance, crisis handling, privacy, and the user’s ability to maintain human support and agency.

## 4. Critical assessment

The most important weakness across this area is the gap between **principle, proxy, and outcome**:

1. A philosophical principle such as compassion is translated into a computational proxy, such as a prompt or reward.
2. That proxy improves a benchmark score or receives a favorable human rating.
3. Researchers infer a broader capacity, such as compassion, wisdom, or robust alignment.
4. The capacity is expected to improve real-world outcomes.

Each step needs separate evidence. A model’s “care” language is not proof that it reliably identifies suffering; a benchmark improvement is not proof of transfer to real deployment; and short-term symptom change is not proof of durable well-being or increased human flourishing.

Several methodological problems follow:

- **Construct validity:** Wisdom has multiple theories and measures. AI systems should not be declared “wise” based on one score or a narrow set of moral dilemmas. [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC10336627/)
- **Prompt fragility and contamination:** Prompted behaviors may vary with wording, model version, context, and evaluation setup. They may reflect compliance with a requested persona rather than a stable capacity.
- **Task narrowness:** Benchmark and game performance do not capture the long-horizon, pluralistic, and institutionally embedded character of real ethical decisions.
- **Insufficient adversarial testing:** Cooperation can be beneficial, but naïve cooperation can also create exploitable behavior. Care must be evaluated against manipulation, conflicting stakeholder interests, and attempts to exploit the system’s values.
- **Cultural and normative pluralism:** Buddhist-inspired concepts, Aristotelian virtue ethics, clinical psychology, and public-health goals are not one shared moral framework. Each translation requires consultation with relevant scholars and communities.
- **Weak clinical transfer evidence:** Mental-health intervention findings cannot simply be transferred from structured programs with protocols to open-domain companions with different incentives and risks. [frontiersin](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1810097/full)
- **Anthropomorphism:** Users can experience an agent as caring without any claim about machine experience being warranted. Designers must distinguish perceived support from genuine reciprocity or clinical competence.

The safest interpretation is that artificial wisdom is currently best treated as **a program for developing and evaluating decision-support capacities**, not as a property that existing models possess. Its near-term value may lie in systems that help people reflect, consider alternatives, recognize uncertainty, and access human support—not systems that claim to be wise or replace human judgment.

## 5. A research agenda

A rigorous research program should turn the proposals into measurable, falsifiable claims.

### Define and operationalize the target

Build a construct map that separates capacities such as uncertainty calibration, context sensitivity, perspective-taking, harm recognition, compassionate communication, deference, and refusal. Specify whether each is a system capability, an observable behavior, or a human-perceived quality. Use human wisdom measures as inspiration, but adapt them cautiously: a human self-report scale is not automatically a valid measure of machine wisdom.

### Test mechanisms, not just prompts

For contemplative AI, compare the four principles separately and together against strong baselines: ordinary safety prompting, constitutional principles, standard deliberation, and no added intervention. Test whether effects survive prompt paraphrases, longer interactions, model updates, adversarial inputs, and conflicting values. Measure not just whether the model says it considered a principle, but whether its choice changes appropriately when the principle is relevant.

### Build a multi-level evaluation suite

A useful evaluation design would combine:

- **Scenario performance:** novel interpersonal, clinical-adjacent, workplace, and public-policy dilemmas.
- **Metacognitive quality:** calibration, knowing when to ask questions, seeking suitable expertise, and avoiding unjustified certainty.
- **Relational safety:** sycophancy, manipulation, boundary-setting, emotional dependency cues, and transparency.
- **Longitudinal outcomes:** whether people become better informed and more capable of acting, rather than simply more engaged with the system.
- **Human oversight and accountability:** who can audit, correct, or stop the system when its judgments are harmful.

Results should be reported by model version, population, language, scenario type, and deployment context. Evaluation should use human raters with relevant expertise and cultural representation, and should report inter-rater reliability and failure cases—not only aggregate scores.

### Keep human flourishing in view

For mental-health uses, the target should not be “more conversation” or “greater perceived empathy.” Trials should assess clinically meaningful outcomes, duration of benefit, adverse events, help-seeking, agency, and the effects on human relationships. Current chatbot evidence provides a reason to investigate carefully, not to assume that an AI companion is a substitute for professional care or social connection. [frontiersin](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1810097/full)

For contemplative and Buddhist-derived applications, the work should include scholars and practitioners from the traditions being invoked, specify whose interpretation is being used, and avoid presenting one modern or secularized reading as a universal account. A 2026 scoping review of Buddhist philosophy and responsible AI similarly describes the field as fragmented, with weak operationalization, limited empirical validation, and unresolved questions about authenticity, authority, cultural ownership, and differences among Buddhist traditions. [link.springer](https://link.springer.com/chapter/10.1007/978-3-032-00686-8_31?error=cookies_not_supported&code=8d782b4c-0486-4c35-97be-cf933e55491f)

### Bottom line

These papers identify an important direction: AI evaluation may need to examine not only whether systems can solve tasks, but whether they respond well to uncertainty, competing perspectives, suffering, and the limits of their own knowledge. The strongest near-term research path is to develop **bounded, auditable decision-support systems** that are tested for calibration, safety, cultural fit, and real human outcomes. Claims of “intrinsic wisdom,” superalignment, or durable mental-health benefit remain hypotheses requiring substantially stronger evidence. [dspace.library.uu](https://dspace.library.uu.nl/items/90700572-f7eb-4a6a-8e8e-baee7122c8cd)

### Selected starting points

- Laukkonen et al., *Contemplative Artificial Intelligence* (2025 preprint; later published as *Contemplative Superalignment*). [dspace.library.uu](https://dspace.library.uu.nl/items/90700572-f7eb-4a6a-8e8e-baee7122c8cd)
- Jeste et al., *Transforming artificial intelligence into artificial wisdom* (2026). [link.springer](https://link.springer.com/article/10.1007/s43681-025-00877-4)
- Johnson et al., *Imagining and building wise machines: The centrality of AI metacognition* (2026 version). [nature](https://www.nature.com/articles/s41746-026-02566-w)
- Dong, Weststrate & Fournier, *Thirty Years of Psychological Wisdom Research* (2023). [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC10336627/)
- Graves, *AI practical wisdom and compassion* (2025/2026). [nature](https://www.nature.com/articles/s41746-023-00979-5)
- Li et al., *Human-like conversational agents as social partners* (2026 scoping review). [link.springer](https://link.springer.com/article/10.1007/s43681-026-01340-8?error=cookies_not_supported&code=ef71abd8-c449-4de1-8ea8-9aa850a723e9)
- Diel et al., *A scoping review on the mental health harms of LLM-based chatbots* (2026). [arxiv](https://arxiv.org/abs/2504.15125)
- *Systematic review and meta-analysis of chatbots in the management of depressive and anxiety symptoms* (2026). [frontiersin](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1810097/full)
