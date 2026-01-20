# HarmonyOS NEXT 自定义字体注册与应用高级指南

## 概述

本文档定义了在 HarmonyOS NEXT 应用中注册和使用自定义字体的标准流程，确保**零闪烁（No FOUT）**和**全局可用性**。

---

## 1. 核心原则

在 HarmonyOS NEXT 中，自定义字体属于**系统级资源**。为了确保最佳用户体验：

| 原则 | 说明 |
|------|------|
| **零闪烁 (No FOUT)** | 字体必须在 UI 渲染前完成加载，避免字体切换闪烁 |
| **全局可用性** | 字体注册一次，所有页面均可使用 |
| **资源引用规范** | 必须使用 `$r()` 语法，禁止硬编码路径 |
| **异常处理** | 必须包含 try-catch 逻辑，处理字体加载失败 |

---

## 2. 最佳注册时机：loadContent 拦截

### ⚠️ 强制规范

```
❌ 禁止：在 Page 级别 (aboutToAppear) 注册全局字体
❌ 禁止：在 build() 方法中注册字体
❌ 禁止：使用硬编码本地绝对路径

✅ 必须：在 EntryAbility.onWindowStageCreate 中注册
✅ 必须：在 loadContent 执行前完成注册
✅ 必须：使用 $r() 引用字体资源
```

### 时序图

```
┌─────────────────────────────────────────────────────────────────┐
│  App Launch                                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  EntryAbility.onWindowStageCreate()                              │
│  ─────────────────────────────────                               │
│  1. FontManager.registerCustomFonts()  ← 字体注册 (先执行)        │
│  2. windowStage.loadContent()          ← 加载 UI (后执行)        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Page Render (字体已可用，无闪烁)                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. 标准实现代码

### A. 字体管理器封装 (FontManager.ets)

将注册逻辑抽离，便于多字体管理和错误追踪。

**文件路径**: `entry/src/main/ets/utils/FontManager.ets`

```typescript
import { font } from '@kit.ArkUI'

/**
 * 自定义字体管理器
 * 在 EntryAbility.onWindowStageCreate 中调用
 */
export class FontManager {
  private static isRegistered: boolean = false

  /**
   * 注册所有自定义字体
   * 必须在 loadContent 之前调用
   */
  public static registerCustomFonts(): void {
    if (this.isRegistered) {
      console.info('FontManager: Fonts already registered, skipping.')
      return
    }

    try {
      // === 注册品牌主字体 ===
      font.registerFont({
        familyName: 'BrandFont',
        familySrc: $r('app.media.BrandFont_Regular')
      })

      // === 注册品牌粗体 ===
      font.registerFont({
        familyName: 'BrandFont-Bold',
        familySrc: $r('app.media.BrandFont_Bold')
      })

      // === 注册品牌细体 (可选) ===
      font.registerFont({
        familyName: 'BrandFont-Light',
        familySrc: $r('app.media.BrandFont_Light')
      })

      this.isRegistered = true
      console.info('FontManager: Custom fonts registered successfully.')
    } catch (error) {
      const err = error as BusinessError
      console.error(`FontManager: Failed to register fonts. Code: ${err.code}, Message: ${err.message}`)
    }
  }

  /**
   * 检查字体是否已注册
   */
  public static isFontRegistered(): boolean {
    return this.isRegistered
  }
}

// 类型定义
interface BusinessError {
  code: number
  message: string
}
```

### B. Ability 集成 (EntryAbility.ets)

在页面加载前拦截并注入字体。

**文件路径**: `entry/src/main/ets/entryability/EntryAbility.ets`

```typescript
import { AbilityConstant, UIAbility, Want } from '@kit.AbilityKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { window } from '@kit.ArkUI'
import { FontManager } from '../utils/FontManager'

export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    hilog.info(0x0000, 'EntryAbility', 'Ability onCreate')
  }

  onDestroy(): void {
    hilog.info(0x0000, 'EntryAbility', 'Ability onDestroy')
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    hilog.info(0x0000, 'EntryAbility', 'Ability onWindowStageCreate')

    // ⚠️ 重要：在加载 UI 之前执行字体注册
    FontManager.registerCustomFonts()

    // 加载入口页面
    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        hilog.error(0x0000, 'EntryAbility', 'Failed to load content. Cause: %{public}s', JSON.stringify(err))
        return
      }
      hilog.info(0x0000, 'EntryAbility', 'Succeeded in loading content.')
    })
  }

  onWindowStageDestroy(): void {
    hilog.info(0x0000, 'EntryAbility', 'Ability onWindowStageDestroy')
  }

  onForeground(): void {
    hilog.info(0x0000, 'EntryAbility', 'Ability onForeground')
  }

  onBackground(): void {
    hilog.info(0x0000, 'EntryAbility', 'Ability onBackground')
  }
}
```

---

## 4. 资源配置规范

### 文件格式

| 格式 | 支持状态 | 说明 |
|------|---------|------|
| `.ttf` | ✅ 支持 | TrueType Font，推荐使用 |
| `.otf` | ✅ 支持 | OpenType Font |
| `.woff` | ❌ 不支持 | Web 字体格式 |
| `.woff2` | ❌ 不支持 | Web 字体格式 |

### 存储位置

| 位置 | 引用方式 | 推荐度 |
|------|---------|-------|
| `resources/base/media/` | `$r('app.media.FontName')` | ⭐⭐⭐ 推荐 |
| `resources/rawfile/` | `$rawfile('fonts/FontName.ttf')` | ⭐⭐ 备选 |

### 目录结构示例

```
entry/src/main/resources/
├── base/
│   ├── element/
│   │   └── string.json
│   └── media/
│       ├── BrandFont_Regular.ttf    ← 常规字体
│       ├── BrandFont_Bold.ttf       ← 粗体
│       ├── BrandFont_Light.ttf      ← 细体
│       └── IconFont.ttf             ← 图标字体
└── rawfile/
    └── fonts/
        └── CustomFont.ttf           ← 备选位置
```

### 命名规范

遵循 `FontName_Weight.ttf` 格式：

| 字重 | 文件名示例 | familyName |
|------|-----------|------------|
| Thin | `BrandFont_Thin.ttf` | `BrandFont-Thin` |
| Light | `BrandFont_Light.ttf` | `BrandFont-Light` |
| Regular | `BrandFont_Regular.ttf` | `BrandFont` |
| Medium | `BrandFont_Medium.ttf` | `BrandFont-Medium` |
| Bold | `BrandFont_Bold.ttf` | `BrandFont-Bold` |
| Black | `BrandFont_Black.ttf` | `BrandFont-Black` |

---

## 5. UI 层调用规范

### 基础用法

```typescript
Text('品牌标题')
  .fontFamily('BrandFont')  // 必须与注册时的 familyName 完全一致
  .fontSize(24)
  .fontWeight(FontWeight.Medium)
  .fontColor($r('app.color.text_primary'))
```

### 多字重组合

```typescript
Column({ space: 8 }) {
  // 细体 - 辅助文字
  Text('Secondary Text')
    .fontFamily('BrandFont-Light')
    .fontSize(12)
    .fontColor($r('app.color.text_secondary'))

  // 常规 - 正文
  Text('Body Text')
    .fontFamily('BrandFont')
    .fontSize(16)
    .fontColor($r('app.color.text_primary'))

  // 粗体 - 标题
  Text('Heading')
    .fontFamily('BrandFont-Bold')
    .fontSize(24)
    .fontColor($r('app.color.text_primary'))
}
```

### 封装为可复用组件

```typescript
@Component
struct BrandText {
  @Prop text: string = ''
  @Prop size: number = 16
  @Prop weight: FontWeight = FontWeight.Normal
  @Prop color: ResourceColor = $r('app.color.text_primary')

  build() {
    Text(this.text)
      .fontFamily(this.getFontFamily())
      .fontSize(this.size)
      .fontColor(this.color)
  }

  private getFontFamily(): string {
    switch (this.weight) {
      case FontWeight.Light:
      case FontWeight.Lighter:
        return 'BrandFont-Light'
      case FontWeight.Bold:
      case FontWeight.Bolder:
        return 'BrandFont-Bold'
      default:
        return 'BrandFont'
    }
  }
}

// 使用
BrandText({ text: '品牌文字', size: 20, weight: FontWeight.Bold })
```

---

## 6. AI 行为检测 (Verification)

当用户请求处理自定义字体时，AI 必须执行以下检查：

### 检查清单

```
┌─────────────────────────────────────────────────────────────────┐
│  Check 1: 注册位置                                               │
│  ─────────────────                                               │
│  ❓ 是否在 EntryAbility.onWindowStageCreate 中注册？              │
│  ✅ 是 → 继续                                                    │
│  ❌ 否 → 自动生成 FontManager.ets 并修改 EntryAbility            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Check 2: 资源引用                                               │
│  ─────────────                                                   │
│  ❓ 是否使用 $r('app.media.xxx') 引用字体？                       │
│  ✅ 是 → 继续                                                    │
│  ❌ 否 → 提醒修改，禁止硬编码路径                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Check 3: 异常处理                                               │
│  ─────────────                                                   │
│  ❓ 是否包含 try-catch 逻辑？                                     │
│  ✅ 是 → 继续                                                    │
│  ❌ 否 → 自动添加异常处理代码                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Check 4: 字体文件                                               │
│  ─────────────                                                   │
│  ❓ resources/base/media/ 下是否存在对应的 .ttf/.otf 文件？        │
│  ✅ 是 → 完成                                                    │
│  ❌ 否 → 提醒用户添加字体文件                                      │
└─────────────────────────────────────────────────────────────────┘
```

### 自动生成触发词

当用户说以下内容时，自动生成字体注册代码：

| 用户输入 | AI 行为 |
|---------|--------|
| "添加自定义字体" | 生成 FontManager + 修改 EntryAbility |
| "使用 xxx 字体" | 检查是否已注册，未注册则提示 |
| "注册品牌字体" | 生成完整字体注册方案 |
| "项目需要用 xxx 字体" | 生成 FontManager + UI 调用示例 |

---

## 7. 进阶：IconFont 图标字体

### 方案一：SymbolGlyph 组件 (API 11+ 推荐)

```typescript
// 使用系统原生图标（推荐）
SymbolGlyph($r('sys.symbol.heart'))
  .fontSize(24)
  .fontColor([$r('app.color.primary')])
```

### 方案二：Text + Unicode (IconFont)

```typescript
// 注册图标字体
font.registerFont({
  familyName: 'IconFont',
  familySrc: $r('app.media.IconFont')
})

// 使用 Unicode 编码
Text('\uE001')  // 对应 IconFont 中的图标编码
  .fontFamily('IconFont')
  .fontSize(24)
  .fontColor($r('app.color.icon_primary'))
```

### 封装图标组件

```typescript
@Component
struct AppIcon {
  @Prop name: string = ''  // Unicode 或图标名
  @Prop size: number = 24
  @Prop color: ResourceColor = $r('app.color.icon_primary')

  // 图标映射表
  private iconMap: Record<string, string> = {
    'home': '\uE001',
    'user': '\uE002',
    'cart': '\uE003',
    'heart': '\uE004',
    'search': '\uE005'
  }

  build() {
    Text(this.iconMap[this.name] || this.name)
      .fontFamily('IconFont')
      .fontSize(this.size)
      .fontColor(this.color)
  }
}

// 使用
AppIcon({ name: 'home', size: 24 })
AppIcon({ name: 'cart', size: 32, color: $r('app.color.primary') })
```

---

## 8. 性能优化

### 字体文件大小优化

| 优化方式 | 说明 |
|---------|------|
| **子集化** | 只保留使用的字符，可减少 50-90% 体积 |
| **压缩** | 使用 woff2 工具压缩后转回 ttf |
| **分离字重** | 按需加载不同字重，避免一次性加载全部 |

### 懒加载策略 (可选)

对于非核心字体，可考虑延迟加载：

```typescript
export class FontManager {
  // 核心字体：立即加载
  public static registerCoreFonts(): void {
    font.registerFont({
      familyName: 'BrandFont',
      familySrc: $r('app.media.BrandFont_Regular')
    })
  }

  // 次要字体：按需加载
  public static registerSecondaryFont(fontName: string): void {
    const fontMap: Record<string, Resource> = {
      'DisplayFont': $r('app.media.DisplayFont'),
      'MonoFont': $r('app.media.MonoFont')
    }

    if (fontMap[fontName]) {
      font.registerFont({
        familyName: fontName,
        familySrc: fontMap[fontName]
      })
    }
  }
}
```

---

## 9. 常见问题

### Q1: 字体注册后不生效？

**检查清单:**
1. familyName 是否与 UI 中使用的完全一致（大小写敏感）
2. 字体文件是否放在正确位置
3. 是否在 loadContent 之前调用了注册方法

### Q2: 如何支持多语言字体？

```typescript
// 中文字体
font.registerFont({
  familyName: 'BrandFont-CN',
  familySrc: $r('app.media.BrandFont_CN')
})

// 英文字体
font.registerFont({
  familyName: 'BrandFont-EN',
  familySrc: $r('app.media.BrandFont_EN')
})

// UI 中根据语言选择
Text('Hello 你好')
  .fontFamily(this.isChineseLocale ? 'BrandFont-CN' : 'BrandFont-EN')
```

### Q3: 字体加载失败如何降级？

```typescript
Text('品牌文字')
  .fontFamily('BrandFont, HarmonyOS Sans')  // 逗号分隔，按顺序降级
  .fontSize(16)
```

---

## 10. 完整示例：从原型图到实现

当用户提供带有自定义字体的原型图时：

```
用户: 原型图使用了 "Noto Sans SC" 字体，帮我配置

AI: 
1. 请将字体文件放置到以下位置：
   entry/src/main/resources/base/media/NotoSansSC_Regular.ttf
   entry/src/main/resources/base/media/NotoSansSC_Bold.ttf

2. 我已生成 FontManager.ets：
   [输出 FontManager 代码]

3. 我已修改 EntryAbility.ets：
   [输出修改后的代码]

4. UI 调用示例：
   Text('你好世界')
     .fontFamily('NotoSansSC')
     .fontSize(16)
```

---

## 相关文档

- `CODING_RULES.md` - 编码规范
- `DESIGN_TOKEN_EXTRACTION.md` - 设计 Token 提取（含字体规范）
- `RESOURCE_SYNC_RULES.md` - 资源同步规则
