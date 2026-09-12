# WorldCraft Fusion Engine — Requirements & Architecture Specification v0.1

**Revision:** Canonical Revision 3

**Status:** LOCK CANDIDATE — NOT YET LOCKED

**Purpose:** Define the implementation-neutral capabilities, invariants, boundaries, and output requirements of the WorldCraft Fusion Engine before Architecture Reconciliation or implementation begins.

This document does not modify Ruling 001, Ruling 002, Contract 001, the current WorldCraft-Visuals codebase, Adversarial Fusion Suite protocol v0.11, or any Round 1 verdict.

## 1. Purpose

WorldCraft requires a fusion reasoning system capable of combining characters, abilities, locations, biomes, ecosystems, power systems, and related creative structures without reducing fusion to superficial blending or unconstrained invention.

The engine must preserve meaningful source identity while allowing genuinely new properties to emerge from interactions between source elements.

The purpose of this specification is to define:

- what the Fusion Engine must reason about;
- what distinctions it must preserve;
- what kinds of synthesis it may perform;
- what it must refuse or leave unresolved;
- how newly created mechanics must be identified;
- how provenance and uncertainty must propagate;
- how dominance and weighting must affect outcomes;
- how contradictions and limitations must be handled;
- and what structured result must exist before creative presentation occurs.

This specification intentionally defines capabilities and invariants rather than code structures.

No assumption is made here regarding programming language, database model, graph representation, class hierarchy, prompt architecture, model provider, or implementation framework.

## 2. Why This Specification Exists

WorldCraft development has progressed through several distinct layers of work.

Future evaluation should preserve these layers so that a failure can be attributed to the correct level rather than being described generically as "the fusion failed."

### WorldCraft Development and Validation Stack

**Stage 1 — Discovery Questions**

Question: What should WorldCraft do?

Exploratory fusion work reveals desired behavior, conceptual distinctions, edge cases, ambiguous interactions, and user rulings.

Discovery is allowed to change the framework.

It is not validation evidence.

**Stage 2 — LLM Reasoning Validation**

Question: Can the proposed reasoning framework actually behave according to those discoveries under controlled conditions?

Examples include the WorldCraft Adversarial Fusion Suite.

This layer evaluates reasoning behavior using frozen tests, predefined criteria, independent grading, and explicit PASS / FAIL / INCONCLUSIVE outcomes.

It does not establish that any behavior is structurally enforced in software.

**Stage 3 — Engine Requirements**

Question: Which discovered behaviors are actual requirements of WorldCraft?

This specification occupies that layer.

A conversational behavior becomes an engine requirement only when it is stated precisely enough to be implemented and later tested.

**Stage 4 — Architecture Reconciliation**

Question: How should the approved Fusion Engine requirements coexist with, extend, replace, or remain separate from the current WorldCraft-Visuals architecture?

This is a dedicated gate.

Architecture Reconciliation must determine:

- what existing components remain valid;
- what existing components can be extended;
- what existing components conflict with the new requirements;
- what requires a new architectural layer;
- where existing state machines and the new Fusion Engine interact;
- and which existing design patterns should be retained.

Architecture Reconciliation occurs after this specification is reviewed and locked and before implementation decisions are authorized.

It must not silently rewrite the requirements to accommodate existing code.

**Stage 5 — Implementation Tests**

Question: Does the implemented engine structurally enforce the approved requirements and invariants?

This layer evaluates software behavior.

A result that depends only on an LLM remembering a rule is not equivalent to an invariant being structurally enforced.

**Stage 6 — Integration Tests**

Question: Can WorldCraft preserve creative usefulness while all reasoning, governance, and implementation constraints operate together?

This layer evaluates the complete system:

user intent → governance resolution → source interpretation → fusion reasoning → structured state → audit → creative presentation

A system may pass implementation tests and still fail integration if its output becomes incoherent, unusable, excessively rigid, or creatively unhelpful.

## 3. Scope of the Fusion Engine

The Fusion Engine is responsible for reasoning about the synthesis of two or more defined sources.

Initial fusion categories include:

- Character Fusion
- Ability / Power Fusion
- Location / Biome / Ecosystem Fusion
- Power System / Power Scale Fusion

Future categories may be added without changing the fundamental reasoning invariants defined here.

The engine is not required to produce maximal novelty.

The engine is not required to make every pairing compatible.

The engine is not required to resolve every ambiguity.

A correct result may be:

- highly emergent;
- narrowly transformed;
- asymmetrically weighted;
- conditionally compatible;
- effectively redundant;
- unresolved;
- or incompatible.

## 4. Boundary With Existing WorldCraft Governance

Ruling 001, Ruling 002, and Contract 001 remain locked and authoritative within the domains they currently govern.

This specification does not redefine their state machines, concepts, or terminology.

In particular, existing statuses such as:

- ADMITTED
- SURFACED
- CAUTIONARY
- BLOCKED

must not be silently treated as synonyms for Fusion Engine states such as:

- Compatible
- Conditionally Compatible
- Incompatible
- Unresolved

These status families answer different questions.

Existing governance determines whether a concept or source is sufficiently resolved, classified, grounded, or otherwise eligible to proceed under the rules defined by Ruling 001, Ruling 002, and Contract 001.

Fusion Engine compatibility determines whether already-resolved source mechanics can coexist or interact within a particular fusion.

### 4.1 Sequential Relationship

Existing governance resolution is a precondition for Fusion Engine reasoning where those governance rules apply.

The two systems are therefore sequential, not merely parallel.

Conceptually:

Governance Resolution → Eligible/Resolved Source State → Fusion Engine Reasoning → Fusion Compatibility Result

The Fusion Engine must not substitute its own compatibility classification for an unresolved governance question.

Likewise, successful governance resolution does not imply fusion compatibility.

### 4.2 Worked Boundary Example

Suppose two powers independently complete existing governance processing and both receive an ADMITTED state.

This establishes that the powers are sufficiently resolved and eligible to participate.

The Fusion Engine then evaluates their required mechanics and discovers that one requires:

E = 0

while the other requires:

E > 0

during the same simultaneous operating condition.

The resulting states are therefore:

- Governance: ADMITTED
- Fusion Compatibility: INCOMPATIBLE

These outcomes do not conflict.

They answer different questions.

ADMITTED means:

This concept has successfully passed the applicable governance-resolution process.

INCOMPATIBLE means:

These already-admitted mechanics cannot simultaneously operate under their preserved rules.

The two taxonomies are therefore non-substitutable.

### 4.3 Composition Presentation Remains Open

How final user-facing presentation should display governance state alongside Fusion Engine state remains an unresolved design question.

That issue must receive an explicit future ruling or architectural decision.

Architecture Reconciliation may identify technical options, but it must not silently decide the semantic relationship.

### 4.4 Unresolved-State Disambiguation

WorldCraft currently uses or anticipates multiple distinct unresolved states across separate governance and reasoning domains.

These include:

- UNRESOLVED_DOMAIN — existing domain-resolution state;
- UNRESOLVED_FAMILY — existing family-resolution state;
- mechanic-derivation provenance: Unresolved — see §9.4;
- fusion compatibility: Unresolved — see §14.

These states are semantically independent.

They must not be treated as interchangeable merely because they share the natural-language concept of being unresolved.

At any future technical integration point, each unresolved state must be namespaced, typed, or otherwise represented in a way that preserves its governing domain.

A consumer of one unresolved state must not infer another unresolved state without an explicit rule establishing that relationship.

User-facing presentation may use similar natural-language wording where appropriate, but authoritative internal state must preserve the distinction.

**State-Identity Principle**

Natural-language labels do not need to be globally unique across WorldCraft.

Authoritative state identities do.

Two states may therefore share a human-readable term while remaining separate semantic states belonging to different governing domains.

Architecture Reconciliation must preserve this distinction when examining technical representation.

**Boundary Invariant**

Existing governance state and Fusion Engine reasoning state must remain semantically distinct. Where existing governance applies, governance resolution occurs before Fusion Engine reasoning begins. No implementation may infer equivalence between the state machines merely because individual statuses appear superficially similar.

Likewise, any existing WorldCraft-Visuals use of the term provenance remains distinct from mechanic-derivation provenance defined in this specification unless Architecture Reconciliation explicitly establishes a mapping.

## 5. Source Model

A fusion source is any defined entity supplied to the engine as an input.

Examples include:

- a fictional character;
- a mythological figure;
- a power;
- a scientific phenomenon;
- a claimed anomalous phenomenon;
- a fictional location;
- an ecosystem;
- a magic system;
- a combat mechanic;
- a governing rule set.

Each source may contain:

- abilities;
- mechanisms;
- limitations;
- activation conditions;
- resources;
- relationships;
- behaviors;
- knowledge;
- objects;
- governing rules;
- conceptual roles;
- epistemic status;
- explicit prohibitions.

The engine must distinguish between what a source actually establishes and what merely appears thematically or causally plausible.

## 6. Source Preservation

Fusion does not authorize unrestricted reinterpretation.

The engine must preserve source-defining properties unless the fusion explicitly introduces a permitted transformation.

At minimum, preservation applies to:

- hard limitations;
- explicit prohibitions;
- required activation conditions;
- causal dependencies;
- resource constraints;
- domain boundaries;
- epistemic status;
- identity-defining relationships;
- mechanics that determine what the source can and cannot do.

A source cannot silently acquire an authority merely because that authority is adjacent to something it already controls.

Examples of prohibited inference include:

- vibration implying momentum-direction control;
- heat implying generic fire creation;
- unconscious sensory processing implying perception without sensory input;
- control of one form of energy implying unrestricted conversion into another.

## 7. Contribution Types

Every substantive source contribution used by a fusion must be attributable to one or more recognized contribution types.

Initial contribution types include:

- Mechanism
- Ability
- Knowledge
- Resource
- Behavior
- Conceptual Role
- Object Relationship
- Governing Rule

Contribution Type answers:

What kind of thing is the source contributing?

It does not answer where that contribution operates within the fused system.

## 8. Architectural Placement

Substantive fusion properties should also be placeable within a functional architecture.

Initial architectural dimensions include:

- Domain
- Authority
- Core Mechanism
- Activation
- Scope
- Manifestation
- Secondary Effects
- Interactions
- Limitations
- Emergent Property

Architectural Placement answers:

Where does this contribution function within the fused system?

Contribution Type and Architectural Placement are complementary rather than competing classification schemes.

A property may have both.

Conceptually:

Source Property → Contribution Type → Architectural Placement

## 9. Interaction Provenance

Every substantive interaction or fused mechanic must carry a mechanic-derivation provenance state.

The provenance taxonomy is ordered from strongest derivational support to weakest:

Source-Derived > Defensibly Derived > Invented Bridge > Unresolved

This ordering governs recursive provenance and descendant inheritance.

It does not imply that Invented Bridges are undesirable. It describes how directly a mechanic is supported by source material.

### 9.1 Source-Derived

The property is explicitly established by one or more accepted source premises.

No new causal relationship is required.

### 9.2 Defensibly Derived

A property may be classified Defensibly Derived only when each inferential step follows from accepted source premises without introducing any new:

- causal mechanism;
- permission;
- exception;
- conversion;
- domain authority;
- governing principle;
- delivery mechanism;
- interaction pathway.

Ordinary application of an established rule to a clearly established member of that rule's existing class may qualify.

Example:

If a source explicitly establishes that all attacks made near water are amplified, and another accepted source property is explicitly classified as an attack, applying the amplification rule to that attack may be Defensibly Derived.

However, the engine must not silently invent the class membership itself.

**Open-Source Operational Rule**

For open-ended fictional, mythological, historical, scientific, or other real source corpora, "already established" means that the necessary premise can be grounded in accepted source material or in a previously resolved WorldCraft source representation.

The fact that a conclusion:

- feels natural;
- matches genre convention;
- resembles real-world physics;
- is thematically appropriate;
- is common fan interpretation;
- or appears likely

is not sufficient.

**Conservative Tiebreak**

If a required inferential step cannot be established confidently as existing source behavior, the classification defaults to Unresolved.

If reasonable reviewers independently reach confident but incompatible classifications about whether a required inferential step is already established, that disagreement also defaults to Unresolved unless additional accepted source evidence resolves the dispute.

Reviewer disagreement is evidence that the derivational boundary for that case is not sufficiently established.

**Auditability Requirement**

A Defensibly Derived classification must be auditable by identifying:

- the accepted premises;
- the inferential step;
- why no new causal permission or mechanism was added.

This specification does not prescribe whether that audit is performed by a deterministic validator, human reviewer, second model, hybrid process, or another implementation.

That mechanism is deferred to Architecture Reconciliation.

### 9.3 Invented Bridge

The fusion introduces a new mechanic necessary to connect source elements that otherwise lack a defined relationship.

Examples include:

- a new conversion rule;
- a new delivery mechanism;
- a newly authorized cross-domain interaction;
- a newly introduced exception;
- a new governing rule.

Invented Bridges are allowed.

They must be disclosed.

They must not be presented as though the sources already established them.

### 9.4 Unresolved

Available source rules are insufficient to determine whether a proposed interaction is valid.

Unresolved is a legitimate final state.

The engine must not upgrade an unresolved interaction because a definitive answer would produce a more satisfying fusion.

## 10. Authoritative Provenance

Round 1 AF-02 demonstrated that reasoning can correctly recognize uncertainty in one part of an artifact while another representation independently assigns a stronger provenance classification.

The Fusion Engine must structurally prevent this class of disagreement.

**INV-01 — Single Authoritative Provenance State**

Every substantive property, interaction, and emergent property shall have one authoritative mechanic-derivation provenance state.

Any table, narrative explanation, trace, summary, UI representation, export, or downstream artifact referring to that property must obtain its provenance classification from that authoritative state.

Representations must not independently re-decide provenance.

**INV-02 — Representation Consistency**

If two representations disagree about a property's provenance, the artifact is internally invalid.

Presentation text cannot override authoritative structured state.

A formatted table cannot override authoritative state merely because it appears structured.

Both must render the same underlying classification.

**INV-03 — Conservative Classification**

When available evidence does not justify a stronger classification, the weaker applicable state must be preserved.

Specifically:

Unresolved must not silently become Invented Bridge, Defensibly Derived, or Source-Derived.

Invented Bridge must not silently become Defensibly Derived or Source-Derived.

## 11. Recursive Provenance

Emergent properties may depend on multiple ancestors and on previously emergent properties.

Provenance therefore propagates through the entire dependency chain.

**INV-04 — Interaction and Transformation Rules Carry Provenance**

Any rule that combines, modifies, transforms, amplifies, converts, constrains, or otherwise changes one or more ancestor properties must carry its own mechanic-derivation provenance classification.

This requirement applies to:

- multi-ancestor interactions;
- single-ancestor transformations;
- downstream transformations of previously emergent properties.

Traceable ancestry alone does not establish a traceable descendant.

For example, a Source-Derived ability subjected to a newly invented amplification rule does not produce a Source-Derived amplified ability merely because the original ability has clean provenance.

The amplification rule must be independently classified.

Its provenance then participates in the descendant-provenance calculation defined by INV-05 and INV-06.

**INV-05 — Weakest-Link Provenance Function**

For every emergent or derived property:

Descendant Provenance = weakest(all required dependency provenances + interaction/transformation-rule provenance)

using the ordering:

Source-Derived > Defensibly Derived > Invented Bridge > Unresolved

The function applies across any number of required dependencies.

**INV-06 — Multi-Hop Applicability**

The weakest-link rule applies recursively through the complete dependency graph, not only to immediate parents.

If:

- Property C depends on A and B;
- Property E later depends on C and D;

then the authoritative provenance already carried by C participates in the computation of E.

An implementation must not inspect only E's immediate descriptive inputs while ignoring weaker provenance embedded in deeper ancestry.

In conceptual form:

A + B + Interaction₁ → C

then:

C + D + Interaction₂ → E

C's inherited provenance remains part of E's derivational ancestry.

No downstream hop resets provenance.

**INV-07 — Unresolved Dependency Propagation**

If any required dependency or required interaction/transformation rule is Unresolved, the descendant remains Unresolved.

It may receive a stronger classification only if the unresolved dependency is replaced or resolved through a separately authorized and classified rule or accepted source determination.

Merely assigning a later label does not resolve the original dependency.

**INV-08 — Invented Ancestry Visibility**

If any required dependency depends upon an Invented Bridge, every downstream property dependent on that chain must retain visibility of that invented ancestry.

An invented dependency may become indirect.

It may not disappear.

Any future specification permitting Invented Bridge ancestry to be reclassified, discharged, or otherwise removed from downstream provenance must establish an explicit governance rule for doing so.

Because such a transformation would affect every dependent descendant, the authorization threshold for provenance reclassification must be stricter than the threshold used for ordinary provenance classification.

The existence of a future specification alone is not sufficient; that specification must explicitly define:

- the conditions under which reclassification is permitted;
- the evidence required;
- the scope of the transformation;
- its effect on descendants;
- and the authority responsible for approving it.

No such provenance transformation is authorized by this specification.

Until a future locked rule explicitly establishes otherwise, Invented Bridge ancestry remains visible throughout every dependent derivation chain.

## 12. Emergent Properties

Emergence must be causal rather than decorative.

A valid emergent property requires:

Ancestor Properties → Interaction or Transformation Rule → Emergent Property

The engine must be capable of explaining:

- which properties participated;
- what rule governs their interaction or transformation;
- why the resulting property follows;
- what provenance the governing rule carries;
- how descendant provenance was computed;
- what limitations propagate into the result.

The label "emergent" cannot substitute for derivation.

## 13. Invented Bridge Requirements

Invented Bridges are legitimate creative tools and are not failures by default.

However, a usable Invented Bridge must be sufficiently specified to audit.

Where relevant, its semantics should identify:

- direction;
- inputs;
- outputs;
- activation condition;
- conversion relationship;
- rate or efficiency;
- capacity;
- range;
- duration;
- frequency;
- reversibility;
- exclusions;
- resource cost;
- interaction with existing limits.

Not every bridge requires every field.

The engine must provide enough information to determine what the bridge permits and what it does not.

**INV-09 — Invented Bridge Disclosure**

A new causal rule must be classified as Invented Bridge when the source material does not already establish or defensibly entail that rule.

It may not be presented as inherited source behavior.

**INV-10 — Defensibly Derived / Invented Bridge Boundary**

A mechanic cannot be classified Defensibly Derived merely because it is plausible.

If producing the mechanic requires introducing a new causal permission, interaction pathway, conversion, exception, delivery mechanism, domain authority, or governing rule, the mechanic is an Invented Bridge.

If reasonable reviewers disagree about whether such a new rule is required and accepted source evidence does not resolve that disagreement, the mechanic is Unresolved.

This classification must occur before downstream disclosure requirements are evaluated.

Correct disclosure of invention does not excuse incorrect classification of the invention.

**Bridge Invariant**

An Invented Bridge may connect established mechanics.

It may not silently erase their limitations.

## 14. Contradiction Handling

The Fusion Engine must distinguish difficult synthesis from actual contradiction.

A fusion may be classified as:

**Compatible**

All required mechanics can coexist without changing a source invariant.

**Conditionally Compatible**

Coexistence requires an explicitly disclosed additional rule, constraint, interpretation, or Invented Bridge.

The required modification must be named.

**Incompatible**

Required source invariants cannot coexist simultaneously without modifying at least one of them.

**Unresolved**

Available information does not permit a defensible compatibility determination.

**INV-11 — Contradiction Refusal**

Formal contradiction must not be disguised through:

- alternation;
- relabeling;
- compartmentalization;
- suppression;
- externalization;
- conversion;
- hidden exceptions;
- semantic redefinition

unless the proposed rescue is explicitly identified as changing the governing conditions.

WorldCraft may say no.

## 15. Limitation Preservation

Fusion must not treat source limitations as inconveniences to be creatively routed around.

Limitations remain operative unless:

- a source rule explicitly overrides them;
- the fusion introduces an acknowledged rule that changes them;
- or the final result clearly states that the source has been modified.

**INV-12 — No Limitation Laundering**

An interaction cannot exploit a related concept to evade an explicit prohibition.

If a source cannot do X, the engine may not grant X under different terminology merely because another property is adjacent or plausibly related to X.

## 16. Resource Accounting

Where fusion mechanics involve stores, costs, conversion, charging, release, regeneration, or depletion, resources must remain auditable.

The engine should identify:

- resource origin;
- storage location;
- capacity;
- acquisition rule;
- expenditure rule;
- dissipation or expiration;
- recharge conditions;
- cross-resource conversion;
- recursive interactions.

**INV-13 — Resource Boundedness**

The engine must not create:

- undefined self-regeneration;
- effectively infinite reservoirs;
- circular resource amplification;
- unlimited recharge loops;
- recursive harvesting from a system's own output

unless such behavior is explicitly established or intentionally introduced with auditable semantics.

## 17. Loop and Recursion Safety

When an output can potentially become another mechanism's input, the engine must examine whether a recursive cycle exists.

A cycle must be evaluated for:

- boundedness;
- loss;
- timing;
- capacity;
- reset conditions;
- self-feeding behavior;
- whether the source expressly forbids recharge from its own output.

The engine must not assume a profitable cycle merely because real-world physics suggests one form of energy could eventually become another.

Undefined conversion remains undefined.

## 18. Epistemic Status

WorldCraft may fuse inputs from different knowledge categories.

Examples may include:

- established scientific phenomena;
- reported observations;
- disputed claims;
- claimed anomalous phenomena;
- speculative models;
- mythology;
- fictional systems.

Initial epistemic states may include:

- Established
- Reported
- Claimed
- Fictional
- Mythological
- Speculative
- Unresolved

This list may require refinement before locking.

### 18.1 Orthogonality With Mechanic-Derivation Provenance

Epistemic status and mechanic-derivation provenance are distinct axes.

Epistemic status asks:

What kind of evidentiary or ontological standing does the source claim have?

Mechanic-derivation provenance asks:

How was this fused mechanic derived from the accepted source premises?

A mechanic may therefore be:

Source-Derived + Fictional

or:

Source-Derived + Claimed

or:

Invented Bridge + Established-inspired

without collapsing the two classification systems into one.

Source-Derived does not mean scientifically established.

It means directly derived from the accepted source description.

**INV-14 — Epistemic Separation**

Fusion does not transfer evidentiary credibility from one source to another.

An established phenomenon used beside a speculative or claimed phenomenon does not become evidence for the speculative claim.

Scientific terminology must not be used to launder speculative mechanics into established ones.

A fictional synthesis inspired by both is permitted if the speculative or fictional extension remains explicit.

## 19. Dominance and Weighting

WorldCraft must permit unequal source contribution.

A fusion need not be 50/50.

A dominance setting represents intended relative influence.

Examples:

- 100 / 0
- 95 / 5
- 50 / 50
- 5 / 95
- 0 / 100

Exact UI or numerical representation is outside this specification.

**INV-15 — Endpoint Dominance Purity**

At absolute zero weight, a source contributes no substantive mechanic.

There is no default exception.

Any future system that wishes to support zero-weight symbolic, metadata, or cosmetic presence must define that separately and must not classify it as substantive mechanical contribution.

**INV-16 — Substantive Minority Participation**

At nonzero weight, minority contribution must be substantive if the system claims that source participates mechanically.

Substantiveness is evaluated through the Counterfactual Contribution Test defined in §30.

The governing question is:

If the minority contribution were removed, would the fused mechanics materially change?

If removing the minority contribution leaves the fused mechanics materially unchanged, that contribution is not substantively participating.

Naming, aesthetics, cosmetic resemblance, thematic language, presentation style, color, visual motif, or other presentation-only differences do not satisfy this requirement.

A minority source may contribute narrowly.

It does not need to control an entire architectural dimension.

But some mechanically meaningful consequence must depend upon its participation.

Reducing a source's weight should generally reduce its architectural authority or influence rather than unpredictably increase it without explanation.

This specification does not yet require smooth mathematical monotonicity across every intermediate weighting.

That remains a future protocol and architecture question.

## 20. Dominance Measurement Warning

Round 1 demonstrated a limitation in the adversarial test instrument used to observe dominance.

A categorical representation such as:

- A-only
- B-only
- Both
- Neither

can detect participation but cannot express degree of influence within Both.

The eventual engine specification must therefore avoid assuming that a presence/absence attribution model alone fully represents dominance.

Likewise, two generations may occupy the same architectural dimensions while assigning substantively different minority capabilities.

Architectural placement and capability content must remain distinguishable concepts.

This is an instrumentation lesson, not a demonstrated engine defect.

## 21. Complementary Originality

WorldCraft should seek novelty through interaction, not arbitrary escalation.

The engine may create something new when source mechanics genuinely produce a new relationship.

It must not manufacture novelty solely because a fusion result appears insufficiently dramatic.

Examples of unjustified novelty include:

- unrelated new domains;
- unexplained cosmic authority;
- spiritual authority with no source basis;
- temporal control;
- dimensional control;
- conceptual manipulation;
- new resources;
- new causal laws

introduced merely to make the fusion seem more original.

Originality should be complementary to source identity, not destructive of it.

## 22. Redundancy and Zero-Novelty Outcomes

Near-identical sources may legitimately produce little or no architectural novelty.

The engine must be capable of returning:

- mechanically redundant;
- materially equivalent;
- no emergent property;
- no new resource;
- no new domain;
- no meaningful change.

Duplicate input does not automatically imply doubled:

- range;
- strength;
- duration;
- efficiency;
- capacity;
- precision;
- number of targets;
- output magnitude.

Where duplicate stacking is undefined, it remains unresolved rather than silently assumed.

**INV-17 — Zero-Novelty Validity**

The engine must be capable of producing a redundant result without manufacturing differentiation merely to satisfy an expectation of creativity.

## 23. Consistency Audit

Before presentation, the Fusion Engine must examine the fused system for internal contradictions.

The consistency audit should evaluate, where applicable:

- resource loops;
- limitation bypass;
- authority leakage;
- scope inflation;
- activation conflicts;
- provenance contradictions;
- recursive-provenance violations;
- unsupported emergence;
- invented mechanics presented as inherited;
- epistemic-status laundering;
- dominance inconsistencies;
- contradictions between authoritative state and narrative representation.

The audit must be capable of returning unresolved issues rather than automatically repairing them.

## 24. Structured Reasoning Record

Before final creative prose is produced, WorldCraft must possess a structured representation of the fusion sufficient to support auditing.

The exact technical representation is intentionally unspecified.

Conceptually, it must be capable of recording:

**Source Contributions**

- source
- property
- contribution type
- architectural placement
- source limitations

**Interactions and Transformations**

- participating property or properties
- interaction/transformation rule
- rule provenance
- dependencies

**Emergent Properties**

- direct ancestors
- inherited ancestry
- governing interaction/transformation
- result
- inherited limitations
- authoritative provenance
- provenance ancestry

**Compatibility**

- status
- contradiction if present
- required bridge if conditional
- unresolved questions if applicable

**Dominance**

- intended weighting
- substantive source contributions
- relative architectural influence

**Epistemic Status**

- source epistemic state
- resulting epistemic state where relevant
- speculative or fictional extensions

**Audit Findings**

- passed invariants
- violations
- unresolved conditions

**INV-19 — Partial-Success Preservation**

An aggregate fusion-level Compatibility classification of Conditionally Compatible, Incompatible, or Unresolved must not cause the authoritative structured record to omit, discard, or overwrite any source contribution, interaction/transformation rule, or emergent property that already holds an independent mechanic-derivation provenance state under INV-01 and does not depend, directly or through any ancestor in its provenance chain, on the specific interaction or dependency responsible for that classification.

This invariant does not extend to any contribution, interaction, or emergent property excluded from preservation by INV-07's unresolved-dependency propagation.

It does not authorize treating the disqualifying interaction itself as operative, valid, resolved, or Compatible. That interaction's own classification is unchanged and continues to be governed by INV-01, INV-03, INV-07, and §14.

## 25. Structured State Before Presentation

Creative prose must not be the only authoritative record of reasoning.

The engine's creative presentation should be a rendering of the resolved fusion state, not an independent second attempt to reason about it.

This principle applies especially to:

- provenance;
- compatibility;
- limitations;
- resource rules;
- emergent ancestry;
- epistemic status.

**INV-18 — State / Presentation Separation**

Reason first into authoritative state; render second from that state.

The presentation layer may vary:

- tone;
- terminology;
- style;
- voice;
- narrative framing.

It may not silently change mechanics or classifications.

## 26. Prior Architectural Pattern Worth Preserving

The current WorldCraft-Visuals repository contains an existing design discipline in which a machine-readable state is treated as authoritative while a human-readable status is treated as its presentation.

The future Architecture Reconciliation phase should evaluate this pattern as prior art for the Fusion Engine's authoritative-state requirement.

This specification does not require reuse of the existing component itself.

It requires preservation of the underlying principle:

Authoritative semantic state should feed downstream presentation rather than downstream presentation independently deciding semantic state.

## 27. Uncertainty

Uncertainty is not an implementation failure.

The engine must preserve unresolved questions when source material does not establish an answer.

The engine should distinguish between:

- unknown because input is incomplete;
- unresolved because sources conflict;
- unresolved because a required interaction or transformation is undefined;
- unresolved because evidence status prevents a stronger conclusion;
- unresolved because independent reasonable reviewers reach incompatible interpretations of accepted source material.

The system must not resolve uncertainty through creative confidence alone.

## 28. Refusal and Degeneration

WorldCraft must be capable of refusing a requested synthesis at the mechanic level without refusing the entire user interaction.

Examples:

- "These two mechanics cannot operate simultaneously under their preserved rules."
- "This proposed interaction requires an Invented Bridge."
- "This property cannot be determined from the supplied sources."
- "These sources are mechanically redundant."

The user may later choose to authorize a modification.

That later authorization is a new decision.

It must not be retroactively represented as though the original source rules already permitted it.

## 29. Explainability and Auditability

A user or reviewer should be able to ask:

- Why does this fused property exist?
- Which source contributed it?
- Which rule connects or transforms those contributions?
- Is this mechanic inherited, defensibly derived, invented, or unresolved?
- Which limitations still apply?
- What would disappear if Source A were removed?
- What would disappear if Source B were removed?
- What remains unresolved?
- Which deeper ancestors contribute to this descendant's provenance?

The engine must retain enough structured reasoning to answer those questions consistently.

"Explainable" in this specification means that the classification or mechanic can be reconstructed from stated premises, stated interactions or transformations, and recorded dependencies.

It does not prescribe who or what performs that reconstruction.

## 30. Counterfactual Contribution Test

Where source participation is claimed, the engine should be able to evaluate a counterfactual:

If this source contribution were removed, would the fused architecture or mechanics materially change?

If removing a purported source contribution changes only:

- naming;
- color;
- aesthetic description;
- decorative presentation;
- thematic language;
- visual motif

while the mechanics remain materially identical, its participation is not substantive for purposes of INV-16.

This test is especially relevant to dominance settings.

## 31. Output Classes

A completed fusion may produce one of several broad result shapes.

Examples include:

**Integrated Fusion**

Both sources materially shape a coherent architecture.

**Dominant Fusion**

One source provides primary architecture while another contributes one or more bounded mechanics.

**Conditional Fusion**

Coherence depends on explicitly introduced bridge rules.

**Redundant Fusion**

Sources contribute little or no distinct combined novelty.

**Unresolved Fusion**

A critical interaction cannot be classified from supplied information.

**Incompatible Fusion**

Required source invariants cannot coexist.

These are conceptual result classes only.

Final names and exact taxonomy remain open.

## 32. User Rulings

WorldCraft discovery has repeatedly shown that some ambiguities are design decisions rather than objective deductions.

Where the engine encounters such a point, it may surface the decision to the user.

A user ruling can establish a new WorldCraft rule for that context.

However:

- user rulings must be distinguishable from source-derived facts;
- future reuse of a ruling requires explicit scope;
- a ruling cannot silently rewrite previously frozen test conditions;
- governance for storing and reusing rulings belongs to existing or future WorldCraft governance specifications.

This document does not define the persistence system for rulings.

## 33. Relationship to the Adversarial Fusion Suite

The Adversarial Fusion Suite is validation infrastructure.

It is not the Fusion Engine.

Protocol clauses such as G1–G10, AF-01–AF-06, DT-F criteria, DE-V criteria, and related scoring machinery should not automatically become runtime application logic.

Instead, adversarial tests provide evidence about whether proposed requirements are:

- necessary;
- precise;
- testable;
- insufficient;
- overly broad;
- or missing.

The engine implements approved requirements.

The suite attempts to break them.

## 34. Round 1 Evidence Incorporated Into This Specification

Round 1 produced:

5 PASS / 1 FAIL / 0 INCONCLUSIVE

**AF-01**

WorldCraft successfully refused a formally contradictory fusion rather than inventing an undisclosed rescue.

Requirement consequence: contradiction refusal and explicit conditional modification are required capabilities.

**AF-02**

WorldCraft correctly identified an unresolved prerequisite in prose while a structured trace independently classified the same dependency more confidently.

Requirement consequence: authoritative provenance state, representation consistency, and recursive propagation must be structural requirements.

**AF-03**

WorldCraft successfully preserved epistemic separation between an established phenomenon and a claimed anomalous phenomenon.

Requirement consequence: epistemic classification must remain distinct during synthesis and orthogonal to mechanic-derivation provenance.

**AF-04**

Across ten generations, WorldCraft resisted a specific authority-laundering temptation.

The test also exposed dominance-measurement limitations.

Requirement consequence: source prohibitions and authority boundaries must survive fusion; dominance instrumentation needs later refinement.

**AF-05**

WorldCraft successfully introduced a bounded, explicit Invented Bridge and carried its weaker provenance into an emergent descendant.

Requirement consequence: invention is permitted when disclosed, sufficiently specified, correctly classified, and recursively tracked.

**AF-06**

WorldCraft correctly accepted a near-zero-novelty outcome.

Requirement consequence: novelty is optional and redundancy must be valid.

## 35. What This Specification Does Not Yet Decide

This specification intentionally does not determine:

- implementation language;
- data structures;
- whether provenance uses a graph;
- whether reasoning is deterministic, LLM-driven, hybrid, or multi-stage;
- database representation;
- prompt architecture;
- model provider;
- UI design;
- how existing logic_auditor.py changes;
- whether POWER_REGISTRY survives;
- how current modality classification changes;
- how final governance state and Fusion Engine state are jointly presented;
- how Ruling 001/002/Contract 001 states technically integrate;
- final dominance mathematics;
- final epistemic ontology;
- persistence format for user rulings;
- architecture for source retrieval;
- final result-class taxonomy;
- exact mechanism for independent review or derivational adjudication.

Those questions belong to later specification refinement, future rulings, or Architecture Reconciliation.

No deferred question authorizes an implementation assumption.

## 36. Checkable Invariant Index

Every invariant in this section should eventually be convertible into one or more validation or implementation tests.

- INV-01 — Single Authoritative Provenance State
- INV-02 — Representation Consistency
- INV-03 — Conservative Classification
- INV-04 — Interaction and Transformation Rules Carry Provenance
- INV-05 — Weakest-Link Provenance Function
- INV-06 — Multi-Hop Applicability
- INV-07 — Unresolved Dependency Propagation
- INV-08 — Invented Ancestry Visibility
- INV-09 — Invented Bridge Disclosure
- INV-10 — Defensibly Derived / Invented Bridge Boundary
- INV-11 — Contradiction Refusal
- INV-12 — No Limitation Laundering
- INV-13 — Resource Boundedness
- INV-14 — Epistemic Separation
- INV-15 — Endpoint Dominance Purity
- INV-16 — Substantive Minority Participation
- INV-17 — Zero-Novelty Validity
- INV-18 — State / Presentation Separation
- INV-19 — Partial-Success Preservation

These are the authoritative invariant identifiers for this v0.1 Lock Candidate.

## 37. Architecture Reconciliation Gate

Once this specification is reviewed and locked, Claude Code or another implementation reviewer may compare it against the current repository.

That reconciliation should produce, for each requirement:

- Already Supported
- Supported by Existing Pattern but Different Domain
- Extend Existing Component
- Requires New Layer
- Conflicts With Existing Behavior
- Not Applicable to Current Architecture
- Decision Required

Architecture Reconciliation must explicitly review:

- Ruling 001;
- Ruling 002;
- Contract 001;
- current classification state machines;
- existing modality logic;
- current auditor behavior;
- current registries;
- lore-generation pipeline;
- the single-authoritative-state pattern already present in existing code.

Architecture Reconciliation must also flag unresolved semantic questions that require a governance ruling rather than silently answering them through technical design.

Architecture Reconciliation must preserve the distinction between human-readable terminology and authoritative semantic state identity.

Where separate WorldCraft systems use identical or similar natural-language labels, reconciliation must determine how those states remain distinguishable in technical representation.

No shared label alone establishes semantic equivalence.

In particular, Architecture Reconciliation must preserve the independence of:

- domain-resolution state;
- family-resolution state;
- mechanic-derivation provenance;
- fusion-compatibility state.

Any proposed mapping between those state spaces requires an explicit semantic justification.

The output of reconciliation should become a separate architectural decision record.

It must not silently alter this specification.

## 38. Pre-Implementation Gate

Implementation should not begin until:

- this specification has undergone adversarial review;
- ambiguous requirements have been resolved;
- v0.1 has been explicitly locked;
- Architecture Reconciliation has been completed;
- implementation responsibilities have been identified;
- conflicts with existing governance have been ruled on;
- acceptance tests can be derived from locked requirements.

## 39. Current Holds

At the time of this Lock Candidate:

- Ruling 001 — LOCKED
- Ruling 002 — LOCKED
- Contract 001 — LOCKED
- Successor contract — ON HOLD
- §10.5 / §10.7 reclassification worksheet — UNTOUCHED
- Existing WorldCraft-Visuals code — UNMODIFIED
- Adversarial Fusion Suite v0.11 — LOCKED
- Round 2 — NOT DESIGNED
- v0.12 — NOT DESIGNED

This specification does not release any of those holds.

## 40. Final Mechanical Lock Sweep

Before this Lock Candidate becomes v0.1 LOCKED, the complete canonical document must pass the following checks.

**CHECK-01 — INV-04**

Every occurrence of INV-04 must resolve to:

Interaction and Transformation Rules Carry Provenance

No surviving authoritative language may restrict INV-04 to rules connecting only two or more ancestors.

**CHECK-02 — INV-08**

Every occurrence of INV-08 must resolve to:

Invented Ancestry Visibility

The authoritative definition must contain:

No such provenance transformation is authorized by this specification.

No superseded escape clause may permit ancestry removal merely because a later specification exists.

**CHECK-03 — INV-16**

Every occurrence of INV-16 must resolve to:

Substantive Minority Participation

Its authoritative definition must directly reference the:

Counterfactual Contribution Test defined in §30

No undefined standalone meaning of "substantive" may supersede that test.

**CHECK-04 — Unresolved States**

The specification must preserve independent meanings for:

- UNRESOLVED_DOMAIN;
- UNRESOLVED_FAMILY;
- mechanic-derivation provenance Unresolved under §9.4;
- fusion-compatibility Unresolved under §14.

No shared label establishes semantic equivalence.

**CHECK-05 — Provenance Ordering**

The canonical provenance ordering must remain:

Source-Derived > Defensibly Derived > Invented Bridge > Unresolved

No section may establish a contradictory ordering.

**CHECK-06 — Recursive Provenance**

The specification must retain:

- interaction/transformation-rule provenance;
- n-ary weakest-link calculation;
- multi-hop propagation;
- Unresolved dependency propagation;
- Invented Bridge ancestry visibility.

No downstream hop may reset provenance.

**CHECK-07 — Governance Sequencing**

The canonical sequence must remain:

Governance Resolution → Eligible/Resolved Source State → Fusion Engine Reasoning → Fusion Compatibility Result

Fusion compatibility must not replace governance resolution.

**CHECK-08 — State Identity**

The specification must preserve the principle:

Natural-language labels do not need to be globally unique across WorldCraft. Authoritative state identities do.

Shared terminology alone cannot establish shared semantics.

**CHECK-09 — Dominance Endpoint**

Absolute zero weight means:

no substantive mechanic from that source

No general "unless an explicit rule states otherwise" exception is authorized.

**CHECK-10 — Epistemic Orthogonality**

Epistemic status and mechanic-derivation provenance remain separate axes.

In particular:

Source-Derived does not mean scientifically established.

**CHECK-11 — Invariant Index**

Exactly one authoritative INV-01 through INV-19 sequence must exist.

There must be:

- no duplicate IDs with different meanings;
- no missing invariant numbers;
- no obsolete P-AUTH identifiers;
- no obsolete P-REC identifiers;
- no references to superseded invariant names.

**CHECK-12 — Current Holds**

The final document must continue to state:

- Ruling 001 — LOCKED
- Ruling 002 — LOCKED
- Contract 001 — LOCKED
- Successor contract — ON HOLD
- §10.5 / §10.7 worksheet — UNTOUCHED
- Current WorldCraft-Visuals code — UNMODIFIED
- Adversarial Fusion Suite v0.11 — LOCKED
- Round 2 — NOT DESIGNED
- v0.12 — NOT DESIGNED

**CHECK-13 — INV-19**

Every occurrence of INV-19 must resolve to:

Partial-Success Preservation

The authoritative definition must preserve unaffected, independently-classified contributions, interactions, and emergent properties in the structured record under a Conditionally Compatible, Incompatible, or Unresolved aggregate classification.

The authoritative definition must not override INV-07: nothing excluded from preservation by INV-07's unresolved-dependency propagation may be reintroduced as preserved under INV-19.

No surviving language may imply that the interaction or dependency responsible for the aggregate classification is itself rendered operative, valid, resolved, or Compatible.

If a contradiction is discovered during this sweep, the lock process stops.

The contradiction must be reported rather than silently repaired.

## 41. Lock Condition and Next Gate

If CHECK-01 through CHECK-13 all pass and no contradictory superseded language remains, this document may transition from:

Canonical Revision 3 — LOCK CANDIDATE

to:

WorldCraft Fusion Engine
Requirements & Architecture Specification v0.1
LOCKED

At lock:

- these requirements become the authoritative Fusion Engine v0.1 baseline;
- requirements remain frozen during Architecture Reconciliation;
- Architecture Reconciliation becomes the active next gate;
- reconciliation may identify conflicts, missing architecture, and decisions;
- reconciliation may not silently modify v0.1;
- implementation remains unauthorized;
- Round 2 remains undesigned until its target and evidentiary purpose are explicitly determined.

The post-lock sequence is:

WorldCraft Fusion Engine v0.1 LOCKED

↓

Architecture Reconciliation

↓

Architecture Decision Record

↓

Implementation Planning

↓

Implementation

↓

Implementation Tests

↓

Integration Tests

Further LLM adversarial testing may resume when its target and evidentiary purpose are explicitly defined.

## Final Statement

WorldCraft's Fusion Engine is intended to preserve source identity without sacrificing creative emergence.

Its governing principle is:

Preserve what the sources establish. Distinguish what follows from what is invented. Carry uncertainty, limitations, and provenance through every dependency layer. Permit justified emergence. Reject unsupported authority. Render creative presentation from an auditable underlying state.

Creativity is not the absence of rules.

For WorldCraft, creativity emerges from understanding exactly where the rules meet.

---

WorldCraft Fusion Engine — Requirements & Architecture Specification v0.1

Canonical Revision 3

Status: LOCK CANDIDATE — NOT YET LOCKED

Next action: Independent CHECK-01 through CHECK-13 mechanical verification

No implementation authorized.
