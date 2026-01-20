# HarmonyOS NEXT 行业实践指南

> 基于 [华为开发者文档中心 - 行业实践](https://developer.huawei.com/consumer/cn/doc/) 整理

## 概述

本文档汇总了 17 个行业的开发实践和常见场景解决方案。

---

## 行业速查表

| 行业 | 典型功能 | 核心 Kit | 参考链接 |
|------|---------|---------|---------|
| 购物比价 | 商品列表、购物车、支付 | IAP Kit, Payment Kit, Map Kit | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/practice-purchase-app-architecture-v1-0000002077367333) |
| 外卖美食 | 商家导航、实况窗配送 | Map Kit, Live View Kit, Location Kit | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/practice-food-app-architecture-v1-0000002041168222) |
| 出行打车 | 定位、地图、实况窗 | Location Kit, Map Kit, Live View Kit | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/practice-bus-app-architecture-v1-0000001938172420) |
| 社交通讯 | 表情包、语音通话 | Media Kit, Core Speech Kit, Push Kit | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/practice-socialcontact-app-architecture-v1-0000002077325925) |
| 影音娱乐 | 视频播放、音频控制 | Media Kit, Audio Kit, AVSession Kit | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/practice-audio-app-architecture-v1-0000002041168218) |
| 新闻阅读 | 富文本、翻页阅读 | ArkUI, Reader Kit | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/practice-news-app-architecture-v1-0000001938013088) |
| 理财保险 | K线图、股票键盘 | ArkGraphics 2D, Crypto Kit | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/practice-insurance-app-architecture-v1-0000001938013084) |
| 综合办公 | 会议、考勤打卡 | Calendar Kit, Location Kit, Camera Kit | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/practice-office-app-architecture-v1-0000001965211649) |
| 运动健康 | 运动数据、计时器 | Health Service Kit, Sensor Kit | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/practice-sports-health-app-architecture-v1-0000001952522073) |
| 教育学习 | 课程表、刷题 | ArkUI, Core Vision Kit | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/practice-educate-app-architecture-v1-0000001904563108) |
| 拍摄美化 | 滤镜、图片编辑 | Camera Kit, Image Kit | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/practice-photo-app-architecture-v1-0000002077325929) |
| 旅游园区 | 景点地图、导览 | Map Kit, Location Kit | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/practice-tourist-park-app-architecture-v1-0000001965211653) |
| 孕育健康 | 成长记录、曲线图 | ArkGraphics 2D, Calendar Kit | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/practice-health-app-architecture-v1-0000001938172424) |
| 儿童教育 | 防沉迷、练字板 | Pen Kit, Screen Time Guard Kit | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/practice-kids-app-architecture-v1-0000001965371453) |
| 便捷生活 | 电影选座、日程 | Calendar Kit, Scenario Fusion Kit | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/practice-convenient-life-app-architecture-v1-0000001952539489) |
| 实用工具 | 悬浮球、工具集 | ArkUI, Core File Kit | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/practice-tools-app-architecture-v1-0000002041326514) |
| 汽车出行 | 车载交互、弹窗 | Car Kit, ArkUI | [官方文档](https://developer.huawei.com/consumer/cn/doc/architecture-guides/shaking_to_dialog-0000001903742656) |

---

## 一、购物比价类

### 典型功能

| 功能 | 实现方案 | 核心组件 |
|------|---------|---------|
| 商品列表 | LazyForEach + 瀑布流 | WaterFlow, LazyForEach |
| 商品详情 | 图片轮播 + 规格选择 | Swiper, BottomSheet |
| 购物车 | 状态管理 + 动画 | @Observed, getUIContext().animateTo |
| 支付下单 | IAP Kit / Payment Kit | iap.purchase() |
| 搜索筛选 | 联想搜索 + 标签 | Search, Chip |

### 代码片段

```typescript
// 商品列表 - 瀑布流布局
@Component
struct ProductWaterfall {
  @State dataSource: ProductDataSource = new ProductDataSource()

  build() {
    WaterFlow() {
      LazyForEach(this.dataSource, (item: Product) => {
        FlowItem() {
          ProductCard({ product: item })
        }
      }, (item: Product) => item.id)
    }
    .columnsTemplate('1fr 1fr')
    .columnsGap(8)
    .rowsGap(8)
  }
}

// 规格选择弹窗
@Builder
specificationSheet() {
  Column() {
    // 规格选项
    ForEach(this.specifications, (spec: Specification) => {
      Row() {
        Text(spec.name)
        Blank()
        ForEach(spec.options, (option: string) => {
          Chip({ label: option })
            .selected(this.selected[spec.name] === option)
            .onClick(() => this.selectSpec(spec.name, option))
        })
      }
    })
    
    // 加入购物车
    Button($r('app.string.add_to_cart'))
      .onClick(() => this.addToCart())
  }
}
```

---

## 二、外卖美食类

### 典型功能

| 功能 | 实现方案 | 核心组件 |
|------|---------|---------|
| 商家列表 | 位置排序 + 距离计算 | Location Kit, List |
| 商家导航 | 地图 + 路线规划 | Map Kit |
| 配送进度 | 实况窗 + 地图标记 | Live View Kit |
| 城市选择 | 定位 + 城市列表 | Location Kit, AlphabetIndexer |

### 实况窗配送进度

```typescript
// 创建实况窗
import { liveViewManager } from '@kit.LiveViewKit';

async function createDeliveryLiveView(order: Order): Promise<void> {
  const liveView: liveViewManager.LiveView = {
    id: order.id,
    event: 'delivery_progress',
    liveViewData: {
      primary: {
        title: '外卖配送中',
        content: [{
          text: `骑手已取餐，预计 ${order.estimatedTime} 送达`
        }],
        progress: {
          percentage: order.progress,
          progressColor: '#0A59F7'
        }
      }
    }
  };
  
  await liveViewManager.startLiveView(liveView);
}

// 更新进度
async function updateProgress(orderId: string, progress: number): Promise<void> {
  await liveViewManager.updateLiveView({
    id: orderId,
    liveViewData: {
      primary: {
        progress: { percentage: progress }
      }
    }
  });
}
```

---

## 三、社交通讯类

### 典型功能

| 功能 | 实现方案 | 核心组件 |
|------|---------|---------|
| 消息列表 | 虚拟列表 + 分页 | LazyForEach, List |
| 表情包 | Grid + 动态加载 | Grid, Image |
| 语音消息 | 录音 + 播放 | Audio Kit |
| 语音通话 | VoIP | Call Service Kit |
| 图片选择 | 相册访问 | Media Library Kit |
| 好友推荐 | AI 推荐 | Intents Kit |

### 语音消息录制

```typescript
import { audio } from '@kit.AudioKit';

@Component
struct VoiceRecorder {
  private audioCapturer: audio.AudioCapturer | null = null
  @State isRecording: boolean = false
  @State duration: number = 0

  async startRecording(): Promise<void> {
    const options: audio.AudioCapturerOptions = {
      streamInfo: {
        samplingRate: audio.AudioSamplingRate.SAMPLE_RATE_16000,
        channels: audio.AudioChannel.CHANNEL_1,
        sampleFormat: audio.AudioSampleFormat.SAMPLE_FORMAT_S16LE,
        encodingType: audio.AudioEncodingType.ENCODING_TYPE_RAW
      },
      capturerInfo: {
        source: audio.SourceType.SOURCE_TYPE_MIC,
        capturerFlags: 0
      }
    };
    
    this.audioCapturer = await audio.createAudioCapturer(options);
    await this.audioCapturer.start();
    this.isRecording = true;
    
    // 开始计时
    this.startTimer();
  }

  async stopRecording(): Promise<ArrayBuffer> {
    if (this.audioCapturer) {
      await this.audioCapturer.stop();
      await this.audioCapturer.release();
      this.isRecording = false;
    }
    return this.audioData;
  }

  build() {
    Column() {
      if (this.isRecording) {
        // 录音波形动画
        VoiceWaveform()
        Text(`${this.duration}s`)
      }
      
      Button(this.isRecording ? '松开发送' : '按住说话')
        .onTouch((event) => {
          if (event.type === TouchType.Down) {
            this.startRecording();
          } else if (event.type === TouchType.Up) {
            this.stopRecording();
          }
        })
    }
  }
}
```

---

## 四、影音娱乐类

### 典型功能

| 功能 | 实现方案 | 核心组件 |
|------|---------|---------|
| 视频播放 | AVPlayer + 控制器 | Media Kit, Video |
| 横竖屏切换 | 窗口旋转 | Window API |
| 后台播放 | AVSession + 后台任务 | AVSession Kit |
| 进度拖动 | Slider + 缩略图 | Slider |
| 弹幕 | Canvas 绘制 | Canvas |

### 视频播放器

```typescript
import { media } from '@kit.MediaKit';
import { window } from '@kit.ArkUI';

@Entry
@Component
struct VideoPlayerPage {
  private avPlayer: media.AVPlayer | null = null
  @State isPlaying: boolean = false
  @State currentTime: number = 0
  @State duration: number = 0
  @State isFullscreen: boolean = false

  async initPlayer(url: string): Promise<void> {
    this.avPlayer = await media.createAVPlayer();
    
    this.avPlayer.on('stateChange', (state) => {
      if (state === 'prepared') {
        this.duration = this.avPlayer!.duration;
      }
    });
    
    this.avPlayer.on('timeUpdate', (time) => {
      this.currentTime = time;
    });
    
    this.avPlayer.url = url;
    await this.avPlayer.prepare();
  }

  toggleFullscreen(): void {
    const win = window.getLastWindow(getContext(this));
    if (this.isFullscreen) {
      win.then(w => w.setPreferredOrientation(window.Orientation.PORTRAIT));
    } else {
      win.then(w => w.setPreferredOrientation(window.Orientation.LANDSCAPE));
    }
    this.isFullscreen = !this.isFullscreen;
  }

  build() {
    Stack() {
      // 视频画面
      XComponent({ id: 'video', type: 'surface' })
        .onLoad(() => {
          this.avPlayer?.setDisplaySurface(this.surfaceId);
        })
      
      // 控制栏
      VideoControls({
        isPlaying: this.isPlaying,
        currentTime: this.currentTime,
        duration: this.duration,
        onPlay: () => this.avPlayer?.play(),
        onPause: () => this.avPlayer?.pause(),
        onSeek: (time) => this.avPlayer?.seek(time),
        onFullscreen: () => this.toggleFullscreen()
      })
    }
  }
}
```

---

## 五、综合办公类

### 典型功能

| 功能 | 实现方案 | 核心组件 |
|------|---------|---------|
| 会议创建 | 日历 + 通知 | Calendar Kit, Notification Kit |
| 考勤打卡 | 定位 + 地理围栏 | Location Kit |
| 证件照 | 相机 + 人脸检测 | Camera Kit, Core Vision Kit |
| 文档预览 | PDF 渲染 | PDF Kit, Preview Kit |
| 扫描文档 | 文档扫描 | Vision Kit |

### 考勤打卡

```typescript
import { geoLocationManager } from '@kit.LocationKit';

@Component
struct AttendancePage {
  @State currentLocation: geoLocationManager.Location | null = null
  @State isInRange: boolean = false
  private officeLocation = { latitude: 39.9, longitude: 116.3 }
  private checkRadius = 100 // 100米范围

  aboutToAppear(): void {
    this.startLocationUpdate();
  }

  async startLocationUpdate(): Promise<void> {
    const request: geoLocationManager.CurrentLocationRequest = {
      priority: geoLocationManager.LocationRequestPriority.ACCURACY,
      scenario: geoLocationManager.LocationRequestScenario.DAILY_LIFE_SERVICE
    };
    
    geoLocationManager.on('locationChange', request, (location) => {
      this.currentLocation = location;
      this.checkInRange(location);
    });
  }

  checkInRange(location: geoLocationManager.Location): void {
    const distance = this.calculateDistance(
      location.latitude, location.longitude,
      this.officeLocation.latitude, this.officeLocation.longitude
    );
    this.isInRange = distance <= this.checkRadius;
  }

  build() {
    Column() {
      // 地图显示当前位置
      MapComponent({
        center: this.currentLocation,
        markers: [this.officeLocation]
      })
      
      // 打卡按钮
      Button(this.isInRange ? '打卡' : '不在打卡范围内')
        .enabled(this.isInRange)
        .onClick(() => this.clockIn())
    }
  }
}
```

---

## 六、运动健康类

### 典型功能

| 功能 | 实现方案 | 核心组件 |
|------|---------|---------|
| 运动数据 | 传感器 + 算法 | Sensor Kit, Health Service Kit |
| 计时器 | 高精度计时 | Timer |
| 轨迹记录 | 定位 + 地图 | Location Kit, Map Kit |
| 心率监测 | 穿戴设备 | Wear Engine Kit |
| 成绩排行 | 云数据库 | Cloud Foundation Kit |

### 运动计时器

```typescript
@Component
struct ExerciseTimer {
  @State hours: number = 0
  @State minutes: number = 0
  @State seconds: number = 0
  @State isRunning: boolean = false
  private timerId: number = 0

  start(): void {
    this.isRunning = true;
    this.timerId = setInterval(() => {
      this.seconds++;
      if (this.seconds >= 60) {
        this.seconds = 0;
        this.minutes++;
      }
      if (this.minutes >= 60) {
        this.minutes = 0;
        this.hours++;
      }
    }, 1000);
  }

  pause(): void {
    this.isRunning = false;
    clearInterval(this.timerId);
  }

  build() {
    Column() {
      // 时间显示
      Row() {
        Text(this.formatTime(this.hours))
          .fontSize(60)
          .fontWeight(FontWeight.Bold)
        Text(':').fontSize(60)
        Text(this.formatTime(this.minutes))
          .fontSize(60)
          .fontWeight(FontWeight.Bold)
        Text(':').fontSize(60)
        Text(this.formatTime(this.seconds))
          .fontSize(60)
          .fontWeight(FontWeight.Bold)
      }
      
      // 控制按钮
      Row({ space: 20 }) {
        Button(this.isRunning ? '暂停' : '开始')
          .onClick(() => this.isRunning ? this.pause() : this.start())
        
        Button('重置')
          .onClick(() => {
            this.pause();
            this.hours = this.minutes = this.seconds = 0;
          })
      }
    }
  }

  formatTime(value: number): string {
    return value.toString().padStart(2, '0');
  }
}
```

---

## 七、教育学习类

### 典型功能

| 功能 | 实现方案 | 核心组件 |
|------|---------|---------|
| 课程表 | 双向滚动 | Scroll + Grid |
| 刷题滑动 | Swiper + 翻页 | Swiper |
| 拍照搜题 | OCR 识别 | Core Vision Kit |
| 直播课堂 | 实时音视频 | Media Kit |
| 错题本 | 本地存储 | ArkData |

### 双向滚动课程表

```typescript
@Component
struct CourseSchedule {
  private weekDays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  private timeSlots = ['8:00', '9:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00']
  @State courses: Course[][] = []

  build() {
    Column() {
      // 表头 - 星期
      Row() {
        Text('').width(60)
        ForEach(this.weekDays, (day: string) => {
          Text(day)
            .width(80)
            .textAlign(TextAlign.Center)
        })
      }
      
      // 课程表主体 - 双向滚动
      Scroll() {
        Column() {
          ForEach(this.timeSlots, (time: string, rowIndex: number) => {
            Row() {
              // 时间列
              Text(time)
                .width(60)
                .textAlign(TextAlign.Center)
              
              // 课程格子
              ForEach(this.weekDays, (_: string, colIndex: number) => {
                this.courseCell(rowIndex, colIndex)
              })
            }
            .height(80)
          })
        }
      }
      .scrollable(ScrollDirection.Vertical)
    }
  }

  @Builder
  courseCell(row: number, col: number) {
    Column() {
      if (this.courses[row]?.[col]) {
        Text(this.courses[row][col].name)
          .fontSize(12)
        Text(this.courses[row][col].location)
          .fontSize(10)
          .fontColor($r('app.color.text_secondary'))
      }
    }
    .width(80)
    .height('100%')
    .backgroundColor(this.courses[row]?.[col] 
      ? this.courses[row][col].color 
      : $r('app.color.bg_secondary'))
    .borderRadius(4)
    .margin(2)
  }
}
```

---

## 公共技术方案

### 用户协议弹窗

```typescript
@CustomDialog
struct PrivacyAgreementDialog {
  controller: CustomDialogController
  onAgree: () => void = () => {}

  build() {
    Column() {
      Text('用户协议与隐私政策')
        .fontSize(18)
        .fontWeight(FontWeight.Bold)
      
      Scroll() {
        Text($r('app.string.privacy_policy_content'))
          .fontSize(14)
      }
      .height(300)
      
      Row({ space: 12 }) {
        Button('不同意')
          .backgroundColor($r('app.color.bg_secondary'))
          .fontColor($r('app.color.text_primary'))
          .onClick(() => this.controller.close())
        
        Button('同意')
          .onClick(() => {
            this.onAgree();
            this.controller.close();
          })
      }
    }
    .padding(20)
  }
}
```

### 主题颜色自定义

```typescript
// 主题管理器
class ThemeManager {
  private static instance: ThemeManager;
  private currentTheme: string = 'default';
  
  static getInstance(): ThemeManager {
    if (!ThemeManager.instance) {
      ThemeManager.instance = new ThemeManager();
    }
    return ThemeManager.instance;
  }
  
  setTheme(theme: string): void {
    this.currentTheme = theme;
    // 触发全局状态更新
    AppStorage.setOrCreate('currentTheme', theme);
  }
  
  getPrimaryColor(): ResourceColor {
    const themes: Record<string, ResourceColor> = {
      'default': '#0A59F7',
      'green': '#64BB5C',
      'orange': '#FF6B35',
      'purple': '#8B5CF6'
    };
    return themes[this.currentTheme] || themes['default'];
  }
}
```
