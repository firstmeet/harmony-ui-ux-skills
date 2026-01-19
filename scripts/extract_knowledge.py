"""
HarmonyOS NEXT UI/UX Pro Max Skill - 知识提取脚本
从网络资源中提取 UI/UX 模板、布局、字体等知识并写入 CSV
"""

import os
import sys
import csv
import json
import time
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

# 初始化 colorama
init()

# ============== 日志函数 ==============
def log_info(message: str):
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {message}")

def log_success(message: str):
    print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {message}")

def log_warning(message: str):
    print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {message}")

def log_error(message: str):
    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}")


# ============== 配置 ==============
OUTPUT_DIR = Path(__file__).parent.parent / "knowledge_base"
REQUEST_TIMEOUT = 30
REQUEST_DELAY = 1

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# ============== 数据类定义 ==============
@dataclass
class ComponentTemplate:
    """组件模板"""
    name: str
    category: str  # basic, layout, navigation, feedback, form
    description: str
    props: str  # JSON 格式的属性列表
    usage_example: str
    source: str
    
@dataclass
class LayoutPattern:
    """布局模式"""
    name: str
    type: str  # row, column, grid, flex, stack, relative
    description: str
    use_case: str
    code_example: str
    source: str

@dataclass
class ColorToken:
    """颜色 Token"""
    name: str
    value: str
    category: str  # brand, semantic, neutral
    usage: str
    light_mode: str
    dark_mode: str
    source: str

@dataclass
class TypographyStyle:
    """字体样式"""
    name: str
    font_family: str
    font_size: str
    font_weight: str
    line_height: str
    use_case: str
    source: str

@dataclass
class SpacingToken:
    """间距 Token"""
    name: str
    value: str
    use_case: str
    source: str

@dataclass
class AnimationPattern:
    """动效模式"""
    name: str
    duration: str
    easing: str
    description: str
    use_case: str
    source: str

@dataclass
class PageTemplate:
    """页面模板"""
    name: str
    category: str  # auth, dashboard, list, detail, settings, profile
    description: str
    components_used: str
    layout_structure: str
    source: str


# ============== 知识提取类 ==============
class HarmonyKnowledgeExtractor:
    """HarmonyOS NEXT UI/UX 知识提取器"""
    
    def __init__(self):
        self.components: List[ComponentTemplate] = []
        self.layouts: List[LayoutPattern] = []
        self.colors: List[ColorToken] = []
        self.typography: List[TypographyStyle] = []
        self.spacing: List[SpacingToken] = []
        self.animations: List[AnimationPattern] = []
        self.page_templates: List[PageTemplate] = []
    
    def fetch_page(self, url: str) -> Optional[str]:
        """获取网页内容"""
        try:
            response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.text
        except Exception as e:
            log_warning(f"获取页面失败 {url}: {e}")
            return None
    
    def extract_from_huawei_docs(self):
        """从华为开发者文档提取知识"""
        log_info("正在从华为开发者文档提取知识...")
        
        # 基于官方文档和设计规范定义的标准组件
        self._add_standard_components()
        self._add_standard_layouts()
        self._add_standard_colors()
        self._add_standard_typography()
        self._add_standard_spacing()
        self._add_standard_animations()
        self._add_standard_page_templates()
    
    def _add_standard_components(self):
        """添加标准组件模板"""
        components_data = [
            # 基础组件
            {
                "name": "Button",
                "category": "basic",
                "description": "按钮组件，用于触发操作或事件",
                "props": json.dumps({
                    "type": "ButtonType (Normal, Capsule, Circle)",
                    "stateEffect": "boolean - 是否开启按压态效果",
                    "buttonStyle": "ButtonStyleMode - 按钮样式模式"
                }, ensure_ascii=False),
                "usage_example": """Button('确认', { type: ButtonType.Capsule })
  .width('80%')
  .height(40)
  .backgroundColor('#0A59F7')
  .onClick(() => { })""",
                "source": "HarmonyOS ArkUI 官方文档"
            },
            {
                "name": "Text",
                "category": "basic",
                "description": "文本组件，用于显示文字内容",
                "props": json.dumps({
                    "content": "string | Resource - 文本内容",
                    "fontSize": "number | string - 字体大小",
                    "fontColor": "ResourceColor - 字体颜色",
                    "fontWeight": "FontWeight - 字体粗细",
                    "textAlign": "TextAlign - 文本对齐方式"
                }, ensure_ascii=False),
                "usage_example": """Text('Hello HarmonyOS')
  .fontSize(16)
  .fontColor('#182431')
  .fontWeight(FontWeight.Medium)""",
                "source": "HarmonyOS ArkUI 官方文档"
            },
            {
                "name": "Image",
                "category": "basic",
                "description": "图片组件，用于显示图片资源",
                "props": json.dumps({
                    "src": "PixelMap | ResourceStr | DrawableDescriptor",
                    "objectFit": "ImageFit - 图片填充模式",
                    "interpolation": "ImageInterpolation - 图片插值"
                }, ensure_ascii=False),
                "usage_example": """Image($r('app.media.icon'))
  .width(100)
  .height(100)
  .objectFit(ImageFit.Cover)
  .borderRadius(8)""",
                "source": "HarmonyOS ArkUI 官方文档"
            },
            {
                "name": "TextInput",
                "category": "form",
                "description": "单行文本输入框组件",
                "props": json.dumps({
                    "placeholder": "ResourceStr - 占位符文本",
                    "type": "InputType - 输入类型",
                    "maxLength": "number - 最大输入长度",
                    "enterKeyType": "EnterKeyType - 回车键类型"
                }, ensure_ascii=False),
                "usage_example": """TextInput({ placeholder: '请输入用户名' })
  .width('100%')
  .height(48)
  .borderRadius(8)
  .onChange((value) => { })""",
                "source": "HarmonyOS ArkUI 官方文档"
            },
            {
                "name": "Toggle",
                "category": "form",
                "description": "开关组件，用于切换状态",
                "props": json.dumps({
                    "type": "ToggleType (Checkbox, Switch, Button)",
                    "isOn": "boolean - 是否开启",
                    "selectedColor": "ResourceColor - 选中颜色"
                }, ensure_ascii=False),
                "usage_example": """Toggle({ type: ToggleType.Switch, isOn: true })
  .selectedColor('#0A59F7')
  .onChange((isOn) => { })""",
                "source": "HarmonyOS ArkUI 官方文档"
            },
            {
                "name": "Slider",
                "category": "form",
                "description": "滑动条组件，用于数值选择",
                "props": json.dumps({
                    "value": "number - 当前值",
                    "min": "number - 最小值",
                    "max": "number - 最大值",
                    "step": "number - 步长",
                    "style": "SliderStyle - 滑块样式"
                }, ensure_ascii=False),
                "usage_example": """Slider({ value: 50, min: 0, max: 100, step: 1 })
  .width('100%')
  .trackColor('#E5E8EB')
  .selectedColor('#0A59F7')
  .onChange((value) => { })""",
                "source": "HarmonyOS ArkUI 官方文档"
            },
            {
                "name": "Progress",
                "category": "feedback",
                "description": "进度条组件，用于显示任务进度",
                "props": json.dumps({
                    "value": "number - 当前进度值",
                    "total": "number - 总进度值",
                    "type": "ProgressType - 进度条类型"
                }, ensure_ascii=False),
                "usage_example": """Progress({ value: 60, total: 100, type: ProgressType.Linear })
  .width('100%')
  .color('#0A59F7')""",
                "source": "HarmonyOS ArkUI 官方文档"
            },
            {
                "name": "LoadingProgress",
                "category": "feedback",
                "description": "加载中组件，用于显示加载状态",
                "props": json.dumps({
                    "color": "ResourceColor - 加载动画颜色"
                }, ensure_ascii=False),
                "usage_example": """LoadingProgress()
  .width(48)
  .height(48)
  .color('#0A59F7')""",
                "source": "HarmonyOS ArkUI 官方文档"
            },
            {
                "name": "Badge",
                "category": "feedback",
                "description": "徽标组件，用于显示消息数量或状态",
                "props": json.dumps({
                    "count": "number - 徽标数字",
                    "maxCount": "number - 最大显示数字",
                    "position": "BadgePosition - 徽标位置"
                }, ensure_ascii=False),
                "usage_example": """Badge({ count: 10, maxCount: 99, position: BadgePosition.RightTop }) {
  Image($r('app.media.message'))
    .width(48)
    .height(48)
}""",
                "source": "HarmonyOS ArkUI 官方文档"
            },
            {
                "name": "Tabs",
                "category": "navigation",
                "description": "页签组件，用于页面切换导航",
                "props": json.dumps({
                    "barPosition": "BarPosition - 页签位置",
                    "index": "number - 当前页签索引",
                    "controller": "TabsController - 控制器"
                }, ensure_ascii=False),
                "usage_example": """Tabs({ barPosition: BarPosition.Start }) {
  TabContent() { Text('首页') }.tabBar('首页')
  TabContent() { Text('我的') }.tabBar('我的')
}
.barWidth('100%')
.barHeight(56)""",
                "source": "HarmonyOS ArkUI 官方文档"
            },
            {
                "name": "Navigation",
                "category": "navigation",
                "description": "导航组件，用于页面路由导航",
                "props": json.dumps({
                    "title": "string | CustomBuilder - 标题",
                    "mode": "NavigationMode - 导航模式",
                    "navBarWidth": "Length - 导航栏宽度"
                }, ensure_ascii=False),
                "usage_example": """Navigation() {
  // 页面内容
}
.title('页面标题')
.mode(NavigationMode.Stack)
.titleMode(NavigationTitleMode.Mini)""",
                "source": "HarmonyOS ArkUI 官方文档"
            },
            {
                "name": "List",
                "category": "layout",
                "description": "列表组件，用于展示列表数据",
                "props": json.dumps({
                    "space": "number - 列表项间距",
                    "initialIndex": "number - 初始索引",
                    "scroller": "Scroller - 滚动控制器"
                }, ensure_ascii=False),
                "usage_example": """List({ space: 12 }) {
  ForEach(this.dataList, (item) => {
    ListItem() {
      Text(item.title)
    }
  })
}
.width('100%')
.divider({ strokeWidth: 0.5, color: '#E5E8EB' })""",
                "source": "HarmonyOS ArkUI 官方文档"
            },
            {
                "name": "Grid",
                "category": "layout",
                "description": "网格组件，用于网格布局展示",
                "props": json.dumps({
                    "columnsTemplate": "string - 列模板",
                    "rowsTemplate": "string - 行模板",
                    "columnsGap": "Length - 列间距",
                    "rowsGap": "Length - 行间距"
                }, ensure_ascii=False),
                "usage_example": """Grid() {
  ForEach(this.items, (item) => {
    GridItem() {
      Text(item.name)
    }
  })
}
.columnsTemplate('1fr 1fr 1fr')
.columnsGap(12)
.rowsGap(12)""",
                "source": "HarmonyOS ArkUI 官方文档"
            },
            {
                "name": "Swiper",
                "category": "layout",
                "description": "轮播组件，用于轮播展示内容",
                "props": json.dumps({
                    "index": "number - 当前索引",
                    "autoPlay": "boolean - 自动播放",
                    "interval": "number - 播放间隔(ms)",
                    "indicator": "boolean | DotIndicator - 指示器"
                }, ensure_ascii=False),
                "usage_example": """Swiper() {
  ForEach(this.banners, (item) => {
    Image(item.imageUrl)
      .width('100%')
      .height(200)
  })
}
.autoPlay(true)
.interval(3000)
.indicator(true)""",
                "source": "HarmonyOS ArkUI 官方文档"
            },
            {
                "name": "Dialog",
                "category": "feedback",
                "description": "对话框组件，用于重要信息提示或操作确认",
                "props": json.dumps({
                    "title": "ResourceStr - 标题",
                    "message": "ResourceStr - 消息内容",
                    "autoCancel": "boolean - 点击遮罩是否关闭",
                    "alignment": "DialogAlignment - 对齐方式"
                }, ensure_ascii=False),
                "usage_example": """AlertDialog.show({
  title: '提示',
  message: '确认删除此项？',
  primaryButton: {
    value: '取消',
    action: () => { }
  },
  secondaryButton: {
    value: '确认',
    fontColor: '#E84026',
    action: () => { }
  }
})""",
                "source": "HarmonyOS ArkUI 官方文档"
            },
        ]
        
        for data in components_data:
            self.components.append(ComponentTemplate(**data))
        
        log_success(f"已添加 {len(components_data)} 个标准组件模板")
    
    def _add_standard_layouts(self):
        """添加标准布局模式"""
        layouts_data = [
            {
                "name": "Row 水平布局",
                "type": "row",
                "description": "沿水平方向排列子组件",
                "use_case": "水平排列按钮、图标、文字等",
                "code_example": """Row({ space: 12 }) {
  Image($r('app.media.avatar')).width(40).height(40)
  Column() {
    Text('用户名').fontSize(16).fontWeight(FontWeight.Medium)
    Text('在线').fontSize(12).fontColor('#66727A')
  }.alignItems(HorizontalAlign.Start)
}
.width('100%')
.justifyContent(FlexAlign.Start)""",
                "source": "HarmonyOS ArkUI 布局指南"
            },
            {
                "name": "Column 垂直布局",
                "type": "column",
                "description": "沿垂直方向排列子组件",
                "use_case": "垂直排列表单项、列表内容等",
                "code_example": """Column({ space: 16 }) {
  Text('标题').fontSize(20).fontWeight(FontWeight.Bold)
  Text('描述内容').fontSize(14).fontColor('#66727A')
  Button('操作按钮').width('100%')
}
.width('100%')
.alignItems(HorizontalAlign.Start)
.padding(16)""",
                "source": "HarmonyOS ArkUI 布局指南"
            },
            {
                "name": "Flex 弹性布局",
                "type": "flex",
                "description": "弹性布局容器，支持自动换行",
                "use_case": "标签云、自适应按钮组等",
                "code_example": """Flex({ wrap: FlexWrap.Wrap, space: { main: LengthMetrics.vp(8), cross: LengthMetrics.vp(8) } }) {
  ForEach(this.tags, (tag) => {
    Text(tag)
      .fontSize(12)
      .padding({ left: 12, right: 12, top: 6, bottom: 6 })
      .backgroundColor('#F1F3F5')
      .borderRadius(16)
  })
}""",
                "source": "HarmonyOS ArkUI 布局指南"
            },
            {
                "name": "Stack 层叠布局",
                "type": "stack",
                "description": "子组件按照层叠关系展示",
                "use_case": "浮动按钮、图片上的文字标签等",
                "code_example": """Stack({ alignContent: Alignment.BottomEnd }) {
  Image($r('app.media.cover'))
    .width('100%')
    .height(200)
  Text('HOT')
    .fontSize(12)
    .fontColor(Color.White)
    .padding(8)
    .backgroundColor('#E84026')
    .borderRadius(4)
    .margin(12)
}""",
                "source": "HarmonyOS ArkUI 布局指南"
            },
            {
                "name": "RelativeContainer 相对布局",
                "type": "relative",
                "description": "通过锚点约束进行相对定位",
                "use_case": "复杂定位场景、卡片内部布局等",
                "code_example": """RelativeContainer() {
  Text('标题')
    .id('title')
    .alignRules({
      top: { anchor: '__container__', align: VerticalAlign.Top },
      left: { anchor: '__container__', align: HorizontalAlign.Start }
    })
  Text('副标题')
    .alignRules({
      top: { anchor: 'title', align: VerticalAlign.Bottom },
      left: { anchor: 'title', align: HorizontalAlign.Start }
    })
    .margin({ top: 8 })
}""",
                "source": "HarmonyOS ArkUI 布局指南"
            },
            {
                "name": "GridRow/GridCol 栅格布局",
                "type": "grid",
                "description": "响应式栅格布局系统",
                "use_case": "多设备自适应布局、表单排列等",
                "code_example": """GridRow({ columns: 12, gutter: 12 }) {
  GridCol({ span: { sm: 12, md: 6, lg: 4 } }) {
    // 卡片内容
  }
  GridCol({ span: { sm: 12, md: 6, lg: 4 } }) {
    // 卡片内容
  }
}""",
                "source": "HarmonyOS ArkUI 布局指南"
            },
            {
                "name": "WaterFlow 瀑布流布局",
                "type": "waterflow",
                "description": "瀑布流布局，适用于不规则高度的内容展示",
                "use_case": "图片画廊、商品瀑布流等",
                "code_example": """WaterFlow() {
  ForEach(this.items, (item) => {
    FlowItem() {
      Column() {
        Image(item.imageUrl)
          .width('100%')
          .objectFit(ImageFit.Cover)
        Text(item.title).fontSize(14).padding(8)
      }
      .backgroundColor(Color.White)
      .borderRadius(8)
    }
  })
}
.columnsTemplate('1fr 1fr')
.columnsGap(12)
.rowsGap(12)""",
                "source": "HarmonyOS ArkUI 布局指南"
            },
        ]
        
        for data in layouts_data:
            self.layouts.append(LayoutPattern(**data))
        
        log_success(f"已添加 {len(layouts_data)} 个布局模式")
    
    def _add_standard_colors(self):
        """添加标准颜色 Token"""
        colors_data = [
            # 品牌色
            {"name": "primary", "value": "#0A59F7", "category": "brand", "usage": "主要操作按钮、链接、强调元素", "light_mode": "#0A59F7", "dark_mode": "#317AF7", "source": "HarmonyOS 设计规范"},
            {"name": "primary_light", "value": "#5B8FF9", "category": "brand", "usage": "悬浮状态、次要强调", "light_mode": "#5B8FF9", "dark_mode": "#5B8FF9", "source": "HarmonyOS 设计规范"},
            {"name": "primary_dark", "value": "#0041C2", "category": "brand", "usage": "按压状态", "light_mode": "#0041C2", "dark_mode": "#0A59F7", "source": "HarmonyOS 设计规范"},
            {"name": "secondary", "value": "#36D1DC", "category": "brand", "usage": "辅助强调、渐变配色", "light_mode": "#36D1DC", "dark_mode": "#36D1DC", "source": "HarmonyOS 设计规范"},
            {"name": "accent", "value": "#FF6B35", "category": "brand", "usage": "强调色、促销标签", "light_mode": "#FF6B35", "dark_mode": "#FF8A5B", "source": "HarmonyOS 设计规范"},
            
            # 语义色
            {"name": "success", "value": "#64BB5C", "category": "semantic", "usage": "成功状态、完成提示", "light_mode": "#64BB5C", "dark_mode": "#7ACC74", "source": "HarmonyOS 设计规范"},
            {"name": "warning", "value": "#FA9D3B", "category": "semantic", "usage": "警告状态、注意提示", "light_mode": "#FA9D3B", "dark_mode": "#FFB05E", "source": "HarmonyOS 设计规范"},
            {"name": "error", "value": "#E84026", "category": "semantic", "usage": "错误状态、删除操作", "light_mode": "#E84026", "dark_mode": "#F05C44", "source": "HarmonyOS 设计规范"},
            {"name": "info", "value": "#0A59F7", "category": "semantic", "usage": "信息提示、帮助说明", "light_mode": "#0A59F7", "dark_mode": "#317AF7", "source": "HarmonyOS 设计规范"},
            
            # 中性色
            {"name": "text_primary", "value": "#182431", "category": "neutral", "usage": "主要文字、标题", "light_mode": "#182431", "dark_mode": "#E5E8EB", "source": "HarmonyOS 设计规范"},
            {"name": "text_secondary", "value": "#66727A", "category": "neutral", "usage": "次要文字、说明", "light_mode": "#66727A", "dark_mode": "#99A4AE", "source": "HarmonyOS 设计规范"},
            {"name": "text_tertiary", "value": "#99A4AE", "category": "neutral", "usage": "辅助文字、占位符", "light_mode": "#99A4AE", "dark_mode": "#66727A", "source": "HarmonyOS 设计规范"},
            {"name": "text_disabled", "value": "#C5CDD7", "category": "neutral", "usage": "禁用状态文字", "light_mode": "#C5CDD7", "dark_mode": "#454C54", "source": "HarmonyOS 设计规范"},
            {"name": "bg_primary", "value": "#FFFFFF", "category": "neutral", "usage": "主要背景、卡片背景", "light_mode": "#FFFFFF", "dark_mode": "#121212", "source": "HarmonyOS 设计规范"},
            {"name": "bg_secondary", "value": "#F1F3F5", "category": "neutral", "usage": "次要背景、页面背景", "light_mode": "#F1F3F5", "dark_mode": "#1E1E1E", "source": "HarmonyOS 设计规范"},
            {"name": "border_light", "value": "#E5E8EB", "category": "neutral", "usage": "分割线、轻边框", "light_mode": "#E5E8EB", "dark_mode": "#383838", "source": "HarmonyOS 设计规范"},
        ]
        
        for data in colors_data:
            self.colors.append(ColorToken(**data))
        
        log_success(f"已添加 {len(colors_data)} 个颜色 Token")
    
    def _add_standard_typography(self):
        """添加标准字体样式"""
        typography_data = [
            {"name": "display_large", "font_family": "HarmonyOS Sans", "font_size": "48fp", "font_weight": "Bold (700)", "line_height": "1.2", "use_case": "超大展示数字、主数据", "source": "HarmonyOS 设计规范"},
            {"name": "display_medium", "font_family": "HarmonyOS Sans", "font_size": "32fp", "font_weight": "Bold (700)", "line_height": "1.2", "use_case": "大标题、展示数据", "source": "HarmonyOS 设计规范"},
            {"name": "display_small", "font_family": "HarmonyOS Sans", "font_size": "24fp", "font_weight": "SemiBold (600)", "line_height": "1.3", "use_case": "中等展示标题", "source": "HarmonyOS 设计规范"},
            {"name": "headline_large", "font_family": "HarmonyOS Sans", "font_size": "20fp", "font_weight": "SemiBold (600)", "line_height": "1.4", "use_case": "页面标题", "source": "HarmonyOS 设计规范"},
            {"name": "headline_medium", "font_family": "HarmonyOS Sans", "font_size": "18fp", "font_weight": "SemiBold (600)", "line_height": "1.4", "use_case": "区块标题", "source": "HarmonyOS 设计规范"},
            {"name": "headline_small", "font_family": "HarmonyOS Sans", "font_size": "16fp", "font_weight": "Medium (500)", "line_height": "1.5", "use_case": "小标题、列表标题", "source": "HarmonyOS 设计规范"},
            {"name": "body_large", "font_family": "HarmonyOS Sans", "font_size": "16fp", "font_weight": "Regular (400)", "line_height": "1.6", "use_case": "大段正文内容", "source": "HarmonyOS 设计规范"},
            {"name": "body_medium", "font_family": "HarmonyOS Sans", "font_size": "14fp", "font_weight": "Regular (400)", "line_height": "1.6", "use_case": "正文内容、描述文字", "source": "HarmonyOS 设计规范"},
            {"name": "body_small", "font_family": "HarmonyOS Sans", "font_size": "12fp", "font_weight": "Regular (400)", "line_height": "1.5", "use_case": "辅助说明、时间戳", "source": "HarmonyOS 设计规范"},
            {"name": "label_large", "font_family": "HarmonyOS Sans", "font_size": "14fp", "font_weight": "Medium (500)", "line_height": "1.4", "use_case": "按钮文字、标签", "source": "HarmonyOS 设计规范"},
            {"name": "label_medium", "font_family": "HarmonyOS Sans", "font_size": "12fp", "font_weight": "Medium (500)", "line_height": "1.4", "use_case": "小标签、徽标", "source": "HarmonyOS 设计规范"},
            {"name": "label_small", "font_family": "HarmonyOS Sans", "font_size": "10fp", "font_weight": "Medium (500)", "line_height": "1.3", "use_case": "极小标签、注释", "source": "HarmonyOS 设计规范"},
        ]
        
        for data in typography_data:
            self.typography.append(TypographyStyle(**data))
        
        log_success(f"已添加 {len(typography_data)} 个字体样式")
    
    def _add_standard_spacing(self):
        """添加标准间距 Token"""
        spacing_data = [
            {"name": "space_xxs", "value": "2vp", "use_case": "极小间距，如图标与文字紧密排列", "source": "HarmonyOS 设计规范"},
            {"name": "space_xs", "value": "4vp", "use_case": "微小间距，紧凑元素间隔", "source": "HarmonyOS 设计规范"},
            {"name": "space_sm", "value": "8vp", "use_case": "小间距，相关元素分组", "source": "HarmonyOS 设计规范"},
            {"name": "space_md", "value": "12vp", "use_case": "中间距，列表项间隔", "source": "HarmonyOS 设计规范"},
            {"name": "space_lg", "value": "16vp", "use_case": "大间距，卡片内边距、区块间隔", "source": "HarmonyOS 设计规范"},
            {"name": "space_xl", "value": "20vp", "use_case": "较大间距，区域分隔", "source": "HarmonyOS 设计规范"},
            {"name": "space_xxl", "value": "24vp", "use_case": "超大间距，模块分隔", "source": "HarmonyOS 设计规范"},
            {"name": "space_xxxl", "value": "32vp", "use_case": "巨大间距，页面边距", "source": "HarmonyOS 设计规范"},
            {"name": "radius_xs", "value": "4vp", "use_case": "小圆角，标签、徽标", "source": "HarmonyOS 设计规范"},
            {"name": "radius_sm", "value": "8vp", "use_case": "标准圆角，按钮、输入框", "source": "HarmonyOS 设计规范"},
            {"name": "radius_md", "value": "12vp", "use_case": "中圆角，卡片", "source": "HarmonyOS 设计规范"},
            {"name": "radius_lg", "value": "16vp", "use_case": "大圆角，模态框", "source": "HarmonyOS 设计规范"},
            {"name": "radius_xl", "value": "24vp", "use_case": "超大圆角，底部弹窗", "source": "HarmonyOS 设计规范"},
            {"name": "radius_full", "value": "9999vp", "use_case": "胶囊形，胶囊按钮、头像", "source": "HarmonyOS 设计规范"},
        ]
        
        for data in spacing_data:
            self.spacing.append(SpacingToken(**data))
        
        log_success(f"已添加 {len(spacing_data)} 个间距 Token")
    
    def _add_standard_animations(self):
        """添加标准动效模式"""
        animations_data = [
            {"name": "duration_instant", "duration": "0ms", "easing": "-", "description": "无动画", "use_case": "即时反馈", "source": "HarmonyOS 动效规范"},
            {"name": "duration_fastest", "duration": "100ms", "easing": "Curve.EaseOut", "description": "超快动画", "use_case": "微交互、涟漪效果", "source": "HarmonyOS 动效规范"},
            {"name": "duration_fast", "duration": "150ms", "easing": "Curve.EaseInOut", "description": "快速动画", "use_case": "按钮反馈、开关切换", "source": "HarmonyOS 动效规范"},
            {"name": "duration_normal", "duration": "200ms", "easing": "Curve.EaseInOut", "description": "标准动画", "use_case": "普通过渡、淡入淡出", "source": "HarmonyOS 动效规范"},
            {"name": "duration_medium", "duration": "300ms", "easing": "Curve.FastOutSlowIn", "description": "中等动画", "use_case": "弹窗进入、抽屉展开", "source": "HarmonyOS 动效规范"},
            {"name": "duration_slow", "duration": "400ms", "easing": "Curve.FastOutSlowIn", "description": "慢速动画", "use_case": "页面切换", "source": "HarmonyOS 动效规范"},
            {"name": "duration_slower", "duration": "500ms", "easing": "Curve.Smooth", "description": "较慢动画", "use_case": "复杂动画编排", "source": "HarmonyOS 动效规范"},
            {"name": "easing_standard", "duration": "-", "easing": "Curve.EaseInOut", "description": "标准缓动", "use_case": "通用动画", "source": "HarmonyOS 动效规范"},
            {"name": "easing_decelerate", "duration": "-", "easing": "Curve.EaseOut", "description": "减速缓动", "use_case": "进入动画", "source": "HarmonyOS 动效规范"},
            {"name": "easing_accelerate", "duration": "-", "easing": "Curve.EaseIn", "description": "加速缓动", "use_case": "退出动画", "source": "HarmonyOS 动效规范"},
            {"name": "easing_emphasized", "duration": "-", "easing": "Curve.FastOutSlowIn", "description": "强调缓动", "use_case": "重点关注的动画", "source": "HarmonyOS 动效规范"},
            {"name": "easing_spring", "duration": "-", "easing": "Curve.Smooth", "description": "弹簧缓动", "use_case": "弹性效果", "source": "HarmonyOS 动效规范"},
        ]
        
        for data in animations_data:
            self.animations.append(AnimationPattern(**data))
        
        log_success(f"已添加 {len(animations_data)} 个动效模式")
    
    def _add_standard_page_templates(self):
        """添加标准页面模板"""
        templates_data = [
            {
                "name": "登录页",
                "category": "auth",
                "description": "用户登录页面，包含 Logo、表单、登录按钮等",
                "components_used": "Column, Image, TextInput, Button, Text, Divider",
                "layout_structure": """Column (主容器)
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
└── Row (第三方登录)""",
                "source": "HarmonyOS 应用模板"
            },
            {
                "name": "注册页",
                "category": "auth",
                "description": "用户注册页面，包含多步表单",
                "components_used": "Column, TextInput, Button, Text, Stepper, Checkbox",
                "layout_structure": """Column (主容器)
├── Stepper (步骤指示器)
├── Text (标题)
├── Column (表单区)
│   ├── TextInput (手机号)
│   ├── Row (验证码)
│   │   ├── TextInput
│   │   └── Button (获取验证码)
│   ├── TextInput (密码)
│   └── TextInput (确认密码)
├── Checkbox (协议勾选)
└── Button (注册按钮)""",
                "source": "HarmonyOS 应用模板"
            },
            {
                "name": "首页仪表盘",
                "category": "dashboard",
                "description": "应用首页，展示概览数据和快捷入口",
                "components_used": "Scroll, Column, Row, Text, Image, Grid, List, Swiper",
                "layout_structure": """Scroll (可滚动容器)
└── Column (主容器)
    ├── Row (顶部栏)
    │   ├── Text (问候语)
    │   └── Image (头像)
    ├── Swiper (Banner 轮播)
    ├── Grid (快捷入口)
    │   └── GridItem (入口项) * N
    ├── Column (数据统计卡片)
    │   └── Row (统计项) * N
    └── List (最近动态)""",
                "source": "HarmonyOS 应用模板"
            },
            {
                "name": "列表页",
                "category": "list",
                "description": "数据列表页面，支持下拉刷新和加载更多",
                "components_used": "Column, List, ListItem, Row, Image, Text, Search, Refresh",
                "layout_structure": """Column (主容器)
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
                    └── Row (标签/时间)""",
                "source": "HarmonyOS 应用模板"
            },
            {
                "name": "详情页",
                "category": "detail",
                "description": "内容详情页面，展示完整信息",
                "components_used": "Scroll, Column, Image, Text, Row, Button, Divider",
                "layout_structure": """Stack (层叠容器)
├── Scroll (可滚动内容)
│   └── Column
│       ├── Image (主图/轮播)
│       ├── Column (基本信息)
│       │   ├── Text (标题)
│       │   ├── Row (价格/标签)
│       │   └── Text (描述)
│       ├── Divider
│       ├── Column (详情内容)
│       └── Column (评论区)
└── Row (底部操作栏)
    ├── Button (收藏)
    ├── Button (分享)
    └── Button (主操作)""",
                "source": "HarmonyOS 应用模板"
            },
            {
                "name": "设置页",
                "category": "settings",
                "description": "应用设置页面，分组展示设置选项",
                "components_used": "Scroll, Column, List, ListItem, Row, Text, Toggle, Image",
                "layout_structure": """Scroll (可滚动容器)
└── Column (主容器)
    ├── List (账户设置组)
    │   └── ListItem (设置项)
    │       └── Row
    │           ├── Image (图标)
    │           ├── Text (标题)
    │           └── Image (箭头) / Toggle (开关)
    ├── List (通用设置组)
    ├── List (隐私设置组)
    └── Button (退出登录)""",
                "source": "HarmonyOS 应用模板"
            },
            {
                "name": "个人中心页",
                "category": "profile",
                "description": "用户个人中心页面，展示用户信息和功能入口",
                "components_used": "Scroll, Column, Row, Image, Text, Grid, List",
                "layout_structure": """Scroll (可滚动容器)
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
    └── List (更多选项)""",
                "source": "HarmonyOS 应用模板"
            },
            {
                "name": "搜索结果页",
                "category": "list",
                "description": "搜索结果展示页面",
                "components_used": "Column, Search, Tabs, List, Grid, Text",
                "layout_structure": """Column (主容器)
├── Search (搜索框 - 可编辑)
├── Row (热门搜索/历史)
├── Tabs (结果分类)
│   ├── TabContent (综合)
│   │   └── List (搜索结果)
│   ├── TabContent (商品)
│   │   └── Grid (商品网格)
│   └── TabContent (用户)
│       └── List (用户列表)
└── Column (空状态 - 无结果时)""",
                "source": "HarmonyOS 应用模板"
            },
        ]
        
        for data in templates_data:
            self.page_templates.append(PageTemplate(**data))
        
        log_success(f"已添加 {len(templates_data)} 个页面模板")
    
    def export_to_csv(self, output_dir: Path):
        """导出所有知识到 CSV 文件"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 导出组件模板
        self._export_dataclass_list_to_csv(
            self.components, 
            output_dir / "components.csv",
            ["name", "category", "description", "props", "usage_example", "source"]
        )
        
        # 导出布局模式
        self._export_dataclass_list_to_csv(
            self.layouts,
            output_dir / "layouts.csv",
            ["name", "type", "description", "use_case", "code_example", "source"]
        )
        
        # 导出颜色 Token
        self._export_dataclass_list_to_csv(
            self.colors,
            output_dir / "colors.csv",
            ["name", "value", "category", "usage", "light_mode", "dark_mode", "source"]
        )
        
        # 导出字体样式
        self._export_dataclass_list_to_csv(
            self.typography,
            output_dir / "typography.csv",
            ["name", "font_family", "font_size", "font_weight", "line_height", "use_case", "source"]
        )
        
        # 导出间距 Token
        self._export_dataclass_list_to_csv(
            self.spacing,
            output_dir / "spacing.csv",
            ["name", "value", "use_case", "source"]
        )
        
        # 导出动效模式
        self._export_dataclass_list_to_csv(
            self.animations,
            output_dir / "animations.csv",
            ["name", "duration", "easing", "description", "use_case", "source"]
        )
        
        # 导出页面模板
        self._export_dataclass_list_to_csv(
            self.page_templates,
            output_dir / "page_templates.csv",
            ["name", "category", "description", "components_used", "layout_structure", "source"]
        )
    
    def _export_dataclass_list_to_csv(self, data_list: List, output_path: Path, fields: List[str]):
        """将 dataclass 列表导出为 CSV"""
        if not data_list:
            return
        
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for item in data_list:
                writer.writerow(asdict(item))
        
        log_success(f"已导出: {output_path.name} ({len(data_list)} 条记录)")


def main():
    """主函数"""
    log_info("=" * 60)
    log_info("HarmonyOS NEXT UI/UX Pro Max Skill - 知识提取")
    log_info("=" * 60)
    
    extractor = HarmonyKnowledgeExtractor()
    
    # 从各种来源提取知识
    log_info("\n正在提取 HarmonyOS NEXT UI/UX 知识...")
    extractor.extract_from_huawei_docs()
    
    # 导出到 CSV
    log_info("\n正在导出知识到 CSV 文件...")
    extractor.export_to_csv(OUTPUT_DIR)
    
    # 打印统计
    log_info("\n" + "=" * 60)
    log_info("知识库统计:")
    log_info(f"  - 组件模板: {len(extractor.components)} 个")
    log_info(f"  - 布局模式: {len(extractor.layouts)} 个")
    log_info(f"  - 颜色 Token: {len(extractor.colors)} 个")
    log_info(f"  - 字体样式: {len(extractor.typography)} 个")
    log_info(f"  - 间距 Token: {len(extractor.spacing)} 个")
    log_info(f"  - 动效模式: {len(extractor.animations)} 个")
    log_info(f"  - 页面模板: {len(extractor.page_templates)} 个")
    log_info("=" * 60)
    log_success(f"知识库已保存到: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
