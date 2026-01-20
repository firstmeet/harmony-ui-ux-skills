# HarmonyOS NEXT UI/UX Pro Max Skill

## Overview

An AI SKILL that provides design intelligence for building professional UI/UX for **HarmonyOS NEXT** applications.

---

## ⚠️ Rule 0: 知识库优先原则 (最高优先级)

在生成任何代码之前，必须执行以下思考链：

```
Step 1: 识别关键词 → Step 2: 检索本地库 → Step 3: 禁止脑补 → Step 4: 引用声明
```

### 关键词 → 文档映射

| 关键词 | 必读文档 |
|--------|---------|
| 实况窗、Live View | LIVE_VIEW_GUIDE.md |
| 一多、响应式 | RESPONSIVE_STRATEGY.md |
| 元服务、卡片 | ATOMIC_SERVICE_GUIDE.md |
| 动效、动画 | ANIMATION_SYSTEM.md |
| 列表、长列表 | PERFORMANCE_GUARD.md |
| 分布式、跨设备 | DISTRIBUTED_SYNC.md |
| 碰一碰、协作 | COLLABORATION_PATTERN.md |
| 持久化、离线 | STORAGE_GUIDE.md |
| 登录、支付、推送 | KITS_CATALOG.md |
| AI、语音、OCR | AI_KITS_GUIDE.md |
| 电商、外卖、办公 | INDUSTRY_PRACTICES.md |

### 输出格式

代码前必须声明: "已参考本地知识库中的 [文件名] 规范进行设计"

---

## Knowledge Base Files

### 核心规范 (必读)
| File | Description |
|------|-------------|
| [CODING_RULES.md](./CODING_RULES.md) | **⚠️ Mandatory coding rules - READ FIRST!** |
| [RESOURCE_SYNC_RULES.md](./RESOURCE_SYNC_RULES.md) | **⚠️ 资源同步规则 - 生成代码时必读!** |

### 设计系统
| File | Description |
|------|-------------|
| [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md) | Design tokens: colors, typography, spacing |
| [COMPONENTS.md](./COMPONENTS.md) | ArkUI component patterns and usage examples |
| [PAGE_TEMPLATES.md](./PAGE_TEMPLATES.md) | Common page structure templates |

### 布局与响应式
| File | Description |
|------|-------------|
| [LAYOUTS.md](./LAYOUTS.md) | Layout patterns for HarmonyOS NEXT |
| [RESPONSIVE_STRATEGY.md](./RESPONSIVE_STRATEGY.md) | 一多架构断点和布局策略选择器 |

### 性能与动画
| File | Description |
|------|-------------|
| [PERFORMANCE_GUARD.md](./PERFORMANCE_GUARD.md) | 性能约束、LazyForEach 模板、反模式 |
| [ANIMATION_SYSTEM.md](./ANIMATION_SYSTEM.md) | 动画曲线、转场动画、共享元素 |

### 最佳实践
| File | Description |
|------|-------------|
| [BEST_PRACTICES.md](./BEST_PRACTICES.md) | UI/UX best practices and anti-patterns |

### 系统能力与 Kit ⭐ NEW
| File | Description |
|------|-------------|
| [KITS_CATALOG.md](./KITS_CATALOG.md) | **HarmonyOS Kit 完整目录** - 60+ Kit 分类与使用场景 |
| [AI_KITS_GUIDE.md](./AI_KITS_GUIDE.md) | **AI Kit 开发指南** - OCR/语音/NLP/智能体 |
| [INDUSTRY_PRACTICES.md](./INDUSTRY_PRACTICES.md) | **行业实践指南** - 17个行业开发方案 |

### 高级功能
| File | Description |
|------|-------------|
| [LIVE_VIEW_GUIDE.md](./LIVE_VIEW_GUIDE.md) | 实况窗开发指南 |
| [DISTRIBUTED_SYNC.md](./DISTRIBUTED_SYNC.md) | 分布式数据同步与流转 |
| [COLLABORATION_PATTERN.md](./COLLABORATION_PATTERN.md) | 分布式协同协议 (碰一碰) |
| [STORAGE_GUIDE.md](./STORAGE_GUIDE.md) | RDB 和 Preferences 持久化 |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | MVVM 架构规范 |

## Mandatory Rules Summary

### 基础规范 (Rule 1-6)
1. **Language**: ArkTS only, NO `any` type
2. **UI Framework**: ArkUI declarative syntax with @Component/@Entry
3. **State Management**: @State, @Prop, @Link, @Provide/@Consume, @Observed/@ObjectLink
4. **Resources**: NO hardcoded colors/strings - use `$r('app.color.xxx')`, `$r('app.string.xxx')`
5. **No Emoji**: NO emoji in code/comments - use icon resources instead
6. **Icon Check**: 先检查原生图标是否存在，不存在则从 allsvgicons.com 获取 SVG

### 设计规范 (Rule 7)
7. **一多架构**: 必须使用 GridCol/breakpoints/layoutWeight 实现响应式布局
8. **视觉风格**: 高端简约，圆角 8/12/16/24vp，分层设计，适当留白
9. **交互动效**: 使用 animateTo/animation，曲线 Curve.Friction/Sharp

### 代码质量 (Rule 8)
10. **禁止 px**: 必须使用 vp/fp 单位
11. **build() 纯净**: 禁止在 build() 中做复杂逻辑
12. **样式抽离**: 推荐 AttributeModifier 复用样式
13. **导航组件**: 推荐 Navigation 而非 Router

### 开发流程 (Rule 9)
14. **执行顺序**: 分析场景 → 定义数据 → 构建 UI → 注入动效

### 项目创建 (Rule 10)
15. **创建项目**: 使用 `python scripts/init_harmony_project.py <项目名> --sdk "<版本>"`
16. **验证编译**: 创建后必须执行 `hvigorw assembleHap --no-daemon` 验证

### 资源完整性 (Rule 11)
17. **同步输出**: 生成 `$r()` 代码时必须同时输出 string.json/color.json 片段
18. **命名规范**: 资源 Key 遵循 `模块名_功能名_属性名` 格式

### 布局策略 (Rule 12)
19. **自适应**: 基础组件用 `layoutWeight` / 百分比
20. **延伸布局**: 列表/宫格用 `Grid` + `breakpoints` (列数随宽度增加)
21. **分栏布局**: `windowWidth > 600vp` 时启用 `SideBarContainer`

### 性能准则 (Rule 13)
22. **减少嵌套**: 优先 `RelativeContainer` 替代多层 Column/Row
23. **长列表**: 数据量 > 50 必须用 `LazyForEach` + `keyGenerator`
24. **状态隔离**: 频繁更新的状态拆分为独立子组件

### 自动修复 (Rule 14)
25. **错误处理**: 编译失败时读取日志自动分析修复

### NEXT 特色 (Rule 15)
26. **元服务**: 主动询问是否需要 Atomic Service 卡片
27. **实况窗**: 进度类功能推荐 `@kit.LiveViewKit`
28. **系统 Kit**: 扫码用 `ScanKit`，分享用 `ShareKit`

### 跨文件同步 (Rule 16)
29. **页面注册**: 创建 @Entry 页面必须同步更新 `main_pages.json`
30. **权限声明**: 使用系统功能必须同步更新权限配置

### 强化禁止硬编码 (Rule 17)
31. **必须提供 Diff**: 修改页面时输出资源文件增量变更
32. **命名规范**: 资源 Key 遵循 `模块名_功能名_属性名` 格式

### 输出增强 (Rule 18)
33. **架构简图**: 生成代码前输出 UI 架构逻辑简图
34. **规范对齐**: 生成代码后附带规范对齐说明

### 脚本验证 (Rule 19)
35. **闭环检查**: 项目创建时检查脚本存在性，编译失败自动修复

## Quick Reference

### Colors
| Token | Value | 用途 |
|-------|-------|------|
| Primary | `#0A59F7` | 主色调 |
| Success | `#64BB5C` | 成功状态 |
| Warning | `#FA9D3B` | 警告状态 |
| Error | `#E84026` | 错误状态 |

### Typography
- **Font Family**: `HarmonyOS Sans`
- **Units**: 使用 `fp` (font pixel)

### Spacing
- **Base Unit**: `4vp`
- **标准间距**: 8, 12, 16, 24, 32vp

### Border Radius
| Size | Value | 用途 |
|------|-------|------|
| xs | 4vp | 徽章、标签 |
| sm | 8vp | 按钮、输入框 |
| md | 12vp | 列表项、小卡片 |
| lg | 16vp | 弹窗、大卡片 |
| xl | 24vp | 底部弹出层 |

### Animation Curves
| Curve | 用途 |
|-------|------|
| `Curve.Friction` | 页面转场、展开收起 |
| `Curve.Sharp` | 按钮反馈、快速交互 |
| `Curve.Smooth` | 滚动惯性 |

### Breakpoints
| Size | Width | 设备 |
|------|-------|------|
| xs | < 320vp | 小屏手机 |
| sm | 320-519vp | 手机 |
| md | 520-839vp | 折叠屏 |
| lg | ≥ 840vp | 平板 |

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

## Extended Knowledge Base

The knowledge base (`knowledge_base/`) contains additional resources scraped from official Huawei samples:

| Category | Files | Description |
|----------|-------|-------------|
| Official Samples | `official_samples.csv`, `ai_samples.csv` | 华为官方示例代码 |
| Components | `arkui_components.csv`, `code_snippets.csv` | ArkUI 组件完整参考 |
| Patterns | `arkui_patterns.csv`, `ui_effects.csv` | 常用 UI 模式与特效 |
| Services | `kits_reference.csv`, `app_services.csv` | HarmonyOS Kit 服务 |
| Distributed | `distributed_features.csv` | 分布式特性参考 |
| State | `state_management.csv`, `navigation_patterns.csv` | 状态管理与导航 |
| System | `system_capabilities.csv` | 系统能力参考 |
| Icons | `icons_guide.csv`, `harmony_symbols.csv` | 图标使用指南与原生图标列表 |

### Key HarmonyOS Kits

| Kit | Purpose |
|-----|---------|
| Core Vision Kit | 文字识别、人脸检测、图像分析 |
| Core Speech Kit | 语音识别(ASR)、语音合成(TTS) |
| Vision Kit | 文档扫描、卡证识别 |
| Speech Kit | AI字幕、朗读控件 |
| Share Kit | 隔空传送、碰一碰分享 |
| Health Kit | 运动健康数据管理 |
| Account Kit | 华为账号登录认证 |

## Usage

When building HarmonyOS NEXT UI/UX, the AI should:

1. Read the knowledge base files
2. Apply the design system tokens
3. Use the component patterns
4. Follow the layout guidelines
5. Check against best practices
6. Reference official samples for implementation