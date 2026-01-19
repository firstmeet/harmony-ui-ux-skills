// ==========================================
// HarmonyBaby Care - 主页面（Tab 导航）
// ==========================================

/**
 * 主页面
 * 底部 Tab 导航：首页、记录、洞察、家庭、设置
 */
@Entry
@Component
struct MainPage {
  // ==================== 状态 ====================
  @State currentTabIndex: number = 0

  // Tab 配置
  private tabItems: TabItem[] = [
    { icon: $r('sys.symbol.house'), label: $r('app.string.tab_home') },
    { icon: $r('sys.symbol.doc_text'), label: $r('app.string.tab_record') },
    { icon: $r('sys.symbol.chart_bar'), label: $r('app.string.tab_insight') },
    { icon: $r('sys.symbol.person_2'), label: $r('app.string.tab_family') },
    { icon: $r('sys.symbol.gearshape'), label: $r('app.string.tab_settings') }
  ]

  // ==================== 构建 ====================
  build() {
    Column() {
      // 内容区域
      Tabs({ barPosition: BarPosition.End, index: this.currentTabIndex }) {
        // 首页
        TabContent() {
          this.HomeTab()
        }
        .tabBar(this.TabBarBuilder(0))

        // 记录
        TabContent() {
          this.RecordTab()
        }
        .tabBar(this.TabBarBuilder(1))

        // 洞察
        TabContent() {
          this.InsightTab()
        }
        .tabBar(this.TabBarBuilder(2))

        // 家庭
        TabContent() {
          this.FamilyTab()
        }
        .tabBar(this.TabBarBuilder(3))

        // 设置
        TabContent() {
          this.SettingsTab()
        }
        .tabBar(this.TabBarBuilder(4))
      }
      .barHeight(56)
      .barBackgroundColor($r('app.color.bg_primary'))
      .animationDuration(200)
      .onChange((index) => {
        this.currentTabIndex = index
      })
    }
    .width('100%')
    .height('100%')
  }

  // ==================== Tab Bar 构建器 ====================
  @Builder
  TabBarBuilder(index: number) {
    Column({ space: 4 }) {
      Image(this.tabItems[index].icon)
        .width(24)
        .height(24)
        .fillColor(this.currentTabIndex === index ?
          $r('app.color.primary') :
          $r('app.color.text_tertiary'))

      Text(this.tabItems[index].label)
        .fontSize(10)
        .fontColor(this.currentTabIndex === index ?
          $r('app.color.primary') :
          $r('app.color.text_tertiary'))
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
  }

  // ==================== 首页 Tab ====================
  @Builder
  HomeTab() {
    // 这里引用 HomePage 的内容
    Column() {
      Text('首页内容')
        .fontSize(20)
    }
    .width('100%')
    .height('100%')
    .backgroundColor($r('app.color.bg_secondary'))
  }

  // ==================== 记录 Tab ====================
  @Builder
  RecordTab() {
    Column() {
      Text('记录页面')
        .fontSize(20)
    }
    .width('100%')
    .height('100%')
    .backgroundColor($r('app.color.bg_secondary'))
  }

  // ==================== 洞察 Tab ====================
  @Builder
  InsightTab() {
    Column() {
      Text('数据洞察')
        .fontSize(20)
    }
    .width('100%')
    .height('100%')
    .backgroundColor($r('app.color.bg_secondary'))
  }

  // ==================== 家庭 Tab ====================
  @Builder
  FamilyTab() {
    Column() {
      Text('家庭共享')
        .fontSize(20)
    }
    .width('100%')
    .height('100%')
    .backgroundColor($r('app.color.bg_secondary'))
  }

  // ==================== 设置 Tab ====================
  @Builder
  SettingsTab() {
    Scroll() {
      Column({ space: 16 }) {
        // 宝宝档案卡片
        this.ProfileCard()

        // 设置分组
        this.SettingsGroup('通用设置', [
          { icon: $r('sys.symbol.bell'), title: '通知设置', hasArrow: true },
          { icon: $r('sys.symbol.moon'), title: '深色模式', hasToggle: true }
        ])

        this.SettingsGroup('隐私与数据', [
          { icon: $r('sys.symbol.lock'), title: '隐私设置', hasArrow: true },
          { icon: $r('sys.symbol.arrow_down_doc'), title: '数据导出', hasArrow: true },
          { icon: $r('sys.symbol.icloud'), title: '云同步', hasToggle: true }
        ])

        this.SettingsGroup('关于', [
          { icon: $r('sys.symbol.info_circle'), title: '关于 HarmonyBaby Care', hasArrow: true },
          { icon: $r('sys.symbol.star'), title: '评价应用', hasArrow: true }
        ])

        // 版本信息
        Text('版本 1.0.0')
          .fontSize(12)
          .fontColor($r('app.color.text_tertiary'))
          .margin({ top: 24 })
      }
      .padding(16)
    }
    .width('100%')
    .height('100%')
    .backgroundColor($r('app.color.bg_secondary'))
  }

  // ==================== 宝宝档案卡片 ====================
  @Builder
  ProfileCard() {
    Row({ space: 16 }) {
      // 头像
      Image($r('app.media.baby_avatar'))
        .width(64)
        .height(64)
        .borderRadius(32)
        .backgroundColor($r('app.color.primary_light'))

      Column({ space: 4 }) {
        Text('小宝贝')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor($r('app.color.text_primary'))

        Text('2025年7月15日 · 女宝')
          .fontSize(12)
          .fontColor($r('app.color.text_secondary'))

        Text('5个月12天')
          .fontSize(12)
          .fontColor($r('app.color.primary'))
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      Image($r('sys.symbol.chevron_right'))
        .width(20)
        .height(20)
        .fillColor($r('app.color.text_tertiary'))
    }
    .width('100%')
    .padding(16)
    .backgroundColor($r('app.color.bg_card'))
    .borderRadius(16)
  }

  // ==================== 设置分组 ====================
  @Builder
  SettingsGroup(title: string, items: SettingItem[]) {
    Column({ space: 0 }) {
      Text(title)
        .fontSize(13)
        .fontColor($r('app.color.text_tertiary'))
        .margin({ bottom: 8, left: 4 })

      Column() {
        ForEach(items, (item: SettingItem, index: number) => {
          Row({ space: 12 }) {
            Image(item.icon)
              .width(22)
              .height(22)
              .fillColor($r('app.color.primary'))

            Text(item.title)
              .fontSize(15)
              .fontColor($r('app.color.text_primary'))
              .layoutWeight(1)

            if (item.hasArrow) {
              Image($r('sys.symbol.chevron_right'))
                .width(18)
                .height(18)
                .fillColor($r('app.color.text_tertiary'))
            }

            if (item.hasToggle) {
              Toggle({ type: ToggleType.Switch, isOn: false })
                .selectedColor($r('app.color.primary'))
            }
          }
          .width('100%')
          .padding({ left: 12, right: 12, top: 14, bottom: 14 })

          if (index < items.length - 1) {
            Divider()
              .color($r('app.color.divider'))
              .margin({ left: 46 })
          }
        })
      }
      .backgroundColor($r('app.color.bg_card'))
      .borderRadius(12)
    }
    .width('100%')
    .alignItems(HorizontalAlign.Start)
  }
}

// ==================== 类型定义 ====================
interface TabItem {
  icon: Resource
  label: Resource
}

interface SettingItem {
  icon: Resource
  title: string
  hasArrow?: boolean
  hasToggle?: boolean
}
