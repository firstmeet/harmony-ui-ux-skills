# HarmonyOS NEXT Navigation 架构与跳转指南

## 1. 核心架构逻辑

Navigation 采用"容器 + 路由表"模式，主要由三部分组成：

| 组件 | 职责 |
|------|------|
| **Navigation** (主容器) | 负责全局路由管理、标题栏显示、一多（多端）适配 |
| **NavDestination** (子页容器) | 所有跳转的目标页面必须包裹在 NavDestination 中 |
| **NavPathStack** (路由栈) | 控制跳转、回退、传参的"方向盘" |

## 2. 标准布局模式 (Standard Layout)

### A. 主页结构 (Index.ets)

主页负责初始化路由栈并定义导航模式。

```typescript
@Entry
@Component
struct Index {
  // 1. 初始化路由栈（必须持久化在主页）
  @Provide('pageStack') pageStack: NavPathStack = new NavPathStack();

  build() {
    // 2. 绑定路由栈
    Navigation(this.pageStack) {
      Column() {
        Button('跳转详情页')
          .onClick(() => {
            // 3. 执行跳转
            this.pageStack.pushPath({ name: 'DetailsPage', param: { id: 101 } })
          })
      }
    }
    .title('首页')
    .mode(NavigationMode.Stack) // Stack: 单层模式; Split: 分栏模式(适配平板)
    .navDestination(this.PageMap) // 4. 绑定路由映射表
  }

  // 5. 路由映射表：根据名字渲染对应的子页面
  @Builder
  PageMap(name: string) {
    if (name === 'DetailsPage') {
      DetailsPage()
    }
  }
}
```

### B. 子页面结构 (DetailsPage.ets)

子页面必须使用 **NavDestination** 作为根节点。

```typescript
@Component
export struct DetailsPage {
  // ⚠️ 关键：使用 @Consume 获取路由栈，key 必须与主页的 @Provide 一致
  @Consume('pageStack') pageStack: NavPathStack;

  build() {
    NavDestination() {
      Column() {
        Text('我是详情页')
        Button('返回').onClick(() => {
          this.pageStack.pop() // 回退
        })
      }
    }
    .title('详情')
    .onBackPressed(() => {
      this.pageStack.pop()
      return true
    })
  }
}
```

## 3. 跳转与传参规范 (Actions)

AI 必须使用以下标准方法，**严禁使用 router.pushUrl**：

| 动作 | 代码实现 | 说明 |
|------|---------|------|
| 基础跳转 | `this.pageStack.pushPath({ name: 'PageName' })` | 普通入栈 |
| 带参跳转 | `this.pageStack.pushPath({ name: 'PageName', param: data })` | 参数可以是对象 |
| 获取参数 | `onReady((ctx) => { ctx.pathInfo.param })` | 在 NavDestination 生命周期中获取 |
| 清空栈跳转 | `this.pageStack.clear(); this.pageStack.pushPath(...)` | 常用于登录成功后跳转首页 |
| 带返回值的跳转 | `this.pageStack.pushPathByName('Page', data, (popInfo) => { ... })` | 类似 startActivityForResult |

## 4. "一多"适配策略 (Multi-device)

Navigation 的核心优势是自动适配屏幕宽度：

- **手机 (sm)**: 自动呈现为单页堆栈模式
- **折叠屏/平板 (md/lg)**: 通过设置 `.mode(NavigationMode.Auto)`，当屏幕够宽时，会自动变为"左侧列表、右侧详情"的分栏布局

```typescript
Navigation(this.pageStack) {
  // 主内容（在分栏模式下显示在左侧）
  MainContent()
}
.mode(NavigationMode.Auto)  // 自动适配：手机=Stack，平板=Split
.navBarWidth('40%')         // 分栏模式下导航栏宽度
```

## 5. AI 行为约束 (Rules)

### ⛔ 禁止混用
如果在项目中检测到 `Navigation`，**严禁**再生成 `router.pushUrl` 的代码。

### ✅ 强制 Provide/Consume
- 主页必须 `@Provide('pageStack')`
- 子页必须 `@Consume('pageStack')`
- **Key 名称必须完全一致！**

### ✅ 解耦建议
当路由表过大时，使用 `route_map.json` 配置文件进行动态路由解耦：

```json
// route_map.json
{
  "routerMap": [
    {
      "name": "DetailsPage",
      "pageSourceFile": "src/main/ets/pages/DetailsPage.ets",
      "buildFunction": "DetailsPageBuilder"
    }
  ]
}
```

## 6. 常见错误排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 子页面空白 | @Consume key 不匹配 | 确保 @Provide 和 @Consume 使用相同的 key |
| 跳转无反应 | pageStack 未绑定 | 检查 Navigation(this.pageStack) 是否正确绑定 |
| 返回失败 | 路由栈为空 | 使用 pageStack.size() 检查栈深度 |
| 参数获取为 undefined | 获取时机错误 | 在 NavDestination 的 onReady 回调中获取 |

## 7. 完整示例：带 Tabs 的主页

```typescript
@Entry
@Component
struct Index {
  @State currentIndex: number = 0
  @Provide('pageStack') pageStack: NavPathStack = new NavPathStack()

  @Builder
  PageMap(name: string) {
    if (name === 'DetailPage') {
      DetailPage()
    } else if (name === 'SettingsPage') {
      SettingsPage()
    }
  }

  build() {
    Navigation(this.pageStack) {
      Tabs({ barPosition: BarPosition.End, index: this.currentIndex }) {
        TabContent() {
          HomePage()
        }
        .tabBar('首页')

        TabContent() {
          ProfilePage()
        }
        .tabBar('我的')
      }
      .onChange((index: number) => {
        this.currentIndex = index
      })
    }
    .hideTitleBar(true)
    .mode(NavigationMode.Stack)
    .navDestination(this.PageMap)
  }
}

// 子组件中跳转
@Component
export struct HomePage {
  @Consume('pageStack') pageStack: NavPathStack

  build() {
    Column() {
      Button('查看详情')
        .onClick(() => {
          this.pageStack.pushPath({ name: 'DetailPage', param: { id: 123 } })
        })
    }
  }
}

// 目标页面
@Component
export struct DetailPage {
  @Consume('pageStack') pageStack: NavPathStack
  @State itemId: number = 0

  build() {
    NavDestination() {
      Column() {
        Text(`详情页 ID: ${this.itemId}`)
        Button('返回')
          .onClick(() => this.pageStack.pop())
      }
    }
    .title('详情')
    .onReady((ctx: NavDestinationContext) => {
      const param = ctx.pathInfo.param as Record<string, number>
      this.itemId = param?.id ?? 0
    })
    .onBackPressed(() => {
      this.pageStack.pop()
      return true
    })
  }
}
```

## 8. Checklist

使用 Navigation 架构时，确保：

- [ ] 主页使用 `@Provide('pageStack')` 初始化 NavPathStack
- [ ] 主页 `build()` 中 Navigation 绑定了 pageStack
- [ ] 主页定义了 `@Builder PageMap(name: string)` 路由映射
- [ ] 主页 Navigation 绑定了 `.navDestination(this.PageMap)`
- [ ] 子组件使用 `@Consume('pageStack')` 获取路由栈
- [ ] 目标页面根节点是 `NavDestination()`
- [ ] 目标页面处理了 `.onBackPressed()` 回调
- [ ] **严禁**在同一项目中混用 `router.pushUrl`
