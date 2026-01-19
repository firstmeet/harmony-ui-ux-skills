// ==========================================
// HarmonyBaby Care - 今日概览卡片 (2×4)
// 原子化服务卡片
// ==========================================

/**
 * 今日概览卡片
 * 功能：展示今日喂养、睡眠、尿布、体温统计
 * 尺寸：2×4
 */
@Entry
@Component
struct TodayOverviewCard {
  // ==================== 状态 ====================
  @State babyName: string = '小宝贝'
  @State feedingCount: number = 5
  @State sleepMinutes: number = 200
  @State diaperCount: number = 4
  @State temperature: number = 36.5
  @State nextEstimate: string = '14:30 喂奶'
  @State currentTime: string = '12:30'

  // ==================== 构建 ====================
  build() {
    Column({ space: 0 }) {
      // 标题行
      Row() {
        Row({ space: 6 }) {
          // 宝宝头像
          Image($r('app.media.baby_avatar'))
            .width(24)
            .height(24)
            .borderRadius(12)
            .backgroundColor($r('app.color.primary_light'))

          Text(`${this.babyName}今日状态`)
            .fontSize(13)
            .fontWeight(FontWeight.Medium)
            .fontColor($r('app.color.text_primary'))
        }

        Blank()

        Text(this.currentTime)
          .fontSize(11)
          .fontColor($r('app.color.text_tertiary'))
      }
      .width('100%')
      .padding({ left: 12, right: 12, top: 10, bottom: 8 })

      Divider()
        .color($r('app.color.divider'))

      // 统计数据
      Row() {
        this.StatItem($r('sys.symbol.drop'), $r('app.color.feeding'),
          `${this.feedingCount}`, '次', '喂养')

        Divider()
          .vertical(true)
          .height(36)
          .color($r('app.color.divider'))

        this.StatItem($r('sys.symbol.moon'), $r('app.color.sleep'),
          this.formatMinutes(this.sleepMinutes), '', '睡眠')

        Divider()
          .vertical(true)
          .height(36)
          .color($r('app.color.divider'))

        this.StatItem($r('sys.symbol.heart'), $r('app.color.diaper'),
          `${this.diaperCount}`, '次', '尿布')

        Divider()
          .vertical(true)
          .height(36)
          .color($r('app.color.divider'))

        this.StatItem($r('sys.symbol.thermometer'), $r('app.color.health'),
          `${this.temperature}`, '℃', '体温')
      }
      .width('100%')
      .padding({ top: 12, bottom: 12 })
      .justifyContent(FlexAlign.SpaceEvenly)

      Divider()
        .color($r('app.color.divider'))

      // 下次预计
      Row({ space: 6 }) {
        Image($r('sys.symbol.clock'))
          .width(14)
          .height(14)
          .fillColor($r('app.color.primary'))

        Text('下次预计:')
          .fontSize(11)
          .fontColor($r('app.color.text_secondary'))

        Text(this.nextEstimate)
          .fontSize(11)
          .fontWeight(FontWeight.Medium)
          .fontColor($r('app.color.primary'))
      }
      .width('100%')
      .padding({ left: 12, right: 12, top: 8, bottom: 10 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor($r('app.color.bg_card'))
    .borderRadius(16)
    .onClick(() => {
      // 打开 App 首页
    })
  }

  // ==================== 统计项 ====================
  @Builder
  StatItem(icon: Resource, color: Resource, value: string, unit: string, label: string) {
    Column({ space: 4 }) {
      Image(icon)
        .width(18)
        .height(18)
        .fillColor(color)

      Row({ space: 2 }) {
        Text(value)
          .fontSize(16)
          .fontWeight(FontWeight.Bold)
          .fontColor($r('app.color.text_primary'))

        if (unit) {
          Text(unit)
            .fontSize(10)
            .fontColor($r('app.color.text_tertiary'))
        }
      }

      Text(label)
        .fontSize(10)
        .fontColor($r('app.color.text_secondary'))
    }
    .layoutWeight(1)
    .alignItems(HorizontalAlign.Center)
  }

  // ==================== 工具方法 ====================
  private formatMinutes(minutes: number): string {
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    return `${hours}h${mins}m`
  }
}
