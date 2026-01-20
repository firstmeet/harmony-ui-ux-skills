# HarmonyOS NEXT 分布式协同协议

## 概述

本文档定义了 HarmonyOS NEXT 应用中"触碰即连接"分布式协同的标准实现模式，涵盖数据交换协议、传输层 (Share Kit)、同步层 (Distributed Data Object) 的完整技术规范。

---

## 协同架构总览

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        分布式协同架构                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────┐     NFC 触碰      ┌─────────────┐                    │
│   │   发送端    │ ───────────────► │   接收端    │                    │
│   │  (Host)     │                   │  (Guest)    │                    │
│   └──────┬──────┘                   └──────┬──────┘                    │
│          │                                  │                          │
│          │  1. 生成邀请码                    │  2. 接收邀请             │
│          │  2. 等待感应                      │  3. 验证身份             │
│          │  3. Share Kit 传输               │  4. 加入会话             │
│          │                                  │                          │
│          ▼                                  ▼                          │
│   ┌─────────────────────────────────────────────────────────────┐     │
│   │              Distributed Data Object (实时同步)              │     │
│   │                                                             │     │
│   │   ┌─────────┐        自动同步         ┌─────────┐          │     │
│   │   │ 本地状态 │ ◄──────────────────► │ 远程状态 │          │     │
│   │   └─────────┘                        └─────────┘          │     │
│   └─────────────────────────────────────────────────────────────┘     │
│                              │                                        │
│                              ▼                                        │
│   ┌─────────────────────────────────────────────────────────────┐     │
│   │                    RDB / Preferences                         │     │
│   │                     (本地持久化)                              │     │
│   └─────────────────────────────────────────────────────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 1. 数据交换协议

### CollaborationInvite 接口定义

```typescript
// model/CollaborationModels.ets

/**
 * 协同邀请数据结构
 * 用于 NFC/分享 传输的标准化协议
 */
export interface CollaborationInvite {
  /** 业务类型标识 (如 'family_share', 'whiteboard', 'game_room') */
  businessType: string

  /** 目标资源 ID (如家庭ID、房间ID、文档ID) */
  targetId: string

  /** 会话 ID (分布式数据对象的 sessionId) */
  sessionId: string

  /** 校验令牌 (用于身份验证) */
  token: string

  /** 邀请过期时间戳 */
  expireAt: number

  /** 发起方设备信息 */
  hostDevice: DeviceInfo

  /** 透传业务数据 (JSON 序列化) */
  payload: string
}

/**
 * 设备信息
 */
export interface DeviceInfo {
  /** 设备 ID */
  deviceId: string
  /** 设备名称 */
  deviceName: string
  /** 设备类型 */
  deviceType: 'phone' | 'tablet' | 'pc' | 'tv' | 'watch'
}

/**
 * 协同状态
 */
export enum CollaborationStatus {
  /** 等待连接 */
  WAITING = 'waiting',
  /** 连接中 */
  CONNECTING = 'connecting',
  /** 已连接 */
  CONNECTED = 'connected',
  /** 已断开 */
  DISCONNECTED = 'disconnected',
  /** 连接失败 */
  FAILED = 'failed'
}

/**
 * 协同成员
 */
export interface CollaborationMember {
  deviceId: string
  deviceName: string
  joinedAt: number
  isHost: boolean
  isOnline: boolean
}

/**
 * 协同会话信息
 */
export interface CollaborationSession {
  sessionId: string
  businessType: string
  targetId: string
  hostDeviceId: string
  members: CollaborationMember[]
  createdAt: number
  status: CollaborationStatus
}
```

### 邀请码生成与解析

```typescript
// utils/CollaborationCodec.ets

import { util } from '@kit.ArkTS'
import { CollaborationInvite } from '../model/CollaborationModels'

/**
 * 协同邀请编解码器
 */
export class CollaborationCodec {
  /** 协议版本 */
  private static readonly PROTOCOL_VERSION = '1.0'
  /** 协议前缀 */
  private static readonly PROTOCOL_PREFIX = 'harmony-collab://'

  /**
   * 生成邀请码
   */
  static encode(invite: CollaborationInvite): string {
    const data = {
      v: CollaborationCodec.PROTOCOL_VERSION,
      ...invite
    }
    const jsonString = JSON.stringify(data)
    const base64 = new util.Base64Helper().encodeToStringSync(
      new util.TextEncoder().encodeInto(jsonString)
    )
    return `${CollaborationCodec.PROTOCOL_PREFIX}${base64}`
  }

  /**
   * 解析邀请码
   */
  static decode(code: string): CollaborationInvite | null {
    try {
      if (!code.startsWith(CollaborationCodec.PROTOCOL_PREFIX)) {
        return null
      }

      const base64 = code.substring(CollaborationCodec.PROTOCOL_PREFIX.length)
      const decoded = new util.TextDecoder().decodeToString(
        new util.Base64Helper().decodeSync(base64)
      )
      const data = JSON.parse(decoded)

      // 验证协议版本
      if (data.v !== CollaborationCodec.PROTOCOL_VERSION) {
        console.warn('Protocol version mismatch')
      }

      return {
        businessType: data.businessType,
        targetId: data.targetId,
        sessionId: data.sessionId,
        token: data.token,
        expireAt: data.expireAt,
        hostDevice: data.hostDevice,
        payload: data.payload
      }
    } catch (error) {
      console.error('Failed to decode invite:', error)
      return null
    }
  }

  /**
   * 生成随机 Token
   */
  static generateToken(): string {
    return util.generateRandomUUID().replace(/-/g, '').substring(0, 16)
  }

  /**
   * 验证邀请是否过期
   */
  static isExpired(invite: CollaborationInvite): boolean {
    return Date.now() > invite.expireAt
  }
}
```

---

## 2. 传输层 (Share Kit + NFC)

### NFC 权限配置

在 `module.json5` 中配置 NFC 权限和意图过滤器：

```json
{
  "module": {
    "requestPermissions": [
      {
        "name": "ohos.permission.NFC_TAG",
        "reason": "$string:nfc_permission_reason",
        "usedScene": {
          "abilities": ["EntryAbility"],
          "when": "inuse"
        }
      }
    ],
    "abilities": [
      {
        "name": "EntryAbility",
        "skills": [
          {
            "entities": ["entity.system.home"],
            "actions": ["ohos.want.action.home"]
          },
          {
            "actions": ["ohos.nfc.tag.action.TAG_DISCOVERED"],
            "uris": [
              {
                "scheme": "harmony-collab"
              }
            ]
          }
        ]
      }
    ]
  }
}
```

### Share Kit 传输封装

```typescript
// collaboration/ShareTransport.ets

import { systemShare } from '@kit.ShareKit'
import { uniformTypeDescriptor as utd } from '@kit.ArkData'
import { common } from '@kit.AbilityKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { CollaborationInvite } from '../model/CollaborationModels'
import { CollaborationCodec } from '../utils/CollaborationCodec'

/**
 * 分享传输服务
 * 封装 NFC 触发的系统分享调用
 */
export class ShareTransport {
  private static readonly TAG = 'ShareTransport'
  private static readonly DOMAIN = 0x0000

  /**
   * 发送协同邀请
   * 通过系统分享面板发送邀请码
   */
  static async sendInvite(
    context: common.UIAbilityContext,
    invite: CollaborationInvite
  ): Promise<void> {
    try {
      const inviteCode = CollaborationCodec.encode(invite)

      // 创建分享数据
      const shareData = new systemShare.SharedData({
        utd: utd.UniformDataType.PLAIN_TEXT,
        content: inviteCode,
        title: ShareTransport.getShareTitle(invite.businessType),
        description: `来自 ${invite.hostDevice.deviceName} 的协作邀请`
      })

      // 配置分享选项
      const controller = new systemShare.ShareController(shareData)
      await controller.show(context, {
        selectionMode: systemShare.SelectionMode.SINGLE,
        previewMode: systemShare.SharePreviewMode.DETAIL
      })

      hilog.info(ShareTransport.DOMAIN, ShareTransport.TAG,
        `Invite sent for session: ${invite.sessionId}`)

    } catch (error) {
      hilog.error(ShareTransport.DOMAIN, ShareTransport.TAG,
        `Send invite failed: ${error}`)
      throw error
    }
  }

  /**
   * 生成 NFC 标签数据
   * 用于写入 NFC 标签
   */
  static generateNfcPayload(invite: CollaborationInvite): string {
    return CollaborationCodec.encode(invite)
  }

  /**
   * 从 NFC 标签读取邀请
   */
  static parseNfcPayload(payload: string): CollaborationInvite | null {
    return CollaborationCodec.decode(payload)
  }

  /**
   * 获取分享标题
   */
  private static getShareTitle(businessType: string): string {
    const titles: Record<string, string> = {
      'family_share': '邀请加入家庭',
      'whiteboard': '邀请协作白板',
      'game_room': '邀请加入游戏',
      'document': '邀请编辑文档'
    }
    return titles[businessType] || '协作邀请'
  }
}
```

### NFC 意图处理

```typescript
// entryability/EntryAbility.ets (部分)

import { AbilityConstant, UIAbility, Want } from '@kit.AbilityKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { CollaborationCodec } from '../utils/CollaborationCodec'
import { CollaborationManager } from '../collaboration/CollaborationManager'

export default class EntryAbility extends UIAbility {
  private collaborationManager = CollaborationManager.getInstance()

  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    hilog.info(0x0000, 'EntryAbility', 'onCreate')
    this.handleNfcIntent(want)
  }

  /**
   * 应用内感应 - 截获新的 NFC 意图
   * 实现平滑跳转而非重启应用
   */
  onNewWant(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    hilog.info(0x0000, 'EntryAbility', 'onNewWant - NFC intent received')
    this.handleNfcIntent(want)
  }

  /**
   * 处理 NFC 意图
   */
  private handleNfcIntent(want: Want): void {
    const action = want.action
    
    // 检查是否是 NFC TAG_DISCOVERED 动作
    if (action === 'ohos.nfc.tag.action.TAG_DISCOVERED') {
      const uri = want.uri
      if (uri) {
        this.processCollaborationInvite(uri)
      }
    }

    // 检查是否是分享传入
    if (want.parameters && want.parameters['shareData']) {
      const shareData = want.parameters['shareData'] as string
      this.processCollaborationInvite(shareData)
    }
  }

  /**
   * 处理协同邀请
   */
  private async processCollaborationInvite(inviteCode: string): Promise<void> {
    const invite = CollaborationCodec.decode(inviteCode)
    
    if (!invite) {
      hilog.warn(0x0000, 'EntryAbility', 'Invalid invite code')
      return
    }

    // 检查是否过期
    if (CollaborationCodec.isExpired(invite)) {
      hilog.warn(0x0000, 'EntryAbility', 'Invite expired')
      // 通知 UI 显示过期提示
      AppStorage.setOrCreate('collaborationError', 'invite_expired')
      return
    }

    // 存储邀请信息，供 UI 层消费
    AppStorage.setOrCreate('pendingInvite', invite)
    
    hilog.info(0x0000, 'EntryAbility', 
      `Collaboration invite received: ${invite.businessType}`)
  }
}
```

---

## 3. 同步层 (Distributed Data Object)

### 通用分布式数据同步管理器

```typescript
// collaboration/DistributedSyncManager.ets

import { distributedDataObject } from '@kit.ArkData'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { BusinessError } from '@kit.BasicServicesKit'

/**
 * 同步状态
 */
export enum SyncStatus {
  ONLINE = 'online',
  OFFLINE = 'offline',
  RESTORED = 'restored'
}

/**
 * 数据变更回调
 */
export type DataChangeCallback<T> = (data: T, changedFields: string[]) => void

/**
 * 状态变更回调
 */
export type StatusChangeCallback = (status: SyncStatus, networkId: string) => void

/**
 * 分布式数据同步管理器
 * 提供基于 distributedDataObject 的通用数据同步模板
 */
export class DistributedSyncManager<T extends object> {
  private static readonly TAG = 'DistributedSyncManager'
  private static readonly DOMAIN = 0x0000

  private dataObject: distributedDataObject.DataObject | null = null
  private sessionId: string = ''
  private isHost: boolean = false

  private dataChangeCallback: DataChangeCallback<T> | null = null
  private statusChangeCallback: StatusChangeCallback | null = null

  // 数据变更监听器引用 (用于解绑)
  private changeListener: ((sessionId: string, fields: string[]) => void) | null = null
  private statusListener: ((sessionId: string, networkId: string, status: string) => void) | null = null

  /**
   * 创建同步会话 (Host 端)
   */
  async createSession(initialData: T): Promise<string> {
    try {
      this.isHost = true
      this.dataObject = distributedDataObject.create(getContext(), initialData)
      this.sessionId = distributedDataObject.genSessionId()

      await this.setupListeners()
      await this.dataObject.setSessionId(this.sessionId)

      hilog.info(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        `Session created: ${this.sessionId}`)

      return this.sessionId

    } catch (error) {
      const err = error as BusinessError
      hilog.error(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        `Create session failed: ${err.code} - ${err.message}`)
      throw error
    }
  }

  /**
   * 加入同步会话 (Guest 端)
   */
  async joinSession(sessionId: string, initialData: T): Promise<void> {
    try {
      this.isHost = false
      this.sessionId = sessionId
      this.dataObject = distributedDataObject.create(getContext(), initialData)

      await this.setupListeners()
      await this.dataObject.setSessionId(sessionId)

      hilog.info(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        `Joined session: ${sessionId}`)

    } catch (error) {
      const err = error as BusinessError
      hilog.error(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        `Join session failed: ${err.code} - ${err.message}`)
      throw error
    }
  }

  /**
   * 设置监听器
   * 必须包含 on('change') 监听实现自动 UI 刷新
   */
  private async setupListeners(): Promise<void> {
    if (!this.dataObject) return

    // 数据变更监听 - 自动 UI 刷新的核心
    this.changeListener = (sessionId: string, fields: string[]) => {
      hilog.info(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        `Data changed: ${fields.join(', ')}`)

      if (this.dataChangeCallback) {
        const currentData = this.getData()
        if (currentData) {
          this.dataChangeCallback(currentData, fields)
        }
      }
    }
    this.dataObject.on('change', this.changeListener)

    // 状态变更监听
    this.statusListener = (sessionId: string, networkId: string, status: string) => {
      hilog.info(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        `Status changed: ${status}`)

      if (this.statusChangeCallback) {
        this.statusChangeCallback(status as SyncStatus, networkId)
      }

      // 数据恢复时自动刷新 UI
      if (status === 'restored' && this.dataChangeCallback) {
        const data = this.getData()
        if (data) {
          this.dataChangeCallback(data, Object.keys(data))
        }
      }
    }
    this.dataObject.on('status', this.statusListener)
  }

  /**
   * 注册数据变更回调
   * 用于自动刷新 UI
   */
  onDataChange(callback: DataChangeCallback<T>): void {
    this.dataChangeCallback = callback
  }

  /**
   * 注册状态变更回调
   */
  onStatusChange(callback: StatusChangeCallback): void {
    this.statusChangeCallback = callback
  }

  /**
   * 获取当前数据
   */
  getData(): T | null {
    if (!this.dataObject) return null

    const result: Record<string, unknown> = {}
    const keys = Object.keys(this.dataObject)

    for (const key of keys) {
      const value = (this.dataObject as Record<string, unknown>)[key]
      if (typeof value !== 'function' && !key.startsWith('__')) {
        result[key] = value
      }
    }

    return result as T
  }

  /**
   * 更新数据 (自动同步到其他设备)
   */
  update(partialData: Partial<T>): void {
    if (!this.dataObject) {
      throw new Error('Session not initialized')
    }

    Object.keys(partialData).forEach(key => {
      (this.dataObject as Record<string, unknown>)[key] = 
        (partialData as Record<string, unknown>)[key]
    })

    hilog.info(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
      `Data updated: ${JSON.stringify(partialData)}`)
  }

  /**
   * 保存数据到目标设备 (用于流转)
   */
  async saveToDevice(deviceId: string): Promise<void> {
    if (!this.dataObject) {
      throw new Error('Session not initialized')
    }

    try {
      await this.dataObject.save(deviceId)
      hilog.info(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        `Data saved to device: ${deviceId}`)
    } catch (error) {
      hilog.error(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        `Save failed: ${error}`)
      throw error
    }
  }

  /**
   * 获取会话 ID
   */
  getSessionId(): string {
    return this.sessionId
  }

  /**
   * 是否为 Host
   */
  isHostDevice(): boolean {
    return this.isHost
  }

  /**
   * 销毁会话
   * ⚠️ 必须在组件 aboutToDisappear 时调用，防止内存泄漏
   */
  destroy(): void {
    if (this.dataObject) {
      // 显式解绑监听器 - 防止内存泄漏
      if (this.changeListener) {
        this.dataObject.off('change', this.changeListener)
        this.changeListener = null
      }
      if (this.statusListener) {
        this.dataObject.off('status', this.statusListener)
        this.statusListener = null
      }

      this.dataObject = null
      hilog.info(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        'Session destroyed')
    }

    this.dataChangeCallback = null
    this.statusChangeCallback = null
    this.sessionId = ''
    this.isHost = false
  }
}
```

---

## 4. 协同管理器 (完整封装)

```typescript
// collaboration/CollaborationManager.ets

import { common } from '@kit.AbilityKit'
import { authentication } from '@kit.AccountKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { 
  CollaborationInvite, 
  CollaborationStatus,
  CollaborationSession,
  CollaborationMember,
  DeviceInfo 
} from '../model/CollaborationModels'
import { CollaborationCodec } from '../utils/CollaborationCodec'
import { ShareTransport } from './ShareTransport'
import { DistributedSyncManager, SyncStatus } from './DistributedSyncManager'
import { PreferencesUtil } from '../utils/PreferencesUtil'
import { deviceInfo } from '@kit.BasicServicesKit'

/**
 * 协同业务数据 (分布式同步)
 */
interface CollaborationData {
  sessionInfo: string  // JSON 序列化的 CollaborationSession
  businessData: string // JSON 序列化的业务数据
  lastUpdatedBy: string
  lastUpdatedAt: number
}

/**
 * 协同管理器
 * 统一管理"触碰即连接"的完整流程
 */
export class CollaborationManager {
  private static readonly TAG = 'CollaborationManager'
  private static readonly DOMAIN = 0x0000

  private static instance: CollaborationManager | null = null

  private syncManager: DistributedSyncManager<CollaborationData> | null = null
  private currentSession: CollaborationSession | null = null
  private statusCallback: ((status: CollaborationStatus) => void) | null = null
  private dataCallback: ((data: unknown) => void) | null = null

  private constructor() {}

  /**
   * 获取单例实例
   */
  static getInstance(): CollaborationManager {
    if (!CollaborationManager.instance) {
      CollaborationManager.instance = new CollaborationManager()
    }
    return CollaborationManager.instance
  }

  // ============================================================
  // Host 端操作
  // ============================================================

  /**
   * 创建协同会话 (Host)
   */
  async createSession(
    businessType: string,
    targetId: string,
    initialBusinessData: unknown
  ): Promise<CollaborationInvite> {
    // 验证用户身份
    const isAuthenticated = await this.verifyUserIdentity()
    if (!isAuthenticated) {
      throw new Error('用户身份验证失败')
    }

    // 获取设备信息
    const hostDevice = this.getDeviceInfo()

    // 创建同步管理器
    this.syncManager = new DistributedSyncManager<CollaborationData>()

    const sessionId = await this.syncManager.createSession({
      sessionInfo: '',
      businessData: JSON.stringify(initialBusinessData),
      lastUpdatedBy: hostDevice.deviceId,
      lastUpdatedAt: Date.now()
    })

    // 创建会话信息
    this.currentSession = {
      sessionId,
      businessType,
      targetId,
      hostDeviceId: hostDevice.deviceId,
      members: [{
        deviceId: hostDevice.deviceId,
        deviceName: hostDevice.deviceName,
        joinedAt: Date.now(),
        isHost: true,
        isOnline: true
      }],
      createdAt: Date.now(),
      status: CollaborationStatus.WAITING
    }

    // 更新会话信息到分布式对象
    this.syncManager.update({
      sessionInfo: JSON.stringify(this.currentSession)
    })

    // 设置监听
    this.setupSyncListeners()

    // 持久化会话信息
    await this.persistSession()

    // 生成邀请
    const invite: CollaborationInvite = {
      businessType,
      targetId,
      sessionId,
      token: CollaborationCodec.generateToken(),
      expireAt: Date.now() + 5 * 60 * 1000, // 5 分钟过期
      hostDevice,
      payload: JSON.stringify({ businessType, targetId })
    }

    hilog.info(CollaborationManager.DOMAIN, CollaborationManager.TAG,
      `Session created: ${sessionId}`)

    return invite
  }

  /**
   * 发送邀请 (通过系统分享)
   */
  async sendInvite(
    context: common.UIAbilityContext,
    invite: CollaborationInvite
  ): Promise<void> {
    await ShareTransport.sendInvite(context, invite)
  }

  // ============================================================
  // Guest 端操作
  // ============================================================

  /**
   * 加入协同会话 (Guest)
   */
  async joinSession(invite: CollaborationInvite): Promise<void> {
    // 验证邀请是否过期
    if (CollaborationCodec.isExpired(invite)) {
      throw new Error('邀请已过期')
    }

    // 验证用户身份
    const isAuthenticated = await this.verifyUserIdentity()
    if (!isAuthenticated) {
      throw new Error('用户身份验证失败')
    }

    // 验证 Token (实际项目中应与服务端比对)
    if (!invite.token || invite.token.length < 8) {
      throw new Error('无效的邀请令牌')
    }

    this.updateStatus(CollaborationStatus.CONNECTING)

    // 创建同步管理器并加入会话
    this.syncManager = new DistributedSyncManager<CollaborationData>()

    await this.syncManager.joinSession(invite.sessionId, {
      sessionInfo: '',
      businessData: '',
      lastUpdatedBy: '',
      lastUpdatedAt: 0
    })

    // 设置监听
    this.setupSyncListeners()

    // 获取设备信息
    const guestDevice = this.getDeviceInfo()

    // 等待数据同步
    setTimeout(() => {
      const data = this.syncManager?.getData()
      if (data && data.sessionInfo) {
        this.currentSession = JSON.parse(data.sessionInfo)
        
        // 添加自己为成员
        if (this.currentSession) {
          this.currentSession.members.push({
            deviceId: guestDevice.deviceId,
            deviceName: guestDevice.deviceName,
            joinedAt: Date.now(),
            isHost: false,
            isOnline: true
          })

          // 更新会话信息
          this.syncManager?.update({
            sessionInfo: JSON.stringify(this.currentSession)
          })
        }

        this.updateStatus(CollaborationStatus.CONNECTED)
        this.persistSession()
      }
    }, 1000)

    hilog.info(CollaborationManager.DOMAIN, CollaborationManager.TAG,
      `Joined session: ${invite.sessionId}`)
  }

  // ============================================================
  // 数据操作
  // ============================================================

  /**
   * 更新业务数据
   */
  updateBusinessData(data: unknown): void {
    if (!this.syncManager) {
      throw new Error('未加入任何会话')
    }

    const deviceInfo = this.getDeviceInfo()
    this.syncManager.update({
      businessData: JSON.stringify(data),
      lastUpdatedBy: deviceInfo.deviceId,
      lastUpdatedAt: Date.now()
    })
  }

  /**
   * 获取当前业务数据
   */
  getBusinessData<T>(): T | null {
    if (!this.syncManager) return null

    const data = this.syncManager.getData()
    if (data && data.businessData) {
      try {
        return JSON.parse(data.businessData) as T
      } catch {
        return null
      }
    }
    return null
  }

  // ============================================================
  // 监听与回调
  // ============================================================

  /**
   * 设置同步监听器
   */
  private setupSyncListeners(): void {
    if (!this.syncManager) return

    // 数据变更监听 - 自动刷新 UI
    this.syncManager.onDataChange((data, changedFields) => {
      hilog.info(CollaborationManager.DOMAIN, CollaborationManager.TAG,
        `Sync data changed: ${changedFields.join(', ')}`)

      // 解析业务数据并通知 UI
      if (changedFields.includes('businessData') && data.businessData) {
        try {
          const businessData = JSON.parse(data.businessData)
          if (this.dataCallback) {
            this.dataCallback(businessData)
          }
        } catch (error) {
          hilog.error(CollaborationManager.DOMAIN, CollaborationManager.TAG,
            `Parse business data failed: ${error}`)
        }
      }

      // 更新会话信息
      if (changedFields.includes('sessionInfo') && data.sessionInfo) {
        try {
          this.currentSession = JSON.parse(data.sessionInfo)
        } catch {
          // ignore
        }
      }
    })

    // 状态变更监听
    this.syncManager.onStatusChange((status, networkId) => {
      switch (status) {
        case SyncStatus.ONLINE:
          this.updateStatus(CollaborationStatus.CONNECTED)
          break
        case SyncStatus.OFFLINE:
          this.updateStatus(CollaborationStatus.DISCONNECTED)
          break
        case SyncStatus.RESTORED:
          this.updateStatus(CollaborationStatus.CONNECTED)
          break
      }
    })
  }

  /**
   * 注册状态回调
   */
  onStatusChange(callback: (status: CollaborationStatus) => void): void {
    this.statusCallback = callback
  }

  /**
   * 注册数据回调
   */
  onDataChange(callback: (data: unknown) => void): void {
    this.dataCallback = callback
  }

  /**
   * 更新状态
   */
  private updateStatus(status: CollaborationStatus): void {
    if (this.currentSession) {
      this.currentSession.status = status
    }
    if (this.statusCallback) {
      this.statusCallback(status)
    }
  }

  // ============================================================
  // 身份验证
  // ============================================================

  /**
   * 验证用户身份
   * 调用 Account Kit 或进行 Token 比对
   */
  private async verifyUserIdentity(): Promise<boolean> {
    try {
      // 尝试静默登录验证
      const loginRequest = new authentication.HuaweiIDProvider()
        .createLoginWithHuaweiIDRequest()
      loginRequest.forceLogin = false

      const controller = new authentication.AuthenticationController()
      const response = await controller.executeRequest(loginRequest)
      
      return response !== null

    } catch (error) {
      hilog.warn(CollaborationManager.DOMAIN, CollaborationManager.TAG,
        `Identity verification failed: ${error}`)
      // 降级：允许未登录用户使用（根据业务需求调整）
      return true
    }
  }

  // ============================================================
  // 持久化
  // ============================================================

  /**
   * 持久化会话信息
   */
  private async persistSession(): Promise<void> {
    if (this.currentSession) {
      await PreferencesUtil.putObject('current_collaboration_session', this.currentSession)
    }
  }

  /**
   * 恢复会话 (应用重启后)
   */
  async restoreSession(): Promise<CollaborationSession | null> {
    const session = await PreferencesUtil.getObject<CollaborationSession>(
      'current_collaboration_session',
      null as unknown as CollaborationSession
    )

    if (session && session.sessionId) {
      this.currentSession = session
      return session
    }

    return null
  }

  // ============================================================
  // 工具方法
  // ============================================================

  /**
   * 获取设备信息
   */
  private getDeviceInfo(): DeviceInfo {
    return {
      deviceId: deviceInfo.udid || 'unknown',
      deviceName: deviceInfo.marketName || 'HarmonyOS Device',
      deviceType: this.mapDeviceType(deviceInfo.deviceType)
    }
  }

  /**
   * 映射设备类型
   */
  private mapDeviceType(type: string): DeviceInfo['deviceType'] {
    const typeMap: Record<string, DeviceInfo['deviceType']> = {
      'phone': 'phone',
      'tablet': 'tablet',
      'pc': 'pc',
      'tv': 'tv',
      'wearable': 'watch'
    }
    return typeMap[type] || 'phone'
  }

  /**
   * 获取当前会话
   */
  getCurrentSession(): CollaborationSession | null {
    return this.currentSession
  }

  /**
   * 离开会话
   */
  async leaveSession(): Promise<void> {
    if (this.syncManager) {
      this.syncManager.destroy()
      this.syncManager = null
    }

    this.currentSession = null
    this.statusCallback = null
    this.dataCallback = null

    await PreferencesUtil.delete('current_collaboration_session')

    hilog.info(CollaborationManager.DOMAIN, CollaborationManager.TAG,
      'Left session')
  }

  /**
   * 销毁
   * ⚠️ 必须在组件销毁时调用
   */
  destroy(): void {
    if (this.syncManager) {
      this.syncManager.destroy()
      this.syncManager = null
    }
    this.statusCallback = null
    this.dataCallback = null
  }
}
```

---

## 5. UI 组件模板

### 发送端 - 等待感应动画

```typescript
// components/WaitingForTapView.ets

/**
 * 等待感应动画组件
 * 用于 Host 端显示"等待碰一碰"状态
 */
@Component
export struct WaitingForTapView {
  @Prop sessionId: string = ''
  @Prop businessType: string = ''
  @State animationScale: number = 1
  @State animationOpacity: number = 1

  aboutToAppear(): void {
    this.startPulseAnimation()
  }

  private startPulseAnimation(): void {
    // 脉冲动画循环
    setInterval(() => {
      animateTo({
        duration: 1000,
        curve: Curve.EaseInOut,
        iterations: -1,
        playMode: PlayMode.Alternate
      }, () => {
        this.animationScale = this.animationScale === 1 ? 1.2 : 1
        this.animationOpacity = this.animationOpacity === 1 ? 0.6 : 1
      })
    }, 2000)
  }

  build() {
    Column() {
      // NFC 图标动画
      Stack() {
        // 外圈脉冲
        Circle()
          .width(160)
          .height(160)
          .fill('transparent')
          .stroke($r('app.color.primary'))
          .strokeWidth(2)
          .scale({ x: this.animationScale, y: this.animationScale })
          .opacity(this.animationOpacity)

        // 内圈
        Circle()
          .width(120)
          .height(120)
          .fill($r('app.color.primary'))
          .opacity(0.1)

        // NFC 图标
        SymbolGlyph($r('sys.symbol.wave_3_right'))
          .fontSize(48)
          .fontColor([$r('app.color.primary')])
      }
      .accessibilityText('等待其他设备触碰连接')

      Text('等待设备触碰...')
        .fontSize($r('app.float.font_size_xl'))
        .fontColor($r('app.color.text_primary'))
        .fontWeight(FontWeight.Medium)
        .margin({ top: 32 })

      Text('请将另一台设备靠近进行配对')
        .fontSize($r('app.float.font_size_md'))
        .fontColor($r('app.color.text_secondary'))
        .margin({ top: 8 })

      // 会话信息
      if (this.sessionId) {
        Text(`会话: ${this.sessionId.substring(0, 8)}...`)
          .fontSize($r('app.float.font_size_xs'))
          .fontColor($r('app.color.text_tertiary'))
          .margin({ top: 24 })
      }
    }
    .width('100%')
    .padding($r('app.float.spacing_xl'))
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
  }
}
```

### 接收端 - 确认加入弹窗

```typescript
// components/JoinConfirmDialog.ets

import { CollaborationInvite } from '../model/CollaborationModels'

/**
 * 确认加入弹窗
 * 用于 Guest 端显示邀请确认
 */
@CustomDialog
export struct JoinConfirmDialog {
  controller: CustomDialogController
  invite: CollaborationInvite | null = null
  onConfirm: () => void = () => {}
  onCancel: () => void = () => {}

  build() {
    Column() {
      // 图标
      SymbolGlyph($r('sys.symbol.link'))
        .fontSize(48)
        .fontColor([$r('app.color.primary')])

      // 标题
      Text('收到协作邀请')
        .fontSize($r('app.float.font_size_xl'))
        .fontColor($r('app.color.text_primary'))
        .fontWeight(FontWeight.Bold)
        .margin({ top: 16 })

      // 邀请信息
      if (this.invite) {
        Column() {
          Row() {
            Text('来自: ')
              .fontSize($r('app.float.font_size_md'))
              .fontColor($r('app.color.text_secondary'))
            Text(this.invite.hostDevice.deviceName)
              .fontSize($r('app.float.font_size_md'))
              .fontColor($r('app.color.text_primary'))
          }
          .margin({ top: 8 })

          Row() {
            Text('类型: ')
              .fontSize($r('app.float.font_size_md'))
              .fontColor($r('app.color.text_secondary'))
            Text(this.getBusinessTypeLabel(this.invite.businessType))
              .fontSize($r('app.float.font_size_md'))
              .fontColor($r('app.color.text_primary'))
          }
          .margin({ top: 4 })
        }
        .margin({ top: 16 })
        .padding(16)
        .backgroundColor($r('app.color.bg_secondary'))
        .borderRadius($r('app.float.radius_md'))
      }

      // 按钮组
      Row() {
        Button($r('app.string.cancel'))
          .backgroundColor($r('app.color.bg_tertiary'))
          .fontColor($r('app.color.text_primary'))
          .layoutWeight(1)
          .onClick(() => {
            this.onCancel()
            this.controller.close()
          })
          .accessibilityText('取消加入')

        Button('加入')
          .backgroundColor($r('app.color.primary'))
          .fontColor($r('app.color.text_inverse'))
          .layoutWeight(1)
          .margin({ left: 12 })
          .onClick(() => {
            this.onConfirm()
            this.controller.close()
          })
          .accessibilityText('确认加入协作')
      }
      .width('100%')
      .margin({ top: 24 })
    }
    .width('100%')
    .padding(24)
  }

  private getBusinessTypeLabel(type: string): string {
    const labels: Record<string, string> = {
      'family_share': '家庭共享',
      'whiteboard': '协作白板',
      'game_room': '游戏房间',
      'document': '文档协作'
    }
    return labels[type] || type
  }
}
```

---

## 6. 使用示例

### ViewModel 集成

```typescript
// viewmodel/CollaborationViewModel.ets

import { BaseViewModel } from './BaseViewModel'
import { CollaborationManager } from '../collaboration/CollaborationManager'
import { CollaborationInvite, CollaborationStatus } from '../model/CollaborationModels'
import { common } from '@kit.AbilityKit'

/**
 * 协作白板数据
 */
interface WhiteboardData {
  strokes: string[]
  backgroundColor: string
}

@ObservedV2
export class CollaborationViewModel extends BaseViewModel {
  @Trace status: CollaborationStatus = CollaborationStatus.DISCONNECTED
  @Trace currentInvite: CollaborationInvite | null = null
  @Trace whiteboardData: WhiteboardData = { strokes: [], backgroundColor: '#FFFFFF' }
  @Trace members: string[] = []

  private manager = CollaborationManager.getInstance()

  override async onInit(): Promise<void> {
    // 注册回调
    this.manager.onStatusChange((status) => {
      this.status = status
    })

    this.manager.onDataChange((data) => {
      if (data) {
        this.whiteboardData = data as WhiteboardData
      }
    })

    // 尝试恢复会话
    const session = await this.manager.restoreSession()
    if (session) {
      this.status = session.status
    }
  }

  /**
   * 创建协作会话
   */
  async createSession(): Promise<void> {
    await this.executeAsync(async () => {
      this.currentInvite = await this.manager.createSession(
        'whiteboard',
        'room_001',
        this.whiteboardData
      )
      return this.currentInvite
    })
  }

  /**
   * 发送邀请
   */
  async sendInvite(context: common.UIAbilityContext): Promise<void> {
    if (this.currentInvite) {
      await this.manager.sendInvite(context, this.currentInvite)
    }
  }

  /**
   * 加入会话
   */
  async joinSession(invite: CollaborationInvite): Promise<void> {
    await this.executeAsync(async () => {
      await this.manager.joinSession(invite)
    })
  }

  /**
   * 更新白板数据
   */
  updateWhiteboard(strokes: string[]): void {
    this.whiteboardData.strokes = strokes
    this.manager.updateBusinessData(this.whiteboardData)
  }

  /**
   * 离开会话
   */
  async leave(): Promise<void> {
    await this.manager.leaveSession()
    this.status = CollaborationStatus.DISCONNECTED
  }

  /**
   * 销毁
   * ⚠️ 必须在 aboutToDisappear 时调用
   */
  override onDestroy(): void {
    this.manager.destroy()
  }
}
```

---

## 最佳实践检查清单

- [ ] NFC 权限已在 `module.json5` 声明
- [ ] 配置了 `TAG_DISCOVERED` 技能过滤器
- [ ] 在 `onNewWant` 中处理 NFC 意图
- [ ] 加入协作前验证用户身份
- [ ] 分布式数据配合 RDB/Preferences 持久化
- [ ] 组件销毁时调用 `destroy()` 解绑监听
- [ ] Host 端显示"等待感应"动画
- [ ] Guest 端显示"确认加入"弹窗
