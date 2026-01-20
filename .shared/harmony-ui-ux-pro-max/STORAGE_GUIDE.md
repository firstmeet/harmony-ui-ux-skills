# HarmonyOS NEXT 数据持久化指南

## 概述

本文档定义了 HarmonyOS NEXT 应用中数据持久化的标准实现方式，包括关系型数据库 (RDB) 和轻量级键值存储 (Preferences)。

---

## 存储方式选择

| 存储方式 | 适用场景 | 数据量 | 查询复杂度 |
|----------|----------|--------|------------|
| **Preferences** | 配置项、用户设置、简单状态 | 小 (< 1MB) | 简单键值 |
| **RDB** | 结构化数据、列表数据、复杂查询 | 中大 | SQL 查询 |
| **分布式数据对象** | 跨设备实时同步 | 小 | 简单对象 |

---

## 1. Preferences (轻量级存储)

### 触发场景
- 用户设置 (主题、语言、通知开关)
- 登录状态、Token 存储
- 简单的应用配置
- 首次启动标记

### 工具类封装

```typescript
// utils/PreferencesUtil.ets

import { preferences } from '@kit.ArkData'
import { common } from '@kit.AbilityKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { BusinessError } from '@kit.BasicServicesKit'

/**
 * Preferences 工具类
 * 封装轻量级键值存储的常用操作
 */
export class PreferencesUtil {
  private static readonly TAG = 'PreferencesUtil'
  private static readonly DOMAIN = 0x0000
  private static readonly STORE_NAME = 'app_preferences'

  private static preferencesInstance: preferences.Preferences | null = null

  /**
   * 初始化 Preferences
   * 应在 EntryAbility.onCreate 中调用
   */
  static async init(context: common.Context): Promise<void> {
    try {
      PreferencesUtil.preferencesInstance = await preferences.getPreferences(
        context,
        PreferencesUtil.STORE_NAME
      )
      hilog.info(PreferencesUtil.DOMAIN, PreferencesUtil.TAG, 'Preferences initialized')
    } catch (error) {
      const err = error as BusinessError
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG,
        `Init failed: ${err.code} - ${err.message}`)
    }
  }

  /**
   * 获取 Preferences 实例
   */
  private static getPreferences(): preferences.Preferences {
    if (!PreferencesUtil.preferencesInstance) {
      throw new Error('Preferences not initialized. Call init() first.')
    }
    return PreferencesUtil.preferencesInstance
  }

  // ============================================================
  // 字符串操作
  // ============================================================

  /**
   * 存储字符串
   */
  static async putString(key: string, value: string): Promise<void> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      await prefs.put(key, value)
      await prefs.flush()
    } catch (error) {
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG,
        `Put string failed: ${error}`)
    }
  }

  /**
   * 获取字符串
   */
  static async getString(key: string, defaultValue: string = ''): Promise<string> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      const value = await prefs.get(key, defaultValue)
      return value as string
    } catch (error) {
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG,
        `Get string failed: ${error}`)
      return defaultValue
    }
  }

  // ============================================================
  // 数值操作
  // ============================================================

  /**
   * 存储数值
   */
  static async putNumber(key: string, value: number): Promise<void> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      await prefs.put(key, value)
      await prefs.flush()
    } catch (error) {
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG,
        `Put number failed: ${error}`)
    }
  }

  /**
   * 获取数值
   */
  static async getNumber(key: string, defaultValue: number = 0): Promise<number> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      const value = await prefs.get(key, defaultValue)
      return value as number
    } catch (error) {
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG,
        `Get number failed: ${error}`)
      return defaultValue
    }
  }

  // ============================================================
  // 布尔值操作
  // ============================================================

  /**
   * 存储布尔值
   */
  static async putBoolean(key: string, value: boolean): Promise<void> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      await prefs.put(key, value)
      await prefs.flush()
    } catch (error) {
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG,
        `Put boolean failed: ${error}`)
    }
  }

  /**
   * 获取布尔值
   */
  static async getBoolean(key: string, defaultValue: boolean = false): Promise<boolean> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      const value = await prefs.get(key, defaultValue)
      return value as boolean
    } catch (error) {
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG,
        `Get boolean failed: ${error}`)
      return defaultValue
    }
  }

  // ============================================================
  // 对象操作 (JSON 序列化)
  // ============================================================

  /**
   * 存储对象 (自动 JSON 序列化)
   */
  static async putObject<T>(key: string, value: T): Promise<void> {
    try {
      const jsonString = JSON.stringify(value)
      await PreferencesUtil.putString(key, jsonString)
    } catch (error) {
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG,
        `Put object failed: ${error}`)
    }
  }

  /**
   * 获取对象 (自动 JSON 反序列化)
   */
  static async getObject<T>(key: string, defaultValue: T): Promise<T> {
    try {
      const jsonString = await PreferencesUtil.getString(key, '')
      if (jsonString) {
        return JSON.parse(jsonString) as T
      }
      return defaultValue
    } catch (error) {
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG,
        `Get object failed: ${error}`)
      return defaultValue
    }
  }

  // ============================================================
  // 通用操作
  // ============================================================

  /**
   * 检查 key 是否存在
   */
  static async has(key: string): Promise<boolean> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      return await prefs.has(key)
    } catch (error) {
      return false
    }
  }

  /**
   * 删除指定 key
   */
  static async delete(key: string): Promise<void> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      await prefs.delete(key)
      await prefs.flush()
    } catch (error) {
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG,
        `Delete failed: ${error}`)
    }
  }

  /**
   * 清空所有数据
   */
  static async clear(): Promise<void> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      await prefs.clear()
      await prefs.flush()
    } catch (error) {
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG,
        `Clear failed: ${error}`)
    }
  }
}

// ============================================================
// 预定义 Key 常量 (推荐使用)
// ============================================================

export class PreferencesKeys {
  // 用户相关
  static readonly IS_LOGGED_IN = 'is_logged_in'
  static readonly USER_TOKEN = 'user_token'
  static readonly USER_INFO = 'user_info'

  // 应用设置
  static readonly THEME_MODE = 'theme_mode'
  static readonly LANGUAGE = 'language'
  static readonly NOTIFICATION_ENABLED = 'notification_enabled'

  // 应用状态
  static readonly IS_FIRST_LAUNCH = 'is_first_launch'
  static readonly LAST_SYNC_TIME = 'last_sync_time'
}
```

### 使用示例

```typescript
// entryability/EntryAbility.ets
import { PreferencesUtil } from '../utils/PreferencesUtil'

export default class EntryAbility extends UIAbility {
  async onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): Promise<void> {
    // 初始化 Preferences
    await PreferencesUtil.init(this.context)
  }
}

// 在业务代码中使用
import { PreferencesUtil, PreferencesKeys } from '../utils/PreferencesUtil'

// 存储用户 Token
await PreferencesUtil.putString(PreferencesKeys.USER_TOKEN, 'xxx-token-xxx')

// 读取用户 Token
const token = await PreferencesUtil.getString(PreferencesKeys.USER_TOKEN)

// 存储对象
const userInfo = { id: '1', name: '张三' }
await PreferencesUtil.putObject(PreferencesKeys.USER_INFO, userInfo)

// 读取对象
const user = await PreferencesUtil.getObject<UserInfo>(PreferencesKeys.USER_INFO, { id: '', name: '' })
```

---

## 2. RDB (关系型数据库)

### 触发场景
- 列表数据本地缓存
- 复杂的数据关系
- 需要 SQL 查询的场景
- 离线优先的数据存储

### 数据库管理器封装

```typescript
// database/DatabaseHelper.ets

import { relationalStore } from '@kit.ArkData'
import { common } from '@kit.AbilityKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { BusinessError } from '@kit.BasicServicesKit'

/**
 * 数据库配置
 */
const DB_CONFIG: relationalStore.StoreConfig = {
  name: 'app_database.db',
  securityLevel: relationalStore.SecurityLevel.S1,
  encrypt: false
}

/**
 * 数据库版本
 */
const DB_VERSION = 1

/**
 * 建表 SQL
 */
const CREATE_TABLES: string[] = [
  `CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    image_url TEXT,
    category TEXT,
    stock INTEGER DEFAULT 0,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
  )`,
  `CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT NOT NULL UNIQUE,
    user_id TEXT NOT NULL,
    total_amount REAL NOT NULL,
    status TEXT NOT NULL,
    created_at INTEGER NOT NULL
  )`,
  `CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)`,
  `CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id)`
]

/**
 * 数据库管理器
 * 单例模式，管理数据库连接和版本升级
 */
export class DatabaseHelper {
  private static readonly TAG = 'DatabaseHelper'
  private static readonly DOMAIN = 0x0000

  private static instance: DatabaseHelper | null = null
  private rdbStore: relationalStore.RdbStore | null = null

  private constructor() {}

  /**
   * 获取单例实例
   */
  static getInstance(): DatabaseHelper {
    if (!DatabaseHelper.instance) {
      DatabaseHelper.instance = new DatabaseHelper()
    }
    return DatabaseHelper.instance
  }

  /**
   * 初始化数据库
   * 应在 EntryAbility.onCreate 中调用
   */
  async init(context: common.Context): Promise<void> {
    try {
      this.rdbStore = await relationalStore.getRdbStore(context, DB_CONFIG)
      hilog.info(DatabaseHelper.DOMAIN, DatabaseHelper.TAG, 'Database initialized')

      // 执行建表语句
      await this.createTables()

    } catch (error) {
      const err = error as BusinessError
      hilog.error(DatabaseHelper.DOMAIN, DatabaseHelper.TAG,
        `Init failed: ${err.code} - ${err.message}`)
      throw error
    }
  }

  /**
   * 创建表
   */
  private async createTables(): Promise<void> {
    if (!this.rdbStore) return

    for (const sql of CREATE_TABLES) {
      try {
        await this.rdbStore.executeSql(sql)
      } catch (error) {
        hilog.error(DatabaseHelper.DOMAIN, DatabaseHelper.TAG,
          `Create table failed: ${error}`)
      }
    }
  }

  /**
   * 获取数据库实例
   */
  getStore(): relationalStore.RdbStore {
    if (!this.rdbStore) {
      throw new Error('Database not initialized. Call init() first.')
    }
    return this.rdbStore
  }

  /**
   * 关闭数据库
   */
  async close(): Promise<void> {
    if (this.rdbStore) {
      this.rdbStore = null
    }
  }
}
```

### 数据访问对象 (DAO) 模板

```typescript
// database/ProductDao.ets

import { relationalStore } from '@kit.ArkData'
import { DatabaseHelper } from './DatabaseHelper'
import { hilog } from '@kit.PerformanceAnalysisKit'

/**
 * 商品数据模型
 */
export interface Product {
  id?: number
  productId: string
  name: string
  price: number
  description?: string
  imageUrl?: string
  category?: string
  stock: number
  createdAt: number
  updatedAt: number
}

/**
 * 商品数据访问对象
 * 封装商品表的增删改查操作
 */
export class ProductDao {
  private static readonly TAG = 'ProductDao'
  private static readonly DOMAIN = 0x0000
  private static readonly TABLE_NAME = 'products'

  /**
   * 获取数据库实例
   */
  private getStore(): relationalStore.RdbStore {
    return DatabaseHelper.getInstance().getStore()
  }

  // ============================================================
  // 插入操作
  // ============================================================

  /**
   * 插入单条记录
   */
  async insert(product: Product): Promise<number> {
    try {
      const store = this.getStore()
      const valueBucket: relationalStore.ValuesBucket = {
        'product_id': product.productId,
        'name': product.name,
        'price': product.price,
        'description': product.description || '',
        'image_url': product.imageUrl || '',
        'category': product.category || '',
        'stock': product.stock,
        'created_at': product.createdAt,
        'updated_at': product.updatedAt
      }

      const rowId = await store.insert(ProductDao.TABLE_NAME, valueBucket)
      hilog.info(ProductDao.DOMAIN, ProductDao.TAG, `Inserted row: ${rowId}`)
      return rowId

    } catch (error) {
      hilog.error(ProductDao.DOMAIN, ProductDao.TAG, `Insert failed: ${error}`)
      throw error
    }
  }

  /**
   * 批量插入 (事务)
   */
  async insertBatch(products: Product[]): Promise<void> {
    const store = this.getStore()

    try {
      await store.beginTransaction()

      for (const product of products) {
        const valueBucket: relationalStore.ValuesBucket = {
          'product_id': product.productId,
          'name': product.name,
          'price': product.price,
          'description': product.description || '',
          'image_url': product.imageUrl || '',
          'category': product.category || '',
          'stock': product.stock,
          'created_at': product.createdAt,
          'updated_at': product.updatedAt
        }
        await store.insert(ProductDao.TABLE_NAME, valueBucket)
      }

      await store.commit()
      hilog.info(ProductDao.DOMAIN, ProductDao.TAG, `Batch inserted: ${products.length}`)

    } catch (error) {
      await store.rollBack()
      hilog.error(ProductDao.DOMAIN, ProductDao.TAG, `Batch insert failed: ${error}`)
      throw error
    }
  }

  // ============================================================
  // 查询操作
  // ============================================================

  /**
   * 查询所有记录
   */
  async queryAll(): Promise<Product[]> {
    try {
      const store = this.getStore()
      const predicates = new relationalStore.RdbPredicates(ProductDao.TABLE_NAME)
      predicates.orderByDesc('created_at')

      const resultSet = await store.query(predicates)
      return this.parseResultSet(resultSet)

    } catch (error) {
      hilog.error(ProductDao.DOMAIN, ProductDao.TAG, `Query all failed: ${error}`)
      return []
    }
  }

  /**
   * 根据 ID 查询
   */
  async queryById(productId: string): Promise<Product | null> {
    try {
      const store = this.getStore()
      const predicates = new relationalStore.RdbPredicates(ProductDao.TABLE_NAME)
      predicates.equalTo('product_id', productId)

      const resultSet = await store.query(predicates)
      const products = this.parseResultSet(resultSet)
      return products.length > 0 ? products[0] : null

    } catch (error) {
      hilog.error(ProductDao.DOMAIN, ProductDao.TAG, `Query by id failed: ${error}`)
      return null
    }
  }

  /**
   * 分页查询
   */
  async queryPage(pageIndex: number, pageSize: number): Promise<Product[]> {
    try {
      const store = this.getStore()
      const predicates = new relationalStore.RdbPredicates(ProductDao.TABLE_NAME)
      predicates
        .orderByDesc('created_at')
        .limitAs(pageSize)
        .offsetAs((pageIndex - 1) * pageSize)

      const resultSet = await store.query(predicates)
      return this.parseResultSet(resultSet)

    } catch (error) {
      hilog.error(ProductDao.DOMAIN, ProductDao.TAG, `Query page failed: ${error}`)
      return []
    }
  }

  /**
   * 按分类查询
   */
  async queryByCategory(category: string): Promise<Product[]> {
    try {
      const store = this.getStore()
      const predicates = new relationalStore.RdbPredicates(ProductDao.TABLE_NAME)
      predicates
        .equalTo('category', category)
        .orderByDesc('created_at')

      const resultSet = await store.query(predicates)
      return this.parseResultSet(resultSet)

    } catch (error) {
      hilog.error(ProductDao.DOMAIN, ProductDao.TAG, `Query by category failed: ${error}`)
      return []
    }
  }

  /**
   * 模糊搜索
   */
  async search(keyword: string): Promise<Product[]> {
    try {
      const store = this.getStore()
      const predicates = new relationalStore.RdbPredicates(ProductDao.TABLE_NAME)
      predicates
        .like('name', `%${keyword}%`)
        .orderByDesc('created_at')

      const resultSet = await store.query(predicates)
      return this.parseResultSet(resultSet)

    } catch (error) {
      hilog.error(ProductDao.DOMAIN, ProductDao.TAG, `Search failed: ${error}`)
      return []
    }
  }

  /**
   * 查询记录数
   */
  async count(): Promise<number> {
    try {
      const store = this.getStore()
      const predicates = new relationalStore.RdbPredicates(ProductDao.TABLE_NAME)
      const resultSet = await store.query(predicates)
      const count = resultSet.rowCount
      resultSet.close()
      return count

    } catch (error) {
      hilog.error(ProductDao.DOMAIN, ProductDao.TAG, `Count failed: ${error}`)
      return 0
    }
  }

  // ============================================================
  // 更新操作
  // ============================================================

  /**
   * 更新记录
   */
  async update(product: Product): Promise<number> {
    try {
      const store = this.getStore()
      const predicates = new relationalStore.RdbPredicates(ProductDao.TABLE_NAME)
      predicates.equalTo('product_id', product.productId)

      const valueBucket: relationalStore.ValuesBucket = {
        'name': product.name,
        'price': product.price,
        'description': product.description || '',
        'image_url': product.imageUrl || '',
        'category': product.category || '',
        'stock': product.stock,
        'updated_at': Date.now()
      }

      const affectedRows = await store.update(valueBucket, predicates)
      hilog.info(ProductDao.DOMAIN, ProductDao.TAG, `Updated rows: ${affectedRows}`)
      return affectedRows

    } catch (error) {
      hilog.error(ProductDao.DOMAIN, ProductDao.TAG, `Update failed: ${error}`)
      throw error
    }
  }

  // ============================================================
  // 删除操作
  // ============================================================

  /**
   * 删除单条记录
   */
  async delete(productId: string): Promise<number> {
    try {
      const store = this.getStore()
      const predicates = new relationalStore.RdbPredicates(ProductDao.TABLE_NAME)
      predicates.equalTo('product_id', productId)

      const affectedRows = await store.delete(predicates)
      hilog.info(ProductDao.DOMAIN, ProductDao.TAG, `Deleted rows: ${affectedRows}`)
      return affectedRows

    } catch (error) {
      hilog.error(ProductDao.DOMAIN, ProductDao.TAG, `Delete failed: ${error}`)
      throw error
    }
  }

  /**
   * 删除所有记录
   */
  async deleteAll(): Promise<number> {
    try {
      const store = this.getStore()
      const predicates = new relationalStore.RdbPredicates(ProductDao.TABLE_NAME)
      predicates.isNotNull('id')

      const affectedRows = await store.delete(predicates)
      hilog.info(ProductDao.DOMAIN, ProductDao.TAG, `Deleted all: ${affectedRows}`)
      return affectedRows

    } catch (error) {
      hilog.error(ProductDao.DOMAIN, ProductDao.TAG, `Delete all failed: ${error}`)
      throw error
    }
  }

  // ============================================================
  // 辅助方法
  // ============================================================

  /**
   * 解析结果集
   */
  private parseResultSet(resultSet: relationalStore.ResultSet): Product[] {
    const products: Product[] = []

    try {
      while (resultSet.goToNextRow()) {
        const product: Product = {
          id: resultSet.getLong(resultSet.getColumnIndex('id')),
          productId: resultSet.getString(resultSet.getColumnIndex('product_id')),
          name: resultSet.getString(resultSet.getColumnIndex('name')),
          price: resultSet.getDouble(resultSet.getColumnIndex('price')),
          description: resultSet.getString(resultSet.getColumnIndex('description')),
          imageUrl: resultSet.getString(resultSet.getColumnIndex('image_url')),
          category: resultSet.getString(resultSet.getColumnIndex('category')),
          stock: resultSet.getLong(resultSet.getColumnIndex('stock')),
          createdAt: resultSet.getLong(resultSet.getColumnIndex('created_at')),
          updatedAt: resultSet.getLong(resultSet.getColumnIndex('updated_at'))
        }
        products.push(product)
      }
    } finally {
      resultSet.close()
    }

    return products
  }

  /**
   * 插入或更新 (Upsert)
   */
  async upsert(product: Product): Promise<void> {
    const existing = await this.queryById(product.productId)
    if (existing) {
      await this.update(product)
    } else {
      await this.insert(product)
    }
  }

  /**
   * 批量 Upsert (用于同步)
   */
  async upsertBatch(products: Product[]): Promise<void> {
    const store = this.getStore()

    try {
      await store.beginTransaction()

      for (const product of products) {
        await this.upsert(product)
      }

      await store.commit()

    } catch (error) {
      await store.rollBack()
      throw error
    }
  }
}
```

### Repository 模式 (结合网络请求)

```typescript
// database/ProductRepository.ets

import { ProductDao, Product } from './ProductDao'
import { ProductApi } from '../services/ProductApi'
import { PreferencesUtil, PreferencesKeys } from '../utils/PreferencesUtil'

/**
 * 商品数据仓库
 * 实现 Offline-First 策略：优先读取本地缓存，后台同步远程数据
 */
export class ProductRepository {
  private dao: ProductDao = new ProductDao()
  private readonly CACHE_EXPIRE_TIME = 5 * 60 * 1000  // 5 分钟缓存

  /**
   * 获取商品列表 (Offline-First)
   * 1. 先返回本地缓存
   * 2. 后台请求远程数据
   * 3. 更新本地缓存
   */
  async getProducts(forceRefresh: boolean = false): Promise<Product[]> {
    // 检查缓存是否过期
    const lastSync = await PreferencesUtil.getNumber(PreferencesKeys.LAST_SYNC_TIME, 0)
    const isExpired = Date.now() - lastSync > this.CACHE_EXPIRE_TIME

    // 读取本地缓存
    let localProducts = await this.dao.queryAll()

    // 如果缓存有效且不强制刷新，直接返回
    if (!forceRefresh && !isExpired && localProducts.length > 0) {
      return localProducts
    }

    // 请求远程数据
    try {
      const remoteProducts = await ProductApi.fetchProducts()

      // 更新本地缓存
      await this.dao.upsertBatch(remoteProducts)
      await PreferencesUtil.putNumber(PreferencesKeys.LAST_SYNC_TIME, Date.now())

      return await this.dao.queryAll()

    } catch (error) {
      // 网络失败，返回本地缓存
      return localProducts
    }
  }

  /**
   * 搜索商品 (本地 + 远程)
   */
  async searchProducts(keyword: string): Promise<Product[]> {
    // 先搜索本地
    const localResults = await this.dao.search(keyword)

    // 异步搜索远程 (不阻塞返回)
    ProductApi.searchProducts(keyword).then(async (remoteResults) => {
      await this.dao.upsertBatch(remoteResults)
    }).catch(() => {
      // 忽略远程搜索失败
    })

    return localResults
  }
}
```

---

## 初始化流程

```typescript
// entryability/EntryAbility.ets

import { UIAbility } from '@kit.AbilityKit'
import { PreferencesUtil } from '../utils/PreferencesUtil'
import { DatabaseHelper } from '../database/DatabaseHelper'

export default class EntryAbility extends UIAbility {
  async onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): Promise<void> {
    // 1. 初始化 Preferences
    await PreferencesUtil.init(this.context)

    // 2. 初始化数据库
    await DatabaseHelper.getInstance().init(this.context)

    hilog.info(0x0000, 'EntryAbility', 'Storage initialized')
  }

  onDestroy(): void {
    // 关闭数据库连接
    DatabaseHelper.getInstance().close()
  }
}
```

---

## 最佳实践

### 1. 何时使用 Preferences vs RDB

| 场景 | 推荐方案 |
|------|----------|
| 用户登录状态 | Preferences |
| 应用设置开关 | Preferences |
| 商品列表缓存 | RDB |
| 订单历史记录 | RDB |
| 搜索历史 | RDB (需要模糊查询) 或 Preferences (简单列表) |
| 草稿箱 | RDB |

### 2. 数据库设计原则

- **主键**: 使用自增 ID 作为本地主键，业务 ID 作为唯一索引
- **时间戳**: 必须包含 `created_at` 和 `updated_at` 字段
- **索引**: 为常用查询条件创建索引
- **事务**: 批量操作必须使用事务

### 3. 缓存策略

```typescript
// 缓存策略枚举
enum CacheStrategy {
  CACHE_FIRST,    // 先缓存后网络 (默认)
  NETWORK_FIRST,  // 先网络后缓存
  CACHE_ONLY,     // 仅缓存
  NETWORK_ONLY    // 仅网络
}
```
