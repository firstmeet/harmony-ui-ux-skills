// ==========================================
// HarmonyBaby Care - 用药管家卡片 (2×2)
// 原子化服务卡片
// ==========================================

/**
 * 用药管家卡片
 * 功能：显示下次用药倒计时，支持标记已服用
 * 尺寸：2×2
 */
@Entry
@Component
struct MedicineReminderCard {
  // ==================== 状态 ====================
  @State medicineName: string = '维生素D'
  @State dosage: string = '1滴'
  @State frequency: string = '每日1次'
  @State countdownText: string = '2h 30m'
  @State isTaken: boolean = false
  @State nextTime: string = '15:00'

  // ==================== 构建 ====================
  build() {
    Column({ space: 8 }) {
      // 标题行
      Row() {
        Image($r('sys.symbol.pills'))
          .width(16)
          .height(16)
          .fillColor($r('app.color.health'))

        Text($r('app.string.card_medicine_reminder'))
          .fontSize(12)
          .fontColor($r('app.color.text_secondary'))
          .margin({ left: 4 })
      }
      .width('100%')

      // 药品信息
      Column({ space: 4 }) {
        Text(this.medicineName)
          .fontSize(16)
          .fontWeight(FontWeight.Bold)
          .fontColor($r('app.color.text_primary'))

        Text(`${this.dosage} · ${this.frequency}`)
          .fontSize(11)
          .fontColor($r('app.color.text_tertiary'))
      }
      .alignItems(HorizontalAlign.Start)
      .width('100%')

      Blank()

      if (this.isTaken) {
        // 已服用状态
        Row({ space: 6 }) {
          Image($r('sys.symbol.checkmark_circle_fill'))
            .width(18)
            .height(18)
            .fillColor($r('app.color.success'))

          Text('今日已服用')
            .fontSize(13)
            .fontColor($r('app.color.success'))
        }
        .width('100%')
        .justifyContent(FlexAlign.Center)
        .padding({ top: 8, bottom: 8 })
        .backgroundColor($r('app.color.growth_light'))
        .borderRadius(20)

      } else {
        // 倒计时状态
        Column({ space: 4 }) {
          Text('距离下次')
            .fontSize(10)
            .fontColor($r('app.color.text_tertiary'))

          Text(this.countdownText)
            .fontSize(20)
            .fontWeight(FontWeight.Bold)
            .fontColor($r('app.color.health'))
        }

        // 已服用按钮
        Button('已服用')
          .width('100%')
          .height(32)
          .fontSize(12)
          .fontColor($r('app.color.text_inverse'))
          .backgroundColor($r('app.color.health'))
          .borderRadius(16)
          .onClick(() => this.onMarkTaken())
      }
    }
    .width('100%')
    .height('100%')
    .padding(12)
    .backgroundColor($r('app.color.bg_card'))
    .borderRadius(16)
  }

  // ==================== 事件处理 ====================
  private onMarkTaken(): void {
    this.isTaken = true
    // 记录用药并通知 App
  }
}
