// ==========================================
// HarmonyBaby Care - 首页/今日概览
// ==========================================

import { TodayStats, QuickRecordItem, FeedingRecord, SleepRecord, DiaperRecord } from '../models/DataModels'

/**
 * 首页 - 今日概览
 * 展示宝宝今日状态、快速记录入口、最近记录和智能建议
 */
@Entry
@Component
struct HomePage {
  // ==================== 状态管理 ====================
  @State babyName: string = '小宝贝'
  @State babyAgeText: string = '5个月12天'

  @State todayStats: TodayStats = {
    feedingCount: 5,
    feedingTotalMl: 650,
    sleepTotalMinutes: 200,
    diaperCount: 4,
    lastTemperature: 36.5,
    nextFeedingEstimate: Date.now() + 2 * 60 * 60 * 1000,
    nextSleepEstimate: Date.now() + 1 * 60 * 60 * 1000
  }

  @State isTimerRunning: boolean = false
  @State timerSeconds: number = 0
  @State currentBreastSide: string = 'left'

  // ==================== 快速记录配置 ====================
  private quickRecordItems: QuickRecordItem[] = [
    {
      id: 'breast',
      icon: $r('sys.symbol.drop'),
      label: $r('app.string.breast_feeding'),
      color: $r('app.color.feeding'),
      bgColor: $r('app.color.feeding_light')
    },
    {
      id: 'bottle',
      icon: $r('sys.symbol.cup_and_saucer'),
      label: $r('app.string.bottle_feeding'),
      color: $r('app.color.feeding'),
      bgColor: $r('app.color.feeding_light')
    },
    {
      id: 'sleep',
      icon: $r('sys.symbol.moon'),
      label: $r('app.string.sleep'),
      color: $r('app.color.sleep'),
      bgColor: $r('app.color.sleep_light')
    },
    {
      id: 'diaper',
      icon: $r('sys.symbol.heart'),
      label: $r('app.string.diaper'),
      color: $r('app.color.diaper'),
      bgColor: $r('app.color.diaper_light')
    }
  ]

  // ==================== 生命周期 ====================
  aboutToAppear(): void {
    // 初始化数据加载
  }

  // ==================== 构建器 ====================
  build() {
    Column() {
      // 顶部导航栏
      this.NavBar()

      // 可滚动内容区
      Scroll() {
        Column({ space: 20 }) {
          // 今日概览卡片
          this.TodayOverviewCard()

          // 快速记录区域
          this.QuickRecordSection()

          // 喂养计时器（如果正在运行）
          if (this.isTimerRunning) {
            this.ActiveTimerCard()
          }

          // 智能建议
          this.SmartSuggestionCard()

          // 最近记录
          this.RecentRecordsSection()
        }
        .padding({
          left: 16,
          right: 16,
          top: 12,
          bottom: 24
        })
      }
      .layoutWeight(1)
      .scrollBar(BarState.Off)
      .edgeEffect(EdgeEffect.Spring)
    }
    .width('100%')
    .height('100%')
    .backgroundColor($r('app.color.bg_secondary'))
  }

  // ==================== 导航栏 ====================
  @Builder
  NavBar() {
    Row() {
      // 宝宝信息
      Row({ space: 12 }) {
        // 头像
        Image($r('app.media.baby_avatar'))
          .width(44)
          .height(44)
          .borderRadius(22)
          .objectFit(ImageFit.Cover)
          .backgroundColor($r('app.color.primary_light'))

        Column({ space: 2 }) {
          Text(this.getGreeting())
            .fontSize($r('app.float.font_body_small'))
            .fontColor($r('app.color.text_secondary'))

          Row({ space: 4 }) {
            Text(this.babyName)
              .fontSize($r('app.float.font_title_small'))
              .fontWeight(FontWeight.Bold)
              .fontColor($r('app.color.text_primary'))

            Text(`(${this.babyAgeText})`)
              .fontSize($r('app.float.font_body_small'))
              .fontColor($r('app.color.text_tertiary'))
          }
        }
        .alignItems(HorizontalAlign.Start)
      }

      Blank()

      // 语音按钮
      Button() {
        Image($r('sys.symbol.mic'))
          .width(24)
          .height(24)
          .fillColor($r('app.color.primary'))
      }
      .type(ButtonType.Circle)
      .width(44)
      .height(44)
      .backgroundColor($r('app.color.primary_light'))
      .onClick(() => this.onVoiceClick())
    }
    .width('100%')
    .height(64)
    .padding({ left: 16, right: 16 })
    .backgroundColor($r('app.color.bg_primary'))
  }

  // ==================== 今日概览卡片 ====================
  @Builder
  TodayOverviewCard() {
    Column({ space: 16 }) {
      // 标题行
      Row() {
        Text($r('app.string.today_overview'))
          .fontSize($r('app.float.font_title_small'))
          .fontWeight(FontWeight.Bold)
          .fontColor($r('app.color.text_primary'))

        Blank()

        Text(this.formatDate(Date.now()))
          .fontSize($r('app.float.font_body_small'))
          .fontColor($r('app.color.text_tertiary'))
      }
      .width('100%')

      // 统计数据网格
      Row() {
        // 喂养统计
        this.StatItem(
          $r('sys.symbol.drop'),
          $r('app.color.feeding'),
          `${this.todayStats.feedingCount}`,
          $r('app.string.times'),
          $r('app.string.feeding')
        )

        // 睡眠统计
        this.StatItem(
          $r('sys.symbol.moon'),
          $r('app.color.sleep'),
          this.formatMinutes(this.todayStats.sleepTotalMinutes),
          $r('app.string.unit_hour'),
          $r('app.string.sleep')
        )

        // 尿布统计
        this.StatItem(
          $r('sys.symbol.heart'),
          $r('app.color.diaper'),
          `${this.todayStats.diaperCount}`,
          $r('app.string.times'),
          $r('app.string.diaper')
        )

        // 体温
        this.StatItem(
          $r('sys.symbol.thermometer'),
          $r('app.color.health'),
          `${this.todayStats.lastTemperature ?? '--'}`,
          $r('app.string.unit_celsius'),
          $r('app.string.temperature')
        )
      }
      .width('100%')
      .justifyContent(FlexAlign.SpaceAround)

      // 下次预计
      if (this.todayStats.nextFeedingEstimate) {
        Row({ space: 8 }) {
          Image($r('sys.symbol.clock'))
            .width(16)
            .height(16)
            .fillColor($r('app.color.primary'))

          Text($r('app.string.next_estimate'))
            .fontSize($r('app.float.font_body_small'))
            .fontColor($r('app.color.text_secondary'))

          Text(this.formatTime(this.todayStats.nextFeedingEstimate))
            .fontSize($r('app.float.font_body_small'))
            .fontWeight(FontWeight.Medium)
            .fontColor($r('app.color.primary'))

          Text($r('app.string.feeding'))
            .fontSize($r('app.float.font_body_small'))
            .fontColor($r('app.color.text_secondary'))
        }
        .width('100%')
        .padding({ top: 12, bottom: 4 })
        .borderWidth({ top: 1 })
        .borderColor($r('app.color.border_light'))
      }
    }
    .width('100%')
    .padding(16)
    .backgroundColor($r('app.color.bg_card'))
    .borderRadius(16)
    .shadow({
      radius: 8,
      color: '#0000000A',
      offsetY: 2
    })
  }

  // ==================== 统计项 ====================
  @Builder
  StatItem(icon: Resource, color: Resource, value: string, unit: Resource, label: Resource) {
    Column({ space: 8 }) {
      // 图标
      Image(icon)
        .width(24)
        .height(24)
        .fillColor(color)

      // 数值
      Row({ space: 2 }) {
        Text(value)
          .fontSize($r('app.float.font_title_medium'))
          .fontWeight(FontWeight.Bold)
          .fontColor($r('app.color.text_primary'))

        Text(unit)
          .fontSize($r('app.float.font_body_small'))
          .fontColor($r('app.color.text_tertiary'))
      }

      // 标签
      Text(label)
        .fontSize($r('app.float.font_body_small'))
        .fontColor($r('app.color.text_secondary'))
    }
    .alignItems(HorizontalAlign.Center)
  }

  // ==================== 快速记录区域 ====================
  @Builder
  QuickRecordSection() {
    Column({ space: 12 }) {
      Text($r('app.string.quick_record'))
        .fontSize($r('app.float.font_title_small'))
        .fontWeight(FontWeight.Bold)
        .fontColor($r('app.color.text_primary'))

      Row() {
        ForEach(this.quickRecordItems, (item: QuickRecordItem) => {
          this.QuickRecordButton(item)
        })
      }
      .width('100%')
      .justifyContent(FlexAlign.SpaceAround)
    }
    .width('100%')
    .alignItems(HorizontalAlign.Start)
  }

  // ==================== 快速记录按钮 ====================
  @Builder
  QuickRecordButton(item: QuickRecordItem) {
    Column({ space: 8 }) {
      Button() {
        Image(item.icon)
          .width(28)
          .height(28)
          .fillColor(item.color)
      }
      .type(ButtonType.Circle)
      .width(64)
      .height(64)
      .backgroundColor(item.bgColor)
      .stateEffect(true)
      .onClick(() => this.onQuickRecord(item.id))

      Text(item.label)
        .fontSize($r('app.float.font_body_small'))
        .fontColor($r('app.color.text_secondary'))
    }
    .alignItems(HorizontalAlign.Center)
  }

  // ==================== 活动计时器卡片 ====================
  @Builder
  ActiveTimerCard() {
    Column({ space: 16 }) {
      Row() {
        Row({ space: 8 }) {
          // 闪烁指示器
          Circle()
            .width(8)
            .height(8)
            .fill($r('app.color.timer_active'))

          Text($r('app.string.breast_feeding'))
            .fontSize($r('app.float.font_title_small'))
            .fontWeight(FontWeight.Medium)
            .fontColor($r('app.color.text_primary'))
        }

        Blank()

        // 当前侧边
        Text(this.currentBreastSide === 'left' ?
          $r('app.string.left_side') :
          $r('app.string.right_side'))
          .fontSize($r('app.float.font_body_medium'))
          .fontColor($r('app.color.feeding'))
          .padding({ left: 12, right: 12, top: 4, bottom: 4 })
          .backgroundColor($r('app.color.feeding_light'))
          .borderRadius(12)
      }
      .width('100%')

      // 计时器显示
      Text(this.formatTimer(this.timerSeconds))
        .fontSize(48)
        .fontWeight(FontWeight.Bold)
        .fontColor($r('app.color.text_primary'))
        .fontFamily('HarmonyOS Sans Mono')

      // 操作按钮
      Row({ space: 16 }) {
        Button($r('app.string.switch_side'))
          .height(40)
          .fontSize($r('app.float.font_body_medium'))
          .fontColor($r('app.color.feeding'))
          .backgroundColor($r('app.color.feeding_light'))
          .borderRadius(20)
          .layoutWeight(1)
          .onClick(() => this.onSwitchSide())

        Button($r('app.string.timer_end'))
          .height(40)
          .fontSize($r('app.float.font_body_medium'))
          .fontColor($r('app.color.text_inverse'))
          .backgroundColor($r('app.color.feeding'))
          .borderRadius(20)
          .layoutWeight(1)
          .onClick(() => this.onEndTimer())
      }
      .width('100%')
    }
    .width('100%')
    .padding(16)
    .backgroundColor($r('app.color.bg_card'))
    .borderRadius(16)
    .borderWidth(2)
    .borderColor($r('app.color.feeding'))
  }

  // ==================== 智能建议卡片 ====================
  @Builder
  SmartSuggestionCard() {
    Column({ space: 12 }) {
      Row({ space: 8 }) {
        Image($r('sys.symbol.lightbulb'))
          .width(20)
          .height(20)
          .fillColor($r('app.color.accent'))

        Text($r('app.string.smart_suggest'))
          .fontSize($r('app.float.font_body_medium'))
          .fontWeight(FontWeight.Medium)
          .fontColor($r('app.color.text_primary'))
      }

      Text('根据宝宝的喂养规律，预计在 14:30 左右会饿哦~')
        .fontSize($r('app.float.font_body_medium'))
        .fontColor($r('app.color.text_secondary'))
        .lineHeight(22)
    }
    .width('100%')
    .padding(16)
    .backgroundColor($r('app.color.bg_card'))
    .borderRadius(16)
    .alignItems(HorizontalAlign.Start)
  }

  // ==================== 最近记录区域 ====================
  @Builder
  RecentRecordsSection() {
    Column({ space: 12 }) {
      Row() {
        Text($r('app.string.recent_records'))
          .fontSize($r('app.float.font_title_small'))
          .fontWeight(FontWeight.Bold)
          .fontColor($r('app.color.text_primary'))

        Blank()

        Text('查看全部')
          .fontSize($r('app.float.font_body_small'))
          .fontColor($r('app.color.primary'))
          .onClick(() => {
            // 跳转到记录列表
          })
      }
      .width('100%')

      // 记录列表
      Column({ space: 8 }) {
        this.RecordItem('breast', '母乳喂养', '左侧 8分钟 + 右侧 10分钟', '12:30')
        this.RecordItem('diaper', '换尿布', '尿湿', '11:45')
        this.RecordItem('sleep', '睡眠', '1小时20分钟', '10:00 - 11:20')
      }
    }
    .width('100%')
    .alignItems(HorizontalAlign.Start)
  }

  // ==================== 记录项 ====================
  @Builder
  RecordItem(type: string, title: string, detail: string, time: string) {
    Row({ space: 12 }) {
      // 图标
      this.RecordIcon(type)

      // 内容
      Column({ space: 4 }) {
        Text(title)
          .fontSize($r('app.float.font_body_medium'))
          .fontWeight(FontWeight.Medium)
          .fontColor($r('app.color.text_primary'))

        Text(detail)
          .fontSize($r('app.float.font_body_small'))
          .fontColor($r('app.color.text_secondary'))
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      // 时间
      Text(time)
        .fontSize($r('app.float.font_body_small'))
        .fontColor($r('app.color.text_tertiary'))
    }
    .width('100%')
    .padding(12)
    .backgroundColor($r('app.color.bg_card'))
    .borderRadius(12)
  }

  // ==================== 记录图标 ====================
  @Builder
  RecordIcon(type: string) {
    if (type === 'breast' || type === 'bottle') {
      Image($r('sys.symbol.drop'))
        .width(20)
        .height(20)
        .fillColor($r('app.color.feeding'))
        .padding(8)
        .backgroundColor($r('app.color.feeding_light'))
        .borderRadius(18)
    } else if (type === 'sleep') {
      Image($r('sys.symbol.moon'))
        .width(20)
        .height(20)
        .fillColor($r('app.color.sleep'))
        .padding(8)
        .backgroundColor($r('app.color.sleep_light'))
        .borderRadius(18)
    } else if (type === 'diaper') {
      Image($r('sys.symbol.heart'))
        .width(20)
        .height(20)
        .fillColor($r('app.color.diaper'))
        .padding(8)
        .backgroundColor($r('app.color.diaper_light'))
        .borderRadius(18)
    }
  }

  // ==================== 工具方法 ====================
  private getGreeting(): string {
    const hour = new Date().getHours()
    if (hour < 12) return '早上好'
    if (hour < 18) return '下午好'
    return '晚上好'
  }

  private formatDate(timestamp: number): string {
    const date = new Date(timestamp)
    return `${date.getMonth() + 1}月${date.getDate()}日`
  }

  private formatTime(timestamp: number): string {
    const date = new Date(timestamp)
    return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
  }

  private formatMinutes(minutes: number): string {
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    return hours > 0 ? `${hours}h${mins}m` : `${mins}m`
  }

  private formatTimer(seconds: number): string {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  // ==================== 事件处理 ====================
  private onVoiceClick(): void {
    // 打开语音交互
  }

  private onQuickRecord(type: string): void {
    if (type === 'breast') {
      this.isTimerRunning = true
      this.timerSeconds = 0
      // 启动计时器
    }
  }

  private onSwitchSide(): void {
    this.currentBreastSide = this.currentBreastSide === 'left' ? 'right' : 'left'
  }

  private onEndTimer(): void {
    this.isTimerRunning = false
    // 保存记录
  }
}
