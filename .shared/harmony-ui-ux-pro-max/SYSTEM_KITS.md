# HarmonyOS NEXT 系统 Kit 集成指南

## 概述

本文档整理了 HarmonyOS NEXT 常用系统 Kit 的集成触发条件和 API 范式，帮助开发者快速接入系统能力。

---

## Kit 集成速查表

| Kit | 功能 | 触发场景 | 所需权限 |
|-----|------|----------|----------|
| **Account Kit** | 华为账号登录 | 用户登录、免密认证 | 无需权限 |
| **Push Kit** | 消息推送 | 通知推送、消息触达 | 无需权限 |
| **Share Kit** | 系统分享 | 内容分享、文件分享 | 无需权限 |
| **Scan Kit** | 扫码识别 | 扫描二维码/条形码 | `ohos.permission.CAMERA` |
| **NFC Kit** | NFC 标签读写 | 碰一碰连接、标签读取 | `ohos.permission.NFC_TAG` |

---

## 🔗 "碰一碰" 场景技术选型

### 概述

"碰一碰"是 HarmonyOS 特色的设备间快速连接方式，通过 NFC 触碰实现设备配对和数据传输。

### 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                     "碰一碰" 技术栈                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────┐         NFC 触碰         ┌─────────────┐ │
│   │   设备 A    │ ◄─────────────────────► │   设备 B    │ │
│   │   (Host)    │                          │   (Guest)   │ │
│   └──────┬──────┘                          └──────┬──────┘ │
│          │                                        │        │
│          ▼                                        ▼        │
│   ┌─────────────────────────────────────────────────────┐ │
│   │              NFC Kit (TAG_DISCOVERED)               │ │
│   │                  触发意图传递                         │ │
│   └─────────────────────────────────────────────────────┘ │
│                          │                                 │
│                          ▼                                 │
│   ┌─────────────────────────────────────────────────────┐ │
│   │              Account Kit (身份验证)                  │ │
│   │              Token 比对 / 华为账号验证                │ │
│   └─────────────────────────────────────────────────────┘ │
│                          │                                 │
│                          ▼                                 │
│   ┌─────────────────────────────────────────────────────┐ │
│   │         Distributed Data Object (实时同步)           │ │
│   │              分布式数据对象同步                        │ │
│   └─────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1. NFC 触发配置

#### 权限声明

在 `module.json5` 中声明 NFC 权限：

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
    ]
  }
}
```

#### 技能过滤器 (Skill Filter)

配置 `TAG_DISCOVERED` 动作，使应用能够响应 NFC 触碰：

```json
{
  "module": {
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
                "scheme": "harmony-collab",
                "host": "*"
              }
            ]
          }
        ]
      }
    ]
  }
}
```

### 2. 身份验证

**强制要求**: 在加入协作前，必须验证用户身份。

#### 验证方式选择

| 方式 | 适用场景 | 安全级别 |
|------|----------|----------|
| **Account Kit** | 需要华为账号体系 | 高 |
| **Token 比对** | 自建用户体系 | 中 |
| **设备 ID** | 简单场景 | 低 |

#### 验证代码模板

```typescript
// services/IdentityVerifier.ets

import { authentication } from '@kit.AccountKit'
import { hilog } from '@kit.PerformanceAnalysisKit'

export class IdentityVerifier {
  private static readonly TAG = 'IdentityVerifier'

  /**
   * 使用 Account Kit 验证用户身份
   */
  static async verifyWithAccountKit(): Promise<boolean> {
    try {
      const loginRequest = new authentication.HuaweiIDProvider()
        .createLoginWithHuaweiIDRequest()
      loginRequest.forceLogin = false

      const controller = new authentication.AuthenticationController()
      const response = await controller.executeRequest(loginRequest)

      return response !== null
    } catch (error) {
      hilog.warn(0x0000, IdentityVerifier.TAG, `Account verification failed: ${error}`)
      return false
    }
  }

  /**
   * 使用 Token 比对验证
   * @param inviteToken 邀请方提供的 Token
   * @param inputToken 用户输入的 Token
   */
  static verifyWithToken(inviteToken: string, inputToken: string): boolean {
    return inviteToken === inputToken && inviteToken.length >= 8
  }

  /**
   * 综合验证
   */
  static async verify(inviteToken?: string): Promise<boolean> {
    // 优先使用 Account Kit
    const accountVerified = await IdentityVerifier.verifyWithAccountKit()
    if (accountVerified) {
      return true
    }

    // 降级到 Token 验证（需要用户手动输入）
    if (inviteToken) {
      // 这里应该弹出输入框让用户输入 Token
      // 简化处理：假设 Token 验证通过
      return inviteToken.length >= 8
    }

    return false
  }
}
```

### 3. 生命周期管理

#### onNewWant 截获 NFC 意图

**关键**: 在 `onNewWant` 中处理 NFC 意图，实现"应用内感应"的平滑跳转。

```typescript
// entryability/EntryAbility.ets

import { AbilityConstant, UIAbility, Want } from '@kit.AbilityKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { window } from '@kit.ArkUI'

export default class EntryAbility extends UIAbility {
  
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    hilog.info(0x0000, 'EntryAbility', 'onCreate')
    // 首次启动时处理 NFC 意图
    this.handleIntent(want)
  }

  /**
   * ⚠️ 关键：应用已在前台时，NFC 触碰会触发此方法
   * 实现平滑跳转而非重启应用
   */
  onNewWant(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    hilog.info(0x0000, 'EntryAbility', 'onNewWant - NFC intent in foreground')
    this.handleIntent(want)
  }

  /**
   * 统一处理意图
   */
  private handleIntent(want: Want): void {
    const action = want.action

    // 检查是否是 NFC TAG_DISCOVERED 动作
    if (action === 'ohos.nfc.tag.action.TAG_DISCOVERED') {
      this.handleNfcTagDiscovered(want)
      return
    }

    // 检查 URI scheme
    if (want.uri?.startsWith('harmony-collab://')) {
      this.handleCollaborationUri(want.uri)
      return
    }
  }

  /**
   * 处理 NFC 标签发现
   */
  private handleNfcTagDiscovered(want: Want): void {
    hilog.info(0x0000, 'EntryAbility', 'NFC tag discovered')
    
    // 从 want 中提取数据
    const uri = want.uri
    const parameters = want.parameters

    if (uri) {
      this.handleCollaborationUri(uri)
    }
  }

  /**
   * 处理协作 URI
   */
  private handleCollaborationUri(uri: string): void {
    hilog.info(0x0000, 'EntryAbility', `Collaboration URI: ${uri}`)
    
    // 存储到 AppStorage，由 UI 层消费
    AppStorage.setOrCreate('pendingCollaborationUri', uri)
    
    // 触发页面刷新或跳转
    AppStorage.setOrCreate('shouldShowJoinDialog', true)
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        hilog.error(0x0000, 'EntryAbility', `Load content failed: ${err}`)
      }
    })
  }
}
```

### 4. 完整流程图

```
发送端 (Host)                              接收端 (Guest)
    │                                           │
    │  1. 创建协作会话                           │
    │  2. 生成邀请码/Token                       │
    │  3. 显示"等待感应"动画                     │
    │                                           │
    │ ◄────────── NFC 触碰 ──────────►          │
    │                                           │
    │                                    4. TAG_DISCOVERED 触发
    │                                    5. onNewWant 接收意图
    │                                    6. 解析邀请数据
    │                                    7. Account Kit 验证
    │                                    8. 显示"确认加入"弹窗
    │                                           │
    │                                    9. 用户确认
    │                                           │
    │ ◄─────── 分布式数据对象同步 ────────►       │
    │                                           │
    │  10. on('status') = 'online'       10. 加入会话成功
    │  11. 更新 UI 显示成员               11. 同步数据到本地
    │                                           │
```

### 5. 权限字符串资源

```json
// resources/base/element/string.json
{
  "string": [
    {
      "name": "nfc_permission_reason",
      "value": "需要使用 NFC 功能进行设备间快速连接"
    },
    {
      "name": "distributed_sync_reason",
      "value": "需要在设备间同步数据"
    }
  ]
}
```

### 6. 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| NFC 无响应 | 未声明权限 | 检查 module.json5 权限配置 |
| 应用重启而非跳转 | 未处理 onNewWant | 在 onNewWant 中处理意图 |
| 验证失败 | 未登录华为账号 | 提示用户登录或降级到 Token |
| 数据不同步 | 未在同一网络 | 检查设备网络连接 |

---

## 1. Account Kit (华为账号)

### 触发条件
- 用户点击"华为账号登录"按钮
- 需要获取用户信息进行业务处理
- 实现免密快速登录

### API 范式

```typescript
// 导入模块
import { authentication } from '@kit.AccountKit'
import { util } from '@kit.ArkTS'
import { hilog } from '@kit.PerformanceAnalysisKit'

/**
 * 华为账号登录服务
 */
export class AccountService {
  private static readonly TAG = 'AccountService'
  private static readonly DOMAIN = 0x0000

  /**
   * 使用华为账号静默登录
   * 适用于已授权用户的快速登录
   */
  static async silentLogin(): Promise<string | undefined> {
    try {
      // 创建登录请求
      const loginRequest = new authentication.HuaweiIDProvider().createLoginWithHuaweiIDRequest()
      loginRequest.forceLogin = false  // 静默登录
      loginRequest.state = util.generateRandomUUID()

      // 执行登录
      const controller = new authentication.AuthenticationController()
      const response = await controller.executeRequest(loginRequest)

      const loginResponse = response as authentication.LoginWithHuaweiIDResponse
      if (loginResponse.state !== loginRequest.state) {
        hilog.error(AccountService.DOMAIN, AccountService.TAG, 'State mismatch')
        return undefined
      }

      // 返回 Authorization Code
      const authCode = loginResponse.data?.authorizationCode
      hilog.info(AccountService.DOMAIN, AccountService.TAG, 'Silent login success')
      return authCode

    } catch (error) {
      hilog.error(AccountService.DOMAIN, AccountService.TAG, `Silent login failed: ${error}`)
      return undefined
    }
  }

  /**
   * 使用华为账号强制登录
   * 会弹出授权页面让用户确认
   */
  static async forceLogin(): Promise<string | undefined> {
    try {
      const loginRequest = new authentication.HuaweiIDProvider().createLoginWithHuaweiIDRequest()
      loginRequest.forceLogin = true  // 强制登录，弹出授权页
      loginRequest.state = util.generateRandomUUID()

      const controller = new authentication.AuthenticationController(getContext())
      const response = await controller.executeRequest(loginRequest)

      const loginResponse = response as authentication.LoginWithHuaweiIDResponse
      return loginResponse.data?.authorizationCode

    } catch (error) {
      const authError = error as authentication.AuthenticationError
      hilog.error(AccountService.DOMAIN, AccountService.TAG, 
        `Force login failed: ${authError.code} - ${authError.message}`)
      return undefined
    }
  }

  /**
   * 取消华为账号授权
   */
  static async cancelAuthorization(): Promise<boolean> {
    try {
      const request = new authentication.HuaweiIDProvider().createCancelAuthorizationRequest()
      const controller = new authentication.AuthenticationController(getContext())
      await controller.executeRequest(request)
      hilog.info(AccountService.DOMAIN, AccountService.TAG, 'Authorization cancelled')
      return true
    } catch (error) {
      hilog.error(AccountService.DOMAIN, AccountService.TAG, `Cancel failed: ${error}`)
      return false
    }
  }
}
```

### 使用示例

```typescript
// 在 ViewModel 中使用
@ObservedV2
export class LoginViewModel extends BaseViewModel {
  @Trace isLoggedIn: boolean = false
  @Trace authCode: string = ''

  async loginWithHuaweiID(): Promise<void> {
    await this.executeAsync(
      async () => {
        // 先尝试静默登录
        let code = await AccountService.silentLogin()
        if (!code) {
          // 静默失败，弹出授权页
          code = await AccountService.forceLogin()
        }
        if (!code) {
          throw new Error('登录失败')
        }
        return code
      },
      (code) => {
        this.authCode = code
        this.isLoggedIn = true
        // 将 authCode 发送到服务端换取业务 token
      }
    )
  }
}
```

### 权限配置

Account Kit 不需要额外权限配置，但需要在 AGC 控制台开通服务。

---

## 2. Push Kit (消息推送)

### 触发条件
- 应用启动时获取 Push Token
- 服务端需要向用户推送通知
- 需要处理推送消息的点击事件

### API 范式

```typescript
// 导入模块
import { pushService } from '@kit.PushKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { BusinessError } from '@kit.BasicServicesKit'

/**
 * 推送服务
 */
export class PushService {
  private static readonly TAG = 'PushService'
  private static readonly DOMAIN = 0x0000

  /**
   * 获取 Push Token
   * 通常在应用启动时调用
   */
  static async getPushToken(): Promise<string | undefined> {
    try {
      const token = await pushService.getToken()
      hilog.info(PushService.DOMAIN, PushService.TAG, `Push token: ${token}`)
      // 将 token 上报到业务服务器
      return token
    } catch (error) {
      const err = error as BusinessError
      hilog.error(PushService.DOMAIN, PushService.TAG, 
        `Get token failed: ${err.code} - ${err.message}`)
      return undefined
    }
  }

  /**
   * 删除 Push Token
   * 用于用户退出登录时清理推送
   */
  static async deleteToken(): Promise<boolean> {
    try {
      await pushService.deleteToken()
      hilog.info(PushService.DOMAIN, PushService.TAG, 'Token deleted')
      return true
    } catch (error) {
      const err = error as BusinessError
      hilog.error(PushService.DOMAIN, PushService.TAG, 
        `Delete token failed: ${err.code} - ${err.message}`)
      return false
    }
  }
}
```

### 在 EntryAbility 中初始化

```typescript
// entryability/EntryAbility.ets
import { UIAbility } from '@kit.AbilityKit'
import { PushService } from '../services/PushService'

export default class EntryAbility extends UIAbility {
  async onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): Promise<void> {
    // 应用启动时获取推送 Token
    const token = await PushService.getPushToken()
    if (token) {
      // 上报 token 到服务器
      await this.uploadTokenToServer(token)
    }
  }

  private async uploadTokenToServer(token: string): Promise<void> {
    // 实现 token 上报逻辑
  }
}
```

### 权限配置

Push Kit 不需要额外权限，但需要在 AGC 控制台开通推送服务并完成配置。

---

## 3. Share Kit (系统分享)

### 触发条件
- 用户点击"分享"按钮
- 需要分享文本、图片、链接等内容
- 需要调起系统分享面板

### API 范式

```typescript
// 导入模块
import { systemShare } from '@kit.ShareKit'
import { uniformTypeDescriptor as utd } from '@kit.ArkData'
import { fileUri } from '@kit.CoreFileKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { common } from '@kit.AbilityKit'

/**
 * 分享服务
 */
export class ShareService {
  private static readonly TAG = 'ShareService'
  private static readonly DOMAIN = 0x0000

  /**
   * 分享文本
   */
  static async shareText(
    context: common.UIAbilityContext,
    text: string,
    title?: string
  ): Promise<void> {
    try {
      const shareData = new systemShare.SharedData({
        utd: utd.UniformDataType.TEXT,
        content: text,
        title: title
      })

      const controller = new systemShare.ShareController(shareData)
      await controller.show(context, {
        selectionMode: systemShare.SelectionMode.SINGLE,
        previewMode: systemShare.SharePreviewMode.DETAIL
      })

      hilog.info(ShareService.DOMAIN, ShareService.TAG, 'Text shared')
    } catch (error) {
      hilog.error(ShareService.DOMAIN, ShareService.TAG, `Share text failed: ${error}`)
    }
  }

  /**
   * 分享链接
   */
  static async shareLink(
    context: common.UIAbilityContext,
    url: string,
    title?: string,
    description?: string
  ): Promise<void> {
    try {
      const shareData = new systemShare.SharedData({
        utd: utd.UniformDataType.HYPERLINK,
        content: url,
        title: title,
        description: description
      })

      const controller = new systemShare.ShareController(shareData)
      await controller.show(context, {
        selectionMode: systemShare.SelectionMode.SINGLE,
        previewMode: systemShare.SharePreviewMode.DETAIL
      })

      hilog.info(ShareService.DOMAIN, ShareService.TAG, 'Link shared')
    } catch (error) {
      hilog.error(ShareService.DOMAIN, ShareService.TAG, `Share link failed: ${error}`)
    }
  }

  /**
   * 分享图片
   * @param imagePath 图片文件路径 (沙箱路径)
   */
  static async shareImage(
    context: common.UIAbilityContext,
    imagePath: string,
    title?: string
  ): Promise<void> {
    try {
      const uri = fileUri.getUriFromPath(imagePath)

      const shareData = new systemShare.SharedData({
        utd: utd.UniformDataType.IMAGE,
        uri: uri,
        title: title
      })

      const controller = new systemShare.ShareController(shareData)
      await controller.show(context, {
        selectionMode: systemShare.SelectionMode.SINGLE,
        previewMode: systemShare.SharePreviewMode.DETAIL
      })

      hilog.info(ShareService.DOMAIN, ShareService.TAG, 'Image shared')
    } catch (error) {
      hilog.error(ShareService.DOMAIN, ShareService.TAG, `Share image failed: ${error}`)
    }
  }

  /**
   * 分享多个文件
   */
  static async shareFiles(
    context: common.UIAbilityContext,
    filePaths: string[],
    title?: string
  ): Promise<void> {
    try {
      const records: systemShare.SharedData[] = filePaths.map(path => {
        return new systemShare.SharedData({
          utd: utd.UniformDataType.FILE,
          uri: fileUri.getUriFromPath(path),
          title: title
        })
      })

      // 合并为单个 SharedData
      const shareData = records[0]
      for (let i = 1; i < records.length; i++) {
        shareData.addRecord(records[i].getRecords()[0])
      }

      const controller = new systemShare.ShareController(shareData)
      await controller.show(context, {
        selectionMode: systemShare.SelectionMode.SINGLE,
        previewMode: systemShare.SharePreviewMode.DEFAULT
      })

      hilog.info(ShareService.DOMAIN, ShareService.TAG, 'Files shared')
    } catch (error) {
      hilog.error(ShareService.DOMAIN, ShareService.TAG, `Share files failed: ${error}`)
    }
  }
}
```

### 使用示例

```typescript
// 在页面中使用
@Entry
@Component
struct ArticlePage {
  private context = getContext(this) as common.UIAbilityContext

  build() {
    Column() {
      // 文章内容...

      Button($r('app.string.share'))
        .onClick(() => this.handleShare())
        .accessibilityText('分享文章')
    }
  }

  private async handleShare(): Promise<void> {
    await ShareService.shareLink(
      this.context,
      'https://example.com/article/123',
      '精彩文章标题',
      '这是一篇非常有价值的文章...'
    )
  }
}
```

### 权限配置

Share Kit 不需要额外权限配置。

---

## 4. Scan Kit (扫码)

### 触发条件
- 用户点击"扫一扫"按钮
- 需要识别二维码/条形码
- 需要从图片中识别码

### API 范式

```typescript
// 导入模块
import { scanCore, scanBarcode } from '@kit.ScanKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { BusinessError } from '@kit.BasicServicesKit'
import { common } from '@kit.AbilityKit'

/**
 * 扫码服务
 */
export class ScanService {
  private static readonly TAG = 'ScanService'
  private static readonly DOMAIN = 0x0000

  /**
   * 启动默认扫码界面
   * 最简单的集成方式，使用系统提供的扫码 UI
   */
  static async startDefaultScan(context: common.UIAbilityContext): Promise<string | undefined> {
    try {
      // 配置扫码选项
      const options: scanBarcode.ScanOptions = {
        scanTypes: [scanCore.ScanType.ALL],  // 支持所有码类型
        enableMultiMode: false,               // 单码模式
        enableAlbum: true                     // 允许从相册选择
      }

      // 启动扫码
      const result = await scanBarcode.startScanForResult(context, options)

      if (result.originalValue) {
        hilog.info(ScanService.DOMAIN, ScanService.TAG, 
          `Scan result: ${result.originalValue}`)
        return result.originalValue
      }

      return undefined
    } catch (error) {
      const err = error as BusinessError
      hilog.error(ScanService.DOMAIN, ScanService.TAG, 
        `Scan failed: ${err.code} - ${err.message}`)

      // 处理特定错误码
      if (err.code === 1000500001) {
        // 用户取消扫码
        return undefined
      }

      throw error
    }
  }

  /**
   * 仅扫描二维码
   */
  static async scanQRCode(context: common.UIAbilityContext): Promise<string | undefined> {
    try {
      const options: scanBarcode.ScanOptions = {
        scanTypes: [scanCore.ScanType.QR_CODE],
        enableMultiMode: false,
        enableAlbum: true
      }

      const result = await scanBarcode.startScanForResult(context, options)
      return result.originalValue

    } catch (error) {
      hilog.error(ScanService.DOMAIN, ScanService.TAG, `QR scan failed: ${error}`)
      return undefined
    }
  }

  /**
   * 仅扫描条形码
   */
  static async scanBarcode(context: common.UIAbilityContext): Promise<string | undefined> {
    try {
      const options: scanBarcode.ScanOptions = {
        scanTypes: [
          scanCore.ScanType.EAN_13,
          scanCore.ScanType.EAN_8,
          scanCore.ScanType.UPC_A,
          scanCore.ScanType.UPC_E,
          scanCore.ScanType.CODE_128,
          scanCore.ScanType.CODE_39
        ],
        enableMultiMode: false,
        enableAlbum: true
      }

      const result = await scanBarcode.startScanForResult(context, options)
      return result.originalValue

    } catch (error) {
      hilog.error(ScanService.DOMAIN, ScanService.TAG, `Barcode scan failed: ${error}`)
      return undefined
    }
  }

  /**
   * 从图片中识别码
   */
  static async detectFromImage(imagePath: string): Promise<scanBarcode.ScanResult[]> {
    try {
      const options: scanBarcode.DetectOptions = {
        scanTypes: [scanCore.ScanType.ALL],
        enableMultiMode: true  // 支持多码识别
      }

      // 创建图片输入流
      const inputImage: scanBarcode.InputImage = {
        uri: imagePath
      }

      const results = await scanBarcode.detect(inputImage, options)
      hilog.info(ScanService.DOMAIN, ScanService.TAG, 
        `Detected ${results.length} codes from image`)
      return results

    } catch (error) {
      hilog.error(ScanService.DOMAIN, ScanService.TAG, `Detect failed: ${error}`)
      return []
    }
  }

  /**
   * 生成二维码
   */
  static async generateQRCode(content: string, size: number = 256): Promise<image.PixelMap | undefined> {
    try {
      const options: scanBarcode.CreateOptions = {
        scanType: scanCore.ScanType.QR_CODE,
        width: size,
        height: size
      }

      const pixelMap = await scanBarcode.createBarcode(content, options)
      hilog.info(ScanService.DOMAIN, ScanService.TAG, 'QR code generated')
      return pixelMap

    } catch (error) {
      hilog.error(ScanService.DOMAIN, ScanService.TAG, `Generate QR failed: ${error}`)
      return undefined
    }
  }
}
```

### 使用示例

```typescript
// 在 ViewModel 中使用
@ObservedV2
export class ScanViewModel extends BaseViewModel {
  @Trace scanResult: string = ''
  @Trace qrCodeImage: PixelMap | undefined = undefined

  async startScan(context: common.UIAbilityContext): Promise<void> {
    await this.executeAsync(
      async () => {
        const result = await ScanService.startDefaultScan(context)
        if (!result) {
          throw new Error('未识别到内容')
        }
        return result
      },
      (result) => {
        this.scanResult = result
        // 处理扫码结果
        this.handleScanResult(result)
      }
    )
  }

  async generateQRCode(content: string): Promise<void> {
    await this.executeAsync(
      async () => ScanService.generateQRCode(content, 300),
      (pixelMap) => {
        this.qrCodeImage = pixelMap
      }
    )
  }

  private handleScanResult(result: string): void {
    // 根据扫码结果类型处理
    if (result.startsWith('http')) {
      // URL - 可以跳转或在 WebView 打开
    } else {
      // 其他内容
    }
  }
}

// 在页面中使用
@Entry
@Component
struct ScanPage {
  @State viewModel: ScanViewModel = new ScanViewModel()
  private context = getContext(this) as common.UIAbilityContext

  build() {
    Column() {
      Button('扫一扫')
        .onClick(() => this.viewModel.startScan(this.context))
        .accessibilityText('启动扫码')

      if (this.viewModel.scanResult) {
        Text(`扫码结果: ${this.viewModel.scanResult}`)
          .fontSize($r('app.float.font_size_md'))
          .margin({ top: 20 })
      }

      // 显示生成的二维码
      if (this.viewModel.qrCodeImage) {
        Image(this.viewModel.qrCodeImage)
          .width(200)
          .height(200)
          .margin({ top: 20 })
          .accessibilityText('生成的二维码')
      }
    }
    .width('100%')
    .padding($r('app.float.spacing_lg'))
  }
}
```

### 权限配置

在 `module.json5` 中添加相机权限：

```json
{
  "module": {
    "requestPermissions": [
      {
        "name": "ohos.permission.CAMERA",
        "reason": "$string:camera_permission_reason",
        "usedScene": {
          "abilities": ["EntryAbility"],
          "when": "inuse"
        }
      }
    ]
  }
}
```

在 `string.json` 中添加权限说明：

```json
{
  "string": [
    {
      "name": "camera_permission_reason",
      "value": "需要使用相机进行扫码"
    }
  ]
}
```

---

## Kit 集成决策流程图

```
┌──────────────────────────────────────────────────────────────┐
│                      用户需求分析                              │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│   需要用户登录?  ──Yes──►  Account Kit                        │
│       │                                                      │
│       No                                                     │
│       ▼                                                      │
│   需要消息推送?  ──Yes──►  Push Kit                           │
│       │                                                      │
│       No                                                     │
│       ▼                                                      │
│   需要分享功能?  ──Yes──►  Share Kit                          │
│       │                                                      │
│       No                                                     │
│       ▼                                                      │
│   需要扫码识别?  ──Yes──►  Scan Kit                           │
│       │                                                      │
│       No                                                     │
│       ▼                                                      │
│   其他系统能力   ──────►   查阅官方 Kit 文档                   │
└──────────────────────────────────────────────────────────────┘
```

---

## 常见问题排查

### Account Kit

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 登录返回空 | 未在 AGC 开通服务 | 登录 AGC 控制台开通 Account Kit |
| State 不匹配 | 请求被篡改 | 检查网络环境，重新发起请求 |

### Push Kit

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 获取 Token 失败 | 设备不支持 HMS | 检查是否为华为设备 |
| 推送不到达 | Token 过期 | 重新获取 Token 并上报 |

### Share Kit

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 分享面板不显示 | Context 类型错误 | 使用 UIAbilityContext |
| 文件分享失败 | 路径权限问题 | 确保使用沙箱路径或 fileUri |

### Scan Kit

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 相机权限被拒 | 未请求权限 | 先请求 CAMERA 权限 |
| 识别率低 | 光线/角度问题 | 提示用户调整拍摄条件 |

---

## 服务依赖配置

确保在 `oh-package.json5` 中已添加相关 Kit 依赖（大部分 Kit 已内置于系统，无需额外添加）。

在 AGC 控制台需要开通的服务：
- Account Kit: 需要开通并配置应用
- Push Kit: 需要开通并配置推送证书
- Share Kit: 无需开通
- Scan Kit: 无需开通
