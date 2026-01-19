# HarmonyOS NEXT Design System

## Overview

This design system defines the visual language and design tokens for HarmonyOS NEXT applications.

---

## Color System

### Brand Colors

| Token | Value | Usage |
|-------|-------|-------|
| `primary` | `#0A59F7` | 主要操作按钮、链接、强调元素 |
| `primary_light` | `#5B8FF9` | 悬浮状态、次要强调 |
| `primary_dark` | `#0041C2` | 按压状态 |
| `secondary` | `#36D1DC` | 辅助强调、渐变配色 |
| `accent` | `#FF6B35` | 强调色、促销标签 |

### Semantic Colors

| Token | Value | Usage |
|-------|-------|-------|
| `success` | `#64BB5C` | 成功状态、完成提示 |
| `warning` | `#FA9D3B` | 警告状态、注意提示 |
| `error` | `#E84026` | 错误状态、删除操作 |
| `info` | `#0A59F7` | 信息提示、帮助说明 |

### Neutral Colors (Light Mode)

| Token | Value | Usage |
|-------|-------|-------|
| `text_primary` | `#182431` | 主要文字、标题 |
| `text_secondary` | `#66727A` | 次要文字、说明 |
| `text_tertiary` | `#99A4AE` | 辅助文字、占位符 |
| `text_disabled` | `#C5CDD7` | 禁用状态文字 |
| `bg_primary` | `#FFFFFF` | 主要背景、卡片背景 |
| `bg_secondary` | `#F1F3F5` | 次要背景、页面背景 |
| `border_light` | `#E5E8EB` | 分割线、轻边框 |

### Neutral Colors (Dark Mode)

| Token | Value | Usage |
|-------|-------|-------|
| `text_primary` | `#E5E8EB` | 主要文字、标题 |
| `text_secondary` | `#99A4AE` | 次要文字、说明 |
| `bg_primary` | `#121212` | 主要背景 |
| `bg_secondary` | `#1E1E1E` | 次要背景 |
| `border_light` | `#383838` | 分割线、轻边框 |

---

## Typography

### Font Family

- **System Font**: `HarmonyOS Sans`
- **Monospace**: `HarmonyOS Sans Mono`

### Font Sizes (unit: fp)

| Token | Size | Usage |
|-------|------|-------|
| `display_large` | `48fp` | 超大展示数字、主数据 |
| `display_medium` | `32fp` | 大标题、展示数据 |
| `display_small` | `24fp` | 中等展示标题 |
| `headline_large` | `20fp` | 页面标题 |
| `headline_medium` | `18fp` | 区块标题 |
| `headline_small` | `16fp` | 小标题、列表标题 |
| `body_large` | `16fp` | 大段正文内容 |
| `body_medium` | `14fp` | 正文内容、描述文字 |
| `body_small` | `12fp` | 辅助说明、时间戳 |
| `label_large` | `14fp` | 按钮文字、标签 |
| `label_medium` | `12fp` | 小标签、徽标 |
| `label_small` | `10fp` | 极小标签、注释 |

### Font Weights

| Token | Weight | Usage |
|-------|--------|-------|
| `regular` | `400` | 正文 |
| `medium` | `500` | 标签、按钮 |
| `semibold` | `600` | 小标题 |
| `bold` | `700` | 大标题 |

---

## Spacing System

### Base Unit: 4vp

| Token | Value | Usage |
|-------|-------|-------|
| `space_xxs` | `2vp` | 极小间距 |
| `space_xs` | `4vp` | 微小间距 |
| `space_sm` | `8vp` | 小间距，相关元素分组 |
| `space_md` | `12vp` | 中间距，列表项间隔 |
| `space_lg` | `16vp` | 大间距，卡片内边距 |
| `space_xl` | `20vp` | 较大间距 |
| `space_xxl` | `24vp` | 超大间距，模块分隔 |
| `space_xxxl` | `32vp` | 巨大间距，页面边距 |

### Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `radius_xs` | `4vp` | 小圆角，标签、徽标 |
| `radius_sm` | `8vp` | 标准圆角，按钮、输入框 |
| `radius_md` | `12vp` | 中圆角，卡片 |
| `radius_lg` | `16vp` | 大圆角，模态框 |
| `radius_xl` | `24vp` | 超大圆角，底部弹窗 |
| `radius_full` | `9999vp` | 胶囊形，胶囊按钮、头像 |

---

## Animation

### Duration

| Token | Duration | Usage |
|-------|----------|-------|
| `duration_instant` | `0ms` | 无动画 |
| `duration_fastest` | `100ms` | 微交互、涟漪效果 |
| `duration_fast` | `150ms` | 按钮反馈、开关切换 |
| `duration_normal` | `200ms` | 普通过渡、淡入淡出 |
| `duration_medium` | `300ms` | 弹窗进入、抽屉展开 |
| `duration_slow` | `400ms` | 页面切换 |

### Easing Curves

| Token | Curve | Usage |
|-------|-------|-------|
| `easing_standard` | `Curve.EaseInOut` | 通用动画 |
| `easing_decelerate` | `Curve.EaseOut` | 进入动画 |
| `easing_accelerate` | `Curve.EaseIn` | 退出动画 |
| `easing_emphasized` | `Curve.FastOutSlowIn` | 重点关注的动画 |
| `easing_spring` | `Curve.Smooth` | 弹性效果 |

---

## Component Sizes

### Button Heights

| Size | Height |
|------|--------|
| Small | `28vp` |
| Medium | `36vp` |
| Large | `44vp` |
| XLarge | `52vp` |

### Input Heights

| Size | Height |
|------|--------|
| Small | `32vp` |
| Medium | `40vp` |
| Large | `48vp` |

### Icon Sizes

| Size | Value |
|------|-------|
| XSmall | `12vp` |
| Small | `16vp` |
| Medium | `20vp` |
| Large | `24vp` |
| XLarge | `32vp` |
| XXLarge | `48vp` |

---

## Multi-Device Breakpoints

| Device | Width |
|--------|-------|
| Compact (Phone) | `< 600vp` |
| Medium (Tablet) | `600vp - 840vp` |
| Expanded (Desktop) | `> 840vp` |
