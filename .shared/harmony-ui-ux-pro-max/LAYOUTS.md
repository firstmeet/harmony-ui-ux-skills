# HarmonyOS NEXT Layout Patterns

## Overview

This document defines the layout patterns for HarmonyOS NEXT ArkUI development.

---

## Row (水平布局)

**Description**: 沿水平方向排列子组件

**Use Case**: 水平排列按钮、图标、文字等

**Pattern**:
```typescript
Row({ space: 12 }) {
  Image($r('app.media.avatar'))
    .width(40)
    .height(40)
    .borderRadius(20)
  
  Column({ space: 4 }) {
    Text('用户名')
      .fontSize(16)
      .fontWeight(FontWeight.Medium)
    Text('在线')
      .fontSize(12)
      .fontColor('#66727A')
  }
  .alignItems(HorizontalAlign.Start)
  .layoutWeight(1)
  
  Image($r('sys.symbol.chevron_right'))
    .width(20)
    .height(20)
    .fillColor('#99A4AE')
}
.width('100%')
.padding(16)
.justifyContent(FlexAlign.Start)
```

---

## Column (垂直布局)

**Description**: 沿垂直方向排列子组件

**Use Case**: 垂直排列表单项、列表内容等

**Pattern**:
```typescript
Column({ space: 16 }) {
  Text('标题')
    .fontSize(20)
    .fontWeight(FontWeight.Bold)
    .fontColor('#182431')
  
  Text('这是一段描述内容，说明当前页面的用途和功能。')
    .fontSize(14)
    .fontColor('#66727A')
    .lineHeight(22)
  
  Button('操作按钮')
    .width('100%')
    .height(44)
    .backgroundColor('#0A59F7')
}
.width('100%')
.alignItems(HorizontalAlign.Start)
.padding(16)
```

---

## Flex (弹性布局)

**Description**: 弹性布局容器，支持自动换行

**Use Case**: 标签云、自适应按钮组等

**Pattern**:
```typescript
Flex({ 
  wrap: FlexWrap.Wrap, 
  justifyContent: FlexAlign.Start 
}) {
  ForEach(this.tags, (tag: string) => {
    Text(tag)
      .fontSize(12)
      .fontColor('#0A59F7')
      .padding({ left: 12, right: 12, top: 6, bottom: 6 })
      .backgroundColor('#E6F0FF')
      .borderRadius(16)
      .margin({ right: 8, bottom: 8 })
  })
}
.width('100%')
```

---

## Stack (层叠布局)

**Description**: 子组件按照层叠关系展示

**Use Case**: 浮动按钮、图片上的文字标签等

**Pattern**:
```typescript
Stack({ alignContent: Alignment.BottomEnd }) {
  Image($r('app.media.cover'))
    .width('100%')
    .height(200)
    .objectFit(ImageFit.Cover)
    .borderRadius(12)
  
  Text('HOT')
    .fontSize(12)
    .fontColor('#FFFFFF')
    .padding({ left: 8, right: 8, top: 4, bottom: 4 })
    .backgroundColor('#E84026')
    .borderRadius(4)
    .margin(12)
}
.width('100%')
```

---

## RelativeContainer (相对布局)

**Description**: 通过锚点约束进行相对定位

**Use Case**: 复杂定位场景、卡片内部布局等

**Pattern**:
```typescript
RelativeContainer() {
  Text('标题')
    .fontSize(18)
    .fontWeight(FontWeight.Bold)
    .id('title')
    .alignRules({
      top: { anchor: '__container__', align: VerticalAlign.Top },
      left: { anchor: '__container__', align: HorizontalAlign.Start }
    })
  
  Text('副标题')
    .fontSize(14)
    .fontColor('#66727A')
    .id('subtitle')
    .alignRules({
      top: { anchor: 'title', align: VerticalAlign.Bottom },
      left: { anchor: 'title', align: HorizontalAlign.Start }
    })
    .margin({ top: 8 })
  
  Image($r('sys.symbol.chevron_right'))
    .width(20)
    .height(20)
    .id('arrow')
    .alignRules({
      center: { anchor: '__container__', align: VerticalAlign.Center },
      right: { anchor: '__container__', align: HorizontalAlign.End }
    })
}
.width('100%')
.height(80)
.padding(16)
```

---

## GridRow/GridCol (栅格布局)

**Description**: 响应式栅格布局系统

**Use Case**: 多设备自适应布局、表单排列等

**Pattern**:
```typescript
GridRow({ 
  columns: 12, 
  gutter: { x: 12, y: 12 } 
}) {
  GridCol({ span: { sm: 12, md: 6, lg: 4 } }) {
    // 卡片 1
    this.CardBuilder('卡片1')
  }
  
  GridCol({ span: { sm: 12, md: 6, lg: 4 } }) {
    // 卡片 2
    this.CardBuilder('卡片2')
  }
  
  GridCol({ span: { sm: 12, md: 12, lg: 4 } }) {
    // 卡片 3
    this.CardBuilder('卡片3')
  }
}
.width('100%')
.padding(16)

@Builder
CardBuilder(title: string) {
  Column() {
    Text(title)
      .fontSize(16)
  }
  .width('100%')
  .padding(16)
  .backgroundColor('#FFFFFF')
  .borderRadius(12)
}
```

---

## WaterFlow (瀑布流布局)

**Description**: 瀑布流布局，适用于不规则高度的内容展示

**Use Case**: 图片画廊、商品瀑布流等

**Pattern**:
```typescript
WaterFlow() {
  ForEach(this.items, (item: WaterFlowItem) => {
    FlowItem() {
      Column() {
        Image(item.imageUrl)
          .width('100%')
          .aspectRatio(item.aspectRatio)
          .objectFit(ImageFit.Cover)
          .borderRadius({ topLeft: 8, topRight: 8 })
        
        Text(item.title)
          .fontSize(14)
          .fontColor('#182431')
          .padding(12)
          .maxLines(2)
          .textOverflow({ overflow: TextOverflow.Ellipsis })
      }
      .backgroundColor('#FFFFFF')
      .borderRadius(8)
    }
  })
}
.columnsTemplate('1fr 1fr')
.columnsGap(12)
.rowsGap(12)
.padding(16)
```

---

## Scroll (滚动布局)

**Description**: 可滚动的容器组件

**Use Case**: 长页面、表单页等

**Pattern**:
```typescript
Scroll() {
  Column({ space: 16 }) {
    // 顶部内容
    this.HeaderSection()
    
    // 中间内容
    this.ContentSection()
    
    // 底部内容
    this.FooterSection()
  }
  .width('100%')
  .padding({ bottom: 24 })
}
.scrollBar(BarState.Off)
.edgeEffect(EdgeEffect.Spring)
.width('100%')
.height('100%')
```

---

## Common Layout Patterns

### List Item Pattern

```typescript
Row({ space: 12 }) {
  // 左侧图标/图片
  Image(icon)
    .width(48)
    .height(48)
    .borderRadius(8)
  
  // 中间内容
  Column({ space: 4 }) {
    Text(title)
      .fontSize(16)
      .fontWeight(FontWeight.Medium)
      .fontColor('#182431')
    Text(subtitle)
      .fontSize(12)
      .fontColor('#66727A')
  }
  .alignItems(HorizontalAlign.Start)
  .layoutWeight(1)
  
  // 右侧操作/箭头
  Image($r('sys.symbol.chevron_right'))
    .width(20)
    .height(20)
    .fillColor('#C5CDD7')
}
.width('100%')
.padding(16)
.backgroundColor('#FFFFFF')
```

### Card Pattern

```typescript
Column({ space: 12 }) {
  // 卡片头部
  Row() {
    Text('标题')
      .fontSize(18)
      .fontWeight(FontWeight.Bold)
    Blank()
    Text('查看更多')
      .fontSize(14)
      .fontColor('#0A59F7')
  }
  .width('100%')
  
  // 卡片内容
  // ...
}
.width('100%')
.padding(16)
.backgroundColor('#FFFFFF')
.borderRadius(12)
.shadow({
  radius: 8,
  color: 'rgba(0, 0, 0, 0.08)',
  offsetY: 2
})
```

### Form Layout Pattern

```typescript
Column({ space: 20 }) {
  // 表单项
  Column({ space: 8 }) {
    Text('标签')
      .fontSize(14)
      .fontWeight(FontWeight.Medium)
      .fontColor('#182431')
    
    TextInput({ placeholder: '请输入' })
      .width('100%')
      .height(48)
      .padding({ left: 16, right: 16 })
      .backgroundColor('#FFFFFF')
      .borderRadius(8)
      .borderWidth(1)
      .borderColor('#E5E8EB')
  }
  .width('100%')
  .alignItems(HorizontalAlign.Start)
  
  // 更多表单项...
  
  // 提交按钮
  Button('提交')
    .width('100%')
    .height(48)
    .backgroundColor('#0A59F7')
    .borderRadius(8)
}
.width('100%')
.padding(16)
```
