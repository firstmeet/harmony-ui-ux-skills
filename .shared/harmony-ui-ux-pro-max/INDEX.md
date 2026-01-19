# HarmonyOS NEXT UI/UX Pro Max Skill

## Overview

An AI SKILL that provides design intelligence for building professional UI/UX for **HarmonyOS NEXT** applications.

## Knowledge Base Files

| File | Description |
|------|-------------|
| [CODING_RULES.md](./CODING_RULES.md) | **⚠️ Mandatory coding rules - READ FIRST!** |
| [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md) | Design tokens: colors, typography, spacing, animations |
| [COMPONENTS.md](./COMPONENTS.md) | ArkUI component patterns and usage examples |
| [LAYOUTS.md](./LAYOUTS.md) | Layout patterns for HarmonyOS NEXT |
| [PAGE_TEMPLATES.md](./PAGE_TEMPLATES.md) | Common page structure templates |
| [BEST_PRACTICES.md](./BEST_PRACTICES.md) | UI/UX best practices and anti-patterns |

## ⚠️ Mandatory Rules Summary

1. **Language**: ArkTS only, NO `any` type
2. **UI Framework**: ArkUI declarative syntax
3. **State Management**: @State, @Prop, @Link, @Provide/@Consume, @Observed/@ObjectLink
4. **Resources**: NO hardcoded colors/strings - use `$r('app.color.xxx')`, `$r('app.string.xxx')`

## Quick Reference

### Primary Color
`#0A59F7`

### Font Family
`HarmonyOS Sans`

### Base Spacing Unit
`4vp`

### Button Height (Medium)
`36vp`

### Standard Border Radius
`8vp`

## Framework

- **UI Framework**: ArkUI
- **Language**: ArkTS (TypeScript-like)
- **Build Tool**: hvigorw
- **IDE**: DevEco Studio

## Supported Devices

- Phone (compact)
- Tablet (medium)
- Watch (wearable)
- TV (expanded)
- Car (automotive)

## Usage

When building HarmonyOS NEXT UI/UX, the AI should:

1. Read the knowledge base files
2. Apply the design system tokens
3. Use the component patterns
4. Follow the layout guidelines
5. Check against best practices
