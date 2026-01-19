# HarmonyOS NEXT Page Templates

## Overview

This document defines common page structure templates for HarmonyOS NEXT applications.

---

## Login Page (登录页)

**Category**: auth

**Description**: 用户登录页面，包含 Logo、表单、登录按钮等

**Components Used**: Column, Image, TextInput, Button, Text, Divider

**Layout Structure**:
```
Column (主容器)
├── Image (Logo)
├── Text (欢迎语)
├── Column (表单区)
│   ├── TextInput (用户名)
│   └── TextInput (密码)
├── Row (辅助操作)
│   ├── Checkbox (记住密码)
│   └── Text (忘记密码)
├── Button (登录按钮)
├── Divider (分割线)
└── Row (第三方登录)
```

**Code Template**:
```typescript
@Entry
@Component
struct LoginPage {
  @State username: string = ''
  @State password: string = ''

  build() {
    Column() {
      Scroll() {
        Column({ space: 24 }) {
          // Logo
          Image($r('app.media.logo'))
            .width(80)
            .height(80)
            .margin({ top: 60 })
          
          // 欢迎语
          Text('欢迎回来')
            .fontSize(24)
            .fontWeight(FontWeight.Bold)
          
          // 表单
          Column({ space: 16 }) {
            TextInput({ placeholder: '请输入用户名' })
              .height(48)
              .borderRadius(8)
            
            TextInput({ placeholder: '请输入密码' })
              .type(InputType.Password)
              .height(48)
              .borderRadius(8)
          }
          .width('100%')
          
          // 登录按钮
          Button('登录')
            .width('100%')
            .height(48)
            .backgroundColor('#0A59F7')
        }
        .padding(24)
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#FFFFFF')
  }
}
```

---

## Dashboard Page (仪表盘页)

**Category**: dashboard

**Description**: 应用首页，展示概览数据和快捷入口

**Components Used**: Scroll, Column, Row, Text, Image, Grid, List, Swiper

**Layout Structure**:
```
Scroll (可滚动容器)
└── Column (主容器)
    ├── Row (顶部栏)
    │   ├── Text (问候语)
    │   └── Image (头像)
    ├── Swiper (Banner 轮播)
    ├── Grid (快捷入口)
    │   └── GridItem (入口项) * N
    ├── Column (数据统计卡片)
    │   └── Row (统计项) * N
    └── List (最近动态)
```

**Code Template**:
```typescript
@Entry
@Component
struct DashboardPage {
  build() {
    Scroll() {
      Column({ space: 16 }) {
        // 顶部问候
        Row() {
          Column({ space: 4 }) {
            Text('Hi, 用户名')
              .fontSize(20)
              .fontWeight(FontWeight.Bold)
            Text('欢迎回来')
              .fontSize(14)
              .fontColor('#66727A')
          }
          Blank()
          Image($r('app.media.avatar'))
            .width(48)
            .height(48)
            .borderRadius(24)
        }
        .width('100%')
        .padding({ left: 16, right: 16 })
        
        // Banner 轮播
        Swiper() {
          // Banner items
        }
        .height(160)
        .autoPlay(true)
        .indicator(true)
        
        // 快捷入口
        Grid() {
          // Grid items
        }
        .columnsTemplate('1fr 1fr 1fr 1fr')
        .rowsGap(16)
        
        // 数据卡片
        Column() {
          // Stats content
        }
        .padding(16)
        .backgroundColor('#FFFFFF')
        .borderRadius(12)
      }
      .padding(16)
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F1F3F5')
  }
}
```

---

## List Page (列表页)

**Category**: list

**Description**: 数据列表页面，支持下拉刷新和加载更多

**Components Used**: Column, List, ListItem, Row, Image, Text, Search, Refresh

**Layout Structure**:
```
Column (主容器)
├── Search (搜索栏)
├── Row (筛选/排序)
└── Refresh (下拉刷新)
    └── List (列表容器)
        └── ListItem (列表项)
            └── Row
                ├── Image (封面图)
                └── Column (内容区)
                    ├── Text (标题)
                    ├── Text (描述)
                    └── Row (标签/时间)
```

**Code Template**:
```typescript
@Entry
@Component
struct ListPage {
  @State dataList: Array<ItemData> = []
  @State isRefreshing: boolean = false

  build() {
    Column() {
      // 搜索栏
      Search({ placeholder: '搜索' })
        .width('100%')
        .height(40)
        .margin({ left: 16, right: 16 })
      
      // 列表
      Refresh({ refreshing: $$this.isRefreshing }) {
        List({ space: 12 }) {
          ForEach(this.dataList, (item: ItemData) => {
            ListItem() {
              Row({ space: 12 }) {
                Image(item.cover)
                  .width(100)
                  .height(80)
                  .borderRadius(8)
                
                Column({ space: 8 }) {
                  Text(item.title)
                    .fontSize(16)
                    .fontWeight(FontWeight.Medium)
                    .maxLines(2)
                  
                  Text(item.desc)
                    .fontSize(12)
                    .fontColor('#66727A')
                    .maxLines(1)
                }
                .layoutWeight(1)
                .alignItems(HorizontalAlign.Start)
              }
              .padding(12)
              .backgroundColor('#FFFFFF')
              .borderRadius(12)
            }
          })
        }
        .padding({ left: 16, right: 16 })
      }
      .layoutWeight(1)
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F1F3F5')
  }
}
```

---

## Detail Page (详情页)

**Category**: detail

**Description**: 内容详情页面，展示完整信息

**Components Used**: Scroll, Column, Image, Text, Row, Button, Divider

**Layout Structure**:
```
Stack (层叠容器)
├── Scroll (可滚动内容)
│   └── Column
│       ├── Image (主图/轮播)
│       ├── Column (基本信息)
│       │   ├── Text (标题)
│       │   ├── Row (价格/标签)
│       │   └── Text (描述)
│       ├── Divider
│       └── Column (详情内容)
└── Row (底部操作栏)
    ├── Button (收藏)
    ├── Button (分享)
    └── Button (主操作)
```

---

## Settings Page (设置页)

**Category**: settings

**Description**: 应用设置页面，分组展示设置选项

**Components Used**: Scroll, Column, List, ListItem, Row, Text, Toggle, Image

**Layout Structure**:
```
Scroll (可滚动容器)
└── Column (主容器)
    ├── List (账户设置组)
    │   └── ListItem (设置项)
    │       └── Row
    │           ├── Image (图标)
    │           ├── Text (标题)
    │           └── Image (箭头) / Toggle (开关)
    ├── List (通用设置组)
    ├── List (隐私设置组)
    └── Button (退出登录)
```

**Code Template**:
```typescript
@Entry
@Component
struct SettingsPage {
  build() {
    Scroll() {
      Column({ space: 16 }) {
        // 设置分组
        this.SettingsGroup('账户设置', [
          { title: '个人资料', icon: $r('sys.symbol.person'), hasArrow: true },
          { title: '账号安全', icon: $r('sys.symbol.lock'), hasArrow: true },
        ])
        
        this.SettingsGroup('通用设置', [
          { title: '消息通知', icon: $r('sys.symbol.bell'), hasToggle: true },
          { title: '深色模式', icon: $r('sys.symbol.moon'), hasToggle: true },
        ])
        
        // 退出登录
        Button('退出登录')
          .width('100%')
          .height(48)
          .backgroundColor('#E84026')
          .margin({ top: 32 })
      }
      .padding(16)
    }
    .backgroundColor('#F1F3F5')
  }
  
  @Builder
  SettingsGroup(title: string, items: Array<SettingItem>) {
    Column() {
      Text(title)
        .fontSize(14)
        .fontColor('#66727A')
        .margin({ bottom: 8 })
      
      Column() {
        ForEach(items, (item: SettingItem, index: number) => {
          // Setting item row
        })
      }
      .backgroundColor('#FFFFFF')
      .borderRadius(12)
    }
    .width('100%')
    .alignItems(HorizontalAlign.Start)
  }
}
```

---

## Profile Page (个人中心页)

**Category**: profile

**Description**: 用户个人中心页面，展示用户信息和功能入口

**Components Used**: Scroll, Column, Row, Image, Text, Grid, List

**Layout Structure**:
```
Scroll (可滚动容器)
└── Column (主容器)
    ├── Row (用户信息卡片)
    │   ├── Image (头像)
    │   └── Column
    │       ├── Text (昵称)
    │       └── Text (签名)
    ├── Row (数据统计)
    │   ├── Column (关注)
    │   ├── Column (粉丝)
    │   └── Column (获赞)
    ├── Grid (功能入口)
    │   └── GridItem (入口项) * N
    └── List (更多选项)
```
