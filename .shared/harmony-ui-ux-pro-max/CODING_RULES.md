# HarmonyOS NEXT Coding Rules

## Overview

This document defines the **mandatory coding rules** for HarmonyOS NEXT development. All generated code MUST follow these rules.

---

## Rule 1: Language - ArkTS Only

### Requirements

- **MUST** use ArkTS (strict TypeScript-based language)
- **MUST NOT** use `any` type - always use explicit types
- **MUST** enable strict type checking

### Examples

```typescript
// ✅ CORRECT - Explicit types
@State count: number = 0
@State items: Array<ItemData> = []
@State user: UserInfo | null = null

interface ItemData {
  id: number
  title: string
  price: number
}

function fetchData(): Promise<Array<ItemData>> {
  // implementation
}

// ❌ WRONG - Using 'any'
@State count: any = 0           // FORBIDDEN
@State items: any[] = []        // FORBIDDEN
let data: any                   // FORBIDDEN

function fetchData(): any {     // FORBIDDEN
  // implementation
}
```

---

## Rule 2: UI Framework - ArkUI Declarative Syntax

### Requirements

- **MUST** use ArkUI declarative UI syntax
- **MUST** use `@Component` decorator for custom components
- **MUST** use `@Entry` decorator for entry pages
- **MUST** implement `build()` method in all components

### Examples

```typescript
// ✅ CORRECT - Declarative component
@Entry
@Component
struct HomePage {
  @State message: string = 'Hello'

  build() {
    Column() {
      Text(this.message)
        .fontSize(20)
      
      Button($r('app.string.click_me'))
        .onClick(() => {
          this.message = 'Clicked!'
        })
    }
    .width('100%')
    .height('100%')
  }
}

// ✅ CORRECT - Reusable component
@Component
struct MyButton {
  @Prop label: string = ''
  onButtonClick: () => void = () => {}

  build() {
    Button(this.label)
      .onClick(() => this.onButtonClick())
  }
}
```

---

## Rule 3: State Management Priority

### Requirements

Use state decorators in this priority order:

| Decorator | Use Case | Binding |
|-----------|----------|---------|
| `@State` | Component internal state | None |
| `@Prop` | Parent to child data | One-way |
| `@Link` | Parent to child data | Two-way |
| `@Provide` / `@Consume` | Cross-component sharing | Descendant access |
| `@Observed` + `@ObjectLink` | Complex object observation | Object reference |

### Examples

```typescript
// @State - Component internal state
@Component
struct Counter {
  @State private count: number = 0

  build() {
    Button(`Count: ${this.count}`)
      .onClick(() => { this.count++ })
  }
}

// @Prop - One-way binding (parent to child)
@Component
struct ChildComponent {
  @Prop title: string = ''  // Receives from parent, cannot modify parent

  build() {
    Text(this.title)
  }
}

// @Link - Two-way binding
@Component
struct ParentComponent {
  @State inputValue: string = ''

  build() {
    InputField({ value: $inputValue })  // Pass with $ prefix
  }
}

@Component
struct InputField {
  @Link value: string  // Changes sync back to parent

  build() {
    TextInput({ text: this.value })
      .onChange((newValue: string) => {
        this.value = newValue
      })
  }
}

// @Provide / @Consume - Cross-component sharing
@Entry
@Component
struct App {
  @Provide('theme') theme: string = 'light'

  build() {
    Column() {
      DeepNestedComponent()
    }
  }
}

@Component
struct DeepNestedComponent {
  @Consume('theme') theme: string  // Access ancestor's @Provide

  build() {
    Text(`Theme: ${this.theme}`)
  }
}

// @Observed + @ObjectLink - Complex object state
@Observed
class CartItem {
  id: number
  name: string
  quantity: number

  constructor(id: number, name: string, quantity: number = 1) {
    this.id = id
    this.name = name
    this.quantity = quantity
  }
}

@Component
struct CartItemView {
  @ObjectLink item: CartItem  // Observes object property changes

  build() {
    Row() {
      Text(this.item.name)
      Button('+')
        .onClick(() => { this.item.quantity++ })
      Text(`${this.item.quantity}`)
    }
  }
}
```

---

## Rule 4: Resource References - NO Hardcoding!

### Requirements

- **MUST NOT** hardcode colors - use `$r('app.color.xxx')`
- **MUST NOT** hardcode strings - use `$r('app.string.xxx')`
- **MUST NOT** hardcode images - use `$r('app.media.xxx')`
- **SHOULD** use `$r('app.float.xxx')` for dimensions when needed

### Resource File Definitions

**resources/base/element/color.json**:
```json
{
  "color": [
    { "name": "primary", "value": "#0A59F7" },
    { "name": "primary_light", "value": "#5B8FF9" },
    { "name": "primary_dark", "value": "#0041C2" },
    { "name": "secondary", "value": "#36D1DC" },
    { "name": "accent", "value": "#FF6B35" },
    { "name": "success", "value": "#64BB5C" },
    { "name": "warning", "value": "#FA9D3B" },
    { "name": "error", "value": "#E84026" },
    { "name": "info", "value": "#0A59F7" },
    { "name": "text_primary", "value": "#182431" },
    { "name": "text_secondary", "value": "#66727A" },
    { "name": "text_tertiary", "value": "#99A4AE" },
    { "name": "text_disabled", "value": "#C5CDD7" },
    { "name": "text_inverse", "value": "#FFFFFF" },
    { "name": "bg_primary", "value": "#FFFFFF" },
    { "name": "bg_secondary", "value": "#F1F3F5" },
    { "name": "bg_tertiary", "value": "#E5E8EB" },
    { "name": "border_light", "value": "#E5E8EB" },
    { "name": "border_medium", "value": "#C5CDD7" },
    { "name": "divider", "value": "#E5E8EB" }
  ]
}
```

**resources/base/element/string.json**:
```json
{
  "string": [
    { "name": "app_name", "value": "我的应用" },
    { "name": "welcome_message", "value": "欢迎回来" },
    { "name": "login", "value": "登录" },
    { "name": "register", "value": "注册" },
    { "name": "confirm", "value": "确认" },
    { "name": "cancel", "value": "取消" },
    { "name": "save", "value": "保存" },
    { "name": "delete", "value": "删除" },
    { "name": "edit", "value": "编辑" },
    { "name": "search", "value": "搜索" },
    { "name": "loading", "value": "加载中..." },
    { "name": "no_data", "value": "暂无数据" },
    { "name": "network_error", "value": "网络错误，请重试" },
    { "name": "input_username", "value": "请输入用户名" },
    { "name": "input_password", "value": "请输入密码" }
  ]
}
```

**resources/base/element/float.json**:
```json
{
  "float": [
    { "name": "font_size_xs", "value": "10fp" },
    { "name": "font_size_sm", "value": "12fp" },
    { "name": "font_size_md", "value": "14fp" },
    { "name": "font_size_lg", "value": "16fp" },
    { "name": "font_size_xl", "value": "18fp" },
    { "name": "font_size_xxl", "value": "20fp" },
    { "name": "font_size_display", "value": "32fp" },
    { "name": "spacing_xs", "value": "4vp" },
    { "name": "spacing_sm", "value": "8vp" },
    { "name": "spacing_md", "value": "12vp" },
    { "name": "spacing_lg", "value": "16vp" },
    { "name": "spacing_xl", "value": "24vp" },
    { "name": "spacing_xxl", "value": "32vp" },
    { "name": "radius_sm", "value": "8vp" },
    { "name": "radius_md", "value": "12vp" },
    { "name": "radius_lg", "value": "16vp" },
    { "name": "radius_full", "value": "9999vp" },
    { "name": "button_height_sm", "value": "28vp" },
    { "name": "button_height_md", "value": "36vp" },
    { "name": "button_height_lg", "value": "44vp" },
    { "name": "input_height", "value": "48vp" },
    { "name": "icon_size_sm", "value": "16vp" },
    { "name": "icon_size_md", "value": "24vp" },
    { "name": "icon_size_lg", "value": "32vp" }
  ]
}
```

### Usage Examples

```typescript
// ✅ CORRECT - Using resource references
@Entry
@Component
struct LoginPage {
  @State username: string = ''
  @State password: string = ''

  build() {
    Column({ space: 16 }) {
      // Text with resource reference
      Text($r('app.string.welcome_message'))
        .fontSize($r('app.float.font_size_xxl'))
        .fontColor($r('app.color.text_primary'))
        .fontWeight(FontWeight.Bold)

      // Input with resource reference
      TextInput({ placeholder: $r('app.string.input_username') })
        .height($r('app.float.input_height'))
        .backgroundColor($r('app.color.bg_primary'))
        .borderRadius($r('app.float.radius_sm'))

      TextInput({ placeholder: $r('app.string.input_password') })
        .type(InputType.Password)
        .height($r('app.float.input_height'))
        .backgroundColor($r('app.color.bg_primary'))
        .borderRadius($r('app.float.radius_sm'))

      // Button with resource reference
      Button($r('app.string.login'))
        .width('100%')
        .height($r('app.float.button_height_lg'))
        .backgroundColor($r('app.color.primary'))
        .borderRadius($r('app.float.radius_sm'))
    }
    .width('100%')
    .padding($r('app.float.spacing_xl'))
    .backgroundColor($r('app.color.bg_secondary'))
  }
}

// ❌ WRONG - Hardcoded values (FORBIDDEN!)
@Component
struct WrongExample {
  build() {
    Column() {
      Text('欢迎回来')           // ❌ Hardcoded string
        .fontSize(20)            // ⚠️ Acceptable but prefer $r()
        .fontColor('#182431')    // ❌ Hardcoded color

      Button('登录')             // ❌ Hardcoded string
        .backgroundColor('#0A59F7')  // ❌ Hardcoded color
    }
  }
}
```

---

## ⚠️ Color Format - Alpha Channel (透明度颜色格式)

### HarmonyOS 使用 `#AARRGGBB` 格式！

**这是最常见的错误**：HarmonyOS 的透明度颜色格式与 CSS 完全不同！

| 平台 | 格式 | 60% 透明白色 |
|------|------|--------------|
| **HarmonyOS** | `#AARRGGBB` | `#99FFFFFF` ✅ |
| CSS | `#RRGGBBAA` | `#FFFFFF99` ❌ |
| Tailwind | `bg-white/60` | 需转换为 `#99FFFFFF` |

### 透明度换算

| 透明度 | Alpha Hex | 示例 (白色) |
|--------|-----------|-------------|
| 100% | FF | `#FFFFFFFF` |
| 80% | CC | `#CCFFFFFF` |
| 65% | A6 | `#A6FFFFFF` |
| 60% | 99 | `#99FFFFFF` |
| 50% | 80 | `#80FFFFFF` |
| 40% | 66 | `#66FFFFFF` |
| 25% | 40 | `#40FFFFFF` |
| 15% | 26 | `#26FFFFFF` |
| 10% | 1A | `#1AFFFFFF` |

### 示例

```json
// color.json - 正确格式
{
  "color": [
    { "name": "bg_glass", "value": "#A6FFFFFF" },     // ✅ 65% 透明白色
    { "name": "overlay", "value": "#66000000" },      // ✅ 40% 透明黑色
    { "name": "shadow_aura", "value": "#40E6AC99" }   // ✅ 25% 透明品牌色
  ]
}
```

```typescript
// 代码中的硬编码颜色也必须使用正确格式
.backgroundColor('#66FFFFFF')    // ✅ 40% 透明白色
.shadow({ color: '#26E6AC99' })  // ✅ 15% 透明阴影
.border({ color: '#80FFFFFF' })  // ✅ 50% 透明边框
```

### 详细规范

完整的颜色格式转换指南请参考 `COLOR_FORMAT_GUIDE.md`

---

## Dark Mode Support

### Requirements

- Define dark mode colors in `resources/dark/element/color.json`
- System will automatically switch based on device theme

**resources/dark/element/color.json**:
```json
{
  "color": [
    { "name": "text_primary", "value": "#E5E8EB" },
    { "name": "text_secondary", "value": "#99A4AE" },
    { "name": "bg_primary", "value": "#121212" },
    { "name": "bg_secondary", "value": "#1E1E1E" },
    { "name": "border_light", "value": "#383838" },
    { "name": "divider", "value": "#383838" }
  ]
}
```

---

## Rule 5: No Emoji in Code

### Requirements

- **MUST NOT** use emoji characters in code, comments, or string resources
- **MUST** use text descriptions or icon resources instead
- Emoji can cause encoding issues and are not professional in production code

### Examples

```typescript
// CORRECT - Using icon resources
Image($r('sys.symbol.heart'))
  .width(24)
  .height(24)

Text($r('app.string.feeding_label'))  // "喂养" in string.json

// CORRECT - Using descriptive comments
// Feeding module - handles breast milk and bottle feeding

// WRONG - Using emoji in code (FORBIDDEN!)
Text('🍼 喂养')           // Emoji in string
// 🍼 喂养模块            // Emoji in comment

// WRONG - Emoji in variable names or identifiers
let feeding🍼Count = 0    // FORBIDDEN
```

---

## Rule 6: Icon Usage - Check Before Use ⚠️ 强制规则

### Requirements

使用图标时必须遵循以下流程：

1. **先检查原生图标是否存在** (查询 `knowledge_base/harmony_symbols.csv`)
2. **存在则使用原生图标** (`sys.symbol.xxx`)
3. **不存在则必须从 allsvgicons.com 下载 SVG 并保存到本地**

### ⛔ 禁止行为（严格执行）

```
❌ 严禁使用"相似图标"替代缺失图标
❌ 严禁使用不存在的图标名称（如 sys.symbol.waterbottle）
❌ 严禁猜测图标名称
❌ 严禁使用 emoji 作为图标替代
```

### ✅ 正确行为

```
✅ 查询 harmony_symbols.csv 确认图标是否存在
✅ 不存在时，使用浏览器工具访问 allsvgicons.com 搜索
✅ 下载 SVG 文件保存到 resources/base/media/
✅ 使用 Image($r('app.media.ic_xxx')) 引用本地 SVG
```

### 违规示例

```typescript
// ❌ 错误：使用不存在的图标名称
SymbolGlyph($r('sys.symbol.waterbottle'))  // 该图标不存在！
SymbolGlyph($r('sys.symbol.diaper'))       // 该图标不存在！
SymbolGlyph($r('sys.symbol.ruler'))        // 该图标不存在！

// ❌ 错误：使用"相似"图标替代
// 需要奶瓶图标，但用了水杯图标
SymbolGlyph($r('sys.symbol.cup'))          // 禁止替代！

// ✅ 正确：从 allsvgicons.com 下载 SVG
Image($r('app.media.ic_baby_bottle'))      // 已下载到本地
Image($r('app.media.ic_diaper'))           // 已下载到本地
Image($r('app.media.ic_ruler'))            // 已下载到本地
```

### Step 1: 检查原生图标是否存在

**方法一：查询官方文档**
- 访问 [HarmonyOS Symbol 图标文档](https://developer.huawei.com/consumer/cn/doc/harmonyos-references-V5/ts-components-general-symbol-glyph-V5)
- 搜索需要的图标名称

**方法二：使用 DevEco Studio**
- 在代码中输入 `$r('sys.symbol.` 
- IDE 会自动提示可用的图标列表
- 如果没有提示或编译报错，说明图标不存在

**方法三：查询知识库**
- 参考 `knowledge_base/harmony_symbols.csv` 中的完整官方图标列表 (404个唯一图标)
- 官方页面显示433个图标符号，包含重复条目（同一图标可能属于多个类别）
- 包含 15 个分类: 系统UI/时间/箭头/相机与照片/办公文件/键盘/媒体/通信/连接/符号标识/编辑/隐私安全/人物/形状/交通出行

### Step 2: 使用原生图标（如果存在）

```typescript
// 方式一：使用 Image 组件
Image($r('sys.symbol.heart'))
  .width(24)
  .height(24)
  .fontColor($r('app.color.icon_primary'))

// 方式二：使用 SymbolGlyph 组件（支持动画）
SymbolGlyph($r('sys.symbol.heart'))
  .fontSize(24)
  .fontColor([$r('app.color.primary')])
```

### Step 3: 下载 SVG 图标（如果原生不存在）⚠️ 强制执行

**⛔ 禁止行为：**
- 不能使用"相似"的系统图标替代（如用 cup 替代 bottle）
- 不能猜测图标名称
- 不能跳过此步骤直接使用不存在的图标

**✅ 必须从 allsvgicons.com 获取：**

1. 使用浏览器工具访问 https://allsvgicons.com/search/?q=关键词
2. 搜索需要的图标（如 "baby bottle", "diaper", "ruler"）
3. 推荐图标库（风格统一、质量高）：
   - **Material Design Icons** (7447 icons) - Google 风格，mdi:xxx
   - **Material Symbols** (15009 icons) - Google 风格
   - **Phosphor** (9072 icons) - 简洁现代
   - **Tabler Icons** (5963 icons) - 线条风格
   - **Lucide** (1641 icons) - Feather 改进版
   - **HeroIcons** (1288 icons) - Tailwind 风格
4. 点击图标，在弹窗中复制 SVG 代码
5. 保存到项目 `resources/base/media/ic_xxx.svg`

### Step 4: 保存 SVG 到项目

**文件位置：** `entry/src/main/resources/base/media/`

**命名规范：** `ic_功能名.svg`

```
resources/base/media/
├── ic_cart.svg          # 购物车
├── ic_wallet.svg        # 钱包
├── ic_coupon.svg        # 优惠券
├── ic_customer_service.svg  # 客服
└── ic_points.svg        # 积分
```

### Step 5: 在代码中使用自定义图标

```typescript
// 使用本地 SVG 图标
Image($r('app.media.ic_cart'))
  .width(24)
  .height(24)
  .fillColor($r('app.color.icon_primary'))  // 支持动态染色

// 封装为可复用组件
@Component
struct AppIcon {
  @Prop name: string = ''
  @Prop size: number = 24
  @Prop color: ResourceColor = $r('app.color.icon_primary')

  build() {
    Image($r(`app.media.${this.name}`))
      .width(this.size)
      .height(this.size)
      .fillColor(this.color)
  }
}

// 使用
AppIcon({ name: 'ic_cart', size: 24 })
```

### 常用原生图标速查

| 功能 | 图标名称 | 用法 |
|------|----------|------|
| 首页 | `sys.symbol.house` | 底部导航 |
| 返回 | `sys.symbol.chevron_left` | 导航栏 |
| 搜索 | `sys.symbol.magnifyingglass` | 搜索框 |
| 设置 | `sys.symbol.gearshape` | 设置入口 |
| 用户 | `sys.symbol.person` | 个人中心 |
| 添加 | `sys.symbol.plus` | 新建/添加 |
| 删除 | `sys.symbol.trash` | 删除操作 |
| 编辑 | `sys.symbol.pencil` | 编辑操作 |
| 分享 | `sys.symbol.square_and_arrow_up` | 分享功能 |
| 收藏 | `sys.symbol.heart` | 收藏/喜欢 |
| 通知 | `sys.symbol.bell` | 消息通知 |
| 更多 | `sys.symbol.ellipsis` | 更多菜单 |
| 关闭 | `sys.symbol.xmark` | 关闭按钮 |
| 确认 | `sys.symbol.checkmark` | 确认/完成 |
| 刷新 | `sys.symbol.arrow_clockwise` | 刷新操作 |

### 需要自定义的常见图标

以下图标原生不存在，需要从 allsvgicons.com 获取：

| 功能 | 推荐搜索词 | 推荐图标库 |
|------|-----------|-----------|
| 购物车 | cart, shopping-cart | Material Symbols |
| 钱包 | wallet | Phosphor |
| 优惠券 | coupon, ticket | Tabler Icons |
| 客服 | headset, support | Lucide |
| 积分 | coin, points | Material Symbols |
| 会员 | crown, vip | Phosphor |
| 签到 | calendar-check | Tabler Icons |
| 物流 | truck, delivery | HeroIcons |
| 评价 | star-half, rating | Material Symbols |
| 订单 | receipt, order | Lucide |

---

## Rule 7: Design Principles - UI/UX Standards

### 7.1 一多架构 (Multi-device Responsive)

**默认必须考虑响应式设计**，适配手机、折叠屏、平板等多种设备。

**必须使用的布局方案：**

```typescript
// ✅ 方案一：GridRow/GridCol 栅格布局（推荐）
GridRow({ columns: 12 }) {
  GridCol({ span: { xs: 12, sm: 6, md: 4, lg: 3 } }) {
    // 卡片内容 - 自适应列数
  }
}

// ✅ 方案二：breakpoints 断点适配
@State currentBreakpoint: string = 'sm'

build() {
  GridRow({
    breakpoints: {
      value: ['320vp', '520vp', '840vp'],  // sm, md, lg
      reference: BreakpointsReference.WindowSize
    }
  }) {
    // 根据 currentBreakpoint 调整布局
  }
  .onBreakpointChange((breakpoint: string) => {
    this.currentBreakpoint = breakpoint
  })
}

// ✅ 方案三：layoutWeight 弹性布局
Row() {
  Column() { /* 固定宽度侧边栏 */ }
    .width(200)
  
  Column() { /* 自适应内容区 */ }
    .layoutWeight(1)  // 占据剩余空间
}

// ✅ 方案四：百分比 + 最大宽度
Column() {
  // 内容
}
.width('100%')
.constraintSize({ maxWidth: 600 })  // 大屏居中限宽
```

### 7.2 视觉风格 (Visual Design)

遵循 **"高端、简约、富有生命力"** 的设计理念。

**分层设计（层级感）：**
```typescript
// 背景层 → 内容层 → 浮层
Stack() {
  // Layer 1: 背景
  Column()
    .backgroundColor($r('app.color.bg_secondary'))
  
  // Layer 2: 卡片内容
  Column()
    .backgroundColor($r('app.color.bg_primary'))
    .shadow({
      radius: 16,
      color: 'rgba(0, 0, 0, 0.08)',
      offsetY: 4
    })
  
  // Layer 3: 悬浮按钮
  Button()
    .shadow({
      radius: 24,
      color: 'rgba(10, 89, 247, 0.3)',
      offsetY: 8
    })
}
```

**圆角规范：**
```typescript
// 标准圆角值
.borderRadius(8)   // 小组件：按钮、输入框、小卡片
.borderRadius(12)  // 中等组件：列表项、普通卡片
.borderRadius(16)  // 大组件：弹窗、大卡片
.borderRadius(24)  // 特大组件：底部弹出层、全屏卡片

// 使用资源引用（推荐）
.borderRadius($r('app.float.radius_xs'))  // 4vp
.borderRadius($r('app.float.radius_sm'))  // 8vp
.borderRadius($r('app.float.radius_md'))  // 12vp
.borderRadius($r('app.float.radius_lg'))  // 16vp
.borderRadius($r('app.float.radius_xl'))  // 24vp
```

**留白规范：**
```typescript
// 适当的间距让界面呼吸
.padding({
  top: 16,
  right: 16,
  bottom: 16,
  left: 16
})

// 组件间距
Column({ space: 12 }) { }  // 紧凑
Column({ space: 16 }) { }  // 标准
Column({ space: 24 }) { }  // 宽松
```

### 7.3 交互逻辑 (Motion Design)

**动效必须自然流畅**，使用系统推荐的动画曲线。

⚠️ **重要：API 12+ 必须使用 `this.getUIContext().animateTo()` 替代废弃的全局 `animateTo()`**

```typescript
// ✅ 推荐动画方式一：getUIContext().animateTo（状态驱动，API 12+）
@State isExpanded: boolean = false

build() {
  Column()
    .height(this.isExpanded ? 200 : 80)
    .onClick(() => {
      this.getUIContext().animateTo({
        duration: 300,
        curve: Curve.Friction,  // 摩擦曲线 - 自然减速
        onFinish: () => { }
      }, () => {
        this.isExpanded = !this.isExpanded
      })
    })
}

// ✅ 推荐动画方式二：animation 属性动画
Column()
  .scale({ x: this.isPressed ? 0.95 : 1.0, y: this.isPressed ? 0.95 : 1.0 })
  .animation({
    duration: 150,
    curve: Curve.Sharp  // 锐利曲线 - 快速响应
  })

// ✅ 推荐动画方式三：transition 转场动画
if (this.showPanel) {
  Column()
    .transition(TransitionEffect.OPACITY
      .combine(TransitionEffect.translate({ y: 100 }))
      .animation({ duration: 300, curve: Curve.Friction }))
}

// ✅ SharedTransition 共享元素动画
Image($r('app.media.cover'))
  .sharedTransition('cover_' + this.id, {
    duration: 300,
    curve: Curve.Friction,
    type: SharedTransitionEffectType.Exchange
  })
```

**推荐动画曲线：**
| 曲线 | 用途 | 特点 |
|------|------|------|
| `Curve.Friction` | 页面转场、展开收起 | 自然减速，物理感强 |
| `Curve.Sharp` | 按钮反馈、快速交互 | 快速响应，干脆利落 |
| `Curve.Smooth` | 滚动惯性、平滑过渡 | 平滑连续 |
| `Curve.EaseOut` | 进入动画 | 快进慢出 |
| `Curve.EaseIn` | 退出动画 | 慢进快出 |

---

## Rule 8: Code Best Practices - Anti-Patterns

### 8.1 禁止使用 px 单位

**必须使用 vp（视觉像素）或 fp（字体像素）**

```typescript
// ✅ CORRECT - 使用 vp/fp
Text('标题')
  .fontSize(18)      // 默认单位是 fp
  .width(100)        // 默认单位是 vp
  .height('100%')    // 百分比

Column()
  .padding(16)       // 16vp
  .margin({ top: 8 }) // 8vp

// ❌ WRONG - 使用 px（禁止！）
Text('标题')
  .fontSize('18px')  // 禁止
  .width('100px')    // 禁止
```

### 8.2 禁止在 build() 中进行复杂逻辑

**build() 方法应保持纯净，只负责 UI 声明**

```typescript
// ❌ WRONG - build() 中做复杂运算
build() {
  Column() {
    // 禁止：在 build 中进行数据处理
    let filteredItems = this.items.filter(item => item.price > 100)
    let sortedItems = filteredItems.sort((a, b) => b.price - a.price)
    
    ForEach(sortedItems, (item: Item) => { })
  }
}

// ✅ CORRECT - 使用计算属性或提前处理
@State items: Array<Item> = []

// 方式一：使用 getter 计算属性
get filteredItems(): Array<Item> {
  return this.items
    .filter(item => item.price > 100)
    .sort((a, b) => b.price - a.price)
}

build() {
  Column() {
    ForEach(this.filteredItems, (item: Item) => { })
  }
}

// 方式二：在数据更新时处理
updateItems(newItems: Array<Item>) {
  this.items = newItems
    .filter(item => item.price > 100)
    .sort((a, b) => b.price - a.price)
}
```

### 8.3 推荐使用 AttributeModifier 抽离样式

**提高样式复用性和可维护性**

```typescript
// 定义样式修改器
class PrimaryButtonModifier implements AttributeModifier<ButtonAttribute> {
  applyNormalAttribute(instance: ButtonAttribute): void {
    instance
      .backgroundColor($r('app.color.primary'))
      .fontColor($r('app.color.text_inverse'))
      .fontSize(16)
      .height(44)
      .borderRadius(8)
  }
}

class SecondaryButtonModifier implements AttributeModifier<ButtonAttribute> {
  applyNormalAttribute(instance: ButtonAttribute): void {
    instance
      .backgroundColor($r('app.color.bg_secondary'))
      .fontColor($r('app.color.text_primary'))
      .fontSize(16)
      .height(44)
      .borderRadius(8)
      .border({ width: 1, color: $r('app.color.border_light') })
  }
}

// 使用
@Entry
@Component
struct ButtonDemo {
  primaryStyle: PrimaryButtonModifier = new PrimaryButtonModifier()
  secondaryStyle: SecondaryButtonModifier = new SecondaryButtonModifier()

  build() {
    Column({ space: 16 }) {
      Button('主要按钮')
        .attributeModifier(this.primaryStyle)
      
      Button('次要按钮')
        .attributeModifier(this.secondaryStyle)
    }
  }
}
```

### 8.4 强制使用 Navigation 组件 ⚠️

**必须使用 Navigation 架构，严禁使用 router.pushUrl**

> 📚 详细规范请参考 `NAVIGATION_ARCHITECTURE_GUIDE.md`

#### 核心要求

1. **主页必须 `@Provide('pageStack')`** - 初始化并提供路由栈
2. **子组件/子页面必须 `@Consume('pageStack')`** - Key 必须完全一致
3. **目标页面必须用 `NavDestination` 包裹**
4. **严禁混用 `router.pushUrl`**

```typescript
// ✅ CORRECT - Navigation 架构
@Entry
@Component
struct Index {
  // 1. 主页提供路由栈
  @Provide('pageStack') pageStack: NavPathStack = new NavPathStack()

  build() {
    // 2. 绑定路由栈
    Navigation(this.pageStack) {
      HomePage()
    }
    .navDestination(this.PageMap)
    .mode(NavigationMode.Stack)
    .hideTitleBar(true)
  }

  // 3. 路由映射表
  @Builder
  PageMap(name: string) {
    if (name === 'DetailPage') {
      DetailPage()
    }
  }
}

// 子组件中跳转
@Component
struct HomePage {
  // 4. 使用 @Consume 获取路由栈 (key 必须一致!)
  @Consume('pageStack') pageStack: NavPathStack

  build() {
    Column() {
      Button('查看详情')
        .onClick(() => {
          // 5. 使用 pushPath 跳转
          this.pageStack.pushPath({ name: 'DetailPage', param: { id: 123 } })
        })
    }
  }
}

// 目标页面
@Component
struct DetailPage {
  @Consume('pageStack') pageStack: NavPathStack

  build() {
    // 6. 必须使用 NavDestination 包裹
    NavDestination() {
      Column() {
        Text('详情页')
        Button('返回')
          .onClick(() => this.pageStack.pop())
      }
    }
    .title('详情')
    .onBackPressed(() => {
      this.pageStack.pop()
      return true
    })
  }
}

// ❌ FORBIDDEN - 旧版 Router API
import router from '@ohos.router'
router.pushUrl({ url: 'pages/Detail' })  // 严禁使用！
```

#### 常见错误排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 子页面空白 | @Consume key 不匹配 | 确保使用相同的 key (如 'pageStack') |
| 跳转无反应 | 未绑定路由栈 | 检查 Navigation(this.pageStack) |
| 无法返回 | 未处理 onBackPressed | 添加 .onBackPressed() 回调 |

---

## Rule 9: Development Workflow

### 开发功能时的思考路径

当收到功能开发需求时，按以下步骤执行：

### Step 1: 分析场景 - 多设备适配

```
思考问题：
├── 手机端如何显示？（竖屏为主）
├── 折叠屏如何显示？（展开/折叠两种状态）
├── 平板端如何显示？（横屏/多列布局）
└── 是否需要响应式断点？
```

```typescript
// 示例：商品列表适配
GridRow({ columns: 12 }) {
  ForEach(this.products, (product: Product) => {
    GridCol({
      span: {
        xs: 6,   // 手机：2列
        sm: 4,   // 折叠屏：3列
        md: 3,   // 平板：4列
        lg: 2    // 大屏：6列
      }
    }) {
      ProductCard({ product: product })
    }
  })
}
```

### Step 2: 定义数据 - Model 层优先

```typescript
// 先定义数据模型
interface Product {
  id: string
  name: string
  price: number
  imageUrl: string
  stock: number
}

// 定义页面状态
@Entry
@Component
struct ProductListPage {
  @State products: Array<Product> = []
  @State isLoading: boolean = true
  @State currentPage: number = 1
  @State hasMore: boolean = true
  
  // 业务逻辑
  async loadProducts() {
    this.isLoading = true
    const result = await ProductService.getList(this.currentPage)
    this.products = result.data
    this.hasMore = result.hasMore
    this.isLoading = false
  }
}
```

### Step 3: 构建 UI - 组件化设计

```typescript
build() {
  Column() {
    // 1. 顶部搜索栏
    SearchBar({ onSearch: this.handleSearch })
    
    // 2. 内容区域
    if (this.isLoading) {
      LoadingView()
    } else if (this.products.length === 0) {
      EmptyView({ message: $r('app.string.no_products') })
    } else {
      // 商品列表
      List() {
        ForEach(this.products, (product: Product) => {
          ListItem() {
            ProductCard({ product: product })
          }
        })
      }
      .onReachEnd(() => this.loadMore())
    }
  }
}
```

### Step 4: 注入动效 - 提升体验

```typescript
// 页面进入动画
pageTransition() {
  PageTransitionEnter({ duration: 300, curve: Curve.Friction })
    .opacity(0)
    .translate({ y: 50 })
  PageTransitionExit({ duration: 200, curve: Curve.Sharp })
    .opacity(0)
}

// 列表项动画
@Component
struct ProductCard {
  @State isPressed: boolean = false
  @Prop product: Product
  
  build() {
    Column() {
      // 卡片内容
    }
    .scale({ x: this.isPressed ? 0.98 : 1.0, y: this.isPressed ? 0.98 : 1.0 })
    .animation({ duration: 100, curve: Curve.Sharp })
    .onTouch((event: TouchEvent) => {
      if (event.type === TouchType.Down) {
        this.isPressed = true
      } else if (event.type === TouchType.Up || event.type === TouchType.Cancel) {
        this.isPressed = false
      }
    })
  }
}

// SharedTransition 详情页
Image($r('app.media.product_image'))
  .sharedTransition('product_' + this.product.id, {
    duration: 300,
    curve: Curve.Friction
  })
```

---

## Rule 10: Project Creation - 项目创建规则

### 触发条件

当用户请求创建新项目时，必须使用初始化脚本：

**触发关键词:**
- "创建xxx项目"、"新建xxx项目"、"初始化xxx项目"
- "Create xxx project"、"Initialize xxx project"

### 执行流程

```
步骤1: 询问 SDK 版本 (如果用户未提供)
       提示: "请提供 SDK 版本，格式如 6.0.2(22)"
       
步骤2: 确认项目信息
       - 项目名称 (从用户请求提取)
       - SDK 版本 (用户提供)
       - 目标路径 (默认当前目录)
       
步骤3: 执行初始化脚本
       python scripts/init_harmony_project.py <项目名> --sdk "<版本>"
       
步骤4: 验证编译
       cd <项目路径>
       hvigorw assembleHap --no-daemon
       
步骤5: 报告结果
       - 成功: 告知用户项目已创建
       - 失败: 分析错误并修复
```

### 脚本命令

```bash
# 基础用法 (SDK 版本必填)
python scripts/init_harmony_project.py MyApp --sdk "6.0.2(22)"

# 指定目标目录
python scripts/init_harmony_project.py MyApp --sdk "6.0.2(22)" --path E:/projects

# 自定义包名前缀
python scripts/init_harmony_project.py MyApp --sdk "6.0.2(22)" --bundle com.mycompany
```

### SDK 版本格式

- 格式: `主版本.次版本.修订版(API版本)`
- 示例: `6.0.2(22)`, `5.0.0(12)`
- 查看方式: DevEco Studio 项目的 `build-profile.json5` 中的 `compatibleSdkVersion`

### 脚本生成内容

| 类别 | 文件 |
|------|------|
| **配置文件** | oh-package.json5, build-profile.json5, hvigorfile.ts |
| **模块配置** | entry/module.json5, entry/build-profile.json5 |
| **资源文件** | color.json, string.json, float.json (含深色模式) |
| **媒体资源** | layered_image.json, foreground.png, background.png, startIcon.png |
| **示例代码** | EntryAbility.ets, Index.ets, HomePage.ets, ProfilePage.ets |

### 示例对话

```
用户: 创建一个母婴健康管理项目

AI: 好的，我来创建母婴健康管理项目。请问您的 SDK 版本是多少？
    格式如 "6.0.2(22)"，可在 DevEco Studio 的 build-profile.json5 中查看。

用户: 6.0.2(22)

AI: 收到，正在创建项目...
    python scripts/init_harmony_project.py BabyHealth --sdk "6.0.2(22)"
    
    项目创建成功！正在验证编译...
    hvigorw assembleHap --no-daemon
    
    ✓ ArkTS 编译通过
    项目已创建: ./BabyHealth
```

---

## Rule 11: Resource Integrity - 资源完整性要求

### 核心原则

**当生成使用 `$r()` 的代码时，必须同时输出对应的资源文件定义。**

### 同步输出要求

```
生成 UI 代码时，必须同时提供:
1. string.json 片段 - 所有 $r('app.string.xxx') 引用的字符串
2. color.json 片段 - 所有 $r('app.color.xxx') 引用的颜色
3. float.json 片段 - 所有 $r('app.float.xxx') 引用的尺寸（如果有新增）
```

### 资源命名规范

资源 Key 必须遵循 **模块名_功能名_属性名** 格式：

```
模块名_功能名_属性名

示例:
- login_button_text          → "登录"
- login_button_bg_color      → "#0A59F7"
- login_input_placeholder    → "请输入用户名"
- cart_badge_count           → 购物车数量
- profile_avatar_size        → 头像尺寸
```

### 输出格式示例

当生成登录页面代码时，必须同时输出：

**代码文件 (Login.ets):**
```typescript
@Entry
@Component
struct LoginPage {
  build() {
    Column() {
      Text($r('app.string.login_title'))
        .fontColor($r('app.color.login_title_color'))
      
      Button($r('app.string.login_button_text'))
        .backgroundColor($r('app.color.login_button_bg'))
    }
  }
}
```

**资源文件片段 (string.json):**
```json
{
  "string": [
    { "name": "login_title", "value": "欢迎登录" },
    { "name": "login_button_text", "value": "登录" }
  ]
}
```

**资源文件片段 (color.json):**
```json
{
  "color": [
    { "name": "login_title_color", "value": "#182431" },
    { "name": "login_button_bg", "value": "#0A59F7" }
  ]
}
```

---

## Rule 12: Layout Strategy Selector - 布局策略选择器

### 决策表

根据 UI 类型和屏幕宽度选择合适的布局策略：

| 场景 | 策略 | 实现方式 | 触发条件 |
|------|------|----------|----------|
| **基础组件** | 自适应伸缩 | `layoutWeight(1)` 或百分比 | 所有屏幕 |
| **列表/宫格** | 延伸布局 | `Grid` + `breakpoints` | 列数随宽度增加 |
| **侧边导航** | 分栏布局 | `SideBarContainer` / `Navigation` | `windowWidth > 600vp` |
| **详情页** | 主次分栏 | 左侧列表 + 右侧详情 | `windowWidth > 840vp` |

### 策略一：自适应伸缩

适用于：按钮组、输入框、卡片内元素

```typescript
Row() {
  Button($r('app.string.cancel'))
    .layoutWeight(1)
  
  Button($r('app.string.confirm'))
    .layoutWeight(1)
}
.width('100%')
```

### 策略二：延伸布局 (Grid + Breakpoints)

适用于：商品列表、图片宫格、功能入口

```typescript
GridRow({
  columns: 12,
  breakpoints: {
    value: ['320vp', '520vp', '840vp'],
    reference: BreakpointsReference.WindowSize
  }
}) {
  ForEach(this.items, (item: ItemData) => {
    GridCol({
      span: { xs: 6, sm: 4, md: 3, lg: 2 }  // 2/3/4/6 列
    }) {
      ItemCard({ item: item })
    }
  })
}
```

### 策略三：分栏布局

适用于：设置页、邮件应用、文件管理

```typescript
// 当 windowWidth > 600vp 时启用分栏
@State isWideScreen: boolean = false

build() {
  if (this.isWideScreen) {
    SideBarContainer(SideBarContainerType.Embed) {
      // 侧边栏
      MenuList()
      // 内容区
      ContentArea()
    }
    .sideBarWidth(200)
  } else {
    Navigation(this.navStack) {
      MenuList()
    }
  }
}

aboutToAppear() {
  // 监听窗口变化
  window.getLastWindow(getContext(this)).then((win) => {
    const windowWidth = win.getWindowProperties().windowRect.width
    this.isWideScreen = px2vp(windowWidth) > 600
  })
}
```

### 策略四：主次分栏 (Master-Detail)

适用于：平板端邮件、笔记应用

```typescript
Navigation(this.navStack) {
  // 列表区域
  List() {
    ForEach(this.dataList, (item: DataItem) => {
      ListItem() {
        ItemRow({ item: item })
      }
      .onClick(() => this.selectItem(item))
    })
  }
}
.mode(NavigationMode.Split)  // 分栏模式
.navBarWidth('40%')          // 导航栏宽度
.minContentWidth(360)        // 内容区最小宽度
```

---

## Rule 13: Performance Constraints - 性能准则

### 13.1 减少嵌套层级

**优先使用 `RelativeContainer` 替代多层嵌套的 Column/Row**

```typescript
// ❌ 错误：过度嵌套
Column() {
  Row() {
    Column() {
      Row() {
        Text('内容')
      }
    }
  }
}

// ✅ 正确：使用 RelativeContainer 扁平化
RelativeContainer() {
  Text('标题')
    .id('title')
    .alignRules({
      top: { anchor: '__container__', align: VerticalAlign.Top },
      left: { anchor: '__container__', align: HorizontalAlign.Start }
    })
  
  Text('内容')
    .id('content')
    .alignRules({
      top: { anchor: 'title', align: VerticalAlign.Bottom },
      left: { anchor: '__container__', align: HorizontalAlign.Start }
    })
}
```

### 13.2 长列表优化

**数据量 > 50 时必须使用 LazyForEach + keyGenerator**

```typescript
// ❌ 错误：大数据量使用 ForEach
List() {
  ForEach(this.bigDataList, (item: DataItem) => {  // 危险！
    ListItem() { ... }
  })
}

// ✅ 正确：使用 LazyForEach + IDataSource
class MyDataSource implements IDataSource {
  private dataArray: DataItem[] = []
  
  totalCount(): number {
    return this.dataArray.length
  }
  
  getData(index: number): DataItem {
    return this.dataArray[index]
  }
  
  // ... 其他必需方法
}

@State dataSource: MyDataSource = new MyDataSource()

List() {
  LazyForEach(this.dataSource, (item: DataItem, index: number) => {
    ListItem() {
      ItemComponent({ item: item })
    }
  }, (item: DataItem) => item.id.toString())  // keyGenerator 必填
}
```

### 13.3 状态隔离

**频繁变动的状态必须拆分为子组件，避免整个父组件重渲染**

```typescript
// ❌ 错误：计时器状态导致整个页面刷新
@Entry
@Component
struct BadPage {
  @State seconds: number = 0  // 每秒更新，整个页面刷新
  
  build() {
    Column() {
      Header()           // 被迫刷新
      Text(`${this.seconds}s`)
      HeavyContent()     // 被迫刷新
      Footer()           // 被迫刷新
    }
  }
}

// ✅ 正确：将计时器拆分为独立子组件
@Component
struct TimerDisplay {
  @State seconds: number = 0  // 只影响此组件
  
  build() {
    Text(`${this.seconds}s`)
  }
}

@Entry
@Component
struct GoodPage {
  build() {
    Column() {
      Header()           // 不受影响
      TimerDisplay()     // 独立更新
      HeavyContent()     // 不受影响
      Footer()           // 不受影响
    }
  }
}
```

### 13.4 避免 build() 中的计算

```typescript
// ❌ 错误：build() 中计算
build() {
  Column() {
    ForEach(this.items.filter(i => i.active).sort((a, b) => a.order - b.order), ...)
  }
}

// ✅ 正确：使用 getter 或提前计算
get filteredItems(): ItemData[] {
  return this.items.filter(i => i.active).sort((a, b) => a.order - b.order)
}

build() {
  Column() {
    ForEach(this.filteredItems, ...)
  }
}
```

---

## Rule 14: Auto Fix Flow - 自动化修复流程

### 编译错误处理

当 `hvigorw assembleHap` 报错时，必须执行以下修复流程：

```
步骤1: 读取错误日志
       - 查看终端输出的错误信息
       - 读取 .hvigor/outputs/build-logs/build.log

步骤2: 分析错误类型
       - SDK 版本不匹配 → 修改 build-profile.json5
       - 依赖冲突 → 修改 oh-package.json5
       - ArkTS 语法错误 → 修复代码
       - 资源缺失 → 补充资源文件

步骤3: 自动修复
       根据错误类型执行对应修复

步骤4: 重新编译验证
       hvigorw assembleHap --no-daemon
```

### 常见错误修复

| 错误类型 | 错误特征 | 修复方案 |
|---------|---------|---------|
| **SDK 版本** | `Configuration Error`, `modelVersionCheck` | 更新 `hvigor-config.json5` 和 `build-profile.json5` 的版本号 |
| **依赖冲突** | `dependency conflict`, `version mismatch` | 更新 `oh-package.json5` 中的依赖版本 |
| **资源缺失** | `Cannot find resource` | 补充 string.json/color.json 中缺失的资源定义 |
| **类型错误** | `Type 'xxx' is not assignable` | 修复 ArkTS 代码类型定义 |
| **导入错误** | `Cannot find module` | 检查 import 路径和模块是否存在 |
| **Java 缺失** | `spawn java ENOENT` | 提示用户配置 Java 环境 (系统问题，非代码问题) |

### 修复示例

```
错误: modelVersionCheck failed

修复:
1. 读取 hvigor/hvigor-config.json5 获取当前 modelVersion
2. 读取用户其他项目的配置确认正确版本
3. 更新 modelVersion 为正确值
4. 重新编译
```

---

## Rule 15: NEXT Features - HarmonyOS NEXT 特色增强

### 主动推荐策略

在以下场景中，**主动询问用户是否需要使用 NEXT 特色功能**：

### 15.1 元服务适配 (Atomic Service)

**触发场景**: 创建新项目、设计首页

```
询问: "是否需要适配元服务（Atomic Service）卡片？
      元服务支持免安装直达，可在负一屏、搜索结果中展示。"

如果需要:
- 生成 FormAbility 配置
- 提供 2x2、2x4、4x4 三种卡片尺寸模板
- 配置 form_config.json
```

### 15.2 实况窗 (Live View)

**触发场景**: 涉及流程进度的功能（外卖、打车、快递、运动）

```
询问: "此功能涉及实时进度展示，是否使用实况窗（Live View）？
      实况窗可在锁屏、灵动岛位置持续显示进度。"

如果需要:
- 引入 @kit.LiveViewKit
- 提供 LiveViewManager 使用示例
- 配置后台保活权限
```

```typescript
// 实况窗示例代码
import { liveViewManager } from '@kit.LiveViewKit'

// 创建实况窗
const liveView = await liveViewManager.createLiveView({
  title: '外卖配送中',
  content: '骑手距您约 2.3km',
  icon: $r('app.media.ic_delivery'),
  // ...
})
```

### 15.3 统一扫码 (Scan Kit)

**触发场景**: 涉及扫码输入（登录、支付、添加好友）

```
询问: "是否使用系统统一扫码（Scan Kit）？
      系统扫码更快速准确，支持多种码制。"

如果需要:
- 引入 @kit.ScanKit
- 提供 scanBarcode API 示例
- 处理扫码结果回调
```

```typescript
import { scanBarcode, scanCore } from '@kit.ScanKit'

// 调用系统扫码
scanBarcode.startScanForResult(getContext(this), {
  scanTypes: [scanCore.ScanType.ALL],
  enableMultiMode: false,
  enableAlbum: true
}).then((result) => {
  console.info(`扫码结果: ${result.originalValue}`)
})
```

### 15.4 原生分享 (Share Kit)

**触发场景**: 涉及内容分享（图片、链接、文件）

```
询问: "是否使用系统原生分享（Share Kit）？
      原生分享支持直接分享到系统应用和第三方应用。"

如果需要:
- 引入 @kit.ShareKit  
- 提供 systemShare API 示例
```

```typescript
import { systemShare } from '@kit.ShareKit'

// 分享文本
const shareData = new systemShare.SharedData()
shareData.addContent({ text: '分享内容' })

const controller = new systemShare.ShareController(shareData)
controller.show(getContext(this))
```

### 15.5 功能推荐触发表

| 用户需求关键词 | 推荐功能 | Kit |
|---------------|---------|-----|
| 扫码、扫一扫、二维码 | 统一扫码 | @kit.ScanKit |
| 分享、转发、发送给 | 原生分享 | @kit.ShareKit |
| 进度、配送、运动、计时 | 实况窗 | @kit.LiveViewKit |
| 卡片、小组件、负一屏 | 元服务 | FormKit |
| 支付、钱包 | 华为支付 | @kit.PaymentKit |
| 推送、通知、消息 | 推送服务 | @kit.PushKit |
| 登录、账号 | 华为账号 | @kit.AccountKit |
| 地图、定位、导航 | 位置服务 | @kit.LocationKit |
| 语音、语音输入 | 语音服务 | @kit.CoreSpeechKit |
| AI、识别、分析 | AI 能力 | @kit.CoreVisionKit |

---

## Rule 16: Prototype Import - 原型图导入

### 触发条件

当用户提供原型图链接或截图时，自动触发设计 Token 提取流程：

| 触发方式 | 示例 |
|---------|------|
| **Google Stitch** | `https://stitch.withgoogle.com/projects/xxx` |
| **Figma** | `https://www.figma.com/file/xxx` |
| **MasterGo** | `https://mastergo.com/files/xxx` |
| **设计截图** | 用户上传的设计规范图片 |
| **联动创建** | "根据这个原型图创建项目" / "参照设计创建 xxx 项目" |

### 两种模式

**模式一：仅提取 Token (已有项目)**
- 用户已有项目，只需提取设计 Token
- 询问是否写入现有项目

**模式二：联动创建项目 (推荐)**
- 用户提供原型图 + 要求创建项目
- 执行完整流程: 分析原型图 → 提取 Token → 创建项目 → 写入 Token → 验证编译

### 执行流程

```
步骤1: 访问原型图
       使用浏览器工具导航到链接
       等待完全加载 (3秒+)
       
步骤2: 遍历所有 Screen
       识别设计系统页面 (Design System / UI Kit)
       截取关键页面截图
       
步骤3: 提取设计 Token
       - 色彩系统 (Color Palette)
       - 字体规范 (Typography)
       - 间距规范 (Spacing)
       - 圆角规范 (Border Radius)
       - 动效参数 (Motion/Animation)
       - 阴影规范 (Shadows)
       
步骤4: 生成资源文件
       输出 color.json / float.json 片段
       输出 dark/color.json (深色模式)
       可选: 生成 design-system/tokens.ets
       
步骤5: 写入项目
       合并到现有资源文件
       记录设计来源
```

### 输出要求

提取完成后必须输出：

**1. 设计摘要表格**

```markdown
| 类型 | Token 名称 | 值 | 用途 |
|-----|-----------|-----|------|
| 颜色 | brand_primary | #00BFFF | 主品牌色 |
| 圆角 | radius_aura | 24vp | Aura 风格卡片 |
```

**2. 资源文件代码块**

```json
// color.json 片段
{
  "color": [
    { "name": "brand_primary", "value": "#00BFFF" },
    { "name": "brand_accent", "value": "#FF6B6B" }
  ]
}
```

**3. 深色模式资源**

如原型图有深色模式规范，同步提取：

```json
// dark/color.json 片段
{
  "color": [
    { "name": "bg_primary", "value": "#0A0A0A" },
    { "name": "brand_primary", "value": "#00D4FF" }
  ]
}
```

### Token 命名规范

从原型图提取的 Token 遵循以下命名：

| 类型 | 格式 | 示例 |
|-----|------|------|
| 品牌色 | `brand_xxx` | `brand_primary`, `brand_accent` |
| 功能色 | 语义化名称 | `success`, `warning`, `error` |
| 背景色 | `bg_xxx` | `bg_primary`, `bg_card` |
| 文字色 | `text_xxx` | `text_primary`, `text_secondary` |
| 项目专属 | `项目名_xxx` | `babytime_mint_green` |

### 冲突处理

当提取的 Token 与现有项目冲突时：

```
情况1: 新 Token 与现有名称不同
       → 直接添加到资源文件

情况2: 名称冲突但值不同
       → 询问用户是否覆盖

情况3: 完全相同
       → 跳过，无需重复添加
```

### 示例对话 - 模式一 (仅提取)

```
用户: 看一下这个原型图 https://stitch.withgoogle.com/xxx

AI: [访问链接，截图分析]

已从原型图中提取 babyTime 设计 Token：

| 类型 | Token | 值 | 说明 |
|-----|-------|-----|------|
| 品牌色 | brand_primary | #00BFFF | 天蓝色主色 |
| 圆角 | radius_aura | 24vp | Aura 风格 |
| 动效 | motion_spring | spring(1,80,10) | 卡片反馈 |

需要我将这些 Token 写入当前项目吗？
```

### 示例对话 - 模式二 (联动创建)

```
用户: 根据这个原型图创建项目 https://stitch.withgoogle.com/xxx

AI: [分析原型图，提取设计 Token]

我已从原型图提取了 "babyTime" 设计系统：
- 品牌色: #A6E8C7, #F9CEEE, #C7E0F4
- Aura 圆角: 24vp
- 深色模式: #0A0A0A 背景

请确认：
1. 项目名称: BabyTime (从原型图识别)
2. SDK 版本: 请提供 (格式如 6.0.2(22))

用户: 6.0.2(22)

AI: [创建项目]
    python scripts/init_harmony_project.py BabyTime --sdk "6.0.2(22)"
    
    [写入设计 Token]
    color.json ← 品牌色 + 深色模式
    float.json ← Aura 圆角
    
    [验证编译]
    hvigorw assembleHap --no-daemon
    
    ✅ 项目创建成功！
    📁 路径: ./BabyTime
    🎨 设计 Token 已写入
```

### 详细规范

完整的提取规则请参考 `DESIGN_TOKEN_EXTRACTION.md`

---

## Rule 17: Custom Font - 自定义字体注册

### 核心原则

自定义字体必须在 UI 渲染前完成注册，确保**零闪烁 (No FOUT)** 和**全局可用性**。

### 强制规范

```
❌ 禁止：在 Page 级别 (aboutToAppear) 注册全局字体
❌ 禁止：在 build() 方法中注册字体
❌ 禁止：使用硬编码本地绝对路径

✅ 必须：在 EntryAbility.onWindowStageCreate 中注册
✅ 必须：在 loadContent 执行前完成注册
✅ 必须：使用 $r('app.media.xxx') 引用字体资源
✅ 必须：包含 try-catch 异常处理
```

### 标准实现

**1. 创建 FontManager (utils/FontManager.ets)**

```typescript
import { font } from '@kit.ArkUI'

export class FontManager {
  public static registerCustomFonts(): void {
    try {
      font.registerFont({
        familyName: 'BrandFont',
        familySrc: $r('app.media.BrandFont_Regular')
      })
      console.info('FontManager: Custom fonts registered.')
    } catch (error) {
      console.error(`FontManager: Failed. Code: ${error.code}`)
    }
  }
}
```

**2. 集成到 EntryAbility**

```typescript
onWindowStageCreate(windowStage: window.WindowStage): void {
  // ⚠️ 先注册字体
  FontManager.registerCustomFonts()
  
  // 再加载页面
  windowStage.loadContent('pages/Index')
}
```

**3. UI 中使用**

```typescript
Text('品牌文字')
  .fontFamily('BrandFont')  // 与注册时 familyName 一致
  .fontSize(16)
```

### 资源配置

| 项目 | 规范 |
|------|------|
| **文件格式** | `.ttf` 或 `.otf` |
| **存放位置** | `resources/base/media/` |
| **命名规范** | `FontName_Weight.ttf` (如 BrandFont_Bold.ttf) |
| **引用方式** | `$r('app.media.FontName_Weight')` |

### AI 检测清单

当用户请求使用自定义字体时，AI 必须检查：

1. ✅ 是否在 EntryAbility 中注册？
2. ✅ 是否使用 $r() 引用字体？
3. ✅ 是否包含 try-catch？
4. ✅ 字体文件是否存在于 resources/base/media/?

### 详细规范

完整的字体注册指南请参考 `CUSTOM_FONT_GUIDE.md`

---

## Summary Checklist

Before submitting any code, verify:

**语言规范 (Rule 1)**
- [ ] No `any` type used
- [ ] All types are explicitly defined

**UI 框架 (Rule 2)**
- [ ] Using @Component decorator
- [ ] Using @Entry for entry pages

**状态管理 (Rule 3)**
- [ ] Using appropriate state decorators (@State, @Prop, @Link, etc.)

**资源引用 (Rule 4)**
- [ ] No hardcoded color values (use $r('app.color.xxx'))
- [ ] No hardcoded string values (use $r('app.string.xxx'))
- [ ] Resource files are properly defined
- [ ] Dark mode resources are defined if needed

**代码规范 (Rule 5 & 6)**
- [ ] No emoji characters in code or comments
- [ ] Icons checked: native symbols used if available, otherwise SVG from allsvgicons.com

**设计规范 (Rule 7)**
- [ ] 响应式布局已实现（GridCol/breakpoints/layoutWeight）
- [ ] 圆角使用标准值（8/12/16/24vp）
- [ ] 动效使用推荐曲线（Curve.Friction/Sharp）
- [ ] **动画使用 `this.getUIContext().animateTo()` 而非废弃的全局 `animateTo()`**

**代码质量 (Rule 8)**
- [ ] No px unit used (use vp/fp)
- [ ] build() 方法保持纯净，无复杂逻辑
- [ ] 复杂样式使用 AttributeModifier 抽离
- [ ] 导航使用 Navigation 组件

**开发流程 (Rule 9)**
- [ ] 已分析多设备适配方案
- [ ] 数据模型已定义
- [ ] UI 组件化设计
- [ ] 已添加适当的动效

**项目创建 (Rule 10)**
- [ ] 使用初始化脚本创建项目 (python scripts/init_harmony_project.py)
- [ ] 已指定正确的 SDK 版本 (--sdk 参数)
- [ ] 已验证 ArkTS 编译通过 (hvigorw assembleHap)

**资源完整性 (Rule 11)**
- [ ] 代码中的 $r('app.string.xxx') 都有对应的 string.json 定义
- [ ] 代码中的 $r('app.color.xxx') 都有对应的 color.json 定义
- [ ] 资源命名遵循 模块名_功能名_属性名 格式

**布局策略 (Rule 12)**
- [ ] 基础组件使用 layoutWeight 或百分比自适应
- [ ] 列表/宫格使用 Grid + breakpoints 延伸布局
- [ ] 宽屏 (>600vp) 启用分栏布局

**性能优化 (Rule 13)**
- [ ] 优先使用 RelativeContainer 减少嵌套层级
- [ ] 大数据列表 (>50) 使用 LazyForEach + keyGenerator
- [ ] 频繁更新的状态拆分为独立子组件
- [ ] build() 中无复杂计算逻辑

**自动修复 (Rule 14)**
- [ ] 编译错误已分析并修复
- [ ] 修复后已重新验证编译

**NEXT 特色 (Rule 15)**
- [ ] 已询问是否需要元服务卡片适配
- [ ] 进度类功能已考虑实况窗
- [ ] 扫码/分享功能优先使用系统 Kit

**原型图导入 (Rule 16)**
- [ ] 已遍历原型图所有 Screen
- [ ] 已提取色彩/字体/间距/圆角/动效 Token
- [ ] 已生成 color.json / float.json 资源片段
- [ ] 已生成深色模式资源 (如适用)
- [ ] Token 命名遵循规范 (brand_xxx, bg_xxx, text_xxx)

**自定义字体 (Rule 17)**
- [ ] 字体在 EntryAbility.onWindowStageCreate 中注册
- [ ] 使用 $r('app.media.xxx') 引用字体资源
- [ ] 包含 try-catch 异常处理
- [ ] 字体文件存放于 resources/base/media/