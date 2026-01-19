// ==========================================
// HarmonyBaby Care - 喂养计时卡片 (2×2)
// 原子化服务卡片
// ==========================================

/**
 * 喂养计时卡片
 * 功能：动态计时器，支持开始/暂停/切换侧边
 * 尺寸：2×2
 */
@Entry
@Component
struct FeedingTimerCard {
  // ==================== 状态 ====================
  @State isRunning: boolean = false
  @State isPaused: boolean = false
  @State currentSide: string = 'left'
  @State timerText: string = '00:00'
  @State elapsedSeconds: number = 0

  // ==================== 构建 ====================
  build() {
    Column({ space: 8 }) {
      // 标题行
      Row() {
        Image($r('sys.symbol.drop'))
          .width(16)
          .height(16)
          .fillColor($r('app.color.feeding'))

        Text($r('app.string.card_feeding_timer'))
          .fontSize(12)
          .fontColor($r('app.color.text_secondary'))
          .margin({ left: 4 })

        Blank()

        if (this.isRunning) {
          // 运行中指示器
          Circle()
            .width(6)
            .height(6)
            .fill($r('app.color.timer_active'))
        }
      }
      .width('100%')

      // 计时器显示
      if (this.isRunning || this.isPaused) {
        Column({ space: 4 }) {
          Text(this.timerText)
            .fontSize(32)
            .fontWeight(FontWeight.Bold)
            .fontColor($r('app.color.text_primary'))
            .fontFamily('HarmonyOS Sans Mono')

          Text(this.currentSide === 'left' ?
            $r('app.string.left_side') :
            $r('app.string.right_side'))
            .fontSize(10)
            .fontColor($r('app.color.feeding'))
            .padding({ left: 8, right: 8, top: 2, bottom: 2 })
            .backgroundColor($r('app.color.feeding_light'))
            .borderRadius(8)
        }
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)

        // 操作按钮
        Row({ space: 8 }) {
          // 切换按钮
          Button() {
            Image($r('sys.symbol.arrow_left_arrow_right'))
              .width(14)
              .height(14)
              .fillColor($r('app.color.feeding'))
          }
          .type(ButtonType.Circle)
          .width(28)
          .height(28)
          .backgroundColor($r('app.color.feeding_light'))
          .onClick(() => this.onSwitch())

          // 暂停/继续按钮
          Button() {
            Image(this.isPaused ?
              $r('sys.symbol.play_fill') :
              $r('sys.symbol.pause_fill'))
              .width(14)
              .height(14)
              .fillColor($r('app.color.text_inverse'))
          }
          .type(ButtonType.Circle)
          .width(28)
          .height(28)
          .backgroundColor(this.isPaused ?
            $r('app.color.success') :
            $r('app.color.warning'))
          .onClick(() => this.onTogglePause())

          // 结束按钮
          Button() {
            Image($r('sys.symbol.checkmark'))
              .width(14)
              .height(14)
              .fillColor($r('app.color.text_inverse'))
          }
          .type(ButtonType.Circle)
          .width(28)
          .height(28)
          .backgroundColor($r('app.color.feeding'))
          .onClick(() => this.onEnd())
        }
        .width('100%')
        .justifyContent(FlexAlign.Center)

      } else {
        // 未开始状态
        Column({ space: 8 }) {
          Image($r('sys.symbol.drop'))
            .width(32)
            .height(32)
            .fillColor($r('app.color.feeding'))

          Text('点击开始喂养')
            .fontSize(12)
            .fontColor($r('app.color.text_tertiary'))
        }
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
        .onClick(() => this.onStart())
      }
    }
    .width('100%')
    .height('100%')
    .padding(12)
    .backgroundColor($r('app.color.bg_card'))
    .borderRadius(16)
  }

  // ==================== 事件处理 ====================
  private onStart(): void {
    this.isRunning = true
    // 通过 FormExtensionAbility 启动计时
  }

  private onSwitch(): void {
    this.currentSide = this.currentSide === 'left' ? 'right' : 'left'
  }

  private onTogglePause(): void {
    this.isPaused = !this.isPaused
  }

  private onEnd(): void {
    this.isRunning = false
    this.isPaused = false
    // 保存记录并打开 App 详情
  }
}
