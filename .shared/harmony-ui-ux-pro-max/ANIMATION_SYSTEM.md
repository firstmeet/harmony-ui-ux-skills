# HarmonyOS NEXT Animation System

## Overview

本文档定义 ArkUI 动画系统的标准用法和推荐实践。

---

## ⚠️ 重要：API 12+ 动画 API 迁移

### 废弃 API 警告

从 **API 12 (HarmonyOS NEXT 5.0)** 开始，全局 `animateTo()` 函数已被标记为 **废弃 (deprecated)**。

```
WARN: 'animateTo' has been deprecated.
```

### 新 API：`getUIContext().animateTo()`

必须使用组件上下文的 `animateTo()` 方法替代全局函数：

| 旧 API (废弃) | 新 API (推荐) |
|--------------|---------------|
| `animateTo(options, closure)` | `this.getUIContext().animateTo(options, closure)` |

### 迁移示例

**❌ 旧写法 (已废弃):**

```typescript
Button('触发动画')
  .onClick(() => {
    animateTo({
      duration: 300,
      curve: Curve.Friction
    }, () => {
      this.isExpanded = !this.isExpanded
    })
  })
```

**✅ 新写法 (推荐):**

```typescript
Button('触发动画')
  .onClick(() => {
    this.getUIContext().animateTo({
      duration: 300,
      curve: Curve.Friction
    }, () => {
      this.isExpanded = !this.isExpanded
    })
  })
```

### 循环动画迁移

对于 `setInterval` 中的动画，同样需要迁移：

```typescript
// ❌ 旧写法
private startBreatheAnimation(): void {
  setInterval(() => {
    animateTo({
      duration: 2000,
      curve: Curve.EaseInOut
    }, () => {
      this.scale = this.scale === 1 ? 1.02 : 1
    })
  }, 2000)
}

// ✅ 新写法
private startBreatheAnimation(): void {
  setInterval(() => {
    this.getUIContext().animateTo({
      duration: 2000,
      curve: Curve.EaseInOut
    }, () => {
      this.scale = this.scale === 1 ? 1.02 : 1
    })
  }, 2000)
}
```

### 迁移原因

1. **上下文隔离**：新 API 通过 `UIContext` 显式管理动画上下文，避免全局状态污染
2. **组件化设计**：更符合 HarmonyOS NEXT 的组件化设计理念
3. **多窗口支持**：为多窗口场景提供更好的支持

### AI 行为规范

生成任何使用 `animateTo` 的代码时，**必须**使用 `this.getUIContext().animateTo()`：

```typescript
// AI 生成代码必须遵循此模式
this.getUIContext().animateTo({
  duration: 300,
  curve: Curve.Friction,
  onFinish: () => {
    console.info('动画完成')
  }
}, () => {
  // 状态变更
})
```

---

## 1. 系统推荐曲线 (Animation Curves)

### 曲线一览表

| 曲线 | 代码 | 特性 | 应用场景 |
|------|------|------|----------|
| **Friction** | `Curve.Friction` | 自然摩擦衰减 | 页面转场、列表滚动、展开收起 |
| **Sharp** | `Curve.Sharp` | 快速响应 | 按钮反馈、开关切换、快速交互 |
| **Smooth** | `Curve.Smooth` | 平滑过渡 | 滚动惯性、渐变效果 |
| **EaseInOut** | `Curve.EaseInOut` | 先慢后快再慢 | 通用过渡动画 |
| **FastOutSlowIn** | `Curve.FastOutSlowIn` | 快出慢入 | 元素进入 |
| **LinearOutSlowIn** | `Curve.LinearOutSlowIn` | 线性出慢入 | 元素退出 |
| **Spring** | `Curve.Spring` | 弹簧效果 | 弹性交互、下拉刷新 |

### 曲线选择决策

```
┌─────────────────────────────────────────────────────────────┐
│                      动画类型判断                            │
└─────────────────────────────────────────────────────────────┘
                              │
     ┌────────────────────────┼────────────────────────┐
     ▼                        ▼                        ▼
┌─────────┐            ┌─────────────┐          ┌─────────┐
│ 页面转场 │            │  交互反馈   │          │ 滚动惯性 │
└─────────┘            └─────────────┘          └─────────┘
     │                        │                        │
     ▼                        ▼                        ▼
┌─────────┐            ┌─────────────┐          ┌─────────┐
│Friction │            │   Sharp     │          │ Smooth  │
│ 300ms   │            │  100-200ms  │          │  自然   │
└─────────┘            └─────────────┘          └─────────┘
```

### Curve.Friction - 自然摩擦

```typescript
// 页面展开/收起
@State isExpanded: boolean = false

Column() {
  Row() {
    Text('详情')
    SymbolGlyph($r('sys.symbol.chevron_down'))
      .rotate({ angle: this.isExpanded ? 180 : 0 })
      .animation({
        duration: 300,
        curve: Curve.Friction
      })
  }
  .onClick(() => {
    this.getUIContext().animateTo({
      duration: 300,
      curve: Curve.Friction
    }, () => {
      this.isExpanded = !this.isExpanded
    })
  })

  if (this.isExpanded) {
    Text('详细内容...')
      .transition({
        type: TransitionType.Insert,
        opacity: 0,
        translate: { y: -20 }
      })
  }
}
```

### Curve.Sharp - 快速响应

```typescript
// 按钮点击反馈
@State isPressed: boolean = false

Button($r('app.string.submit'))
  .scale({ x: this.isPressed ? 0.95 : 1, y: this.isPressed ? 0.95 : 1 })
  .animation({
    duration: 100,
    curve: Curve.Sharp
  })
  .onTouch((event) => {
    if (event.type === TouchType.Down) {
      this.isPressed = true
    } else if (event.type === TouchType.Up || event.type === TouchType.Cancel) {
      this.isPressed = false
    }
  })

// 开关切换
@State isOn: boolean = false

Toggle({ type: ToggleType.Switch, isOn: this.isOn })
  .onChange((value) => {
    this.getUIContext().animateTo({
      duration: 150,
      curve: Curve.Sharp
    }, () => {
      this.isOn = value
    })
  })
```

### Curve.Spring - 弹簧效果

```typescript
// 下拉刷新弹性
@State refreshOffset: number = 0
@State isRefreshing: boolean = false

Column() {
  // 刷新指示器
  Row() {
    if (this.isRefreshing) {
      LoadingProgress().width(24).height(24)
    } else {
      SymbolGlyph($r('sys.symbol.arrow_down'))
        .rotate({ angle: this.refreshOffset > 60 ? 180 : 0 })
    }
    Text(this.refreshOffset > 60 ? '释放刷新' : '下拉刷新')
  }
  .height(this.refreshOffset)
  .animation({
    duration: 300,
    curve: Curve.Spring
  })
  
  // 内容列表
  List() {
    // ...
  }
}
.gesture(
  PanGesture()
    .onActionUpdate((event) => {
      if (event.offsetY > 0) {
        this.refreshOffset = Math.min(event.offsetY, 100)
      }
    })
    .onActionEnd(() => {
      if (this.refreshOffset > 60) {
        this.startRefresh()
      } else {
        this.getUIContext().animateTo({ duration: 300, curve: Curve.Spring }, () => {
          this.refreshOffset = 0
        })
      }
    })
)
```

---

## 2. 页面转场动画 (Page Transition)

### 标准转场模板

```typescript
// 页面入场/退场动画
@Entry
@Component
struct AnimatedPage {
  // 入场动画
  pageTransition() {
    // 进入时：从右侧滑入 + 淡入
    PageTransitionEnter({
      duration: 300,
      curve: Curve.Friction
    })
      .slide(SlideEffect.Right)
      .opacity(0)

    // 退出时：向左滑出 + 淡出
    PageTransitionExit({
      duration: 300,
      curve: Curve.Friction
    })
      .slide(SlideEffect.Left)
      .opacity(0)
  }

  build() {
    Column() {
      // 页面内容
    }
  }
}
```

### 常用转场效果

```typescript
// 1. 水平滑动（默认）
pageTransition() {
  PageTransitionEnter({ duration: 300, curve: Curve.Friction })
    .slide(SlideEffect.Right)
  PageTransitionExit({ duration: 300, curve: Curve.Friction })
    .slide(SlideEffect.Left)
}

// 2. 垂直滑动（底部弹出）
pageTransition() {
  PageTransitionEnter({ duration: 300, curve: Curve.Friction })
    .slide(SlideEffect.Bottom)
  PageTransitionExit({ duration: 300, curve: Curve.Friction })
    .slide(SlideEffect.Bottom)
}

// 3. 缩放 + 淡入淡出
pageTransition() {
  PageTransitionEnter({ duration: 300, curve: Curve.EaseInOut })
    .opacity(0)
    .scale({ x: 0.9, y: 0.9 })
  PageTransitionExit({ duration: 300, curve: Curve.EaseInOut })
    .opacity(0)
    .scale({ x: 1.1, y: 1.1 })
}

// 4. 纯淡入淡出
pageTransition() {
  PageTransitionEnter({ duration: 250, curve: Curve.EaseInOut })
    .opacity(0)
  PageTransitionExit({ duration: 250, curve: Curve.EaseInOut })
    .opacity(0)
}
```

---

## 3. 共享元素转场 (Shared Transition)

### 图片预览转场

```typescript
// 列表页
@Component
struct ImageList {
  @State images: string[] = []

  build() {
    GridRow({ columns: 3 }) {
      ForEach(this.images, (image: string, index: number) => {
        GridCol({ span: 1 }) {
          Image(image)
            .aspectRatio(1)
            .borderRadius(8)
            // 设置共享元素 ID
            .sharedTransition(`image_${index}`, {
              duration: 300,
              curve: Curve.Friction,
              type: SharedTransitionEffectType.Exchange
            })
            .onClick(() => {
              router.pushUrl({
                url: 'pages/ImagePreview',
                params: { image: image, index: index }
              })
            })
        }
      })
    }
  }
}

// 预览页
@Entry
@Component
struct ImagePreview {
  @State image: string = ''
  @State index: number = 0

  aboutToAppear() {
    const params = router.getParams() as Record<string, Object>
    this.image = params.image as string
    this.index = params.index as number
  }

  build() {
    Stack() {
      Image(this.image)
        .width('100%')
        .objectFit(ImageFit.Contain)
        // 匹配共享元素 ID
        .sharedTransition(`image_${this.index}`, {
          duration: 300,
          curve: Curve.Friction,
          type: SharedTransitionEffectType.Exchange
        })
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#000000')
  }
}
```

---

## 4. 属性动画 (Property Animation)

### 基础属性动画

```typescript
@Component
struct PropertyAnimationDemo {
  @State opacity: number = 1
  @State scale: number = 1
  @State rotate: number = 0
  @State translateY: number = 0

  build() {
    Column({ space: 20 }) {
      // 透明度动画
      Text('淡入淡出')
        .opacity(this.opacity)
        .animation({ duration: 300, curve: Curve.EaseInOut })

      // 缩放动画
      Text('缩放')
        .scale({ x: this.scale, y: this.scale })
        .animation({ duration: 200, curve: Curve.Sharp })

      // 旋转动画
      SymbolGlyph($r('sys.symbol.arrow_clockwise'))
        .rotate({ angle: this.rotate })
        .animation({ duration: 500, curve: Curve.Friction })

      // 位移动画
      Text('上下移动')
        .translate({ y: this.translateY })
        .animation({ duration: 300, curve: Curve.Spring })

      // 触发按钮
      Button('播放动画')
        .onClick(() => {
          this.opacity = this.opacity === 1 ? 0.3 : 1
          this.scale = this.scale === 1 ? 1.2 : 1
          this.rotate += 360
          this.translateY = this.translateY === 0 ? -20 : 0
        })
    }
  }
}
```

### getUIContext().animateTo 显式动画

```typescript
@Component
struct AnimateToDemo {
  @State boxWidth: number = 100
  @State boxColor: ResourceColor = $r('app.color.primary')

  build() {
    Column({ space: 20 }) {
      // 动画目标元素
      Column()
        .width(this.boxWidth)
        .height(100)
        .backgroundColor(this.boxColor)
        .borderRadius(12)

      // 触发按钮
      Button('切换状态')
        .onClick(() => {
          this.getUIContext().animateTo({
            duration: 300,
            curve: Curve.Friction,
            onFinish: () => {
              console.info('动画完成')
            }
          }, () => {
            // 在闭包中修改状态
            this.boxWidth = this.boxWidth === 100 ? 200 : 100
            this.boxColor = this.boxWidth === 200 
              ? $r('app.color.success') 
              : $r('app.color.primary')
          })
        })
    }
    .padding(20)
  }
}
```

---

## 5. 组件转场 (Component Transition)

### 条件渲染转场

```typescript
@Component
struct ConditionalTransition {
  @State showContent: boolean = false

  build() {
    Column({ space: 20 }) {
      Button(this.showContent ? '隐藏' : '显示')
        .onClick(() => {
          this.getUIContext().animateTo({ duration: 300, curve: Curve.Friction }, () => {
            this.showContent = !this.showContent
          })
        })

      if (this.showContent) {
        Column() {
          Text('这是一段内容')
          Text('带有入场和退场动画')
        }
        .padding(20)
        .backgroundColor($r('app.color.bg_secondary'))
        .borderRadius(12)
        // 入场动画
        .transition({
          type: TransitionType.Insert,
          opacity: 0,
          translate: { y: 20 },
          scale: { x: 0.9, y: 0.9 }
        })
        // 退场动画
        .transition({
          type: TransitionType.Delete,
          opacity: 0,
          translate: { y: -20 },
          scale: { x: 0.9, y: 0.9 }
        })
      }
    }
  }
}
```

### 列表项动画

```typescript
@Component
struct AnimatedList {
  @State items: string[] = ['项目1', '项目2', '项目3']

  build() {
    Column() {
      Button('添加项目')
        .onClick(() => {
          this.getUIContext().animateTo({ duration: 300, curve: Curve.Friction }, () => {
            this.items.push(`项目${this.items.length + 1}`)
          })
        })

      List() {
        ForEach(this.items, (item: string, index: number) => {
          ListItem() {
            Row() {
              Text(item)
              Blank()
              Button('删除')
                .onClick(() => {
                  this.getUIContext().animateTo({ duration: 300, curve: Curve.Friction }, () => {
                    this.items.splice(index, 1)
                  })
                })
            }
            .padding(16)
          }
          .transition({
            type: TransitionType.All,
            opacity: 0,
            translate: { x: -100 }
          })
        }, (item: string) => item)
      }
    }
  }
}
```

---

## 6. 动画时长规范

| 动画类型 | 推荐时长 | 说明 |
|---------|---------|------|
| 按钮反馈 | 100ms | 快速响应，用户感知即时 |
| 开关切换 | 150ms | 状态变化清晰可见 |
| 卡片展开 | 250-300ms | 内容变化平滑过渡 |
| 页面转场 | 300ms | 标准页面切换时长 |
| 模态弹出 | 300ms | 弹窗/底部面板出现 |
| 加载动画 | 循环 | 持续旋转，无固定时长 |
| 复杂动画 | 400-500ms | 多属性联动动画 |

---

## 7. 动画检查清单

- [ ] **使用 `this.getUIContext().animateTo()` 而非全局 `animateTo()`**
- [ ] 页面转场使用 `Curve.Friction`，时长 300ms
- [ ] 按钮反馈使用 `Curve.Sharp`，时长 100-150ms
- [ ] 弹性效果使用 `Curve.Spring`
- [ ] 条件渲染配置 transition 入场/退场动画
- [ ] 列表项增删使用 `getUIContext().animateTo()` 包裹
- [ ] 共享元素设置相同的 sharedTransition ID
- [ ] 动画时长不超过 500ms（除循环动画外）
