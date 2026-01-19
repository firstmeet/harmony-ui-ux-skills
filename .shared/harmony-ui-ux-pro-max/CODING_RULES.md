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

## Summary Checklist

Before submitting any code, verify:

- [ ] No `any` type used
- [ ] All types are explicitly defined
- [ ] Using @Component decorator
- [ ] Using appropriate state decorators
- [ ] No hardcoded color values (use $r('app.color.xxx'))
- [ ] No hardcoded string values (use $r('app.string.xxx'))
- [ ] Resource files are properly defined
- [ ] Dark mode resources are defined if needed
