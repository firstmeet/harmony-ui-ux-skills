// ==========================================
// HarmonyBaby Care - 喂养记录页面
// ==========================================

import { FeedingType, BreastSide, TimerState } from '../models/DataModels'

/**
 * 喂养记录页面
 * 支持母乳计时、奶瓶记录、辅食记录
 */
@Entry
@Component
struct FeedingPage {
  // ==================== 状态管理 ====================
  @State currentTab: FeedingType = FeedingType.BREAST
  @State timerState: TimerState = {
    isRunning: false,
    isPaused: false,
    startTime: 0,
    pausedTime: 0,
    totalPausedDuration: 0,
    currentSide: BreastSide.LEFT
  }
  @State timerDisplay: string = '00:00'
  @State leftDuration: number = 0
  @State rightDuration: number = 0

  // 奶瓶表单
  @State bottleAmount: number = 0
  @State bottleBrand: string = ''
  @State bottleTemp: number = 40

  // 辅食表单
  @State foodIngredients: string[] = []
  @State foodWeight: number = 0
  @State isAllergyMarked: boolean = false
  @State note: string = ''

  private timerInterval: number = -1

  // ==================== 生命周期 ====================
  aboutToDisappear(): void {
    if (this.timerInterval !== -1) {
      clearInterval(this.timerInterval)
    }
  }

  // ==================== 主构建 ====================
  build() {
    Column() {
      // 顶部标签切换
      this.TabBar()

      // 内容区域
      if (this.currentTab === FeedingType.BREAST) {
        this.BreastFeedingContent()
      } else if (this.currentTab === FeedingType.BOTTLE) {
        this.BottleFeedingContent()
      } else {
        this.BabyFoodContent()
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor($r('app.color.bg_secondary'))
  }

  // ==================== 标签栏 ====================
  @Builder
  TabBar() {
    Row() {
      this.TabItem(FeedingType.BREAST, $r('app.string.breast_feeding'))
      this.TabItem(FeedingType.BOTTLE, $r('app.string.bottle_feeding'))
      this.TabItem(FeedingType.BABY_FOOD, $r('app.string.baby_food'))
    }
    .width('100%')
    .height(48)
    .padding({ left: 16, right: 16 })
    .backgroundColor($r('app.color.bg_primary'))
    .justifyContent(FlexAlign.SpaceEvenly)
  }

  @Builder
  TabItem(type: FeedingType, label: Resource) {
    Column() {
      Text(label)
        .fontSize($r('app.float.font_body_medium'))
        .fontWeight(this.currentTab === type ? FontWeight.Bold : FontWeight.Normal)
        .fontColor(this.currentTab === type ?
          $r('app.color.feeding') :
          $r('app.color.text_secondary'))
        .padding({ top: 12, bottom: 10 })

      // 下划线指示器
      if (this.currentTab === type) {
        Divider()
          .width('60%')
          .strokeWidth(3)
          .color($r('app.color.feeding'))
          .lineCap(LineCapStyle.Round)
      }
    }
    .layoutWeight(1)
    .alignItems(HorizontalAlign.Center)
    .onClick(() => {
      this.currentTab = type
    })
  }

  // ==================== 母乳喂养内容 ====================
  @Builder
  BreastFeedingContent() {
    Column({ space: 24 }) {
      Scroll() {
        Column({ space: 24 }) {
          // 计时器显示
          this.TimerDisplay()

          // 侧边切换
          this.SideSelector()

          // 本次统计
          this.SessionStats()

          // 操作按钮
          this.TimerControls()
        }
        .padding(24)
      }
      .layoutWeight(1)
    }
    .width('100%')
    .layoutWeight(1)
  }

  // ==================== 计时器显示 ====================
  @Builder
  TimerDisplay() {
    Stack() {
      // 背景圆环
      Circle()
        .width(200)
        .height(200)
        .fill(Color.Transparent)
        .stroke($r('app.color.bg_tertiary'))
        .strokeWidth(8)

      // 进度圆环
      if (this.timerState.isRunning || this.timerState.isPaused) {
        Circle()
          .width(200)
          .height(200)
          .fill(Color.Transparent)
          .stroke(this.timerState.currentSide === BreastSide.LEFT ?
            $r('app.color.secondary') :
            $r('app.color.secondary_blue'))
          .strokeWidth(8)
          .strokeLineCap(LineCapStyle.Round)
      }

      // 时间文字
      Column({ space: 8 }) {
        Text(this.timerDisplay)
          .fontSize(48)
          .fontWeight(FontWeight.Bold)
          .fontColor($r('app.color.text_primary'))
          .fontFamily('HarmonyOS Sans Mono')

        if (this.timerState.isRunning) {
          Row({ space: 4 }) {
            Circle()
              .width(8)
              .height(8)
              .fill($r('app.color.timer_active'))

            Text(this.timerState.currentSide === BreastSide.LEFT ?
              $r('app.string.left_side') :
              $r('app.string.right_side'))
              .fontSize($r('app.float.font_body_medium'))
              .fontColor($r('app.color.text_secondary'))
          }
        } else if (!this.timerState.isRunning && !this.timerState.isPaused) {
          Text('点击开始')
            .fontSize($r('app.float.font_body_medium'))
            .fontColor($r('app.color.text_tertiary'))
        }
      }
    }
    .width(200)
    .height(200)
  }

  // ==================== 侧边选择器 ====================
  @Builder
  SideSelector() {
    Row({ space: 16 }) {
      // 左侧
      this.SideButton(BreastSide.LEFT, $r('app.string.left_side'), this.leftDuration)

      // 切换按钮
      Button() {
        Image($r('sys.symbol.arrow_left_arrow_right'))
          .width(24)
          .height(24)
          .fillColor($r('app.color.text_inverse'))
      }
      .type(ButtonType.Circle)
      .width(48)
      .height(48)
      .backgroundColor($r('app.color.feeding'))
      .enabled(this.timerState.isRunning)
      .onClick(() => this.switchSide())

      // 右侧
      this.SideButton(BreastSide.RIGHT, $r('app.string.right_side'), this.rightDuration)
    }
    .width('100%')
    .justifyContent(FlexAlign.Center)
  }

  @Builder
  SideButton(side: BreastSide, label: Resource, duration: number) {
    Column({ space: 8 }) {
      Text(label)
        .fontSize($r('app.float.font_body_medium'))
        .fontWeight(FontWeight.Medium)
        .fontColor(this.timerState.currentSide === side ?
          $r('app.color.text_primary') :
          $r('app.color.text_tertiary'))

      Text(this.formatSeconds(duration))
        .fontSize($r('app.float.font_title_medium'))
        .fontWeight(FontWeight.Bold)
        .fontColor(this.timerState.currentSide === side ?
          (side === BreastSide.LEFT ? $r('app.color.secondary') : $r('app.color.secondary_blue')) :
          $r('app.color.text_disabled'))
    }
    .width(100)
    .padding(16)
    .backgroundColor(this.timerState.currentSide === side ?
      $r('app.color.bg_card') :
      $r('app.color.bg_tertiary'))
    .borderRadius(16)
    .borderWidth(this.timerState.currentSide === side ? 2 : 0)
    .borderColor(side === BreastSide.LEFT ? $r('app.color.secondary') : $r('app.color.secondary_blue'))
    .onClick(() => {
      if (!this.timerState.isRunning) {
        this.timerState.currentSide = side
      }
    })
  }

  // ==================== 本次统计 ====================
  @Builder
  SessionStats() {
    Row() {
      Column({ space: 4 }) {
        Text('总时长')
          .fontSize($r('app.float.font_body_small'))
          .fontColor($r('app.color.text_tertiary'))
        Text(this.formatSeconds(this.leftDuration + this.rightDuration))
          .fontSize($r('app.float.font_title_small'))
          .fontWeight(FontWeight.Bold)
          .fontColor($r('app.color.text_primary'))
      }
      .layoutWeight(1)

      Divider()
        .vertical(true)
        .height(40)
        .color($r('app.color.border_light'))

      Column({ space: 4 }) {
        Text('切换次数')
          .fontSize($r('app.float.font_body_small'))
          .fontColor($r('app.color.text_tertiary'))
        Text('2')
          .fontSize($r('app.float.font_title_small'))
          .fontWeight(FontWeight.Bold)
          .fontColor($r('app.color.text_primary'))
      }
      .layoutWeight(1)
    }
    .width('100%')
    .padding(16)
    .backgroundColor($r('app.color.bg_card'))
    .borderRadius(12)
  }

  // ==================== 计时器控制按钮 ====================
  @Builder
  TimerControls() {
    if (!this.timerState.isRunning && !this.timerState.isPaused) {
      // 开始状态
      Button($r('app.string.timer_start'))
        .width('100%')
        .height(56)
        .fontSize($r('app.float.font_title_small'))
        .fontWeight(FontWeight.Bold)
        .backgroundColor($r('app.color.feeding'))
        .borderRadius(28)
        .onClick(() => this.startTimer())
    } else {
      // 运行/暂停状态
      Row({ space: 16 }) {
        Button(this.timerState.isPaused ?
          $r('app.string.timer_resume') :
          $r('app.string.timer_pause'))
          .height(48)
          .fontSize($r('app.float.font_body_large'))
          .fontColor($r('app.color.feeding'))
          .backgroundColor($r('app.color.feeding_light'))
          .borderRadius(24)
          .layoutWeight(1)
          .onClick(() => this.togglePause())

        Button($r('app.string.timer_save'))
          .height(48)
          .fontSize($r('app.float.font_body_large'))
          .fontColor($r('app.color.text_inverse'))
          .backgroundColor($r('app.color.feeding'))
          .borderRadius(24)
          .layoutWeight(1)
          .onClick(() => this.saveRecord())
      }
      .width('100%')
    }
  }

  // ==================== 奶瓶喂养内容 ====================
  @Builder
  BottleFeedingContent() {
    Scroll() {
      Column({ space: 20 }) {
        // 奶量输入
        this.FormSection($r('app.string.milk_amount')) {
          Row({ space: 12 }) {
            // 快捷按钮
            ForEach([60, 90, 120, 150, 180], (amount: number) => {
              Button(`${amount}`)
                .height(40)
                .fontSize($r('app.float.font_body_medium'))
                .fontColor(this.bottleAmount === amount ?
                  $r('app.color.text_inverse') :
                  $r('app.color.feeding'))
                .backgroundColor(this.bottleAmount === amount ?
                  $r('app.color.feeding') :
                  $r('app.color.feeding_light'))
                .borderRadius(20)
                .onClick(() => {
                  this.bottleAmount = amount
                })
            })

            Text($r('app.string.unit_ml'))
              .fontSize($r('app.float.font_body_medium'))
              .fontColor($r('app.color.text_secondary'))
          }
        }

        // 品牌选择
        this.FormSection($r('app.string.milk_brand')) {
          TextInput({ placeholder: '选择或输入品牌' })
            .height(48)
            .backgroundColor($r('app.color.bg_primary'))
            .borderRadius(12)
            .borderWidth(1)
            .borderColor($r('app.color.border_light'))
            .onChange((value) => {
              this.bottleBrand = value
            })
        }

        // 水温选择
        this.FormSection($r('app.string.water_temp')) {
          Row({ space: 8 }) {
            Slider({
              value: this.bottleTemp,
              min: 30,
              max: 50,
              step: 1
            })
              .layoutWeight(1)
              .blockColor($r('app.color.feeding'))
              .trackColor($r('app.color.feeding_light'))
              .selectedColor($r('app.color.feeding'))
              .onChange((value: number) => {
                this.bottleTemp = value
              })

            Text(`${this.bottleTemp}℃`)
              .width(50)
              .fontSize($r('app.float.font_body_medium'))
              .fontColor($r('app.color.text_primary'))
              .textAlign(TextAlign.End)
          }
        }

        // 备注
        this.FormSection('备注') {
          TextArea({ placeholder: '添加备注（可选）' })
            .height(80)
            .backgroundColor($r('app.color.bg_primary'))
            .borderRadius(12)
            .borderWidth(1)
            .borderColor($r('app.color.border_light'))
            .onChange((value) => {
              this.note = value
            })
        }

        // 保存按钮
        Button($r('app.string.save'))
          .width('100%')
          .height(56)
          .fontSize($r('app.float.font_title_small'))
          .fontWeight(FontWeight.Bold)
          .backgroundColor($r('app.color.feeding'))
          .borderRadius(28)
          .margin({ top: 16 })
          .onClick(() => this.saveBottleRecord())
      }
      .padding(24)
    }
    .layoutWeight(1)
  }

  // ==================== 辅食内容 ====================
  @Builder
  BabyFoodContent() {
    Scroll() {
      Column({ space: 20 }) {
        // 食材选择
        this.FormSection($r('app.string.food_ingredient')) {
          Flex({ wrap: FlexWrap.Wrap }) {
            ForEach(['米糊', '蔬菜泥', '水果泥', '蛋黄', '肉泥', '面条'], (item: string) => {
              Text(item)
                .fontSize($r('app.float.font_body_small'))
                .fontColor(this.foodIngredients.includes(item) ?
                  $r('app.color.text_inverse') :
                  $r('app.color.feeding'))
                .backgroundColor(this.foodIngredients.includes(item) ?
                  $r('app.color.feeding') :
                  $r('app.color.feeding_light'))
                .padding({ left: 16, right: 16, top: 8, bottom: 8 })
                .borderRadius(16)
                .margin({ right: 8, bottom: 8 })
                .onClick(() => this.toggleIngredient(item))
            })
          }
        }

        // 克重
        this.FormSection($r('app.string.food_weight')) {
          Row({ space: 12 }) {
            ForEach([30, 50, 80, 100], (weight: number) => {
              Button(`${weight}g`)
                .height(40)
                .fontSize($r('app.float.font_body_medium'))
                .fontColor(this.foodWeight === weight ?
                  $r('app.color.text_inverse') :
                  $r('app.color.feeding'))
                .backgroundColor(this.foodWeight === weight ?
                  $r('app.color.feeding') :
                  $r('app.color.feeding_light'))
                .borderRadius(20)
                .onClick(() => {
                  this.foodWeight = weight
                })
            })
          }
        }

        // 过敏标记
        Row() {
          Row({ space: 8 }) {
            Image($r('sys.symbol.exclamationmark_triangle'))
              .width(20)
              .height(20)
              .fillColor($r('app.color.warning'))

            Text($r('app.string.allergy_mark'))
              .fontSize($r('app.float.font_body_medium'))
              .fontColor($r('app.color.text_primary'))
          }

          Blank()

          Toggle({ type: ToggleType.Switch, isOn: this.isAllergyMarked })
            .selectedColor($r('app.color.warning'))
            .onChange((isOn) => {
              this.isAllergyMarked = isOn
            })
        }
        .width('100%')
        .padding(16)
        .backgroundColor($r('app.color.bg_card'))
        .borderRadius(12)

        // 保存按钮
        Button($r('app.string.save'))
          .width('100%')
          .height(56)
          .fontSize($r('app.float.font_title_small'))
          .fontWeight(FontWeight.Bold)
          .backgroundColor($r('app.color.feeding'))
          .borderRadius(28)
          .margin({ top: 16 })
          .onClick(() => this.saveFoodRecord())
      }
      .padding(24)
    }
    .layoutWeight(1)
  }

  // ==================== 表单区块 ====================
  @Builder
  FormSection(title: Resource | string, content: () => void) {
    Column({ space: 12 }) {
      Text(title)
        .fontSize($r('app.float.font_body_medium'))
        .fontWeight(FontWeight.Medium)
        .fontColor($r('app.color.text_primary'))

      content()
    }
    .width('100%')
    .alignItems(HorizontalAlign.Start)
  }

  // ==================== 工具方法 ====================
  private formatSeconds(seconds: number): string {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  // ==================== 事件处理 ====================
  private startTimer(): void {
    this.timerState.isRunning = true
    this.timerState.startTime = Date.now()
    // 启动定时器更新
  }

  private togglePause(): void {
    this.timerState.isPaused = !this.timerState.isPaused
  }

  private switchSide(): void {
    // 保存当前侧的时长
    if (this.timerState.currentSide === BreastSide.LEFT) {
      this.timerState.currentSide = BreastSide.RIGHT
    } else {
      this.timerState.currentSide = BreastSide.LEFT
    }
  }

  private saveRecord(): void {
    this.timerState.isRunning = false
    this.timerState.isPaused = false
    // 保存到数据库
  }

  private saveBottleRecord(): void {
    // 保存奶瓶记录
  }

  private saveFoodRecord(): void {
    // 保存辅食记录
  }

  private toggleIngredient(ingredient: string): void {
    const index = this.foodIngredients.indexOf(ingredient)
    if (index >= 0) {
      this.foodIngredients.splice(index, 1)
    } else {
      this.foodIngredients.push(ingredient)
    }
  }
}
