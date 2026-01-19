// ==========================================
// HarmonyBaby Care - 快速记录卡片 (1×4)
// 原子化服务卡片
// ==========================================

/**
 * 快速记录卡片
 * 功能：一键快速记录喂奶、睡眠、尿布、体温
 * 尺寸：1×4
 */
@Entry
@Component
struct QuickRecordCard {
  // ==================== 构建 ====================
  build() {
    Row() {
      // 喂奶
      this.QuickButton(
        $r('sys.symbol.drop'),
        $r('app.color.feeding'),
        $r('app.color.feeding_light'),
        '喂奶',
        'feeding'
      )

      // 睡眠
      this.QuickButton(
        $r('sys.symbol.moon'),
        $r('app.color.sleep'),
        $r('app.color.sleep_light'),
        '睡眠',
        'sleep'
      )

      // 尿布
      this.QuickButton(
        $r('sys.symbol.heart'),
        $r('app.color.diaper'),
        $r('app.color.diaper_light'),
        '尿布',
        'diaper'
      )

      // 体温
      this.QuickButton(
        $r('sys.symbol.thermometer'),
        $r('app.color.health'),
        $r('app.color.health_light'),
        '体温',
        'temperature'
      )
    }
    .width('100%')
    .height('100%')
    .padding(8)
    .backgroundColor($r('app.color.bg_card'))
    .borderRadius(16)
    .justifyContent(FlexAlign.SpaceEvenly)
  }

  // ==================== 快速按钮 ====================
  @Builder
  QuickButton(icon: Resource, color: Resource, bgColor: Resource, label: string, type: string) {
    Column({ space: 4 }) {
      Button() {
        Image(icon)
          .width(20)
          .height(20)
          .fillColor(color)
      }
      .type(ButtonType.Circle)
      .width(40)
      .height(40)
      .backgroundColor(bgColor)
      .onClick(() => this.onQuickRecord(type))

      Text(label)
        .fontSize(10)
        .fontColor($r('app.color.text_secondary'))
    }
    .alignItems(HorizontalAlign.Center)
  }

  // ==================== 事件处理 ====================
  private onQuickRecord(type: string): void {
    // 根据类型执行快速记录
    // 发送消息到 App 进行处理
  }
}
