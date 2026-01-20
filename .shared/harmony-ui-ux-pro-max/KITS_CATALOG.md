# HarmonyOS NEXT Kit 完整目录

> 基于 [华为开发者文档中心](https://developer.huawei.com/consumer/cn/doc/) 整理

## 快速索引

根据用户需求快速定位所需 Kit：

| 需求关键词 | 推荐 Kit | 导入路径 |
|-----------|---------|---------|
| 登录、账号 | Account Kit | `@kit.AccountKit` |
| 支付、购买 | IAP Kit / Payment Kit | `@kit.IAPKit` / `@kit.PaymentKit` |
| 推送、消息 | Push Kit / Notification Kit | `@kit.PushKit` |
| 定位、位置 | Location Kit | `@kit.LocationKit` |
| 地图、导航 | Map Kit | `@kit.MapKit` |
| 扫码、二维码 | Scan Kit | `@kit.ScanKit` |
| 分享 | Share Kit | `@kit.ShareKit` |
| 相机、拍照 | Camera Kit | `@kit.CameraKit` |
| 音频、播放 | Audio Kit / Media Kit | `@kit.AudioKit` |
| 视频、录制 | Media Kit / AVCodec Kit | `@kit.MediaKit` |
| 图片、处理 | Image Kit | `@kit.ImageKit` |
| 文件、存储 | Core File Kit | `@kit.CoreFileKit` |
| 数据库 | ArkData | `@ohos.data.relationalStore` |
| 网络、HTTP | Network Kit | `@kit.NetworkKit` |
| 日历、日程 | Calendar Kit | `@kit.CalendarKit` |
| 联系人 | Contacts Kit | `@kit.ContactsKit` |
| 实况窗、进度 | Live View Kit | `@kit.LiveViewKit` |
| 卡片、Widget | Form Kit | `@kit.FormKit` |
| 后台任务 | Background Tasks Kit | `@kit.BackgroundTasksKit` |
| 语音识别 | Core Speech Kit | `@kit.CoreSpeechKit` |
| 文字识别、OCR | Core Vision Kit | `@kit.CoreVisionKit` |
| 人脸检测 | Core Vision Kit | `@kit.CoreVisionKit` |
| 指纹、人脸认证 | User Authentication Kit | `@kit.UserAuthenticationKit` |
| 加密、安全 | Crypto Architecture Kit | `@kit.CryptoArchitectureKit` |
| 蓝牙、WiFi | Connectivity Kit | `@kit.ConnectivityKit` |
| 分布式、跨设备 | Distributed Service Kit | `@kit.DistributedServiceKit` |
| 穿戴设备 | Wear Engine Kit | `@kit.WearEngineKit` |
| AR、增强现实 | AR Engine | `@kit.AREngine` |
| 智能体、AI助手 | Agent Framework Kit | `@kit.AgentFrameworkKit` |

---

## 一、应用框架类 Kit

### Ability Kit (程序框架)
```typescript
import { UIAbility, AbilityConstant, Want } from '@kit.AbilityKit';
```
**能力**: 应用生命周期管理、Ability 组件、Stage 模型
**适用场景**: 所有应用的基础框架

### ArkUI (UI 框架)
```typescript
// 内置，无需显式导入
@Component
struct MyComponent {
  build() { /* ... */ }
}
```
**能力**: 声明式 UI、组件系统、状态管理
**适用场景**: 所有 UI 开发

### ArkData (数据管理)
```typescript
import { relationalStore } from '@ohos.data.relationalStore';
import { preferences } from '@ohos.data.preferences';
import { distributedKVStore } from '@ohos.data.distributedKVStore';
```
**能力**: 关系型数据库(RDB)、首选项(Preferences)、分布式 KV 存储
**适用场景**: 本地数据持久化、配置存储、分布式数据同步

### Form Kit (卡片开发)
```typescript
import { formProvider, formInfo } from '@kit.FormKit';
```
**能力**: 卡片创建、更新、删除
**适用场景**: 桌面卡片、负一屏卡片、元服务卡片

### Background Tasks Kit (后台任务)
```typescript
import { backgroundTaskManager } from '@kit.BackgroundTasksKit';
import { reminderAgentManager } from '@kit.BackgroundTasksKit';
```
**能力**: 短时任务、长时任务、延迟任务、提醒代理
**适用场景**: 后台下载、音乐播放、定时提醒

### Localization Kit (国际化)
```typescript
import { i18n } from '@kit.LocalizationKit';
```
**能力**: 多语言、日期格式、数字格式
**适用场景**: 多语言应用

---

## 二、系统服务类 Kit

### Basic Services Kit (基础服务)
```typescript
import { bundleManager } from '@kit.BasicServicesKit';
import { wantAgent } from '@kit.BasicServicesKit';
import { BusinessError } from '@kit.BasicServicesKit';
```
**能力**: 包管理、意图代理、错误处理
**适用场景**: 应用信息获取、跨应用交互

### Network Kit (网络服务)
```typescript
import { http } from '@kit.NetworkKit';
import { socket } from '@kit.NetworkKit';
import { webSocket } from '@kit.NetworkKit';
```
**能力**: HTTP 请求、Socket 通信、WebSocket
**适用场景**: 网络数据请求

### Connectivity Kit (短距通信)
```typescript
import { bluetooth } from '@kit.ConnectivityKit';
import { wifiManager } from '@kit.ConnectivityKit';
```
**能力**: 蓝牙、WiFi、NFC
**适用场景**: 设备连接、数据传输

### Distributed Service Kit (分布式服务)
```typescript
import { distributedDeviceManager } from '@kit.DistributedServiceKit';
import { distributedHardware } from '@kit.DistributedServiceKit';
```
**能力**: 设备发现、设备管理、硬件共享
**适用场景**: 多设备协同、跨设备操作

### User Authentication Kit (用户认证)
```typescript
import { userAuth } from '@kit.UserAuthenticationKit';
```
**能力**: 人脸识别、指纹识别、PIN 码
**适用场景**: 身份验证、支付确认

### Crypto Architecture Kit (加解密)
```typescript
import { cryptoFramework } from '@kit.CryptoArchitectureKit';
```
**能力**: 加密、解密、签名、哈希
**适用场景**: 数据加密、安全传输

### Sensor Service Kit (传感器)
```typescript
import { sensor } from '@kit.SensorServiceKit';
import { vibrator } from '@kit.SensorServiceKit';
```
**能力**: 加速度、陀螺仪、光线、振动
**适用场景**: 运动检测、游戏控制、触感反馈

---

## 三、媒体类 Kit

### Camera Kit (相机)
```typescript
import { camera } from '@kit.CameraKit';
```
**能力**: 拍照、录像、预览
**适用场景**: 相机应用、扫码、人脸采集

### Audio Kit (音频)
```typescript
import { audio } from '@kit.AudioKit';
```
**能力**: 音频播放、录制、音效
**适用场景**: 音乐播放、语音录制、音频处理

### Media Kit (媒体)
```typescript
import { media } from '@kit.MediaKit';
```
**能力**: AVPlayer、AVRecorder
**适用场景**: 视频播放、音视频录制

### Image Kit (图片)
```typescript
import { image } from '@kit.ImageKit';
```
**能力**: 图片解码、编辑、转换
**适用场景**: 图片查看、编辑、压缩

### Media Library Kit (媒体库)
```typescript
import { photoAccessHelper } from '@kit.MediaLibraryKit';
```
**能力**: 相册访问、媒体文件管理
**适用场景**: 相册选择、媒体浏览

### Scan Kit (扫码)
```typescript
import { scanCore, scanBarcode } from '@kit.ScanKit';
```
**能力**: 二维码/条形码扫描、生成
**适用场景**: 扫一扫、商品扫描、支付码

---

## 四、应用服务类 Kit

### Account Kit (华为账号)
```typescript
import { authentication } from '@kit.AccountKit';
```
**能力**: 华为账号登录、授权
**适用场景**: 用户登录、一键登录

### IAP Kit (应用内支付)
```typescript
import { iap } from '@kit.IAPKit';
```
**能力**: 商品购买、订阅、消耗品
**适用场景**: 虚拟商品购买、VIP 订阅

### Payment Kit (华为支付)
```typescript
import { paymentService } from '@kit.PaymentKit';
```
**能力**: 实体商品支付、服务支付
**适用场景**: 电商支付、服务付费

### Push Kit (推送)
```typescript
import { pushService } from '@kit.PushKit';
```
**能力**: 消息推送、Token 管理
**适用场景**: 消息通知、营销推送

### Notification Kit (通知)
```typescript
import { notificationManager } from '@kit.NotificationKit';
```
**能力**: 本地通知发布、管理
**适用场景**: 本地提醒、状态通知

### Location Kit (位置)
```typescript
import { geoLocationManager } from '@kit.LocationKit';
```
**能力**: 定位、地理编码、地理围栏
**适用场景**: 位置获取、附近搜索

### Map Kit (地图)
```typescript
import { map, mapCommon } from '@kit.MapKit';
```
**能力**: 地图展示、标记、路线规划
**适用场景**: 地图展示、导航

### Live View Kit (实况窗) ⭐
```typescript
import { liveViewManager } from '@kit.LiveViewKit';
```
**能力**: 锁屏/状态栏实时状态展示
**适用场景**: 外卖配送、打车进度、航班动态

### Share Kit (分享) ⭐
```typescript
import { systemShare } from '@kit.ShareKit';
```
**能力**: 跨应用内容分享、碰一碰分享
**适用场景**: 分享到社交应用、文件传输

### Calendar Kit (日历)
```typescript
import { calendarManager } from '@kit.CalendarKit';
```
**能力**: 日程创建、查询、提醒
**适用场景**: 日程管理、会议提醒

---

## 五、AI 类 Kit

### Core Speech Kit (基础语音)
```typescript
import { speechRecognizer } from '@kit.CoreSpeechKit';
import { textToSpeech } from '@kit.CoreSpeechKit';
```
**能力**: 语音识别(ASR)、语音合成(TTS)
**适用场景**: 语音输入、语音播报

### Core Vision Kit (基础视觉)
```typescript
import { textRecognition } from '@kit.CoreVisionKit';
import { faceDetector } from '@kit.CoreVisionKit';
```
**能力**: 文字识别(OCR)、人脸检测、图像分类
**适用场景**: 文档扫描、人脸识别、图像分析

### Speech Kit (场景化语音)
```typescript
import { readAloud } from '@kit.SpeechKit';
import { aiCaption } from '@kit.SpeechKit';
```
**能力**: 朗读控件、AI 字幕
**适用场景**: 文章朗读、视频字幕

### Vision Kit (场景化视觉)
```typescript
import { documentScanner } from '@kit.VisionKit';
import { cardRecognition } from '@kit.VisionKit';
```
**能力**: 文档扫描、卡证识别
**适用场景**: 拍照识别、证件采集

### Natural Language Kit (自然语言)
```typescript
import { textProcessing } from '@kit.NaturalLanguageKit';
```
**能力**: 分词、实体识别、情感分析
**适用场景**: 文本分析、智能搜索

### Agent Framework Kit (智能体框架) ⭐
```typescript
import { agentFramework } from '@kit.AgentFrameworkKit';
```
**能力**: 智能体调用、AI 助手集成
**适用场景**: 智能客服、AI 问答

### Intents Kit (意图框架)
```typescript
import { insightIntent } from '@kit.IntentsKit';
```
**能力**: 意图注册、意图触发
**适用场景**: 小艺建议、智能推荐

---

## 六、图形类 Kit

### ArkGraphics 2D
```typescript
import { drawing } from '@kit.ArkGraphics2D';
```
**能力**: 2D 绑制、图形渲染
**适用场景**: 自定义绘图、图表

### ArkGraphics 3D
```typescript
import { scene } from '@kit.ArkGraphics3D';
```
**能力**: 3D 场景渲染
**适用场景**: 3D 展示、游戏

### AR Engine
```typescript
import { arSession } from '@kit.AREngine';
```
**能力**: 增强现实、平面检测
**适用场景**: AR 应用、虚拟试穿

---

## Kit 选择决策树

```
┌─────────────────────────────────────────────────────────────┐
│                    用户需求分析                              │
└─────────────────────────────────────────────────────────────┘
                              │
     ┌────────────────────────┼────────────────────────────────┐
     ▼                        ▼                                ▼
┌─────────┐            ┌─────────────┐                  ┌─────────────┐
│ 用户体验 │            │   功能实现   │                  │  数据处理   │
└─────────┘            └─────────────┘                  └─────────────┘
     │                        │                                │
┌────┼────┐              ┌────┼────┐                      ┌────┼────┐
│    │    │              │    │    │                      │    │    │
▼    ▼    ▼              ▼    ▼    ▼                      ▼    ▼    ▼
登录  支付  通知         相机  地图  分享                数据库 网络 文件
│    │    │              │    │    │                      │    │    │
▼    ▼    ▼              ▼    ▼    ▼                      ▼    ▼    ▼
Account IAP Push      Camera Map Share               ArkData Network CoreFile
Kit    Kit  Kit         Kit  Kit  Kit                 (RDB)   Kit    Kit
```

---

## 权限配置参考

### 常用权限列表

| 功能 | 权限名称 | 说明 |
|------|---------|------|
| 网络访问 | `ohos.permission.INTERNET` | HTTP 请求 |
| 定位 | `ohos.permission.LOCATION` | 获取位置 |
| 相机 | `ohos.permission.CAMERA` | 拍照录像 |
| 麦克风 | `ohos.permission.MICROPHONE` | 录音 |
| 读取媒体 | `ohos.permission.READ_MEDIA` | 访问相册 |
| 蓝牙 | `ohos.permission.ACCESS_BLUETOOTH` | 蓝牙连接 |
| 通知 | `ohos.permission.NOTIFICATION_CONTROLLER` | 发送通知 |
| 分布式 | `ohos.permission.DISTRIBUTED_DATASYNC` | 跨设备同步 |
| 日历 | `ohos.permission.READ_CALENDAR` | 读取日历 |
| 联系人 | `ohos.permission.READ_CONTACTS` | 读取联系人 |

### module.json5 权限配置示例

```json5
{
  "module": {
    "requestPermissions": [
      {
        "name": "ohos.permission.INTERNET"
      },
      {
        "name": "ohos.permission.LOCATION",
        "reason": "$string:location_reason",
        "usedScene": {
          "abilities": ["EntryAbility"],
          "when": "inuse"
        }
      }
    ]
  }
}
```
