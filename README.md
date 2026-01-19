# HarmonyOS NEXT UI/UX Pro Max Skill

An AI SKILL that provides design intelligence for building professional UI/UX for **HarmonyOS NEXT** applications using **ArkUI/ArkTS**.

## Overview

This skill is inspired by [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) but specifically focused on **HarmonyOS NEXT** platform.

## Features

- ⚠️ **Coding Rules** - Mandatory rules for ArkTS development
- 🎨 **Design System** - Complete design tokens for HarmonyOS NEXT
- 📦 **Component Patterns** - ArkUI component usage examples
- 📐 **Layout Guidelines** - Layout patterns for different devices
- 📄 **Page Templates** - Common page structure templates
- ✅ **Best Practices** - UI/UX best practices and anti-patterns
- 🔍 **Search Script** - Python script for design intelligence search

## ⚠️ Mandatory Coding Rules

All generated code MUST follow these rules:

| Rule | Requirement |
|------|-------------|
| **Language** | ArkTS only, NO `any` type allowed |
| **UI Framework** | ArkUI declarative syntax |
| **State Management** | @State, @Prop, @Link, @Provide/@Consume, @Observed/@ObjectLink |
| **Resources** | NO hardcoded colors/strings - use `$r('app.color.xxx')`, `$r('app.string.xxx')` |

```typescript
// ✅ CORRECT
Text($r('app.string.welcome'))
  .fontColor($r('app.color.text_primary'))
  .backgroundColor($r('app.color.bg_primary'))

// ❌ WRONG - FORBIDDEN!
Text('Welcome')
  .fontColor('#182431')
  .backgroundColor('#FFFFFF')
```

## Installation

### For Cursor

Copy the following folders to your project:

```
.cursor/commands/harmony-ui-ux-pro-max.md
.shared/harmony-ui-ux-pro-max/
```

### For Other AI Assistants

| AI Assistant | Folders to Copy |
|--------------|-----------------|
| Claude Code | `.claude/skills/harmony-ui-ux-pro-max/` |
| Windsurf | `.windsurf/workflows/harmony-ui-ux-pro-max.md` + `.shared/` |
| GitHub Copilot | `.github/prompts/harmony-ui-ux-pro-max.prompt.md` + `.shared/` |

## Usage

### Cursor

Use the slash command to invoke the skill:

```
/harmony-ui-ux-pro-max 创建一个登录页面
/harmony-ui-ux-pro-max Build a dashboard for my HarmonyOS app
```

### Search Script

```bash
# Search for components
python .shared/harmony-ui-ux-pro-max/scripts/search.py "button"

# Generate design system
python .shared/harmony-ui-ux-pro-max/scripts/search.py "电商应用" --design-system -p "MyShop"

# Search by domain
python .shared/harmony-ui-ux-pro-max/scripts/search.py "列表" --domain layout
```

## Knowledge Base

The skill contains knowledge about:

### Design System

- **Colors**: Brand colors, semantic colors, neutral colors (light/dark mode)
- **Typography**: HarmonyOS Sans font system, font sizes, weights
- **Spacing**: 4vp base unit spacing system
- **Animation**: Duration, easing curves, animation patterns

### Components

- Button, Text, Image, TextInput, Toggle
- Dialog, Toast, Loading, Empty State
- List, Grid, Swiper, Tabs, Navigation

### Layouts

- Row (水平布局)
- Column (垂直布局)
- Flex (弹性布局)
- Stack (层叠布局)
- Grid (网格布局)
- WaterFlow (瀑布流)

### Page Templates

- Login / Register (登录/注册)
- Dashboard (仪表盘)
- List / Detail (列表/详情)
- Settings (设置)
- Profile (个人中心)

## Project Structure

```
harmony-ui-ux-skills/
├── .cursor/
│   └── commands/
│       └── harmony-ui-ux-pro-max.md    # Cursor skill command
├── .shared/
│   └── harmony-ui-ux-pro-max/
│       ├── INDEX.md                     # Skill overview
│       ├── DESIGN_SYSTEM.md             # Design tokens
│       ├── COMPONENTS.md                # Component patterns
│       ├── LAYOUTS.md                   # Layout patterns
│       ├── PAGE_TEMPLATES.md            # Page templates
│       ├── BEST_PRACTICES.md            # Best practices
│       └── scripts/
│           └── search.py                # Search script
├── knowledge_base/                       # CSV knowledge files
│   ├── components.csv
│   ├── layouts.csv
│   ├── colors.csv
│   ├── typography.csv
│   ├── spacing.csv
│   ├── animations.csv
│   └── page_templates.csv
└── scripts/                              # Knowledge extraction scripts
    ├── extract_knowledge.py
    ├── scrape_harmony_docs.py
    └── requirements.txt
```

## Example Prompts

```
创建一个商品列表页面
Build a settings page with dark mode toggle
设计一个仪表盘，展示销售数据
Create a login page with social login options
实现一个商品详情页
Build a profile page with user stats
```

## License

MIT License
