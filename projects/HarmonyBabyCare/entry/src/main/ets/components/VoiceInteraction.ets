// ==========================================
// HarmonyBaby Care - 语音交互组件
// ==========================================

/**
 * 语音交互状态
 */
export enum VoiceState {
  IDLE = 'idle',           // 空闲
  LISTENING = 'listening', // 聆听中
  PROCESSING = 'processing', // 处理中
  SUCCESS = 'success',     // 成功
  ERROR = 'error'          // 错误
}

/**
 * 语音交互结果
 */
export interface VoiceResult {
  success: boolean
  message: string
  recordType: string | null
  recordData: object | null
}

/**
 * 语音交互浮层
 * 展示语音识别状态和结果反馈
 */
@Component
export struct VoiceOverlay {
  // ==================== 属性 ====================
  @Prop state: VoiceState = VoiceState.IDLE
  @Prop recognizedText: string = ''
  @Prop resultMessage: string = ''

  onCancel: () => void = () => {}
  onRetry: () => void = () => {}

  // ==================== 波形动画状态 ====================
  @State waveScale1: number = 1
  @State waveScale2: number = 1
  @State waveScale3: number = 1
  @State waveOpacity1: number = 0.3
  @State waveOpacity2: number = 0.2
  @State waveOpacity3: number = 0.1

  // ==================== 构建 ====================
  build() {
    Column() {
      Blank()
        .layoutWeight(1)

      // 语音交互面板
      Column({ space: 24 }) {
        // 主要内容区
        if (this.state === VoiceState.LISTENING) {
          this.ListeningContent()
        } else if (this.state === VoiceState.PROCESSING) {
          this.ProcessingContent()
        } else if (this.state === VoiceState.SUCCESS) {
          this.SuccessContent()
        } else if (this.state === VoiceState.ERROR) {
          this.ErrorContent()
        }
      }
      .width('100%')
      .padding({ left: 24, right: 24, top: 32, bottom: 40 })
      .backgroundColor($r('app.color.bg_primary'))
      .borderRadius({ topLeft: 24, topRight: 24 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor($r('app.color.overlay'))
  }

  // ==================== 聆听中内容 ====================
  @Builder
  ListeningContent() {
    Column({ space: 20 }) {
      // 波形动画区域
      Stack() {
        // 外圈波纹
        Circle()
          .width(120)
          .height(120)
          .fill(Color.Transparent)
          .stroke($r('app.color.voice_wave'))
          .strokeWidth(2)
          .scale({ x: this.waveScale3, y: this.waveScale3 })
          .opacity(this.waveOpacity3)

        Circle()
          .width(100)
          .height(100)
          .fill(Color.Transparent)
          .stroke($r('app.color.voice_wave'))
          .strokeWidth(2)
          .scale({ x: this.waveScale2, y: this.waveScale2 })
          .opacity(this.waveOpacity2)

        Circle()
          .width(80)
          .height(80)
          .fill(Color.Transparent)
          .stroke($r('app.color.voice_wave'))
          .strokeWidth(2)
          .scale({ x: this.waveScale1, y: this.waveScale1 })
          .opacity(this.waveOpacity1)

        // 中心麦克风按钮
        Button() {
          Image($r('sys.symbol.mic'))
            .width(32)
            .height(32)
            .fillColor($r('app.color.text_inverse'))
        }
        .type(ButtonType.Circle)
        .width(72)
        .height(72)
        .backgroundColor($r('app.color.voice_active'))
        .shadow({
          radius: 16,
          color: '#7B8CDE40',
          offsetY: 4
        })
      }
      .width(150)
      .height(150)
      .onAppear(() => this.startWaveAnimation())

      // 识别文字
      if (this.recognizedText.length > 0) {
        Text(this.recognizedText)
          .fontSize(18)
          .fontColor($r('app.color.text_primary'))
          .textAlign(TextAlign.Center)
          .maxLines(3)
      } else {
        Text($r('app.string.voice_listening'))
          .fontSize(16)
          .fontColor($r('app.color.text_secondary'))
      }

      // 提示
      Text($r('app.string.voice_hint'))
        .fontSize(12)
        .fontColor($r('app.color.text_tertiary'))
        .textAlign(TextAlign.Center)

      // 取消按钮
      Button($r('app.string.cancel'))
        .width(120)
        .height(44)
        .fontSize(14)
        .fontColor($r('app.color.text_secondary'))
        .backgroundColor($r('app.color.bg_tertiary'))
        .borderRadius(22)
        .onClick(() => this.onCancel())
    }
    .alignItems(HorizontalAlign.Center)
  }

  // ==================== 处理中内容 ====================
  @Builder
  ProcessingContent() {
    Column({ space: 20 }) {
      // 加载动画
      LoadingProgress()
        .width(60)
        .height(60)
        .color($r('app.color.primary'))

      Text($r('app.string.voice_processing'))
        .fontSize(16)
        .fontColor($r('app.color.text_secondary'))

      if (this.recognizedText.length > 0) {
        Text(`"${this.recognizedText}"`)
          .fontSize(14)
          .fontColor($r('app.color.text_tertiary'))
          .textAlign(TextAlign.Center)
      }
    }
    .alignItems(HorizontalAlign.Center)
  }

  // ==================== 成功内容 ====================
  @Builder
  SuccessContent() {
    Column({ space: 20 }) {
      // 成功图标
      Stack() {
        Circle()
          .width(72)
          .height(72)
          .fill($r('app.color.success'))

        Image($r('sys.symbol.checkmark'))
          .width(36)
          .height(36)
          .fillColor($r('app.color.text_inverse'))
      }

      Text($r('app.string.voice_success'))
        .fontSize(18)
        .fontWeight(FontWeight.Medium)
        .fontColor($r('app.color.success'))

      // 结果消息
      Text(this.resultMessage)
        .fontSize(14)
        .fontColor($r('app.color.text_secondary'))
        .textAlign(TextAlign.Center)
        .padding({ left: 16, right: 16 })
    }
    .alignItems(HorizontalAlign.Center)
  }

  // ==================== 错误内容 ====================
  @Builder
  ErrorContent() {
    Column({ space: 20 }) {
      // 错误图标
      Stack() {
        Circle()
          .width(72)
          .height(72)
          .fill($r('app.color.error'))

        Image($r('sys.symbol.xmark'))
          .width(32)
          .height(32)
          .fillColor($r('app.color.text_inverse'))
      }

      Text($r('app.string.voice_failed'))
        .fontSize(16)
        .fontColor($r('app.color.error'))

      // 操作按钮
      Row({ space: 16 }) {
        Button($r('app.string.cancel'))
          .height(44)
          .fontSize(14)
          .fontColor($r('app.color.text_secondary'))
          .backgroundColor($r('app.color.bg_tertiary'))
          .borderRadius(22)
          .layoutWeight(1)
          .onClick(() => this.onCancel())

        Button('重试')
          .height(44)
          .fontSize(14)
          .fontColor($r('app.color.text_inverse'))
          .backgroundColor($r('app.color.primary'))
          .borderRadius(22)
          .layoutWeight(1)
          .onClick(() => this.onRetry())
      }
      .width('100%')
      .padding({ left: 32, right: 32 })
    }
    .alignItems(HorizontalAlign.Center)
  }

  // ==================== 波形动画 ====================
  private startWaveAnimation(): void {
    // 动画会在实际项目中使用 animateTo 实现
    // 这里展示动画结构
  }
}

/**
 * 语音反馈 Toast
 * 短暂展示语音操作结果
 */
@Component
export struct VoiceToast {
  @Prop success: boolean = true
  @Prop message: string = ''
  @Prop visible: boolean = false

  build() {
    if (this.visible) {
      Row({ space: 8 }) {
        Image(this.success ?
          $r('sys.symbol.checkmark_circle_fill') :
          $r('sys.symbol.xmark_circle_fill'))
          .width(20)
          .height(20)
          .fillColor($r('app.color.text_inverse'))

        Text(this.message)
          .fontSize(14)
          .fontColor($r('app.color.text_inverse'))
      }
      .padding({ left: 16, right: 16, top: 12, bottom: 12 })
      .backgroundColor(this.success ?
        'rgba(107, 203, 119, 0.95)' :
        'rgba(255, 123, 123, 0.95)')
      .borderRadius(24)
      .shadow({
        radius: 8,
        color: '#00000020',
        offsetY: 2
      })
    }
  }
}

/**
 * 语音激活按钮
 * 悬浮在页面上的语音快捷入口
 */
@Component
export struct VoiceFAB {
  onPress: () => void = () => {}
  @State isPressed: boolean = false

  build() {
    Button() {
      Image($r('sys.symbol.mic'))
        .width(28)
        .height(28)
        .fillColor($r('app.color.text_inverse'))
    }
    .type(ButtonType.Circle)
    .width(56)
    .height(56)
    .backgroundColor($r('app.color.primary'))
    .shadow({
      radius: 12,
      color: '#7B8CDE50',
      offsetY: 4
    })
    .scale({ x: this.isPressed ? 0.95 : 1, y: this.isPressed ? 0.95 : 1 })
    .animation({
      duration: 100,
      curve: Curve.EaseOut
    })
    .onTouch((event: TouchEvent) => {
      if (event.type === TouchType.Down) {
        this.isPressed = true
      } else if (event.type === TouchType.Up || event.type === TouchType.Cancel) {
        this.isPressed = false
      }
    })
    .onClick(() => this.onPress())
  }
}
