"""
Fusion Synthesis — AUTH-011 Phase 1: authored synthesis cards.

A reusable system for AUTHORED pairings. A person authors each pair's emergent
ability and every visual descriptor; this package validates that data, runs it
through the existing Fusion Engine C1 -> C2 -> C3 slice (unmodified), and
renders one card per pair: appearance slots, visual provenance, traits with
sources, one emergent ability with limitations, exclusions, and one
descriptor-only image prompt.

It is NOT a general-purpose fusion engine. It derives nothing automatically,
accepts no arbitrary input, makes no model, network or provider call, and has
no dashboard, server or legacy-engine integration.

Boundary (AUTH-011, ADR-001 AD-1): this package imports only the Fusion
Engine's public modules and the standard library. It must never import the
legacy governance modules or reference their registries.
"""
