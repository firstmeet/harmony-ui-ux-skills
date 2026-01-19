# HarmonyOS NEXT Component Patterns

## Overview

This document defines the component patterns and usage guidelines for HarmonyOS NEXT ArkUI development.

---

## Mandatory Rules for Components

Before using any component, ensure you follow these rules:

1. **Use resource references** - No hardcoded colors or strings
2. **Use explicit types** - No `any` type allowed
3. **Use proper state decorators** - @State, @Prop, @Link, etc.

### Resource Reference Pattern

```typescript
// Define resources in resources/base/element/color.json
// { "color": [{ "name": "primary", "value": "#0A59F7" }] }

// Use in code:
.backgroundColor($r('app.color.primary'))
.fontColor($r('app.color.text_primary'))

// Define strings in resources/base/element/string.json
// { "string": [{ "name": "confirm", "value": "确认" }] }

// Use in code:
Button($r('app.string.confirm'))
Text($r('app.string.welcome_message'))
```

---

## Basic Components

### Button

**Description**: 按钮组件，用于触发操作或事件

**Props**:
- `type`: ButtonType (Normal, Capsule, Circle)
- `stateEffect`: boolean - 是否开启按压态效果
- `buttonStyle`: ButtonStyleMode - 按钮样式模式

**Usage Example**:
```typescript
Button('确认', { type: ButtonType.Capsule })
  .width('80%')
  .height(40)
  .backgroundColor('#0A59F7')
  .fontColor('#FFFFFF')
  .fontSize(14)
  .fontWeight(FontWeight.Medium)
  .onClick(() => { })
```

**Variants**:
- Primary: `backgroundColor('#0A59F7')` + `fontColor('#FFFFFF')`
- Secondary: `backgroundColor('#F1F3F5')` + `fontColor('#182431')`
- Outline: `backgroundColor('transparent')` + `borderWidth(1)` + `borderColor('#0A59F7')`
- Danger: `backgroundColor('#E84026')` + `fontColor('#FFFFFF')`

---

### Text

**Description**: 文本组件，用于显示文字内容

**Props**:
- `content`: string | Resource - 文本内容
- `fontSize`: number | string - 字体大小
- `fontColor`: ResourceColor - 字体颜色
- `fontWeight`: FontWeight - 字体粗细
- `textAlign`: TextAlign - 文本对齐方式

**Usage Example**:
```typescript
Text('Hello HarmonyOS')
  .fontSize(16)
  .fontColor('#182431')
  .fontWeight(FontWeight.Medium)
  .lineHeight(24)
  .maxLines(2)
  .textOverflow({ overflow: TextOverflow.Ellipsis })
```

---

### Image

**Description**: 图片组件，用于显示图片资源

**Props**:
- `src`: PixelMap | ResourceStr | DrawableDescriptor
- `objectFit`: ImageFit - 图片填充模式
- `interpolation`: ImageInterpolation - 图片插值

**Usage Example**:
```typescript
Image($r('app.media.icon'))
  .width(100)
  .height(100)
  .objectFit(ImageFit.Cover)
  .borderRadius(8)
```

---

### TextInput

**Description**: 单行文本输入框组件

**Props**:
- `placeholder`: ResourceStr - 占位符文本
- `type`: InputType - 输入类型
- `maxLength`: number - 最大输入长度
- `enterKeyType`: EnterKeyType - 回车键类型

**Usage Example**:
```typescript
TextInput({ placeholder: '请输入用户名' })
  .width('100%')
  .height(48)
  .padding({ left: 16, right: 16 })
  .backgroundColor('#FFFFFF')
  .borderRadius(8)
  .borderWidth(1)
  .borderColor('#E5E8EB')
  .fontSize(14)
  .placeholderColor('#99A4AE')
  .onChange((value) => { })
  .onFocus(() => { })
  .onBlur(() => { })
```

---

### Toggle

**Description**: 开关组件，用于切换状态

**Props**:
- `type`: ToggleType (Checkbox, Switch, Button)
- `isOn`: boolean - 是否开启
- `selectedColor`: ResourceColor - 选中颜色

**Usage Example**:
```typescript
Toggle({ type: ToggleType.Switch, isOn: true })
  .selectedColor('#0A59F7')
  .switchPointColor('#FFFFFF')
  .onChange((isOn) => { })
```

---

## Feedback Components

### Dialog

**Description**: 对话框组件，用于重要信息提示或操作确认

**Usage Example**:
```typescript
AlertDialog.show({
  title: '提示',
  message: '确认删除此项？',
  autoCancel: true,
  alignment: DialogAlignment.Center,
  primaryButton: {
    value: '取消',
    action: () => { }
  },
  secondaryButton: {
    value: '确认',
    fontColor: '#E84026',
    action: () => { }
  }
})
```

---

### Toast (Custom)

**Description**: 轻提示组件

**Pattern**:
```typescript
Row({ space: 8 }) {
  Image($r('sys.symbol.checkmark_circle_fill'))
    .width(20)
    .height(20)
    .fillColor('#FFFFFF')
  Text('操作成功')
    .fontSize(14)
    .fontColor('#FFFFFF')
}
.padding({ left: 16, right: 16, top: 12, bottom: 12 })
.backgroundColor('rgba(0, 0, 0, 0.75)')
.borderRadius(8)
```

---

### Loading

**Description**: 加载中组件

**Usage Example**:
```typescript
LoadingProgress()
  .width(48)
  .height(48)
  .color('#0A59F7')
```

---

## Navigation Components

### Tabs

**Description**: 页签组件，用于页面切换导航

**Usage Example**:
```typescript
Tabs({ barPosition: BarPosition.End }) {
  TabContent() {
    // 首页内容
  }
  .tabBar(this.TabBuilder('首页', 0, $r('sys.symbol.house')))
  
  TabContent() {
    // 我的内容
  }
  .tabBar(this.TabBuilder('我的', 1, $r('sys.symbol.person')))
}
.barWidth('100%')
.barHeight(56)
.animationDuration(200)
.onChange((index) => { this.currentIndex = index })

@Builder
TabBuilder(title: string, index: number, icon: Resource) {
  Column({ space: 4 }) {
    Image(icon)
      .width(24)
      .height(24)
      .fillColor(this.currentIndex === index ? '#0A59F7' : '#99A4AE')
    Text(title)
      .fontSize(10)
      .fontColor(this.currentIndex === index ? '#0A59F7' : '#99A4AE')
  }
}
```

---

### Navigation

**Description**: 导航组件，用于页面路由导航

**Usage Example**:
```typescript
Navigation() {
  // 页面内容
}
.title('页面标题')
.mode(NavigationMode.Stack)
.titleMode(NavigationTitleMode.Mini)
.navBarWidth('100%')
.navBarPosition(NavBarPosition.Start)
.menus([
  {
    value: '',
    icon: $r('sys.symbol.ellipsis'),
    action: () => { }
  }
])
```

---

## Layout Components

### List

**Description**: 列表组件，用于展示列表数据

**Usage Example**:
```typescript
List({ space: 12 }) {
  ForEach(this.dataList, (item: DataItem) => {
    ListItem() {
      Row({ space: 12 }) {
        Image(item.avatar)
          .width(48)
          .height(48)
          .borderRadius(24)
        Column({ space: 4 }) {
          Text(item.title)
            .fontSize(16)
            .fontWeight(FontWeight.Medium)
          Text(item.subtitle)
            .fontSize(12)
            .fontColor('#66727A')
        }
        .alignItems(HorizontalAlign.Start)
        .layoutWeight(1)
      }
      .width('100%')
      .padding(16)
      .backgroundColor('#FFFFFF')
      .borderRadius(12)
    }
  })
}
.width('100%')
.divider({ strokeWidth: 0 })
```

---

### Grid

**Description**: 网格组件，用于网格布局展示

**Usage Example**:
```typescript
Grid() {
  ForEach(this.items, (item: GridItemData) => {
    GridItem() {
      Column({ space: 8 }) {
        Image(item.icon)
          .width(48)
          .height(48)
        Text(item.name)
          .fontSize(12)
          .fontColor('#182431')
      }
      .width('100%')
      .padding(16)
      .backgroundColor('#FFFFFF')
      .borderRadius(12)
    }
  })
}
.columnsTemplate('1fr 1fr 1fr 1fr')
.columnsGap(12)
.rowsGap(12)
.padding(16)
```

---

### Swiper

**Description**: 轮播组件，用于轮播展示内容

**Usage Example**:
```typescript
Swiper() {
  ForEach(this.banners, (item: BannerData) => {
    Image(item.imageUrl)
      .width('100%')
      .height(180)
      .borderRadius(12)
      .objectFit(ImageFit.Cover)
  })
}
.autoPlay(true)
.interval(4000)
.indicator(
  Indicator.dot()
    .selectedColor('#0A59F7')
    .color('#C5CDD7')
)
.loop(true)
```
