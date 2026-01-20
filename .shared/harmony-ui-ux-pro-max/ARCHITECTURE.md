# HarmonyOS NEXT 架构规范

## 概述

本文档定义了 HarmonyOS NEXT 应用的标准架构模式，基于 **MVVM (Model-View-ViewModel)** 设计模式，实现业务逻辑与 UI 的完全分离。

---

## MVVM 架构原则

### 核心理念

```
┌─────────────────────────────────────────────────────────────┐
│                        MVVM 架构                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────┐      数据绑定      ┌──────────────┐           │
│   │  View   │ ◄──────────────► │  ViewModel   │           │
│   │ (ArkUI) │      @State       │  (业务逻辑)   │           │
│   └─────────┘                   └──────┬───────┘           │
│       │                                │                   │
│       │ 用户交互                         │ 数据操作          │
│       ▼                                ▼                   │
│   ┌─────────────────────────────────────────────────┐     │
│   │                    Model                         │     │
│   │              (数据模型 / 服务层)                   │     │
│   └─────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 职责划分

| 层级 | 职责 | 位置 |
|------|------|------|
| **View** | UI 渲染、用户交互响应 | `src/main/ets/pages/*.ets` |
| **ViewModel** | 业务逻辑、状态管理、数据转换 | `src/main/ets/viewmodel/*.ets` |
| **Model** | 数据结构定义、数据持久化 | `src/main/ets/model/*.ets` |

---

## 目录结构标准

```
entry/src/main/ets/
├── entryability/
│   └── EntryAbility.ets          # 应用入口
├── pages/
│   ├── Index.ets                 # 主入口页面
│   └── [Feature]Page.ets         # 功能页面 (仅包含 UI)
├── viewmodel/
│   ├── BaseViewModel.ets         # ViewModel 基类
│   └── [Feature]ViewModel.ets    # 功能 ViewModel
├── model/
│   ├── [Entity].ets              # 数据实体
│   └── [Entity]Repository.ets    # 数据仓库
├── components/
│   └── [Component].ets           # 可复用组件
├── services/
│   └── [Service].ets             # 服务层 (API调用等)
└── utils/
    └── [Utility].ets             # 工具函数
```

---

## ViewModel 基类模板

```typescript
// viewmodel/BaseViewModel.ets

/**
 * ViewModel 基类
 * 提供通用的状态管理和生命周期钩子
 */
@ObservedV2
export class BaseViewModel {
  /** 加载状态 */
  @Trace isLoading: boolean = false

  /** 错误信息 */
  @Trace errorMessage: string = ''

  /** 是否有错误 */
  @Trace hasError: boolean = false

  /**
   * 初始化 ViewModel
   * 子类可重写此方法进行初始化操作
   */
  async onInit(): Promise<void> {
    // 子类实现
  }

  /**
   * 清理资源
   * 在组件销毁时调用
   */
  onDestroy(): void {
    // 子类实现
  }

  /**
   * 设置加载状态
   */
  protected setLoading(loading: boolean): void {
    this.isLoading = loading
  }

  /**
   * 设置错误信息
   */
  protected setError(message: string): void {
    this.errorMessage = message
    this.hasError = message.length > 0
  }

  /**
   * 清除错误
   */
  protected clearError(): void {
    this.errorMessage = ''
    this.hasError = false
  }

  /**
   * 执行异步操作的包装器
   * 自动处理加载状态和错误
   */
  protected async executeAsync<T>(
    operation: () => Promise<T>,
    onSuccess?: (result: T) => void,
    onError?: (error: Error) => void
  ): Promise<T | undefined> {
    this.setLoading(true)
    this.clearError()

    try {
      const result = await operation()
      if (onSuccess) {
        onSuccess(result)
      }
      return result
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '操作失败'
      this.setError(errorMessage)
      if (onError) {
        onError(error as Error)
      }
      return undefined
    } finally {
      this.setLoading(false)
    }
  }
}
```

---

## ViewModel + View 协作模板

### 1. Model 定义

```typescript
// model/Product.ets

/**
 * 商品数据模型
 */
export interface Product {
  id: string
  name: string
  price: number
  imageUrl: string
  description: string
  stock: number
  category: string
}

/**
 * 商品列表响应
 */
export interface ProductListResponse {
  items: Product[]
  total: number
  pageIndex: number
  pageSize: number
}
```

### 2. ViewModel 实现

```typescript
// viewmodel/ProductListViewModel.ets

import { BaseViewModel } from './BaseViewModel'
import type { Product, ProductListResponse } from '../model/Product'

/**
 * 商品列表 ViewModel
 * 
 * 职责:
 * - 管理商品列表状态
 * - 处理分页加载
 * - 提供搜索和筛选功能
 */
@ObservedV2
export class ProductListViewModel extends BaseViewModel {
  /** 商品列表 */
  @Trace products: Product[] = []

  /** 当前页码 */
  @Trace currentPage: number = 1

  /** 是否还有更多数据 */
  @Trace hasMore: boolean = true

  /** 搜索关键词 */
  @Trace searchKeyword: string = ''

  /** 选中的分类 */
  @Trace selectedCategory: string = ''

  /** 每页数量 */
  private readonly pageSize: number = 20

  /**
   * 初始化 - 加载首页数据
   */
  override async onInit(): Promise<void> {
    await this.loadProducts(true)
  }

  /**
   * 加载商品列表
   * @param refresh 是否刷新(重置分页)
   */
  async loadProducts(refresh: boolean = false): Promise<void> {
    if (refresh) {
      this.currentPage = 1
      this.hasMore = true
    }

    if (!this.hasMore && !refresh) {
      return
    }

    await this.executeAsync<ProductListResponse>(
      async () => {
        // 模拟 API 调用
        return await this.fetchProducts()
      },
      (response) => {
        if (refresh) {
          this.products = response.items
        } else {
          this.products = [...this.products, ...response.items]
        }
        this.hasMore = this.products.length < response.total
        this.currentPage++
      }
    )
  }

  /**
   * 搜索商品
   */
  async search(keyword: string): Promise<void> {
    this.searchKeyword = keyword
    await this.loadProducts(true)
  }

  /**
   * 筛选分类
   */
  async filterByCategory(category: string): Promise<void> {
    this.selectedCategory = category
    await this.loadProducts(true)
  }

  /**
   * 加载更多
   */
  async loadMore(): Promise<void> {
    await this.loadProducts(false)
  }

  /**
   * 刷新数据
   */
  async refresh(): Promise<void> {
    await this.loadProducts(true)
  }

  /**
   * 获取筛选后的商品数量
   */
  get filteredCount(): number {
    return this.products.length
  }

  /**
   * 模拟 API 获取商品
   */
  private async fetchProducts(): Promise<ProductListResponse> {
    // 实际项目中替换为真实 API 调用
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          items: this.generateMockProducts(),
          total: 100,
          pageIndex: this.currentPage,
          pageSize: this.pageSize
        })
      }, 500)
    })
  }

  /**
   * 生成模拟数据
   */
  private generateMockProducts(): Product[] {
    const products: Product[] = []
    const startIndex = (this.currentPage - 1) * this.pageSize
    for (let i = 0; i < this.pageSize; i++) {
      products.push({
        id: `product_${startIndex + i}`,
        name: `商品 ${startIndex + i + 1}`,
        price: Math.floor(Math.random() * 1000) + 100,
        imageUrl: '',
        description: '商品描述',
        stock: Math.floor(Math.random() * 100),
        category: ['电子产品', '服饰', '食品'][i % 3]
      })
    }
    return products
  }
}
```

### 3. View 实现

```typescript
// pages/ProductListPage.ets

import { ProductListViewModel } from '../viewmodel/ProductListViewModel'
import type { Product } from '../model/Product'

/**
 * 商品列表页面
 * 
 * 职责:
 * - 纯 UI 渲染
 * - 用户交互事件触发
 * - 不包含业务逻辑
 */
@Entry
@Component
struct ProductListPage {
  /** ViewModel 实例 */
  @State viewModel: ProductListViewModel = new ProductListViewModel()
  /** 下拉刷新状态 */
  @State isRefreshing: boolean = false

  aboutToAppear(): void {
    this.viewModel.onInit()
  }

  aboutToDisappear(): void {
    this.viewModel.onDestroy()
  }

  build() {
    Column() {
      // 顶部搜索栏
      this.buildSearchBar()

      // 内容区域
      if (this.viewModel.isLoading && this.viewModel.products.length === 0) {
        this.buildLoadingState()
      } else if (this.viewModel.hasError) {
        this.buildErrorState()
      } else if (this.viewModel.products.length === 0) {
        this.buildEmptyState()
      } else {
        this.buildProductList()
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor($r('app.color.bg_secondary'))
  }

  @Builder
  buildSearchBar() {
    Row() {
      Search({ placeholder: $r('app.string.search') })
        .width('100%')
        .height(40)
        .onSubmit((value: string) => {
          this.viewModel.search(value)
        })
    }
    .padding($r('app.float.spacing_lg'))
    .backgroundColor($r('app.color.bg_primary'))
  }

  @Builder
  buildProductList() {
    Refresh({ refreshing: $$this.isRefreshing }) {
      List() {
        LazyForEach(
          new ProductDataSource(this.viewModel.products),
          (item: Product) => {
            ListItem() {
              this.buildProductCard(item)
            }
          },
          (item: Product) => item.id
        )

        // 加载更多指示器
        if (this.viewModel.hasMore) {
          ListItem() {
            this.buildLoadMoreIndicator()
          }
        }
      }
      .width('100%')
      .layoutWeight(1)
      .padding($r('app.float.spacing_md'))
      .onReachEnd(() => {
        this.viewModel.loadMore()
      })
    }
    .onRefreshing(async () => {
      await this.viewModel.refresh()
      this.isRefreshing = false
    })
  }

  @Builder
  buildProductCard(product: Product) {
    Row() {
      // 商品图片
      Column() {
        if (product.imageUrl) {
          Image(product.imageUrl)
            .width(80)
            .height(80)
            .borderRadius($r('app.float.radius_sm'))
            .objectFit(ImageFit.Cover)
        } else {
          Column() {
            SymbolGlyph($r('sys.symbol.photo'))
              .fontSize(32)
              .fontColor([$r('app.color.icon_secondary')])
          }
          .width(80)
          .height(80)
          .borderRadius($r('app.float.radius_sm'))
          .backgroundColor($r('app.color.bg_tertiary'))
          .justifyContent(FlexAlign.Center)
        }
      }
      .accessibilityText(`商品图片: ${product.name}`)

      // 商品信息
      Column() {
        Text(product.name)
          .fontSize($r('app.float.font_size_lg'))
          .fontColor($r('app.color.text_primary'))
          .fontWeight(FontWeight.Medium)
          .maxLines(2)
          .textOverflow({ overflow: TextOverflow.Ellipsis })

        Text(product.description)
          .fontSize($r('app.float.font_size_sm'))
          .fontColor($r('app.color.text_secondary'))
          .maxLines(1)
          .margin({ top: 4 })

        Row() {
          Text(`¥${product.price}`)
            .fontSize($r('app.float.font_size_xl'))
            .fontColor($r('app.color.error'))
            .fontWeight(FontWeight.Bold)

          Blank()

          Text(`库存: ${product.stock}`)
            .fontSize($r('app.float.font_size_xs'))
            .fontColor($r('app.color.text_tertiary'))
        }
        .width('100%')
        .margin({ top: 8 })
      }
      .layoutWeight(1)
      .alignItems(HorizontalAlign.Start)
      .margin({ left: 12 })
    }
    .width('100%')
    .padding(12)
    .backgroundColor($r('app.color.bg_primary'))
    .borderRadius($r('app.float.radius_md'))
    .margin({ bottom: 8 })
  }

  @Builder
  buildLoadingState() {
    Column() {
      LoadingProgress()
        .width(48)
        .height(48)
        .color($r('app.color.primary'))
      Text($r('app.string.loading'))
        .fontSize($r('app.float.font_size_md'))
        .fontColor($r('app.color.text_secondary'))
        .margin({ top: 16 })
    }
    .width('100%')
    .layoutWeight(1)
    .justifyContent(FlexAlign.Center)
  }

  @Builder
  buildErrorState() {
    Column() {
      SymbolGlyph($r('sys.symbol.exclamationmark_triangle'))
        .fontSize(48)
        .fontColor([$r('app.color.error')])
      Text(this.viewModel.errorMessage)
        .fontSize($r('app.float.font_size_md'))
        .fontColor($r('app.color.text_secondary'))
        .margin({ top: 16 })
      Button($r('app.string.retry'))
        .onClick(() => this.viewModel.refresh())
        .margin({ top: 24 })
        .accessibilityText('重试加载')
    }
    .width('100%')
    .layoutWeight(1)
    .justifyContent(FlexAlign.Center)
  }

  @Builder
  buildEmptyState() {
    Column() {
      SymbolGlyph($r('sys.symbol.tray'))
        .fontSize(48)
        .fontColor([$r('app.color.icon_secondary')])
      Text($r('app.string.no_data'))
        .fontSize($r('app.float.font_size_md'))
        .fontColor($r('app.color.text_secondary'))
        .margin({ top: 16 })
    }
    .width('100%')
    .layoutWeight(1)
    .justifyContent(FlexAlign.Center)
  }

  @Builder
  buildLoadMoreIndicator() {
    Row() {
      LoadingProgress()
        .width(24)
        .height(24)
        .color($r('app.color.primary'))
      Text('加载更多...')
        .fontSize($r('app.float.font_size_sm'))
        .fontColor($r('app.color.text_secondary'))
        .margin({ left: 8 })
    }
    .width('100%')
    .height(48)
    .justifyContent(FlexAlign.Center)
  }
}

/**
 * LazyForEach 数据源
 */
class ProductDataSource implements IDataSource {
  private products: Product[]

  constructor(products: Product[]) {
    this.products = products
  }

  totalCount(): number {
    return this.products.length
  }

  getData(index: number): Product {
    return this.products[index]
  }

  registerDataChangeListener(listener: DataChangeListener): void {}

  unregisterDataChangeListener(listener: DataChangeListener): void {}
}
```

---

## MVVM 最佳实践

### 1. ViewModel 设计原则

| 原则 | 说明 |
|------|------|
| **单一职责** | 每个 ViewModel 只负责一个页面/功能模块 |
| **状态隔离** | 使用 `@ObservedV2` + `@Trace` 实现细粒度更新 |
| **无 UI 依赖** | ViewModel 不应引用任何 UI 组件 |
| **可测试性** | 业务逻辑可独立单元测试 |

### 2. View 设计原则

| 原则 | 说明 |
|------|------|
| **纯渲染** | `build()` 方法只做 UI 渲染，不做逻辑判断 |
| **事件委托** | 用户交互直接委托给 ViewModel 处理 |
| **状态来源单一** | 所有状态从 ViewModel 获取 |
| **组件化** | 复杂 UI 拆分为独立 `@Builder` 或 `@Component` |

### 3. Model 设计原则

| 原则 | 说明 |
|------|------|
| **纯数据** | Model 只定义数据结构，不包含业务逻辑 |
| **类型安全** | 使用 TypeScript interface 定义，禁止 `any` |
| **可序列化** | 支持 JSON 序列化/反序列化 |

---

## 状态管理对照表

### ViewModel 中使用的装饰器

| 场景 | 装饰器 | 示例 |
|------|--------|------|
| 基本类型状态 | `@Trace` | `@Trace count: number = 0` |
| 对象/数组状态 | `@Trace` | `@Trace items: Item[] = []` |
| 类标记 | `@ObservedV2` | `@ObservedV2 class ViewModel {}` |

### View 中使用的装饰器

| 场景 | 装饰器 | 示例 |
|------|--------|------|
| 持有 ViewModel | `@State` | `@State vm: ViewModel = new ViewModel()` |
| 本地 UI 状态 | `@State` | `@State isExpanded: boolean = false` |
| 父子双向绑定 | `@Link` | `@Link selectedId: string` |

---

## 代码审查清单

生成代码时，确保满足以下条件：

- [ ] ViewModel 类使用 `@ObservedV2` 装饰
- [ ] ViewModel 属性使用 `@Trace` 装饰
- [ ] View 的 `build()` 方法不包含业务逻辑
- [ ] 用户交互事件委托给 ViewModel 方法
- [ ] Model 使用 interface 定义，类型完整
- [ ] 所有 Image/Button 组件包含无障碍描述
- [ ] 资源引用使用 `$r()` 而非硬编码
