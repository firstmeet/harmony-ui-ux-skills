# HarmonyOS NEXT UI/UX Best Practices

## Overview

This document defines UI/UX best practices and anti-patterns for HarmonyOS NEXT development.

---

## Mandatory Coding Rules ⚠️

### Language: ArkTS Only

- **MUST** use ArkTS (strict TypeScript-based)
- **MUST NOT** use `any` type - always use explicit types
- **MUST** enable strict type checking

```typescript
// ✅ CORRECT
let count: number = 0
let items: Array<ItemData> = []
function getData(): Promise<ResponseData> { }

// ❌ WRONG
let count: any = 0
let items: any[] = []
function getData(): any { }
```

### UI Framework: ArkUI Declarative Syntax

- **MUST** use ArkUI declarative UI syntax
- **MUST** use `@Component` decorator for custom components
- **MUST** implement `build()` method in components

```typescript
// ✅ CORRECT
@Component
struct MyComponent {
  build() {
    Column() {
      Text('Hello')
    }
  }
}

// ❌ WRONG - No imperative UI construction
```

### State Management Priority

Use state decorators in this priority order:

1. `@State` - Component internal state
2. `@Prop` - One-way data binding from parent
3. `@Link` - Two-way data binding with parent
4. `@Provide` / `@Consume` - Cross-component state sharing
5. `@Observed` + `@ObjectLink` - Complex object state management

```typescript
// ✅ CORRECT
@Component
struct ParentComponent {
  @State count: number = 0                    // Internal state
  @Provide('userData') user: UserInfo = {}   // Provide to descendants

  build() {
    Column() {
      ChildComponent({ count: this.count })   // Pass as @Prop
    }
  }
}

@Component
struct ChildComponent {
  @Prop count: number = 0                     // One-way binding
  @Consume('userData') user: UserInfo        // Consume from ancestor
  @Link selectedId: number                    // Two-way binding

  build() { }
}

// For complex objects
@Observed
class CartItem {
  id: number = 0
  quantity: number = 1
}

@Component
struct CartItemView {
  @ObjectLink item: CartItem                  // Observe object changes

  build() { }
}
```

### Resource References: NO Hardcoding!

- **MUST NOT** hardcode colors - use `$r('app.color.xxx')`
- **MUST NOT** hardcode strings - use `$r('app.string.xxx')`
- **MUST NOT** hardcode dimensions - use `$r('app.float.xxx')` or design tokens

```typescript
// ✅ CORRECT - Use resource references
Text($r('app.string.welcome_message'))
  .fontColor($r('app.color.text_primary'))
  .fontSize($r('app.float.font_size_body'))

Button($r('app.string.button_confirm'))
  .backgroundColor($r('app.color.primary'))

Image($r('app.media.icon_home'))

// ❌ WRONG - Hardcoded values
Text('Welcome')                    // Hardcoded string
  .fontColor('#182431')            // Hardcoded color
  .fontSize(14)                    // Hardcoded size (acceptable for design tokens)

Button('确认')                      // Hardcoded string
  .backgroundColor('#0A59F7')      // Hardcoded color
```

### Resource File Structure

Define resources in `resources/base/element/`:

**color.json**:
```json
{
  "color": [
    { "name": "primary", "value": "#0A59F7" },
    { "name": "text_primary", "value": "#182431" },
    { "name": "text_secondary", "value": "#66727A" },
    { "name": "bg_primary", "value": "#FFFFFF" },
    { "name": "bg_secondary", "value": "#F1F3F5" },
    { "name": "success", "value": "#64BB5C" },
    { "name": "warning", "value": "#FA9D3B" },
    { "name": "error", "value": "#E84026" }
  ]
}
```

**string.json**:
```json
{
  "string": [
    { "name": "app_name", "value": "我的应用" },
    { "name": "button_confirm", "value": "确认" },
    { "name": "button_cancel", "value": "取消" },
    { "name": "welcome_message", "value": "欢迎回来" }
  ]
}
```

**float.json**:
```json
{
  "float": [
    { "name": "font_size_body", "value": "14fp" },
    { "name": "font_size_title", "value": "20fp" },
    { "name": "spacing_md", "value": "12vp" },
    { "name": "radius_sm", "value": "8vp" }
  ]
}
```

---

## Design Principles

### 1. Consistency (一致性)

- Use the design system tokens consistently
- Maintain visual and interaction consistency across pages
- Follow HarmonyOS design language

### 2. Hierarchy (层次感)

- Use typography scale to create visual hierarchy
- Apply proper spacing between elements
- Use shadows and elevation appropriately

### 3. Feedback (反馈)

- Provide immediate feedback for user actions
- Use loading states for async operations
- Show success/error states clearly

### 4. Accessibility (无障碍)

- Ensure sufficient color contrast (4.5:1 for text)
- Support dynamic font scaling
- Add accessibility labels for icons and images

---

## Color Best Practices

### DO ✅

```typescript
// Use semantic colors for states
Text('成功')
  .fontColor('#64BB5C')  // success color

// Use opacity for disabled states
Button('禁用')
  .opacity(0.5)
  .enabled(false)

// Support dark mode
.backgroundColor(this.isDarkMode ? '#121212' : '#FFFFFF')
```

### DON'T ❌

```typescript
// Don't use random colors
Text('文字')
  .fontColor('#1a2b3c')  // Non-standard color

// Don't use pure black on pure white
Text('文字')
  .fontColor('#000000')  // Too harsh

// Don't use low contrast
Text('文字')
  .fontColor('#CCCCCC')  // Poor contrast on white bg
```

---

## Typography Best Practices

### DO ✅

```typescript
// Use consistent font sizes from the scale
Text('标题')
  .fontSize(20)  // headline_large
  .fontWeight(FontWeight.SemiBold)

// Set proper line height for readability
Text('正文内容')
  .fontSize(14)
  .lineHeight(22)  // 1.5x font size

// Handle text overflow properly
Text('很长的文字...')
  .maxLines(2)
  .textOverflow({ overflow: TextOverflow.Ellipsis })
```

### DON'T ❌

```typescript
// Don't use arbitrary font sizes
Text('文字')
  .fontSize(13)  // Not in the scale

// Don't use too many font weights on one page
// Limit to 2-3 weights maximum

// Don't center long paragraphs
Text('很长的段落文字...')
  .textAlign(TextAlign.Center)  // Hard to read
```

---

## Spacing Best Practices

### DO ✅

```typescript
// Use consistent spacing from the system
Column({ space: 16 }) {  // Use 4, 8, 12, 16, 20, 24, 32
  // content
}

// Use proper padding
.padding(16)  // Standard content padding

// Group related elements with tighter spacing
Column({ space: 4 }) {  // Related items
  Text('标题')
  Text('副标题')
}
```

### DON'T ❌

```typescript
// Don't use arbitrary spacing
.margin(17)  // Not in the spacing scale

// Don't use inconsistent spacing
Column({ space: 10 }) {  // Not in scale
  // content
}

// Don't overcrowd elements
.padding(4)  // Too tight for content
```

---

## Component Best Practices

### Button

```typescript
// Primary action - use brand color
Button('确认')
  .backgroundColor('#0A59F7')
  .fontColor('#FFFFFF')
  .height(44)
  .borderRadius(8)

// Secondary action - use neutral color
Button('取消')
  .backgroundColor('#F1F3F5')
  .fontColor('#182431')

// Add loading state
Button('提交')
  .enabled(!this.isLoading)
// Show LoadingProgress when loading
```

### Input

```typescript
// Show clear feedback for states
TextInput()
  .borderColor(this.hasError ? '#E84026' : '#E5E8EB')

// Always provide placeholder
TextInput({ placeholder: '请输入用户名' })

// Handle focus states
.onFocus(() => { this.isFocused = true })
.onBlur(() => { this.isFocused = false })
```

### List

```typescript
// Use proper item spacing
List({ space: 12 })

// Provide visual feedback for tap
ListItem()
  .onClick(() => { })
  .stateStyles({
    pressed: { .backgroundColor('#F5F5F5') }
  })

// Handle empty states
if (this.dataList.length === 0) {
  // Show empty state component
}
```

---

## Animation Best Practices

### DO ✅

```typescript
// Use appropriate duration
.animation({
  duration: 200,  // Normal transition
  curve: Curve.EaseInOut
})

// Animate meaningful changes
.opacity(this.isVisible ? 1 : 0)
.animation({ duration: 150 })

// Use spring for natural feel
.animation({ curve: Curve.Smooth })
```

### DON'T ❌

```typescript
// Don't animate everything
// Only animate meaningful state changes

// Don't use long durations for simple actions
.animation({ duration: 1000 })  // Too slow

// Don't use linear easing for UI
.animation({ curve: Curve.Linear })  // Feels mechanical
```

---

## Performance Best Practices

### DO ✅

```typescript
// Use @State only when needed
@State private counter: number = 0  // Will trigger re-render

// Use LazyForEach for large lists
LazyForEach(this.dataList, (item) => {
  ListItem() { }
})

// Optimize images
Image(src)
  .width(100)
  .height(100)  // Specify dimensions
```

### DON'T ❌

```typescript
// Don't create new objects in build()
build() {
  // Bad: creates new array every render
  ForEach([1,2,3], (item) => { })
}

// Don't use ForEach for large lists
ForEach(this.largeList, ...)  // Use LazyForEach instead

// Don't load large images without sizing
Image(largeImage)  // Should specify size
```

---

## Multi-Device Adaptation

### Responsive Layout

```typescript
// Use GridRow/GridCol for responsive layouts
GridRow({ columns: 12 }) {
  GridCol({ span: { sm: 12, md: 6, lg: 4 } }) {
    // Adapts to screen size
  }
}

// Use percentage or layoutWeight
Row() {
  Column()
    .layoutWeight(1)  // Flexible width
  Column()
    .width(100)  // Fixed width
}
```

### Device-Specific Considerations

- **Phone**: Single column layout, bottom navigation
- **Tablet**: Multi-column layout, sidebar navigation
- **Watch**: Compact UI, large touch targets
- **TV**: Focus-based navigation, large text

---

## Accessibility Checklist

- [ ] Color contrast ratio ≥ 4.5:1 for text
- [ ] Touch targets ≥ 44x44 vp
- [ ] Text can scale up to 200%
- [ ] Icons have text labels or descriptions
- [ ] Error messages are descriptive
- [ ] Focus indicators are visible
- [ ] Screen reader labels are meaningful

---

## Common Anti-Patterns

### Avoid These ❌

1. **Inconsistent Colors**: Using non-standard colors
2. **Tiny Touch Targets**: Buttons smaller than 44vp
3. **Missing Loading States**: No feedback during async ops
4. **Poor Error Messages**: Generic or missing error text
5. **Overcrowded UI**: Too many elements, insufficient spacing
6. **Inconsistent Navigation**: Different patterns across pages
7. **Missing Empty States**: Blank screens when no data
8. **No Skeleton Loading**: No placeholder during load
9. **Hard-coded Colors**: Not supporting dark mode
10. **Blocking Main Thread**: Long operations without async
