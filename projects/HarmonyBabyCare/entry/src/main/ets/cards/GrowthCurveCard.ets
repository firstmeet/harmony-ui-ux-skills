// ==========================================
// HarmonyBaby Care - 生长曲线卡片 (2×2)
// 原子化服务卡片
// ==========================================

/**
 * 生长曲线卡片
 * 功能：展示宝宝身高体重趋势曲线
 * 尺寸：2×2
 */
@Entry
@Component
struct GrowthCurveCard {
  // ==================== 状态 ====================
  @State currentHeight: number = 68.5
  @State currentWeight: number = 8.2
  @State heightPercentile: number = 75
  @State weightPercentile: number = 60

  // ==================== 构建 ====================
  build() {
    Column({ space: 8 }) {
      // 标题行
      Row() {
        Image($r('sys.symbol.chart_line_uptrend_xyaxis'))
          .width(16)
          .height(16)
          .fillColor($r('app.color.growth'))

        Text($r('app.string.card_growth_curve'))
          .fontSize(12)
          .fontColor($r('app.color.text_secondary'))
          .margin({ left: 4 })

        Blank()

        Text('WHO标准')
          .fontSize(10)
          .fontColor($r('app.color.text_tertiary'))
      }
      .width('100%')

      // 简化曲线图（使用 Shape 绘制）
      Stack() {
        // 背景网格
        Column() {
          ForEach([0, 1, 2], () => {
            Divider()
              .color($r('app.color.border_light'))
              .margin({ top: 15 })
          })
        }
        .width('100%')
        .height('100%')

        // 曲线路径（简化表示）
        Path()
          .commands('M 0 40 Q 30 35 60 30 T 120 20')
          .stroke($r('app.color.growth'))
          .strokeWidth(2)
          .fill(Color.Transparent)
          .width('100%')
          .height('100%')
      }
      .width('100%')
      .height(50)
      .backgroundColor($r('app.color.growth_light'))
      .borderRadius(8)
      .padding(8)

      // 数据展示
      Row() {
        // 身高
        Column({ space: 2 }) {
          Row({ space: 4 }) {
            Text(`${this.currentHeight}`)
              .fontSize(16)
              .fontWeight(FontWeight.Bold)
              .fontColor($r('app.color.text_primary'))

            Text('cm')
              .fontSize(10)
              .fontColor($r('app.color.text_tertiary'))
          }

          Text(`身高 P${this.heightPercentile}`)
            .fontSize(10)
            .fontColor($r('app.color.text_secondary'))
        }
        .layoutWeight(1)
        .alignItems(HorizontalAlign.Center)

        Divider()
          .vertical(true)
          .height(30)
          .color($r('app.color.divider'))

        // 体重
        Column({ space: 2 }) {
          Row({ space: 4 }) {
            Text(`${this.currentWeight}`)
              .fontSize(16)
              .fontWeight(FontWeight.Bold)
              .fontColor($r('app.color.text_primary'))

            Text('kg')
              .fontSize(10)
              .fontColor($r('app.color.text_tertiary'))
          }

          Text(`体重 P${this.weightPercentile}`)
            .fontSize(10)
            .fontColor($r('app.color.text_secondary'))
        }
        .layoutWeight(1)
        .alignItems(HorizontalAlign.Center)
      }
      .width('100%')
    }
    .width('100%')
    .height('100%')
    .padding(12)
    .backgroundColor($r('app.color.bg_card'))
    .borderRadius(16)
    .onClick(() => {
      // 打开生长曲线详情页
    })
  }
}
