# HarmonyOS NEXT Responsive Strategy

## Overview

本文档定义"一多"（一次开发，多端部署）的响应式布局策略和断点规范。

---

## 1. 断点定义 (Breakpoints)

### 标准断点值

| 断点 | 代号 | 窗口宽度 | 典型设备 | 栅格列数 |
|------|------|----------|----------|----------|
| **xs** | 超小屏 | < 320vp | 小尺寸手机 | 2-4 |
| **sm** | 小屏 | 320vp - 520vp | 普通手机 | 4-6 |
| **md** | 中屏 | 520vp - 840vp | 折叠屏展开/小平板 | 8 |
| **lg** | 大屏 | ≥ 840vp | 平板/2in1 | 12 |

### 断点配置代码

```typescript
// 标准断点配置
const BREAKPOINTS = {
  value: ['320vp', '520vp', '840vp'],
  reference: BreakpointsReference.WindowSize
}

// 使用示例
GridRow({
  columns: 12,
  breakpoints: BREAKPOINTS
}) {
  // ...
}
```

### 断点监听

```typescript
@Entry
@Component
struct ResponsivePage {
  @State currentBreakpoint: string = 'sm'
  @State windowWidth: number = 0

  aboutToAppear() {
    this.getWindowInfo()
  }

  private async getWindowInfo() {
    const win = await window.getLastWindow(getContext(this))
    const rect = win.getWindowProperties().windowRect
    this.windowWidth = px2vp(rect.width)
    this.updateBreakpoint()
    
    // 监听窗口变化
    win.on('windowSizeChange', (size) => {
      this.windowWidth = px2vp(size.width)
      this.updateBreakpoint()
    })
  }

  private updateBreakpoint() {
    if (this.windowWidth < 320) {
      this.currentBreakpoint = 'xs'
    } else if (this.windowWidth < 520) {
      this.currentBreakpoint = 'sm'
    } else if (this.windowWidth < 840) {
      this.currentBreakpoint = 'md'
    } else {
      this.currentBreakpoint = 'lg'
    }
  }

  build() {
    Column() {
      Text(`当前断点: ${this.currentBreakpoint}`)
      Text(`窗口宽度: ${this.windowWidth}vp`)
    }
  }
}
```

---

## 2. 布局策略选择器

### 决策流程图

```
┌─────────────────────────────────────────────────────────────┐
│                      UI 元素类型判断                          │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
    ┌─────────┐         ┌─────────┐         ┌─────────┐
    │ 基础组件 │         │ 列表宫格 │         │ 页面框架 │
    └─────────┘         └─────────┘         └─────────┘
          │                   │                   │
          ▼                   ▼                   ▼
    ┌─────────┐         ┌─────────┐         ┌─────────┐
    │自适应伸缩│         │ 延伸布局 │         │ 分栏布局 │
    │layoutWeight       │Grid+breakpoints    │SideBarContainer
    │ 百分比   │         │ 列数变化 │         │Navigation Split
    └─────────┘         └─────────┘         └─────────┘
```

### 策略一：自适应伸缩 (Flex Scaling)

**适用场景**: 按钮组、输入框组、工具栏、卡片内部元素

```typescript
// 按钮组自适应
Row() {
  Button($r('app.string.cancel'))
    .layoutWeight(1)
    .backgroundColor($r('app.color.bg_secondary'))
  
  Blank().width(12)
  
  Button($r('app.string.confirm'))
    .layoutWeight(1)
    .backgroundColor($r('app.color.primary'))
}
.width('100%')
.padding(16)

// 搜索框自适应
Row() {
  Search({ placeholder: '搜索' })
    .layoutWeight(1)
  
  Button('筛选')
    .width(60)
}
.width('100%')
```

### 策略二：延伸布局 (Grid Extension)

**适用场景**: 商品列表、图片宫格、功能入口、卡片列表

```typescript
// 商品列表 - 列数随断点变化
@Component
struct ProductGrid {
  @State products: Product[] = []

  build() {
    GridRow({
      columns: 12,
      breakpoints: {
        value: ['320vp', '520vp', '840vp'],
        reference: BreakpointsReference.WindowSize
      },
      gutter: { x: 8, y: 8 }
    }) {
      ForEach(this.products, (product: Product) => {
        GridCol({
          span: { xs: 6, sm: 4, md: 3, lg: 2 }
          // xs: 2列, sm: 3列, md: 4列, lg: 6列
        }) {
          ProductCard({ product: product })
        }
      }, (product: Product) => product.id)
    }
    .padding(16)
  }
}

// 功能入口宫格
@Component  
struct FunctionGrid {
  private functions: FunctionItem[] = [
    { icon: 'sys.symbol.star', label: '收藏' },
    { icon: 'sys.symbol.clock', label: '历史' },
    { icon: 'sys.symbol.heart', label: '喜欢' },
    { icon: 'sys.symbol.gearshape', label: '设置' },
  ]

  build() {
    GridRow({
      columns: { xs: 4, sm: 4, md: 8, lg: 8 },
      breakpoints: {
        value: ['320vp', '520vp', '840vp'],
        reference: BreakpointsReference.WindowSize
      }
    }) {
      ForEach(this.functions, (item: FunctionItem) => {
        GridCol({ span: 1 }) {
          Column() {
            SymbolGlyph($r(item.icon))
              .fontSize(24)
              .fontColor([$r('app.color.primary')])
            Text(item.label)
              .fontSize($r('app.float.font_size_sm'))
              .margin({ top: 4 })
          }
          .width('100%')
          .padding(12)
        }
      })
    }
  }
}
```

### 策略三：分栏布局 (Split Layout)

**适用场景**: 设置页、邮件应用、文件管理、主从详情

```typescript
// 自适应分栏 - 基于断点切换
@Entry
@Component
struct AdaptiveSplitPage {
  @State currentBreakpoint: string = 'sm'
  @Provide('navStack') navStack: NavPathStack = new NavPathStack()

  build() {
    // 大屏使用分栏，小屏使用栈式导航
    if (this.currentBreakpoint === 'lg' || this.currentBreakpoint === 'md') {
      this.buildSplitLayout()
    } else {
      this.buildStackLayout()
    }
  }

  @Builder
  buildSplitLayout() {
    SideBarContainer(SideBarContainerType.Embed) {
      // 侧边栏 - 菜单列表
      Column() {
        MenuList()
      }
      .width('100%')
      .backgroundColor($r('app.color.bg_secondary'))

      // 内容区
      Column() {
        ContentArea()
      }
      .width('100%')
    }
    .sideBarWidth(280)
    .minSideBarWidth(200)
    .maxSideBarWidth(360)
    .showSideBar(true)
  }

  @Builder
  buildStackLayout() {
    Navigation(this.navStack) {
      MenuList()
    }
    .mode(NavigationMode.Stack)
    .navBarWidth('100%')
  }
}

// 使用 Navigation 的分栏模式
@Entry
@Component
struct NavigationSplitPage {
  @Provide('navStack') navStack: NavPathStack = new NavPathStack()

  build() {
    Navigation(this.navStack) {
      // 主列表
      List() {
        ForEach(this.dataList, (item: DataItem) => {
          ListItem() {
            this.listItemBuilder(item)
          }
          .onClick(() => {
            this.navStack.pushPath({ name: 'detail', param: item })
          })
        })
      }
    }
    .navDestination(this.pageBuilder)
    .mode(NavigationMode.Auto)  // 自动切换 Stack/Split
    .navBarWidth(320)
    .minContentWidth(360)
  }

  @Builder
  pageBuilder(name: string, param: object) {
    if (name === 'detail') {
      DetailPage({ item: param as DataItem })
    }
  }

  @Builder
  listItemBuilder(item: DataItem) {
    Row() {
      Text(item.title)
      Blank()
      SymbolGlyph($r('sys.symbol.chevron_right'))
    }
    .width('100%')
    .padding(16)
  }
}
```

---

## 3. GridCol + MediaColumn 组合用法

### 响应式卡片布局

```typescript
@Component
struct ResponsiveCardLayout {
  @State cards: CardData[] = []

  build() {
    Scroll() {
      GridRow({
        columns: 12,
        breakpoints: {
          value: ['320vp', '520vp', '840vp'],
          reference: BreakpointsReference.WindowSize
        },
        gutter: { x: 12, y: 12 }
      }) {
        // 横幅卡片 - 始终全宽
        GridCol({ span: 12 }) {
          BannerCard()
        }

        // 主要内容卡片 - 响应式
        GridCol({
          span: { xs: 12, sm: 12, md: 8, lg: 8 }
        }) {
          MainContentCard()
        }

        // 侧边信息卡片 - 小屏隐藏或全宽
        GridCol({
          span: { xs: 12, sm: 12, md: 4, lg: 4 }
        }) {
          SideInfoCard()
        }

        // 功能卡片组 - 列数随断点变化
        ForEach(this.cards, (card: CardData) => {
          GridCol({
            span: { xs: 6, sm: 4, md: 3, lg: 2 }
          }) {
            FunctionCard({ data: card })
          }
        })
      }
      .padding(16)
    }
  }
}
```

### 表单响应式布局

```typescript
@Component
struct ResponsiveForm {
  @State formData: FormData = new FormData()

  build() {
    Scroll() {
      GridRow({
        columns: 12,
        breakpoints: {
          value: ['320vp', '520vp', '840vp'],
          reference: BreakpointsReference.WindowSize
        },
        gutter: { x: 16, y: 16 }
      }) {
        // 姓名 - 大屏半宽，小屏全宽
        GridCol({ span: { xs: 12, sm: 12, md: 6, lg: 6 } }) {
          this.inputField('姓名', this.formData.name)
        }

        // 手机号 - 大屏半宽，小屏全宽
        GridCol({ span: { xs: 12, sm: 12, md: 6, lg: 6 } }) {
          this.inputField('手机号', this.formData.phone)
        }

        // 地址 - 始终全宽
        GridCol({ span: 12 }) {
          this.inputField('详细地址', this.formData.address)
        }

        // 备注 - 始终全宽
        GridCol({ span: 12 }) {
          this.textAreaField('备注', this.formData.remark)
        }
      }
      .padding(16)
    }
  }

  @Builder
  inputField(label: string, value: string) {
    Column() {
      Text(label)
        .fontSize($r('app.float.font_size_sm'))
        .fontColor($r('app.color.text_secondary'))
        .margin({ bottom: 4 })
      TextInput({ text: value })
        .height(44)
        .backgroundColor($r('app.color.bg_secondary'))
        .borderRadius(8)
    }
    .alignItems(HorizontalAlign.Start)
  }

  @Builder
  textAreaField(label: string, value: string) {
    Column() {
      Text(label)
        .fontSize($r('app.float.font_size_sm'))
        .fontColor($r('app.color.text_secondary'))
        .margin({ bottom: 4 })
      TextArea({ text: value })
        .height(100)
        .backgroundColor($r('app.color.bg_secondary'))
        .borderRadius(8)
    }
    .alignItems(HorizontalAlign.Start)
  }
}
```

---

## 4. 断点相关组件显隐

```typescript
@Component
struct ResponsiveVisibility {
  @State currentBreakpoint: string = 'sm'

  build() {
    Column() {
      // 仅在大屏显示
      if (this.currentBreakpoint === 'lg' || this.currentBreakpoint === 'md') {
        DesktopOnlyComponent()
      }

      // 仅在小屏显示
      if (this.currentBreakpoint === 'sm' || this.currentBreakpoint === 'xs') {
        MobileOnlyComponent()
      }

      // 根据断点显示不同版本
      if (this.currentBreakpoint === 'lg') {
        FullFeatureNav()
      } else if (this.currentBreakpoint === 'md') {
        CompactNav()
      } else {
        BottomTabBar()
      }
    }
  }
}
```

---

## 5. 响应式检查清单

- [ ] 所有列表/宫格使用 GridRow + GridCol
- [ ] 断点配置使用标准值 ['320vp', '520vp', '840vp']
- [ ] 大屏 (>600vp) 页面使用分栏布局
- [ ] 按钮组/输入框使用 layoutWeight 自适应
- [ ] 图片资源提供多分辨率版本
- [ ] 导航方式随断点切换 (底部Tab ↔ 侧边栏)
