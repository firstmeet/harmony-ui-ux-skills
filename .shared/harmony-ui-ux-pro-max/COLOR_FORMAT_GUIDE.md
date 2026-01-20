# HarmonyOS 颜色格式规范

## ⚠️ 核心规则：颜色格式

HarmonyOS 使用 **`#AARRGGBB`** 格式（Alpha 在前），与 CSS 的 `#RRGGBBAA` 格式**完全不同**！

### 格式对比

| 平台 | 格式 | 示例 (60% 透明白色) |
|------|------|---------------------|
| **HarmonyOS** | `#AARRGGBB` | `#99FFFFFF` ✅ |
| CSS | `#RRGGBBAA` | `#FFFFFF99` ❌ |
| Tailwind | `bg-white/60` | 需转换为 `#99FFFFFF` |

### 透明度换算表

| 透明度 | Hex 值 | HarmonyOS 格式 |
|--------|--------|----------------|
| 100% | FF | `#FFRRGGBB` |
| 90% | E6 | `#E6RRGGBB` |
| 80% | CC | `#CCRRGGBB` |
| 70% | B3 | `#B3RRGGBB` |
| 65% | A6 | `#A6RRGGBB` |
| 60% | 99 | `#99RRGGBB` |
| 50% | 80 | `#80RRGGBB` |
| 40% | 66 | `#66RRGGBB` |
| 30% | 4D | `#4DRRGGBB` |
| 25% | 40 | `#40RRGGBB` |
| 20% | 33 | `#33RRGGBB` |
| 15% | 26 | `#26RRGGBB` |
| 10% | 1A | `#1ARRGGBB` |
| 5% | 0D | `#0DRRGGBB` |
| 0% | 00 | `#00RRGGBB` |

---

## 常见错误案例

### ❌ 错误：使用 CSS 格式

```json
// color.json - 错误格式
{
  "color": [
    { "name": "bg_glass", "value": "#FFFFFFA6" },     // ❌ 会显示异常颜色
    { "name": "overlay", "value": "#00000066" },      // ❌ 会显示异常颜色
    { "name": "shadow_aura", "value": "#E6AC9940" }   // ❌ 会显示异常颜色
  ]
}
```

```typescript
// HomePage.ets - 错误格式
.backgroundColor('#FFFFFF66')    // ❌ 会显示异常颜色
.shadow({ color: '#E6AC9926' })  // ❌ 阴影颜色错误
.border({ color: '#FFFFFF80' })  // ❌ 边框颜色错误
```

### ✅ 正确：使用 HarmonyOS 格式

```json
// color.json - 正确格式
{
  "color": [
    { "name": "bg_glass", "value": "#A6FFFFFF" },     // ✅ 65% 透明白色
    { "name": "overlay", "value": "#66000000" },      // ✅ 40% 透明黑色
    { "name": "shadow_aura", "value": "#40E6AC99" }   // ✅ 25% 透明主色
  ]
}
```

```typescript
// HomePage.ets - 正确格式
.backgroundColor('#66FFFFFF')    // ✅ 40% 透明白色
.shadow({ color: '#26E6AC99' })  // ✅ 15% 透明主色阴影
.border({ color: '#80FFFFFF' })  // ✅ 50% 透明白色边框
```

---

## Tailwind CSS 转换指南

从原型图（如 Google Stitch 使用 Tailwind）提取颜色时的转换规则：

### Tailwind 透明度类转换

| Tailwind 类 | CSS 值 | HarmonyOS 格式 |
|-------------|--------|----------------|
| `bg-white` | `#FFFFFF` | `#FFFFFF` |
| `bg-white/90` | `rgba(255,255,255,0.9)` | `#E6FFFFFF` |
| `bg-white/80` | `rgba(255,255,255,0.8)` | `#CCFFFFFF` |
| `bg-white/70` | `rgba(255,255,255,0.7)` | `#B3FFFFFF` |
| `bg-white/60` | `rgba(255,255,255,0.6)` | `#99FFFFFF` |
| `bg-white/50` | `rgba(255,255,255,0.5)` | `#80FFFFFF` |
| `bg-white/40` | `rgba(255,255,255,0.4)` | `#66FFFFFF` |
| `bg-white/30` | `rgba(255,255,255,0.3)` | `#4DFFFFFF` |
| `bg-white/20` | `rgba(255,255,255,0.2)` | `#33FFFFFF` |
| `bg-white/10` | `rgba(255,255,255,0.1)` | `#1AFFFFFF` |

### 常用 Tailwind 颜色转换

| Tailwind | HarmonyOS |
|----------|-----------|
| `bg-black/50` | `#80000000` |
| `bg-primary/40` | `#66{主色值}` |
| `shadow-lg` (阴影颜色) | `#1A000000` 或 `#26000000` |
| `border-white/50` | `#80FFFFFF` |

---

## 转换工具函数

在代码中可使用以下工具函数进行转换：

```typescript
/**
 * 将 CSS 颜色格式 (#RRGGBBAA) 转换为 HarmonyOS 格式 (#AARRGGBB)
 */
function cssToHarmonyColor(cssColor: string): string {
  if (cssColor.length === 9 && cssColor.startsWith('#')) {
    // #RRGGBBAA -> #AARRGGBB
    const rrggbb = cssColor.substring(1, 7)
    const aa = cssColor.substring(7, 9)
    return `#${aa}${rrggbb}`
  }
  return cssColor // 无需转换
}

/**
 * 根据透明度百分比生成 HarmonyOS 颜色
 */
function colorWithOpacity(hexColor: string, opacity: number): string {
  const alpha = Math.round(opacity * 255).toString(16).padStart(2, '0').toUpperCase()
  const rgb = hexColor.replace('#', '').substring(0, 6)
  return `#${alpha}${rgb}`
}

// 使用示例
const glassWhite = colorWithOpacity('#FFFFFF', 0.65)  // -> #A6FFFFFF
const shadowColor = colorWithOpacity('#E6AC99', 0.25) // -> #40E6AC99
```

---

## AI 检测清单

当从原型图（尤其是 Tailwind CSS 原型）提取颜色时，AI 必须：

1. ✅ 识别带透明度的颜色值
2. ✅ 将 `#RRGGBBAA` 转换为 `#AARRGGBB`
3. ✅ 将 Tailwind 透明度类 (`bg-white/60`) 转换为正确格式
4. ✅ 将 `rgba()` 格式转换为 8 位 hex
5. ✅ 检查代码中硬编码的颜色是否为正确格式

### 输出时自检

```
❓ 这个颜色有透明度吗？
    ↓
如果有，Alpha 值是否在颜色值的最前面？
    ↓
✅ #AARRGGBB 正确
❌ #RRGGBBAA 错误，需要转换
```

---

## 常见场景示例

### 玻璃态效果 (Glassmorphism)

```typescript
// 正确的玻璃态卡片
Column() {
  // 内容
}
.backgroundColor('#A6FFFFFF')        // 65% 透明白色背景
.border({ 
  width: 1, 
  color: '#66FFFFFF'                 // 40% 透明白色边框
})
.backdropBlur(24)                    // 模糊效果
.shadow({
  radius: 20,
  color: '#26000000',                // 15% 透明黑色阴影
  offsetY: 10
})
```

### 品牌色阴影

```typescript
// 带品牌色光晕的按钮
Button('确认')
.backgroundColor('#E6AC99')           // 主色
.shadow({
  radius: 16,
  color: '#66E6AC99',                 // 40% 透明主色阴影
  offsetY: 8
})
```

### 遮罩层

```typescript
// 半透明遮罩
Column()
.backgroundColor('#80000000')         // 50% 透明黑色遮罩
.width('100%')
.height('100%')
```
