# 原型图源码分析指南

## 概述

当原型图是基于 HTML/CSS 实现时（如 Google Stitch），可以直接分析其源码提取精确的设计信息，包括：

- 精确的颜色值（Tailwind 类 → HarmonyOS 颜色）
- 完整的 SVG 图标
- 图片资源 URL
- CSS 动画定义
- 布局参数

---

## 触发条件

当用户提供以下类型的链接时，应启动源码分析流程：

| 平台 | 特征 | 源码类型 |
|------|------|----------|
| **Google Stitch** | `stitch.withgoogle.com` | HTML + Tailwind CSS |
| **Framer** | `framer.com/sites` | React + CSS |
| **Webflow** | `webflow.io` | HTML + CSS |
| **原型预览链接** | 可在浏览器中打开的 HTML 页面 | HTML + CSS |

---

## 完整分析流程

### Step 1: 获取页面源码

```
1. 使用 browser_navigate 访问原型图链接
2. 等待页面完全加载 (browser_wait_for)
3. 使用 browser_evaluate 获取 HTML 源码
4. 或者使用终端工具下载 HTML 文件
```

**示例命令：**

```powershell
# 下载 HTML 源码
curl -L "https://stitch.withgoogle.com/preview/xxx" -o prototype.html

# 读取并分析
Get-Content prototype.html | Select-String "bg-|text-|rounded-|shadow-"
```

### Step 2: 提取 Tailwind 颜色类

扫描 HTML 中的 Tailwind 类名，识别颜色定义：

```html
<!-- 原型图 HTML 示例 -->
<div class="bg-[#fbfaf9] text-[#191210]">
  <div class="bg-white/60 border-white/40 shadow-aura">
    <span class="text-orange-600 bg-orange-100">标签</span>
  </div>
</div>
```

**提取并转换：**

| Tailwind 类 | 值 | HarmonyOS 格式 |
|-------------|-----|----------------|
| `bg-[#fbfaf9]` | #fbfaf9 | `#FBFAF9` |
| `text-[#191210]` | #191210 | `#191210` |
| `bg-white/60` | rgba(255,255,255,0.6) | `#99FFFFFF` |
| `border-white/40` | rgba(255,255,255,0.4) | `#66FFFFFF` |
| `text-orange-600` | Tailwind orange-600 | `#EA580C` |
| `bg-orange-100` | Tailwind orange-100 | `#FFEDD5` |

### Step 3: 提取 SVG 图标

从 HTML 源码中直接提取完整的 SVG 代码：

```html
<!-- 原型图中的图标 -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M12 2C6.48 2 2 6.48 2 12..."/>
</svg>
```

**保存为本地文件：**

```
resources/base/media/
├── ic_breastfeeding.svg
├── ic_baby_changing.svg
├── ic_bedtime.svg
└── ic_vaccines.svg
```

⚠️ **注意**：确保复制完整的 SVG（包含 `<svg>` 标签和所有 `<path>` 元素），不完整的 SVG 会导致图标显示不全！

### Step 4: 下载图片资源

识别并下载原型图中的图片：

```html
<!-- 原型图中的图片 -->
<img src="https://lh3.googleusercontent.com/aida-public/xxx" alt="Baby photo">
```

**下载命令：**

```powershell
# 下载到项目 media 目录
Invoke-WebRequest -Uri "https://lh3.googleusercontent.com/aida-public/xxx" -OutFile "baby_photo.png"
```

**图片命名规范：**

| 用途 | 命名 |
|------|------|
| 用户头像 | `avatar_mom.png`, `avatar_dad.png` |
| 宝宝照片 | `baby_photo.png`, `baby_sleeping.png` |
| 背景图 | `bg_gradient.png`, `bg_pattern.svg` |
| 产品图 | `product_xxx.png` |

### Step 5: 提取 CSS 动画

识别 HTML 中的动画类并转换为 ArkTS：

```html
<!-- 原型图中的动画类 -->
<div class="animate-pulse">...</div>
<div class="animate-breathe">...</div>
```

**Tailwind 动画 → ArkTS 转换：**

| Tailwind 动画 | ArkTS 实现 |
|---------------|------------|
| `animate-pulse` | `opacity` 在 1 和 0.3 之间循环 |
| `animate-spin` | `rotate` 360度无限循环 |
| `animate-bounce` | `translateY` 弹跳效果 |

**自定义动画 (如 breathe)：**

```css
/* 原型图 CSS */
@keyframes breathe {
  0%, 100% { 
    transform: scale(1); 
    box-shadow: 0 0 0 0 rgba(230,172,153,0.4); 
  }
  50% { 
    transform: scale(1.02); 
    box-shadow: 0 0 12px 0 rgba(230,172,153,0); 
  }
}
```

**转换为 ArkTS：**

```typescript
@State breatheScale: number = 1
@State breatheOpacity: number = 0.4

aboutToAppear() {
  this.startBreatheAnimation()
}

// 使用 getUIContext().animateTo() 替代废弃的全局 animateTo
private startBreatheAnimation(): void {
  setInterval(() => {
    this.getUIContext().animateTo({
      duration: 2000,
      curve: Curve.EaseInOut
    }, () => {
      if (this.breatheScale === 1) {
        this.breatheScale = 1.02
        this.breatheOpacity = 0
      } else {
        this.breatheScale = 1
        this.breatheOpacity = 0.4
      }
    })
  }, 2000)
}

build() {
  Stack() {
    // 呼吸光环
    Circle()
      .fill($r('app.color.primary'))
      .opacity(this.breatheOpacity)
      .scale({ x: this.breatheScale, y: this.breatheScale })
    
    // 内容
    Image($r('app.media.baby_photo'))
      .scale({ x: this.breatheScale, y: this.breatheScale })
  }
}
```

---

## Tailwind 颜色速查表

### 标准颜色

| Tailwind | HarmonyOS |
|----------|-----------|
| `gray-50` | `#F9FAFB` |
| `gray-100` | `#F3F4F6` |
| `gray-200` | `#E5E7EB` |
| `gray-300` | `#D1D5DB` |
| `gray-400` | `#9CA3AF` |
| `gray-500` | `#6B7280` |
| `gray-600` | `#4B5563` |
| `gray-700` | `#374151` |
| `gray-800` | `#1F2937` |
| `gray-900` | `#111827` |

| Tailwind | HarmonyOS |
|----------|-----------|
| `orange-100` | `#FFEDD5` |
| `orange-200` | `#FED7AA` |
| `orange-300` | `#FDBA74` |
| `orange-600` | `#EA580C` |
| `yellow-100` | `#FEF9C3` |
| `yellow-600` | `#CA8A04` |
| `teal-100` | `#CCFBF1` |
| `teal-600` | `#0D9488` |
| `indigo-100` | `#E0E7FF` |
| `indigo-600` | `#4F46E5` |
| `purple-100` | `#F3E8FF` |
| `purple-600` | `#9333EA` |
| `red-100` | `#FEE2E2` |
| `red-500` | `#EF4444` |
| `red-600` | `#DC2626` |
| `green-500` | `#22C55E` |

---

## 实战案例：BabyTime 首页

### 分析结果

从 Google Stitch 原型图源码中提取：

**1. 颜色系统**

```json
{
  "color": [
    { "name": "primary", "value": "#E6AC99" },
    { "name": "primary_dark", "value": "#D08E7A" },
    { "name": "bg_primary", "value": "#FBFAF9" },
    { "name": "bg_glass", "value": "#A6FFFFFF" },
    { "name": "border_light", "value": "#66FFFFFF" },
    { "name": "feature_feeding_bg", "value": "#FFEDD5" },
    { "name": "feature_feeding_icon", "value": "#EA580C" },
    { "name": "feature_bottle_bg", "value": "#FEF9C3" },
    { "name": "feature_bottle_icon", "value": "#CA8A04" },
    { "name": "feature_diaper_bg", "value": "#CCFBF1" },
    { "name": "feature_diaper_icon", "value": "#0D9488" },
    { "name": "feature_sleep_bg", "value": "#E0E7FF" },
    { "name": "feature_sleep_icon", "value": "#4F46E5" },
    { "name": "feature_growth_bg", "value": "#F3E8FF" },
    { "name": "feature_growth_icon", "value": "#9333EA" },
    { "name": "feature_health_bg", "value": "#FFE4E6" },
    { "name": "feature_health_icon", "value": "#DC2626" }
  ]
}
```

**2. 图标 (从 SVG 提取)**

| 图标 | 文件 | 来源 |
|------|------|------|
| 母乳喂养 | `ic_breastfeeding.svg` | Material Symbols |
| 换尿布 | `ic_baby_changing.svg` | Material Symbols |
| 睡眠 | `ic_bedtime.svg` | Material Symbols |
| 疫苗 | `ic_vaccines.svg` | Material Symbols |
| 测量 | `ic_straighten.svg` | Material Symbols |
| 餐饮 | `ic_restaurant.svg` | Material Symbols |

**3. 图片资源**

| 资源 | 文件 | 尺寸 |
|------|------|------|
| 妈妈头像 | `avatar_mom.png` | 48x48 |
| 宝宝照片 | `baby_photo.png` | 80x80 |
| 爸爸头像 | `avatar_dad.png` | 40x40 |
| 奶奶头像 | `avatar_grandma.png` | 40x40 |

**4. 动画效果**

| 效果 | 实现 |
|------|------|
| 呼吸动画 | `scale: 1 → 1.02`, `opacity: 0.4 → 0`, 4s 循环 |
| 状态点闪烁 | `opacity: 1 → 0.3`, 1s 循环 |

---

## AI 检测清单

当分析原型图源码时，AI 必须：

1. ✅ 完整获取 HTML 源码（不只是截图）
2. ✅ 提取所有 Tailwind 颜色类并转换格式
3. ✅ **提取完整的 SVG 代码**（不要截断！）
4. ✅ 下载所有图片资源到本地
5. ✅ 识别并转换 CSS 动画为 ArkTS
6. ✅ 将透明度颜色转换为 `#AARRGGBB` 格式
7. ✅ 验证所有资源文件已正确保存

### 常见错误

| 错误 | 正确做法 |
|------|----------|
| SVG 只复制了部分 path | 复制完整的 `<svg>...</svg>` |
| 透明度格式错误 `#FFFFFF99` | 转换为 `#99FFFFFF` |
| 图片链接无法访问 | 使用 `curl -L` 跟随重定向下载 |
| 遗漏深色模式颜色 | 同时提取 dark mode 变体 |
