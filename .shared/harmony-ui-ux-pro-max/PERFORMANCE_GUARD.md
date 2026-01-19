# HarmonyOS NEXT Performance Guard

## Overview

本文档定义 ArkUI 渲染性能的硬性约束和最佳实践，确保应用流畅运行。

---

## 1. Build() 嵌套层级限制

### 硬性规则

| 指标 | 限制值 | 说明 |
|------|--------|------|
| **最大嵌套层级** | ≤ 8 层 | 超过会导致渲染性能下降 |
| **推荐嵌套层级** | ≤ 5 层 | 最佳实践 |
| **单组件子元素** | ≤ 50 个 | 超过应使用 LazyForEach |

### 嵌套层级计算

```typescript
// 层级计算示例
Column() {                    // 第 1 层
  Row() {                     // 第 2 层
    Column() {                // 第 3 层
      Text('内容')            // 第 4 层 (叶子节点)
    }
  }
}
```

### 优化方案：使用 RelativeContainer

```typescript
// ❌ 错误：深层嵌套 (6 层)
Column() {
  Row() {
    Column() {
      Row() {
        Column() {
          Text('标题')
          Text('副标题')
        }
        Image($r('app.media.avatar'))
      }
    }
  }
}

// ✅ 正确：扁平化布局 (2 层)
RelativeContainer() {
  Text('标题')
    .id('title')
    .alignRules({
      top: { anchor: '__container__', align: VerticalAlign.Top },
      left: { anchor: '__container__', align: HorizontalAlign.Start }
    })
  
  Text('副标题')
    .id('subtitle')
    .alignRules({
      top: { anchor: 'title', align: VerticalAlign.Bottom },
      left: { anchor: '__container__', align: HorizontalAlign.Start }
    })
    .margin({ top: 4 })
  
  Image($r('app.media.avatar'))
    .id('avatar')
    .width(48).height(48)
    .alignRules({
      top: { anchor: '__container__', align: VerticalAlign.Top },
      right: { anchor: '__container__', align: HorizontalAlign.End }
    })
}
```

---

## 2. LazyForEach 实现模板

### 何时使用 LazyForEach

| 数据量 | 推荐方案 |
|--------|---------|
| < 20 | `ForEach` |
| 20 - 50 | `ForEach` 或 `LazyForEach` |
| > 50 | **必须使用 `LazyForEach`** |
| > 500 | `LazyForEach` + 分页加载 |

### IDataSource 标准实现

```typescript
/**
 * 基础数据源实现
 * 用于 LazyForEach 的数据管理
 */
class BasicDataSource<T> implements IDataSource {
  private listeners: DataChangeListener[] = []
  private dataArray: T[] = []

  // 获取数据总数
  totalCount(): number {
    return this.dataArray.length
  }

  // 获取指定索引的数据
  getData(index: number): T {
    return this.dataArray[index]
  }

  // 注册数据变化监听
  registerDataChangeListener(listener: DataChangeListener): void {
    if (this.listeners.indexOf(listener) < 0) {
      this.listeners.push(listener)
    }
  }

  // 注销数据变化监听
  unregisterDataChangeListener(listener: DataChangeListener): void {
    const index = this.listeners.indexOf(listener)
    if (index >= 0) {
      this.listeners.splice(index, 1)
    }
  }

  // ============ 数据操作方法 ============

  // 设置新数据
  setData(data: T[]): void {
    this.dataArray = data
    this.notifyDataReload()
  }

  // 添加单条数据
  addData(item: T): void {
    this.dataArray.push(item)
    this.notifyDataAdd(this.dataArray.length - 1)
  }

  // 插入数据到指定位置
  insertData(index: number, item: T): void {
    this.dataArray.splice(index, 0, item)
    this.notifyDataAdd(index)
  }

  // 删除指定位置数据
  deleteData(index: number): void {
    this.dataArray.splice(index, 1)
    this.notifyDataDelete(index)
  }

  // 更新指定位置数据
  updateData(index: number, item: T): void {
    this.dataArray[index] = item
    this.notifyDataChange(index)
  }

  // ============ 通知方法 ============

  private notifyDataReload(): void {
    this.listeners.forEach(listener => {
      listener.onDataReloaded()
    })
  }

  private notifyDataAdd(index: number): void {
    this.listeners.forEach(listener => {
      listener.onDataAdd(index)
    })
  }

  private notifyDataDelete(index: number): void {
    this.listeners.forEach(listener => {
      listener.onDataDelete(index)
    })
  }

  private notifyDataChange(index: number): void {
    this.listeners.forEach(listener => {
      listener.onDataChange(index)
    })
  }
}
```

### LazyForEach 使用模板

```typescript
// 数据模型
interface ProductItem {
  id: string
  name: string
  price: number
  image: string
}

@Component
struct ProductList {
  // 使用数据源
  @State dataSource: BasicDataSource<ProductItem> = new BasicDataSource()

  aboutToAppear() {
    // 初始化数据
    this.loadData()
  }

  build() {
    List() {
      LazyForEach(
        this.dataSource,
        (item: ProductItem, index: number) => {
          ListItem() {
            ProductCard({ item: item })
          }
        },
        // ⚠️ keyGenerator 必填！使用唯一标识
        (item: ProductItem) => item.id
      )
    }
    .cachedCount(5)  // 预加载缓存数量
    .onReachEnd(() => {
      this.loadMoreData()  // 触底加载更多
    })
  }

  private async loadData() {
    const data = await fetchProducts()
    this.dataSource.setData(data)
  }

  private async loadMoreData() {
    const moreData = await fetchMoreProducts()
    moreData.forEach(item => this.dataSource.addData(item))
  }
}
```

### keyGenerator 规范

```typescript
// ✅ 正确：使用唯一且稳定的 key
LazyForEach(this.dataSource, (item) => {
  // ...
}, (item: ProductItem) => item.id)  // 使用业务 ID

// ✅ 正确：组合字段生成唯一 key
LazyForEach(this.dataSource, (item) => {
  // ...
}, (item: OrderItem) => `${item.orderId}_${item.productId}`)

// ❌ 错误：使用 index 作为 key
LazyForEach(this.dataSource, (item, index) => {
  // ...
}, (item, index) => index.toString())  // 危险！删除/排序时会出错

// ❌ 错误：使用随机数
LazyForEach(this.dataSource, (item) => {
  // ...
}, () => Math.random().toString())  // 每次渲染都会重建
```

---

## 3. 性能反模式 (Anti-Patterns)

### 3.1 在 build() 中创建复杂对象

```typescript
// ❌ 反模式：build() 中创建对象
@Component
struct BadComponent {
  @State items: string[] = []

  build() {
    Column() {
      // 每次渲染都会创建新对象
      ForEach(this.items.filter(i => i.length > 0).map(i => ({
        value: i,
        display: i.toUpperCase()
      })), (item) => {
        Text(item.display)
      })
    }
  }
}

// ✅ 正确：使用 getter 预计算
@Component
struct GoodComponent {
  @State items: string[] = []

  // 使用 getter 缓存计算结果
  get processedItems(): Array<{ value: string; display: string }> {
    return this.items
      .filter(i => i.length > 0)
      .map(i => ({ value: i, display: i.toUpperCase() }))
  }

  build() {
    Column() {
      ForEach(this.processedItems, (item) => {
        Text(item.display)
      }, (item) => item.value)
    }
  }
}
```

### 3.2 在 build() 中进行异步操作

```typescript
// ❌ 反模式：build() 中进行异步操作
build() {
  Column() {
    Button('加载')
      .onClick(async () => {
        const data = await fetchData()  // 异步操作阻塞渲染
        this.items = data
      })
  }
}

// ✅ 正确：异步操作放在生命周期或单独方法
aboutToAppear() {
  this.loadData()
}

private async loadData() {
  this.isLoading = true
  try {
    this.items = await fetchData()
  } finally {
    this.isLoading = false
  }
}

build() {
  Column() {
    if (this.isLoading) {
      LoadingProgress()
    } else {
      ForEach(this.items, ...)
    }
  }
}
```

### 3.3 过度使用 @State 导致不必要的重渲染

```typescript
// ❌ 反模式：所有状态放在同一层级
@Entry
@Component
struct BadPage {
  @State userName: string = ''
  @State userAvatar: string = ''
  @State cartCount: number = 0      // 频繁更新
  @State scrollPosition: number = 0  // 频繁更新
  @State products: Product[] = []

  build() {
    Column() {
      // 任何一个 @State 变化都会导致整个页面重渲染
      Header({ name: this.userName, avatar: this.userAvatar })
      CartBadge({ count: this.cartCount })
      ProductList({ items: this.products })
    }
  }
}

// ✅ 正确：状态下沉到子组件
@Entry
@Component
struct GoodPage {
  @State userName: string = ''
  @State userAvatar: string = ''
  @State products: Product[] = []

  build() {
    Column() {
      Header({ name: this.userName, avatar: this.userAvatar })
      CartBadgeWrapper()  // 内部管理自己的状态
      ProductList({ items: this.products })
    }
  }
}

@Component
struct CartBadgeWrapper {
  @State cartCount: number = 0  // 状态隔离，只影响此组件

  build() {
    Badge({ count: this.cartCount }) {
      SymbolGlyph($r('sys.symbol.cart'))
    }
  }
}
```

### 3.4 在循环中使用条件渲染

```typescript
// ❌ 反模式：循环中频繁条件判断
ForEach(this.items, (item: Item) => {
  if (item.type === 'A') {
    TypeAComponent({ item: item })
  } else if (item.type === 'B') {
    TypeBComponent({ item: item })
  } else {
    DefaultComponent({ item: item })
  }
})

// ✅ 正确：使用 @Builder 工厂方法
@Builder
itemBuilder(item: Item) {
  if (item.type === 'A') {
    TypeAComponent({ item: item })
  } else if (item.type === 'B') {
    TypeBComponent({ item: item })
  } else {
    DefaultComponent({ item: item })
  }
}

build() {
  List() {
    ForEach(this.items, (item: Item) => {
      ListItem() {
        this.itemBuilder(item)
      }
    }, (item) => item.id)
  }
}
```

---

## 4. 性能检查清单

### 渲染性能

- [ ] build() 嵌套层级 ≤ 5
- [ ] 无在 build() 中创建复杂对象
- [ ] 大列表 (>50) 使用 LazyForEach
- [ ] LazyForEach 有正确的 keyGenerator
- [ ] 频繁更新的状态已拆分到子组件

### 内存管理

- [ ] 图片资源使用适当尺寸
- [ ] 列表设置了 cachedCount
- [ ] 页面销毁时清理定时器/监听器

### 加载优化

- [ ] 首屏内容优先加载
- [ ] 图片使用懒加载
- [ ] 大数据分页加载

---

## 5. 性能监控代码

```typescript
/**
 * 性能监控工具
 */
class PerformanceMonitor {
  private static startTime: number = 0

  // 标记开始
  static start(tag: string) {
    this.startTime = Date.now()
    console.info(`[PERF] ${tag} - Start`)
  }

  // 标记结束
  static end(tag: string) {
    const duration = Date.now() - this.startTime
    console.info(`[PERF] ${tag} - End: ${duration}ms`)
    
    // 超过阈值告警
    if (duration > 16) {  // 超过一帧 (60fps = 16.67ms)
      console.warn(`[PERF WARNING] ${tag} took ${duration}ms, may cause frame drop`)
    }
  }
}

// 使用示例
aboutToAppear() {
  PerformanceMonitor.start('DataLoad')
  this.loadData().then(() => {
    PerformanceMonitor.end('DataLoad')
  })
}
```
