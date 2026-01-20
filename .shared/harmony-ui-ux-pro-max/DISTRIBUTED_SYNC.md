# HarmonyOS NEXT 分布式同步指南

## 概述

本文档定义了 HarmonyOS NEXT 应用中分布式数据同步的标准实现方式，包括分布式数据对象 (Distributed Data Object) 和跨设备流转 (Continuity)。

---

## 分布式能力速查表

| 能力 | 适用场景 | 数据规模 | 同步方式 |
|------|----------|----------|----------|
| **分布式数据对象** | 小规模数据实时同步 | < 1KB/对象 | 自动同步 |
| **分布式 KV 存储** | 中等规模键值数据 | < 4MB/entry | 自动同步 |
| **跨设备流转** | 应用状态迁移 | 按需 | 手动触发 |
| **分布式文件** | 大文件传输 | 无限制 | 显式调用 |

---

## 1. 分布式数据对象 (Distributed Data Object)

### 触发场景
- 多设备间实时同步小规模数据
- 协同办公场景 (共享白板、协作编辑)
- 设备间状态同步 (播放进度、阅读位置)
- 多屏互动 (手机操控平板)

### 权限配置

在 `module.json5` 中添加分布式数据同步权限：

```json
{
  "module": {
    "requestPermissions": [
      {
        "name": "ohos.permission.DISTRIBUTED_DATASYNC",
        "reason": "$string:distributed_sync_reason",
        "usedScene": {
          "abilities": ["EntryAbility"],
          "when": "inuse"
        }
      }
    ]
  }
}
```

### 分布式数据对象管理器

```typescript
// services/DistributedDataService.ets

import { distributedDataObject } from '@kit.ArkData'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { BusinessError } from '@kit.BasicServicesKit'

/**
 * 分布式数据对象状态
 */
export enum DistributedObjectStatus {
  ONLINE = 'online',
  OFFLINE = 'offline',
  RESTORED = 'restored'
}

/**
 * 状态变更回调
 */
export type StatusCallback = (sessionId: string, networkId: string, status: DistributedObjectStatus) => void

/**
 * 数据变更回调
 */
export type DataChangeCallback = (sessionId: string, fields: string[]) => void

/**
 * 分布式数据对象管理器
 */
export class DistributedDataManager<T extends object> {
  private static readonly TAG = 'DistributedDataManager'
  private static readonly DOMAIN = 0x0000

  private dataObject: distributedDataObject.DataObject | null = null
  private sessionId: string = ''
  private statusCallback: StatusCallback | null = null
  private dataChangeCallback: DataChangeCallback | null = null

  /**
   * 创建分布式数据对象
   * @param source 初始数据对象
   */
  async create(source: T): Promise<void> {
    try {
      this.dataObject = distributedDataObject.create(getContext(), source)
      hilog.info(DistributedDataManager.DOMAIN, DistributedDataManager.TAG,
        'Distributed object created')
    } catch (error) {
      const err = error as BusinessError
      hilog.error(DistributedDataManager.DOMAIN, DistributedDataManager.TAG,
        `Create failed: ${err.code} - ${err.message}`)
      throw error
    }
  }

  /**
   * 生成会话 ID
   */
  genSessionId(): string {
    this.sessionId = distributedDataObject.genSessionId()
    hilog.info(DistributedDataManager.DOMAIN, DistributedDataManager.TAG,
      `Session ID generated: ${this.sessionId}`)
    return this.sessionId
  }

  /**
   * 设置会话 ID (用于加入已有会话)
   */
  async setSessionId(sessionId: string): Promise<void> {
    if (!this.dataObject) {
      throw new Error('Data object not created')
    }

    try {
      this.sessionId = sessionId
      await this.dataObject.setSessionId(sessionId)
      hilog.info(DistributedDataManager.DOMAIN, DistributedDataManager.TAG,
        `Joined session: ${sessionId}`)
    } catch (error) {
      const err = error as BusinessError
      hilog.error(DistributedDataManager.DOMAIN, DistributedDataManager.TAG,
        `Set session failed: ${err.code} - ${err.message}`)
      throw error
    }
  }

  /**
   * 获取当前会话 ID
   */
  getSessionId(): string {
    return this.sessionId
  }

  /**
   * 获取数据对象
   */
  getData(): T | null {
    if (!this.dataObject) return null

    // 获取代理对象的数据
    const keys = Object.keys(this.dataObject)
    const result: Record<string, unknown> = {}
    for (const key of keys) {
      if (key !== '__proxy__' && typeof (this.dataObject as Record<string, unknown>)[key] !== 'function') {
        result[key] = (this.dataObject as Record<string, unknown>)[key]
      }
    }
    return result as T
  }

  /**
   * 更新数据
   */
  update(data: Partial<T>): void {
    if (!this.dataObject) {
      throw new Error('Data object not created')
    }

    // 更新数据对象的属性
    Object.keys(data).forEach(key => {
      (this.dataObject as Record<string, unknown>)[key] = (data as Record<string, unknown>)[key]
    })

    hilog.info(DistributedDataManager.DOMAIN, DistributedDataManager.TAG,
      `Data updated: ${JSON.stringify(data)}`)
  }

  /**
   * 监听状态变更
   */
  onStatusChange(callback: StatusCallback): void {
    if (!this.dataObject) {
      throw new Error('Data object not created')
    }

    this.statusCallback = callback
    this.dataObject.on('status', (sessionId: string, networkId: string, status: string) => {
      hilog.info(DistributedDataManager.DOMAIN, DistributedDataManager.TAG,
        `Status changed: ${status}`)

      const statusEnum = status as DistributedObjectStatus
      if (this.statusCallback) {
        this.statusCallback(sessionId, networkId, statusEnum)
      }
    })
  }

  /**
   * 监听数据变更
   */
  onDataChange(callback: DataChangeCallback): void {
    if (!this.dataObject) {
      throw new Error('Data object not created')
    }

    this.dataChangeCallback = callback
    this.dataObject.on('change', (sessionId: string, fields: string[]) => {
      hilog.info(DistributedDataManager.DOMAIN, DistributedDataManager.TAG,
        `Data changed: ${fields.join(', ')}`)

      if (this.dataChangeCallback) {
        this.dataChangeCallback(sessionId, fields)
      }
    })
  }

  /**
   * 保存数据 (用于流转恢复)
   */
  async save(deviceId: string): Promise<distributedDataObject.SaveSuccessResponse> {
    if (!this.dataObject) {
      throw new Error('Data object not created')
    }

    try {
      const result = await this.dataObject.save(deviceId)
      hilog.info(DistributedDataManager.DOMAIN, DistributedDataManager.TAG,
        `Data saved to device: ${deviceId}`)
      return result
    } catch (error) {
      hilog.error(DistributedDataManager.DOMAIN, DistributedDataManager.TAG,
        `Save failed: ${error}`)
      throw error
    }
  }

  /**
   * 撤销保存
   */
  async revokeSave(): Promise<void> {
    if (!this.dataObject) {
      throw new Error('Data object not created')
    }

    try {
      await this.dataObject.revokeSave()
      hilog.info(DistributedDataManager.DOMAIN, DistributedDataManager.TAG,
        'Save revoked')
    } catch (error) {
      hilog.error(DistributedDataManager.DOMAIN, DistributedDataManager.TAG,
        `Revoke save failed: ${error}`)
      throw error
    }
  }

  /**
   * 销毁数据对象
   */
  destroy(): void {
    if (this.dataObject) {
      // 移除监听
      this.dataObject.off('status')
      this.dataObject.off('change')
      this.dataObject = null
      this.sessionId = ''
      hilog.info(DistributedDataManager.DOMAIN, DistributedDataManager.TAG,
        'Distributed object destroyed')
    }
  }
}
```

### 使用示例：协同白板

```typescript
// 定义共享数据结构
interface WhiteboardData {
  strokes: string      // JSON 序列化的笔画数据
  backgroundColor: string
  lastModifiedBy: string
  lastModifiedTime: number
}

// ViewModel 中使用
@ObservedV2
export class WhiteboardViewModel extends BaseViewModel {
  @Trace strokes: Stroke[] = []
  @Trace backgroundColor: string = '#FFFFFF'
  @Trace isConnected: boolean = false

  private distributedManager = new DistributedDataManager<WhiteboardData>()

  /**
   * 创建协作会话 (发起方)
   */
  async createSession(): Promise<string> {
    const initialData: WhiteboardData = {
      strokes: '[]',
      backgroundColor: '#FFFFFF',
      lastModifiedBy: 'local',
      lastModifiedTime: Date.now()
    }

    await this.distributedManager.create(initialData)

    // 监听数据变更
    this.distributedManager.onDataChange((sessionId, fields) => {
      this.handleRemoteChange(fields)
    })

    // 监听状态变更
    this.distributedManager.onStatusChange((sessionId, networkId, status) => {
      this.isConnected = status === DistributedObjectStatus.ONLINE
    })

    const sessionId = this.distributedManager.genSessionId()
    await this.distributedManager.setSessionId(sessionId)

    return sessionId
  }

  /**
   * 加入协作会话 (加入方)
   */
  async joinSession(sessionId: string): Promise<void> {
    const initialData: WhiteboardData = {
      strokes: '[]',
      backgroundColor: '#FFFFFF',
      lastModifiedBy: '',
      lastModifiedTime: 0
    }

    await this.distributedManager.create(initialData)

    // 监听数据变更
    this.distributedManager.onDataChange((sessionId, fields) => {
      this.handleRemoteChange(fields)
    })

    // 监听状态变更
    this.distributedManager.onStatusChange((sessionId, networkId, status) => {
      this.isConnected = status === DistributedObjectStatus.ONLINE

      // 恢复数据
      if (status === DistributedObjectStatus.RESTORED) {
        this.handleRestored()
      }
    })

    await this.distributedManager.setSessionId(sessionId)
  }

  /**
   * 添加笔画 (本地变更)
   */
  addStroke(stroke: Stroke): void {
    this.strokes.push(stroke)

    // 同步到分布式对象
    this.distributedManager.update({
      strokes: JSON.stringify(this.strokes),
      lastModifiedBy: 'local',
      lastModifiedTime: Date.now()
    })
  }

  /**
   * 处理远程变更
   */
  private handleRemoteChange(fields: string[]): void {
    const data = this.distributedManager.getData()
    if (!data) return

    if (fields.includes('strokes')) {
      this.strokes = JSON.parse(data.strokes)
    }
    if (fields.includes('backgroundColor')) {
      this.backgroundColor = data.backgroundColor
    }
  }

  /**
   * 处理数据恢复
   */
  private handleRestored(): void {
    const data = this.distributedManager.getData()
    if (data) {
      this.strokes = JSON.parse(data.strokes)
      this.backgroundColor = data.backgroundColor
    }
  }

  /**
   * 销毁会话
   */
  destroy(): void {
    this.distributedManager.destroy()
  }
}
```

---

## 2. 跨设备流转 (Continuity)

### 触发场景
- 用户在手机上操作，切换到平板继续
- 视频播放进度在设备间同步
- 文档编辑状态迁移
- 应用状态无缝流转

### 权限配置

```json
{
  "module": {
    "requestPermissions": [
      {
        "name": "ohos.permission.DISTRIBUTED_DATASYNC",
        "reason": "$string:distributed_sync_reason",
        "usedScene": {
          "abilities": ["EntryAbility"],
          "when": "inuse"
        }
      }
    ],
    "abilities": [
      {
        "name": "EntryAbility",
        "continuable": true,
        "launchType": "singleton"
      }
    ]
  }
}
```

### 流转状态保存与恢复

```typescript
// entryability/EntryAbility.ets

import { AbilityConstant, UIAbility, Want, wantConstant } from '@kit.AbilityKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { window } from '@kit.ArkUI'

/**
 * 流转数据 Key
 */
const CONTINUITY_KEYS = {
  PAGE_URL: 'pageUrl',           // 当前页面路径
  PAGE_STATE: 'pageState',       // 页面状态 JSON
  SCROLL_POSITION: 'scrollPos',  // 滚动位置
  PLAY_PROGRESS: 'playProgress'  // 播放进度
}

export default class EntryAbility extends UIAbility {
  private currentPageUrl: string = 'pages/Index'
  private pageState: Record<string, unknown> = {}

  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    hilog.info(0x0000, 'EntryAbility', 'onCreate')

    // 检查是否是流转恢复启动
    if (launchParam.launchReason === AbilityConstant.LaunchReason.CONTINUATION) {
      this.restoreFromContinuation(want)
    }
  }

  onNewWant(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    // 处理新的 Want
    if (launchParam.launchReason === AbilityConstant.LaunchReason.CONTINUATION) {
      this.restoreFromContinuation(want)
    }
  }

  /**
   * 保存流转状态
   * 系统触发流转时自动调用
   */
  onContinue(wantParam: Record<string, Object>): AbilityConstant.OnContinueResult {
    hilog.info(0x0000, 'EntryAbility', 'onContinue called')

    try {
      // 保存当前页面路径
      wantParam[CONTINUITY_KEYS.PAGE_URL] = this.currentPageUrl

      // 保存页面状态
      wantParam[CONTINUITY_KEYS.PAGE_STATE] = JSON.stringify(this.pageState)

      // 保存滚动位置 (示例)
      wantParam[CONTINUITY_KEYS.SCROLL_POSITION] = 0

      hilog.info(0x0000, 'EntryAbility', 
        `Continuation state saved: ${JSON.stringify(wantParam)}`)

      return AbilityConstant.OnContinueResult.AGREE

    } catch (error) {
      hilog.error(0x0000, 'EntryAbility', `Save continuation failed: ${error}`)
      return AbilityConstant.OnContinueResult.REJECT
    }
  }

  /**
   * 从流转状态恢复
   */
  private restoreFromContinuation(want: Want): void {
    hilog.info(0x0000, 'EntryAbility', 'Restoring from continuation')

    try {
      const params = want.parameters
      if (!params) return

      // 恢复页面路径
      const pageUrl = params[CONTINUITY_KEYS.PAGE_URL] as string
      if (pageUrl) {
        this.currentPageUrl = pageUrl
      }

      // 恢复页面状态
      const pageStateJson = params[CONTINUITY_KEYS.PAGE_STATE] as string
      if (pageStateJson) {
        this.pageState = JSON.parse(pageStateJson)
      }

      hilog.info(0x0000, 'EntryAbility', 
        `Restored to page: ${this.currentPageUrl}`)

      // 存储到 AppStorage 供页面使用
      AppStorage.setOrCreate('continuityState', this.pageState)
      AppStorage.setOrCreate('continuityPageUrl', this.currentPageUrl)

    } catch (error) {
      hilog.error(0x0000, 'EntryAbility', `Restore failed: ${error}`)
    }
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    // 加载恢复的页面或默认页面
    windowStage.loadContent(this.currentPageUrl, (err) => {
      if (err.code) {
        hilog.error(0x0000, 'EntryAbility', `Load content failed: ${err}`)
        return
      }
    })
  }

  /**
   * 更新当前状态 (供页面调用)
   */
  updateContinuityState(pageUrl: string, state: Record<string, unknown>): void {
    this.currentPageUrl = pageUrl
    this.pageState = state
  }
}
```

### 页面中处理流转状态

```typescript
// pages/VideoPlayerPage.ets

import { router } from '@kit.ArkUI'
import { common } from '@kit.AbilityKit'

/**
 * 视频播放器 ViewModel
 */
@ObservedV2
export class VideoPlayerViewModel extends BaseViewModel {
  @Trace videoUrl: string = ''
  @Trace currentProgress: number = 0
  @Trace duration: number = 0
  @Trace isPlaying: boolean = false

  private context: common.UIAbilityContext

  constructor(context: common.UIAbilityContext) {
    super()
    this.context = context
  }

  /**
   * 初始化 - 检查是否有流转状态需要恢复
   */
  async onInit(): Promise<void> {
    // 检查是否有流转状态
    const continuityState = AppStorage.get<VideoPlayerState>('continuityState')

    if (continuityState && continuityState.videoUrl) {
      // 恢复流转状态
      this.videoUrl = continuityState.videoUrl
      this.currentProgress = continuityState.progress
      this.isPlaying = true

      // 清除已使用的状态
      AppStorage.delete('continuityState')
    }
  }

  /**
   * 更新播放进度
   */
  updateProgress(progress: number): void {
    this.currentProgress = progress
    // 同步状态到 Ability (用于流转)
    this.syncStateToAbility()
  }

  /**
   * 同步状态到 Ability
   */
  private syncStateToAbility(): void {
    const ability = this.context.abilityInfo
    const state: VideoPlayerState = {
      videoUrl: this.videoUrl,
      progress: this.currentProgress,
      duration: this.duration
    }

    // 通过 EventHub 或直接调用更新状态
    this.context.eventHub.emit('updateContinuityState', {
      pageUrl: 'pages/VideoPlayerPage',
      state: state
    })
  }
}

interface VideoPlayerState {
  videoUrl: string
  progress: number
  duration: number
}

/**
 * 视频播放器页面
 */
@Entry
@Component
struct VideoPlayerPage {
  private context = getContext(this) as common.UIAbilityContext
  @State viewModel: VideoPlayerViewModel = new VideoPlayerViewModel(this.context)

  aboutToAppear(): void {
    this.viewModel.onInit()
  }

  build() {
    Column() {
      // 视频播放器组件
      Video({
        src: this.viewModel.videoUrl,
        currentProgressRate: this.viewModel.currentProgress
      })
        .width('100%')
        .aspectRatio(16/9)
        .onUpdate((event) => {
          if (event) {
            this.viewModel.updateProgress(event.time)
          }
        })
        .accessibilityText('视频播放器')

      // 播放控制
      Row() {
        Text(`${this.formatTime(this.viewModel.currentProgress)} / ${this.formatTime(this.viewModel.duration)}`)
          .fontSize($r('app.float.font_size_sm'))
          .fontColor($r('app.color.text_secondary'))
      }
      .width('100%')
      .padding($r('app.float.spacing_md'))
    }
  }

  private formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }
}
```

### 分布式数据对象 + 流转结合使用

```typescript
// services/ContinuityService.ets

import { distributedDataObject } from '@kit.ArkData'
import { common, AbilityConstant } from '@kit.AbilityKit'
import { hilog } from '@kit.PerformanceAnalysisKit'

/**
 * 流转服务
 * 结合分布式数据对象实现无缝流转
 */
export class ContinuityService {
  private static readonly TAG = 'ContinuityService'
  private static readonly DOMAIN = 0x0000

  private dataObject: distributedDataObject.DataObject | null = null
  private sessionId: string = ''

  /**
   * 准备流转 (发起端)
   * 在用户触发流转前调用
   */
  async prepareForContinuation<T extends object>(
    context: common.Context,
    data: T
  ): Promise<string> {
    try {
      // 创建分布式数据对象
      this.dataObject = distributedDataObject.create(context, data)

      // 生成会话 ID
      this.sessionId = distributedDataObject.genSessionId()
      await this.dataObject.setSessionId(this.sessionId)

      hilog.info(ContinuityService.DOMAIN, ContinuityService.TAG,
        `Prepared for continuation: ${this.sessionId}`)

      return this.sessionId

    } catch (error) {
      hilog.error(ContinuityService.DOMAIN, ContinuityService.TAG,
        `Prepare failed: ${error}`)
      throw error
    }
  }

  /**
   * 保存到目标设备
   */
  async saveToDevice(deviceId: string): Promise<void> {
    if (!this.dataObject) {
      throw new Error('Data object not prepared')
    }

    try {
      await this.dataObject.save(deviceId)
      hilog.info(ContinuityService.DOMAIN, ContinuityService.TAG,
        `Saved to device: ${deviceId}`)
    } catch (error) {
      hilog.error(ContinuityService.DOMAIN, ContinuityService.TAG,
        `Save to device failed: ${error}`)
      throw error
    }
  }

  /**
   * 恢复流转数据 (目标端)
   */
  async restoreFromContinuation<T extends object>(
    context: common.Context,
    sessionId: string,
    defaultData: T
  ): Promise<T> {
    return new Promise((resolve, reject) => {
      try {
        // 创建数据对象并加入会话
        this.dataObject = distributedDataObject.create(context, defaultData)

        // 监听状态恢复
        this.dataObject.on('status', (sid: string, networkId: string, status: string) => {
          if (status === 'restored') {
            // 获取恢复的数据
            const data = this.getDataFromObject<T>()
            hilog.info(ContinuityService.DOMAIN, ContinuityService.TAG,
              'Data restored from continuation')
            resolve(data)
          }
        })

        // 加入会话
        this.dataObject.setSessionId(sessionId)
        this.sessionId = sessionId

      } catch (error) {
        hilog.error(ContinuityService.DOMAIN, ContinuityService.TAG,
          `Restore failed: ${error}`)
        reject(error)
      }
    })
  }

  /**
   * 从数据对象获取数据
   */
  private getDataFromObject<T>(): T {
    if (!this.dataObject) {
      throw new Error('No data object')
    }

    const result: Record<string, unknown> = {}
    const keys = Object.keys(this.dataObject)

    for (const key of keys) {
      const value = (this.dataObject as Record<string, unknown>)[key]
      if (typeof value !== 'function') {
        result[key] = value
      }
    }

    return result as T
  }

  /**
   * 清理资源
   */
  destroy(): void {
    if (this.dataObject) {
      this.dataObject.off('status')
      this.dataObject = null
    }
  }
}
```

---

## 3. 分布式 KV 存储

### 适用场景
- 配置同步 (用户设置在多设备间同步)
- 离线编辑同步 (最终一致性)
- 设备间数据共享

```typescript
// services/DistributedKVStore.ets

import { distributedKVStore } from '@kit.ArkData'
import { common } from '@kit.AbilityKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { BusinessError } from '@kit.BasicServicesKit'

/**
 * 分布式 KV 存储管理器
 */
export class DistributedKVStoreManager {
  private static readonly TAG = 'DistributedKVStore'
  private static readonly DOMAIN = 0x0000

  private kvManager: distributedKVStore.KVManager | null = null
  private kvStore: distributedKVStore.SingleKVStore | null = null

  /**
   * 初始化 KV 存储
   */
  async init(context: common.Context, storeId: string): Promise<void> {
    try {
      // 创建 KVManager
      const config: distributedKVStore.KVManagerConfig = {
        bundleName: context.abilityInfo.bundleName,
        context: context
      }
      this.kvManager = distributedKVStore.createKVManager(config)

      // 创建/获取 KVStore
      const options: distributedKVStore.Options = {
        createIfMissing: true,
        encrypt: false,
        backup: false,
        autoSync: true,  // 自动同步
        kvStoreType: distributedKVStore.KVStoreType.SINGLE_VERSION,
        securityLevel: distributedKVStore.SecurityLevel.S1
      }

      this.kvStore = await this.kvManager.getKVStore<distributedKVStore.SingleKVStore>(
        storeId,
        options
      )

      hilog.info(DistributedKVStoreManager.DOMAIN, DistributedKVStoreManager.TAG,
        'KV Store initialized')

    } catch (error) {
      const err = error as BusinessError
      hilog.error(DistributedKVStoreManager.DOMAIN, DistributedKVStoreManager.TAG,
        `Init failed: ${err.code} - ${err.message}`)
      throw error
    }
  }

  /**
   * 存储数据
   */
  async put(key: string, value: string | number | boolean | Uint8Array): Promise<void> {
    if (!this.kvStore) throw new Error('KV Store not initialized')

    try {
      await this.kvStore.put(key, value)
    } catch (error) {
      hilog.error(DistributedKVStoreManager.DOMAIN, DistributedKVStoreManager.TAG,
        `Put failed: ${error}`)
      throw error
    }
  }

  /**
   * 获取数据
   */
  async get(key: string): Promise<string | number | boolean | Uint8Array | undefined> {
    if (!this.kvStore) throw new Error('KV Store not initialized')

    try {
      return await this.kvStore.get(key)
    } catch (error) {
      return undefined
    }
  }

  /**
   * 删除数据
   */
  async delete(key: string): Promise<void> {
    if (!this.kvStore) throw new Error('KV Store not initialized')

    try {
      await this.kvStore.delete(key)
    } catch (error) {
      hilog.error(DistributedKVStoreManager.DOMAIN, DistributedKVStoreManager.TAG,
        `Delete failed: ${error}`)
    }
  }

  /**
   * 监听数据变更
   */
  onDataChange(callback: (entries: distributedKVStore.Entry[]) => void): void {
    if (!this.kvStore) throw new Error('KV Store not initialized')

    this.kvStore.on('dataChange', distributedKVStore.SubscribeType.SUBSCRIBE_TYPE_ALL,
      (data: distributedKVStore.ChangeNotification) => {
        callback(data.insertEntries.concat(data.updateEntries))
      }
    )
  }

  /**
   * 手动同步
   */
  async sync(deviceIds: string[]): Promise<void> {
    if (!this.kvStore) throw new Error('KV Store not initialized')

    try {
      await this.kvStore.sync(deviceIds, distributedKVStore.SyncMode.PUSH_PULL)
    } catch (error) {
      hilog.error(DistributedKVStoreManager.DOMAIN, DistributedKVStoreManager.TAG,
        `Sync failed: ${error}`)
    }
  }

  /**
   * 关闭存储
   */
  async close(storeId: string): Promise<void> {
    if (this.kvManager) {
      await this.kvManager.closeKVStore(storeId)
      this.kvStore = null
    }
  }
}
```

---

## 最佳实践

### 1. 选择合适的同步方式

| 场景 | 推荐方案 |
|------|----------|
| 实时协作 (白板/游戏) | 分布式数据对象 |
| 应用流转 | Continuity API |
| 设置同步 | 分布式 KV 存储 |
| 大文件传输 | 分布式文件 |

### 2. 数据结构设计

```typescript
// 好的做法：扁平化结构，减少嵌套
interface GoodSyncData {
  id: string
  name: string
  progress: number
  status: string
  timestamp: number
}

// 避免：深层嵌套
interface BadSyncData {
  user: {
    profile: {
      settings: {
        theme: {
          primary: string
          // ...
        }
      }
    }
  }
}
```

### 3. 错误处理

```typescript
// 分布式操作必须处理网络异常
async function syncWithFallback<T>(
  operation: () => Promise<T>,
  fallback: T
): Promise<T> {
  try {
    return await operation()
  } catch (error) {
    hilog.warn(0x0000, 'Sync', `Sync failed, using fallback: ${error}`)
    return fallback
  }
}
```

### 4. 权限检查

```typescript
import { abilityAccessCtrl, Permissions } from '@kit.AbilityKit'

async function checkDistributedPermission(): Promise<boolean> {
  const atManager = abilityAccessCtrl.createAtManager()
  const permission: Permissions = 'ohos.permission.DISTRIBUTED_DATASYNC'

  try {
    const result = await atManager.checkAccessToken(
      getContext().abilityInfo.accessTokenId,
      permission
    )
    return result === abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED
  } catch {
    return false
  }
}
```

---

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 数据不同步 | 未登录同一华为账号 | 确保设备登录同一账号 |
| 连接超时 | 设备不在同一网络 | 检查 WiFi/蓝牙连接 |
| 权限被拒 | 未申请分布式权限 | 添加 DISTRIBUTED_DATASYNC 权限 |
| 流转失败 | Ability 未配置 continuable | 在 module.json5 中设置 continuable: true |
