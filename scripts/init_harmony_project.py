#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HarmonyOS NEXT 6.0 Project Initializer

根据 harmony-ui-ux-pro-max 规范初始化项目结构和资源文件。

Usage:
    python init_harmony_project.py <project_name> [options]

Options:
    --path, -p       目标目录 (默认: 当前目录)
    --bundle, -b     包名前缀 (默认: com.example)
    --sdk, -s        SDK版本，格式如 "6.0.2(22)" (必填)

Example:
    python init_harmony_project.py MyApp --sdk "6.0.2(22)"
    python init_harmony_project.py MyApp --sdk "5.0.0(12)" --path E:/projects
    python init_harmony_project.py MyApp --sdk "6.0.2(22)" --bundle com.mycompany
"""

import os
import sys
import json
import argparse
import base64
import re
from pathlib import Path
from datetime import datetime


# ============================================================================
# 配置常量 (运行时通过命令行参数设置)
# ============================================================================

# 版本信息 (由命令行参数 --sdk 设置)
HARMONY_VERSION = ""  # modelVersion, 如 "6.0.2"
SDK_VERSION = ""      # targetSdkVersion, 如 "6.0.2(22)"
BUNDLE_NAME_PREFIX = "com.example"


def parse_sdk_version(sdk_version: str) -> tuple:
    """
    解析 SDK 版本字符串，提取 modelVersion 和完整版本
    
    Args:
        sdk_version: 如 "6.0.2(22)" 或 "5.0.0(12)"
    
    Returns:
        (model_version, full_version): 如 ("6.0.2", "6.0.2(22)")
    """
    match = re.match(r'^(\d+\.\d+\.\d+)(\(\d+\))?$', sdk_version)
    if not match:
        raise ValueError(f"无效的 SDK 版本格式: {sdk_version}。期望格式如 '6.0.2(22)' 或 '6.0.2'")
    
    model_version = match.group(1)
    full_version = sdk_version if match.group(2) else f"{model_version}(12)"
    
    return model_version, full_version

# 设计规范 - 颜色
COLORS_BASE = {
    "color": [
        {"name": "primary", "value": "#0A59F7"},
        {"name": "primary_light", "value": "#5B8FF9"},
        {"name": "primary_dark", "value": "#0041C2"},
        {"name": "secondary", "value": "#36D1DC"},
        {"name": "accent", "value": "#FF6B35"},
        {"name": "success", "value": "#64BB5C"},
        {"name": "warning", "value": "#FA9D3B"},
        {"name": "error", "value": "#E84026"},
        {"name": "info", "value": "#0A59F7"},
        {"name": "text_primary", "value": "#182431"},
        {"name": "text_secondary", "value": "#66727A"},
        {"name": "text_tertiary", "value": "#99A4AE"},
        {"name": "text_disabled", "value": "#C5CDD7"},
        {"name": "text_inverse", "value": "#FFFFFF"},
        {"name": "bg_primary", "value": "#FFFFFF"},
        {"name": "bg_secondary", "value": "#F1F3F5"},
        {"name": "bg_tertiary", "value": "#E5E8EB"},
        {"name": "border_light", "value": "#E5E8EB"},
        {"name": "border_medium", "value": "#C5CDD7"},
        {"name": "divider", "value": "#E5E8EB"},
        {"name": "icon_primary", "value": "#182431"},
        {"name": "icon_secondary", "value": "#66727A"},
        {"name": "overlay", "value": "#00000066"},
    ]
}

# 深色模式颜色
COLORS_DARK = {
    "color": [
        {"name": "primary", "value": "#317AF7"},
        {"name": "primary_light", "value": "#5B8FF9"},
        {"name": "text_primary", "value": "#E5E8EB"},
        {"name": "text_secondary", "value": "#99A4AE"},
        {"name": "text_tertiary", "value": "#66727A"},
        {"name": "text_disabled", "value": "#4A4A4A"},
        {"name": "text_inverse", "value": "#182431"},
        {"name": "bg_primary", "value": "#121212"},
        {"name": "bg_secondary", "value": "#1E1E1E"},
        {"name": "bg_tertiary", "value": "#2C2C2C"},
        {"name": "border_light", "value": "#383838"},
        {"name": "border_medium", "value": "#4A4A4A"},
        {"name": "divider", "value": "#383838"},
        {"name": "icon_primary", "value": "#E5E8EB"},
        {"name": "icon_secondary", "value": "#99A4AE"},
        {"name": "overlay", "value": "#000000CC"},
    ]
}

# 设计规范 - 尺寸
FLOATS_BASE = {
    "float": [
        # 字体大小 (fp)
        {"name": "font_size_xs", "value": "10fp"},
        {"name": "font_size_sm", "value": "12fp"},
        {"name": "font_size_md", "value": "14fp"},
        {"name": "font_size_lg", "value": "16fp"},
        {"name": "font_size_xl", "value": "18fp"},
        {"name": "font_size_xxl", "value": "20fp"},
        {"name": "font_size_title", "value": "24fp"},
        {"name": "font_size_headline", "value": "32fp"},
        # 间距 (vp)
        {"name": "spacing_xs", "value": "4vp"},
        {"name": "spacing_sm", "value": "8vp"},
        {"name": "spacing_md", "value": "12vp"},
        {"name": "spacing_lg", "value": "16vp"},
        {"name": "spacing_xl", "value": "24vp"},
        {"name": "spacing_xxl", "value": "32vp"},
        # 圆角 (vp)
        {"name": "radius_xs", "value": "4vp"},
        {"name": "radius_sm", "value": "8vp"},
        {"name": "radius_md", "value": "12vp"},
        {"name": "radius_lg", "value": "16vp"},
        {"name": "radius_xl", "value": "24vp"},
        {"name": "radius_full", "value": "999vp"},
        # 按钮高度
        {"name": "button_height_sm", "value": "28vp"},
        {"name": "button_height_md", "value": "36vp"},
        {"name": "button_height_lg", "value": "44vp"},
        # 输入框高度
        {"name": "input_height", "value": "44vp"},
        # 图标大小
        {"name": "icon_size_sm", "value": "16vp"},
        {"name": "icon_size_md", "value": "24vp"},
        {"name": "icon_size_lg", "value": "32vp"},
        # 头像大小
        {"name": "avatar_size_sm", "value": "32vp"},
        {"name": "avatar_size_md", "value": "48vp"},
        {"name": "avatar_size_lg", "value": "64vp"},
    ]
}

# 字符串资源
STRINGS_BASE = {
    "string": [
        {"name": "app_name", "value": "我的应用"},
        {"name": "welcome", "value": "欢迎"},
        {"name": "welcome_message", "value": "欢迎回来"},
        {"name": "login", "value": "登录"},
        {"name": "register", "value": "注册"},
        {"name": "logout", "value": "退出登录"},
        {"name": "confirm", "value": "确认"},
        {"name": "cancel", "value": "取消"},
        {"name": "save", "value": "保存"},
        {"name": "delete", "value": "删除"},
        {"name": "edit", "value": "编辑"},
        {"name": "search", "value": "搜索"},
        {"name": "loading", "value": "加载中..."},
        {"name": "no_data", "value": "暂无数据"},
        {"name": "network_error", "value": "网络错误，请重试"},
        {"name": "input_username", "value": "请输入用户名"},
        {"name": "input_password", "value": "请输入密码"},
        {"name": "input_phone", "value": "请输入手机号"},
        {"name": "submit", "value": "提交"},
        {"name": "retry", "value": "重试"},
        {"name": "back", "value": "返回"},
        {"name": "next", "value": "下一步"},
        {"name": "done", "value": "完成"},
        {"name": "settings", "value": "设置"},
        {"name": "profile", "value": "个人中心"},
        {"name": "home", "value": "首页"},
        {"name": "message", "value": "消息"},
        {"name": "notification", "value": "通知"},
        # 权限说明
        {"name": "permission_distributed_datasync_reason", "value": "用于多设备间同步应用数据"},
    ]
}

# 媒体资源 - 最小有效的 PNG 图像 (1x1 像素)
# 蓝色前景图 (用于应用图标)
FOREGROUND_PNG_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

# 白色背景图
BACKGROUND_PNG_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="

# 启动图标 (蓝色)
START_ICON_PNG_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="


def get_layered_image_json() -> str:
    """生成 layered_image.json"""
    return '''{
  "layered-image": {
    "background": "$media:background",
    "foreground": "$media:foreground"
  }
}
'''


# ============================================================================
# 项目模板
# ============================================================================

def get_oh_package_json5(project_name: str, bundle_name: str) -> str:
    """生成 oh-package.json5"""
    return f'''{{
  "modelVersion": "{HARMONY_VERSION}",
  "description": "{project_name} - HarmonyOS NEXT Application",
  "dependencies": {{
  }},
  "devDependencies": {{
    "@ohos/hypium": "1.0.24",
    "@ohos/hamock": "1.0.0"
  }}
}}
'''


def get_build_profile_json5(project_name: str) -> str:
    """生成 build-profile.json5"""
    return f'''{{
  "app": {{
    "signingConfigs": [],
    "products": [
      {{
        "name": "default",
        "signingConfig": "default",
        "targetSdkVersion": "{SDK_VERSION}",
        "compatibleSdkVersion": "{SDK_VERSION}",
        "runtimeOS": "HarmonyOS",
        "buildOption": {{
          "strictMode": {{
            "caseSensitiveCheck": true,
            "useNormalizedOHMUrl": true
          }}
        }}
      }}
    ],
    "buildModeSet": [
      {{
        "name": "debug"
      }},
      {{
        "name": "release"
      }}
    ]
  }},
  "modules": [
    {{
      "name": "entry",
      "srcPath": "./entry",
      "targets": [
        {{
          "name": "default",
          "applyToProducts": [
            "default"
          ]
        }}
      ]
    }}
  ]
}}
'''


def get_hvigor_config() -> str:
    """生成 hvigor/hvigor-config.json5"""
    return f'''{{
  "modelVersion": "{HARMONY_VERSION}",
  "dependencies": {{
  }},
  "execution": {{
  }},
  "logging": {{
  }},
  "debugging": {{
  }},
  "nodeOptions": {{
  }}
}}
'''


def get_hvigorfile() -> str:
    """生成 hvigorfile.ts"""
    return '''import { appTasks } from '@ohos/hvigor-ohos-plugin';

export default {
    system: appTasks,
    plugins:[]
}
'''


def get_module_json5(project_name: str, bundle_name: str) -> str:
    """生成 entry/src/main/module.json5"""
    return f'''{{
  "module": {{
    "name": "entry",
    "type": "entry",
    "description": "$string:module_desc",
    "mainElement": "EntryAbility",
    "deviceTypes": [
      "phone",
      "tablet"
    ],
    "deliveryWithInstall": true,
    "installationFree": false,
    "pages": "$profile:main_pages",
    "abilities": [
      {{
        "name": "EntryAbility",
        "srcEntry": "./ets/entryability/EntryAbility.ets",
        "description": "$string:EntryAbility_desc",
        "icon": "$media:layered_image",
        "label": "$string:EntryAbility_label",
        "startWindowIcon": "$media:startIcon",
        "startWindowBackground": "$color:start_window_background",
        "exported": true,
        "skills": [
          {{
            "entities": [
              "entity.system.home"
            ],
            "actions": [
              "ohos.want.action.home"
            ]
          }}
        ]
      }}
    ],
    "extensionAbilities": [],
    "requestPermissions": [
      {{
        "name": "ohos.permission.DISTRIBUTED_DATASYNC",
        "reason": "$string:permission_distributed_datasync_reason",
        "usedScene": {{
          "abilities": ["EntryAbility"],
          "when": "inuse"
        }}
      }}
    ]
  }}
}}
'''


def get_app_json5(project_name: str, bundle_name: str) -> str:
    """生成 AppScope/app.json5"""
    return f'''{{
  "app": {{
    "bundleName": "{bundle_name}",
    "vendor": "example",
    "versionCode": 1000000,
    "versionName": "1.0.0",
    "icon": "$media:layered_image",
    "label": "$string:app_name"
  }}
}}
'''


def get_main_pages() -> str:
    """生成 entry/src/main/resources/base/profile/main_pages.json"""
    return '''{
  "src": [
    "pages/Index"
  ]
}
'''


def get_entry_ability() -> str:
    """生成 EntryAbility.ets"""
    return '''import { AbilityConstant, UIAbility, Want } from '@kit.AbilityKit';
import { hilog } from '@kit.PerformanceAnalysisKit';
import { window } from '@kit.ArkUI';

export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    hilog.info(0x0000, 'EntryAbility', '%{public}s', 'Ability onCreate');
  }

  onDestroy(): void {
    hilog.info(0x0000, 'EntryAbility', '%{public}s', 'Ability onDestroy');
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    hilog.info(0x0000, 'EntryAbility', '%{public}s', 'Ability onWindowStageCreate');

    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        hilog.error(0x0000, 'EntryAbility', 'Failed to load content. Cause: %{public}s', JSON.stringify(err) ?? '');
        return;
      }
      hilog.info(0x0000, 'EntryAbility', 'Succeeded in loading content.');
    });
  }

  onWindowStageDestroy(): void {
    hilog.info(0x0000, 'EntryAbility', '%{public}s', 'Ability onWindowStageDestroy');
  }

  onForeground(): void {
    hilog.info(0x0000, 'EntryAbility', '%{public}s', 'Ability onForeground');
  }

  onBackground(): void {
    hilog.info(0x0000, 'EntryAbility', '%{public}s', 'Ability onBackground');
  }
}
'''


def get_index_page() -> str:
    """生成主入口页面 Index.ets - 使用 Tabs 组件"""
    return '''/**
 * 主入口页面
 * 使用 Tabs 组件实现底部导航
 */
import { HomePage } from './HomePage'
import { ProfilePage } from './ProfilePage'

@Entry
@Component
struct Index {
  @State currentIndex: number = 0

  build() {
    Column() {
      Tabs({ barPosition: BarPosition.End, index: this.currentIndex }) {
        TabContent() {
          HomePage()
        }
        .tabBar(this.tabBuilder(0, $r('app.string.home'), 'sys.symbol.house'))

        TabContent() {
          MessagePage()
        }
        .tabBar(this.tabBuilder(1, $r('app.string.message'), 'sys.symbol.ellipsis_message'))

        TabContent() {
          ProfilePage()
        }
        .tabBar(this.tabBuilder(2, $r('app.string.profile'), 'sys.symbol.person'))
      }
      .barMode(BarMode.Fixed)
      .onChange((index: number) => {
        this.currentIndex = index
      })
    }
    .width('100%')
    .height('100%')
  }

  @Builder
  tabBuilder(index: number, label: Resource, icon: string) {
    Column() {
      SymbolGlyph($r(icon))
        .fontSize(24)
        .fontColor([this.currentIndex === index ? $r('app.color.primary') : $r('app.color.icon_secondary')])

      Text(label)
        .fontSize($r('app.float.font_size_xs'))
        .fontColor(this.currentIndex === index ? $r('app.color.primary') : $r('app.color.text_secondary'))
        .margin({ top: 4 })
    }
    .width('100%')
    .height(56)
    .justifyContent(FlexAlign.Center)
  }
}

/**
 * 消息页面占位
 */
@Component
struct MessagePage {
  build() {
    Column() {
      Text($r('app.string.message'))
        .fontSize($r('app.float.font_size_title'))
        .fontColor($r('app.color.text_primary'))
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .backgroundColor($r('app.color.bg_secondary'))
  }
}
'''


def get_home_page() -> str:
    """生成首页 HomePage.ets - 遵循设计规范"""
    return '''/**
 * 首页
 * 展示响应式布局和设计规范
 */
@Component
export struct HomePage {
  @State isRefreshing: boolean = false
  @State currentBreakpoint: string = 'sm'

  build() {
    Column() {
      // 顶部标题栏
      this.buildHeader()

      // 内容区域
      Refresh({ refreshing: $$this.isRefreshing }) {
        Scroll() {
          GridRow({
            columns: 12,
            breakpoints: {
              value: ['320vp', '520vp', '840vp'],
              reference: BreakpointsReference.WindowSize
            }
          }) {
            // 欢迎卡片 - 全宽
            GridCol({ span: 12 }) {
              this.buildWelcomeCard()
            }

            // 功能入口 - 响应式
            ForEach(this.getQuickActions(), (action: QuickAction, index: number) => {
              GridCol({
                span: { xs: 6, sm: 4, md: 3, lg: 2 }
              }) {
                this.buildActionCard(action)
              }
            })
          }
          .onBreakpointChange((breakpoint: string) => {
            this.currentBreakpoint = breakpoint
          })
          .padding($r('app.float.spacing_lg'))
        }
        .scrollBar(BarState.Off)
      }
      .onRefreshing(() => {
        this.handleRefresh()
      })
    }
    .width('100%')
    .height('100%')
    .backgroundColor($r('app.color.bg_secondary'))
  }

  @Builder
  buildHeader() {
    Row() {
      Text($r('app.string.home'))
        .fontSize($r('app.float.font_size_title'))
        .fontColor($r('app.color.text_primary'))
        .fontWeight(FontWeight.Bold)

      Blank()

      SymbolGlyph($r('sys.symbol.bell'))
        .fontSize(24)
        .fontColor([$r('app.color.icon_primary')])
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor($r('app.color.bg_primary'))
  }

  @Builder
  buildWelcomeCard() {
    Column() {
      Text($r('app.string.welcome_message'))
        .fontSize($r('app.float.font_size_xxl'))
        .fontColor($r('app.color.text_inverse'))
        .fontWeight(FontWeight.Bold)

      Text('今天是个好日子')
        .fontSize($r('app.float.font_size_md'))
        .fontColor($r('app.color.text_inverse'))
        .opacity(0.8)
        .margin({ top: 8 })
    }
    .width('100%')
    .padding(24)
    .borderRadius($r('app.float.radius_lg'))
    .linearGradient({
      direction: GradientDirection.Right,
      colors: [[$r('app.color.primary'), 0], [$r('app.color.primary_light'), 1]]
    })
    .margin({ bottom: 16 })
    .alignItems(HorizontalAlign.Start)
  }

  @Builder
  buildActionCard(action: QuickAction) {
    Column() {
      SymbolGlyph($r(action.icon))
        .fontSize(32)
        .fontColor([$r('app.color.primary')])

      Text(action.label)
        .fontSize($r('app.float.font_size_sm'))
        .fontColor($r('app.color.text_primary'))
        .margin({ top: 8 })
    }
    .width('100%')
    .padding(16)
    .backgroundColor($r('app.color.bg_primary'))
    .borderRadius($r('app.float.radius_md'))
    .margin(4)
    .justifyContent(FlexAlign.Center)
    .onClick(() => {
      this.handleActionClick(action)
    })
    .stateStyles({
      pressed: {
        .scale({ x: 0.98, y: 0.98 })
      }
    })
    .animation({ duration: 100, curve: Curve.Sharp })
  }

  private getQuickActions(): QuickAction[] {
    return [
      { id: '1', label: '功能一', icon: 'sys.symbol.star' },
      { id: '2', label: '功能二', icon: 'sys.symbol.heart' },
      { id: '3', label: '功能三', icon: 'sys.symbol.gearshape' },
      { id: '4', label: '功能四', icon: 'sys.symbol.magnifyingglass' },
    ]
  }

  private handleRefresh() {
    setTimeout(() => {
      this.isRefreshing = false
    }, 1500)
  }

  private handleActionClick(action: QuickAction) {
    // 处理点击事件
  }
}

/**
 * 快捷入口数据模型
 */
interface QuickAction {
  id: string
  label: string
  icon: string
}
'''


def get_base_viewmodel() -> str:
    """生成 ViewModel 基类 BaseViewModel.ets"""
    return '''/**
 * ViewModel 基类
 * 提供通用的状态管理和生命周期钩子
 * 
 * 使用方式:
 * @ObservedV2
 * export class MyViewModel extends BaseViewModel {
 *   @Trace myData: string = ''
 *   
 *   async loadData(): Promise<void> {
 *     await this.executeAsync(
 *       async () => fetchData(),
 *       (result) => { this.myData = result }
 *     )
 *   }
 * }
 */
@ObservedV2
export class BaseViewModel {
  /** 加载状态 */
  @Trace isLoading: boolean = false

  /** 错误信息 */
  @Trace errorMessage: string = ''

  /** 是否有错误 */
  @Trace hasError: boolean = false

  /**
   * 初始化 ViewModel
   * 子类可重写此方法进行初始化操作
   */
  async onInit(): Promise<void> {
    // 子类实现
  }

  /**
   * 清理资源
   * 在组件 aboutToDisappear 时调用
   */
  onDestroy(): void {
    // 子类实现
  }

  /**
   * 设置加载状态
   */
  protected setLoading(loading: boolean): void {
    this.isLoading = loading
  }

  /**
   * 设置错误信息
   */
  protected setError(message: string): void {
    this.errorMessage = message
    this.hasError = message.length > 0
  }

  /**
   * 清除错误
   */
  protected clearError(): void {
    this.errorMessage = ''
    this.hasError = false
  }

  /**
   * 执行异步操作的包装器
   * 自动处理加载状态和错误
   * 
   * @param operation 异步操作
   * @param onSuccess 成功回调
   * @param onError 错误回调
   */
  protected async executeAsync<T>(
    operation: () => Promise<T>,
    onSuccess?: (result: T) => void,
    onError?: (error: Error) => void
  ): Promise<T | undefined> {
    this.setLoading(true)
    this.clearError()

    try {
      const result = await operation()
      if (onSuccess) {
        onSuccess(result)
      }
      return result
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '操作失败'
      this.setError(errorMessage)
      if (onError) {
        onError(error as Error)
      }
      return undefined
    } finally {
      this.setLoading(false)
    }
  }
}
'''


def get_database_helper() -> str:
    """生成数据库管理器 DatabaseHelper.ets"""
    return '''/**
 * 数据库管理器
 * 单例模式，管理 RDB 数据库连接和版本升级
 * 
 * 使用方式:
 * 1. 在 EntryAbility.onCreate 中调用 DatabaseHelper.getInstance().init(context)
 * 2. 通过 DatabaseHelper.getInstance().getStore() 获取数据库实例
 */
import { relationalStore } from '@kit.ArkData'
import { common } from '@kit.AbilityKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { BusinessError } from '@kit.BasicServicesKit'

/**
 * 数据库配置
 */
const DB_CONFIG: relationalStore.StoreConfig = {
  name: 'app_database.db',
  securityLevel: relationalStore.SecurityLevel.S1,
  encrypt: false
}

/**
 * 建表 SQL - 根据业务需求添加表结构
 */
const CREATE_TABLES: string[] = [
  // 示例表 - 根据实际需求修改
  `CREATE TABLE IF NOT EXISTS cache_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cache_key TEXT NOT NULL UNIQUE,
    cache_value TEXT NOT NULL,
    expire_at INTEGER,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
  )`,
  `CREATE INDEX IF NOT EXISTS idx_cache_key ON cache_data(cache_key)`
]

export class DatabaseHelper {
  private static readonly TAG = 'DatabaseHelper'
  private static readonly DOMAIN = 0x0000

  private static instance: DatabaseHelper | null = null
  private rdbStore: relationalStore.RdbStore | null = null

  private constructor() {}

  /**
   * 获取单例实例
   */
  static getInstance(): DatabaseHelper {
    if (!DatabaseHelper.instance) {
      DatabaseHelper.instance = new DatabaseHelper()
    }
    return DatabaseHelper.instance
  }

  /**
   * 初始化数据库
   * @param context 应用上下文
   */
  async init(context: common.Context): Promise<void> {
    try {
      this.rdbStore = await relationalStore.getRdbStore(context, DB_CONFIG)
      hilog.info(DatabaseHelper.DOMAIN, DatabaseHelper.TAG, 'Database initialized')

      await this.createTables()
    } catch (error) {
      const err = error as BusinessError
      hilog.error(DatabaseHelper.DOMAIN, DatabaseHelper.TAG,
        `Init failed: ${err.code} - ${err.message}`)
      throw new Error(`Database init failed: ${err.message || String(error)}`)
    }
  }

  /**
   * 创建表结构
   */
  private async createTables(): Promise<void> {
    if (!this.rdbStore) return

    for (const sql of CREATE_TABLES) {
      try {
        await this.rdbStore.executeSql(sql)
      } catch (error) {
        hilog.error(DatabaseHelper.DOMAIN, DatabaseHelper.TAG,
          `Create table failed: ${error}`)
      }
    }
  }

  /**
   * 获取数据库实例
   */
  getStore(): relationalStore.RdbStore {
    if (!this.rdbStore) {
      throw new Error('Database not initialized. Call init() first.')
    }
    return this.rdbStore
  }

  /**
   * 关闭数据库连接
   */
  async close(): Promise<void> {
    if (this.rdbStore) {
      this.rdbStore = null
    }
  }
}
'''


def get_preferences_util() -> str:
    """生成 Preferences 工具类 PreferencesUtil.ets"""
    return '''/**
 * Preferences 工具类
 * 封装轻量级键值存储的常用操作
 * 
 * 使用方式:
 * 1. 在 EntryAbility.onCreate 中调用 PreferencesUtil.init(context)
 * 2. 通过静态方法进行存取操作
 */
import { preferences } from '@kit.ArkData'
import { common } from '@kit.AbilityKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { BusinessError } from '@kit.BasicServicesKit'

export class PreferencesUtil {
  private static readonly TAG = 'PreferencesUtil'
  private static readonly DOMAIN = 0x0000
  private static readonly STORE_NAME = 'app_preferences'

  private static preferencesInstance: preferences.Preferences | null = null

  /**
   * 初始化 Preferences
   */
  static async init(context: common.Context): Promise<void> {
    try {
      PreferencesUtil.preferencesInstance = await preferences.getPreferences(
        context,
        PreferencesUtil.STORE_NAME
      )
      hilog.info(PreferencesUtil.DOMAIN, PreferencesUtil.TAG, 'Preferences initialized')
    } catch (error) {
      const err = error as BusinessError
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG,
        `Init failed: ${err.code} - ${err.message}`)
    }
  }

  private static getPreferences(): preferences.Preferences {
    if (!PreferencesUtil.preferencesInstance) {
      throw new Error('Preferences not initialized. Call init() first.')
    }
    return PreferencesUtil.preferencesInstance
  }

  // 字符串操作
  static async putString(key: string, value: string): Promise<void> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      await prefs.put(key, value)
      await prefs.flush()
    } catch (error) {
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG, `Put string failed: ${error}`)
    }
  }

  static async getString(key: string, defaultValue: string = ''): Promise<string> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      return await prefs.get(key, defaultValue) as string
    } catch (error) {
      return defaultValue
    }
  }

  // 数值操作
  static async putNumber(key: string, value: number): Promise<void> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      await prefs.put(key, value)
      await prefs.flush()
    } catch (error) {
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG, `Put number failed: ${error}`)
    }
  }

  static async getNumber(key: string, defaultValue: number = 0): Promise<number> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      return await prefs.get(key, defaultValue) as number
    } catch (error) {
      return defaultValue
    }
  }

  // 布尔值操作
  static async putBoolean(key: string, value: boolean): Promise<void> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      await prefs.put(key, value)
      await prefs.flush()
    } catch (error) {
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG, `Put boolean failed: ${error}`)
    }
  }

  static async getBoolean(key: string, defaultValue: boolean = false): Promise<boolean> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      return await prefs.get(key, defaultValue) as boolean
    } catch (error) {
      return defaultValue
    }
  }

  // 对象操作 (JSON 序列化)
  static async putObject<T>(key: string, value: T): Promise<void> {
    await PreferencesUtil.putString(key, JSON.stringify(value))
  }

  static async getObject<T>(key: string, defaultValue: T): Promise<T> {
    try {
      const json = await PreferencesUtil.getString(key, '')
      return json ? JSON.parse(json) as T : defaultValue
    } catch (error) {
      return defaultValue
    }
  }

  // 通用操作
  static async has(key: string): Promise<boolean> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      return await prefs.has(key)
    } catch {
      return false
    }
  }

  static async delete(key: string): Promise<void> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      await prefs.delete(key)
      await prefs.flush()
    } catch (error) {
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG, `Delete failed: ${error}`)
    }
  }

  static async clear(): Promise<void> {
    try {
      const prefs = PreferencesUtil.getPreferences()
      await prefs.clear()
      await prefs.flush()
    } catch (error) {
      hilog.error(PreferencesUtil.DOMAIN, PreferencesUtil.TAG, `Clear failed: ${error}`)
    }
  }
}

/**
 * 预定义 Key 常量
 */
export class PreferencesKeys {
  static readonly IS_LOGGED_IN = 'is_logged_in'
  static readonly USER_TOKEN = 'user_token'
  static readonly USER_INFO = 'user_info'
  static readonly THEME_MODE = 'theme_mode'
  static readonly LANGUAGE = 'language'
  static readonly IS_FIRST_LAUNCH = 'is_first_launch'
  static readonly LAST_SYNC_TIME = 'last_sync_time'
}
'''


def get_collaboration_manager() -> str:
    """生成协同管理器 CollaborationManager.ets"""
    return '''/**
 * 分布式协同管理器
 * 封装"碰一碰"连接的完整流程
 *
 * 使用方式:
 * 1. Host 端: CollaborationManager.getInstance().createSession()
 * 2. Guest 端: CollaborationManager.getInstance().joinSession(invite)
 * 3. 销毁时: CollaborationManager.getInstance().destroy()
 *
 * ⚠️ 权限要求: 需要在 module.json5 中声明 ohos.permission.DISTRIBUTED_DATASYNC
 */
import { distributedDataObject } from '@kit.ArkData'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { BusinessError } from '@kit.BasicServicesKit'

/**
 * 同步状态
 */
export enum SyncStatus {
  ONLINE = 'online',
  OFFLINE = 'offline',
  RESTORED = 'restored'
}

/**
 * 协同会话状态
 */
export enum CollaborationStatus {
  WAITING = 'waiting',
  CONNECTING = 'connecting',
  CONNECTED = 'connected',
  DISCONNECTED = 'disconnected'
}

/**
 * 同步数据容器
 * 使用 JSON 字符串封装，避免 ArkTS 索引签名限制
 */
export class SyncData {
  /** 数据 JSON 字符串 */
  data: string = '{}'
  /** 数据版本号，用于变更检测 */
  version: number = 0
  /** 最后更新时间戳 */
  timestamp: number = 0
}

/**
 * 数据变更回调
 */
export type DataChangeCallback = (jsonData: string, changedFields: string[]) => void

/**
 * 状态变更回调
 */
export type StatusChangeCallback = (status: SyncStatus) => void

/**
 * 分布式数据同步管理器
 * ⚠️ 需要权限: ohos.permission.DISTRIBUTED_DATASYNC
 */
export class DistributedSyncManager {
  private static readonly TAG: string = 'DistributedSyncManager'
  private static readonly DOMAIN: number = 0x0000

  private dataObject: distributedDataObject.DataObject | null = null
  private currentSessionId: string = ''
  private isHost: boolean = false

  private dataChangeCallback: DataChangeCallback | null = null
  private statusChangeCallback: StatusChangeCallback | null = null
  private changeListener: ((sessionId: string, fields: string[]) => void) | null = null
  private statusListener: ((sessionId: string, networkId: string, status: string) => void) | null = null

  /**
   * 创建同步会话 (Host 端)
   * ⚠️ 需要权限: ohos.permission.DISTRIBUTED_DATASYNC
   * @param initialData 初始数据 JSON 字符串
   */
  async createSession(initialData: string = '{}'): Promise<string> {
    try {
      this.isHost = true
      const syncData: SyncData = new SyncData()
      syncData.data = initialData
      syncData.version = 1
      syncData.timestamp = Date.now()

      this.dataObject = distributedDataObject.create(getContext(), syncData)
      this.currentSessionId = distributedDataObject.genSessionId()

      this.setupListeners()
      await this.dataObject.setSessionId(this.currentSessionId)

      hilog.info(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        `Session created: ${this.currentSessionId}`)

      return this.currentSessionId
    } catch (error) {
      const err: BusinessError = error as BusinessError
      hilog.error(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        `Create session failed: ${err.code} - ${err.message}`)
      throw new Error(`Create session failed: ${err.message || String(error)}`)
    }
  }

  /**
   * 加入同步会话 (Guest 端)
   * ⚠️ 需要权限: ohos.permission.DISTRIBUTED_DATASYNC
   * @param sessionId 会话 ID
   * @param initialData 初始数据 JSON 字符串
   */
  async joinSession(sessionId: string, initialData: string = '{}'): Promise<void> {
    try {
      this.isHost = false
      this.currentSessionId = sessionId

      const syncData: SyncData = new SyncData()
      syncData.data = initialData
      syncData.version = 0
      syncData.timestamp = Date.now()

      this.dataObject = distributedDataObject.create(getContext(), syncData)

      this.setupListeners()
      await this.dataObject.setSessionId(sessionId)

      hilog.info(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        `Joined session: ${sessionId}`)
    } catch (error) {
      const err: BusinessError = error as BusinessError
      hilog.error(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        `Join session failed: ${err.code} - ${err.message}`)
      throw new Error(`Join session failed: ${err.message || String(error)}`)
    }
  }

  /**
   * 设置监听器
   */
  private setupListeners(): void {
    if (!this.dataObject) return

    // 数据变更监听
    this.changeListener = (_sessionId: string, fields: string[]): void => {
      hilog.info(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        `Data changed: ${fields.join(', ')}`)
      if (this.dataChangeCallback) {
        const data: string = this.getData()
        this.dataChangeCallback(data, fields)
      }
    }
    try {
      this.dataObject.on('change', this.changeListener)
    } catch (error) {
      hilog.error(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        `Register change listener failed: ${String(error)}`)
    }

    // 状态变更监听
    this.statusListener = (_sessionId: string, _networkId: string, status: string): void => {
      hilog.info(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        `Status changed: ${status}`)
      if (this.statusChangeCallback) {
        this.statusChangeCallback(status as SyncStatus)
      }
      // 数据恢复时刷新
      if (status === 'restored' && this.dataChangeCallback) {
        const data: string = this.getData()
        this.dataChangeCallback(data, ['data'])
      }
    }
    try {
      this.dataObject.on('status', this.statusListener)
    } catch (error) {
      hilog.error(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
        `Register status listener failed: ${String(error)}`)
    }
  }

  /**
   * 注册数据变更回调
   */
  onDataChange(callback: DataChangeCallback): void {
    this.dataChangeCallback = callback
  }

  /**
   * 注册状态变更回调
   */
  onStatusChange(callback: StatusChangeCallback): void {
    this.statusChangeCallback = callback
  }

  /**
   * 获取当前数据 JSON 字符串
   */
  getData(): string {
    if (!this.dataObject) return '{}'
    // 使用 ESObject 访问动态属性
    const obj: ESObject = this.dataObject
    const data: string | undefined = obj.data
    return data || '{}'
  }

  /**
   * 获取数据版本号
   */
  getVersion(): number {
    if (!this.dataObject) return 0
    const obj: ESObject = this.dataObject
    const version: number | undefined = obj.version
    return version || 0
  }

  /**
   * 更新数据
   * @param jsonData JSON 字符串格式的数据
   */
  update(jsonData: string): void {
    if (!this.dataObject) {
      throw new Error('Session not initialized')
    }
    const obj: ESObject = this.dataObject
    const currentVersion: number = obj.version || 0
    obj.data = jsonData
    obj.version = currentVersion + 1
    obj.timestamp = Date.now()
  }

  /**
   * 获取会话 ID
   */
  getSessionId(): string {
    return this.currentSessionId
  }

  /**
   * 是否为 Host
   */
  isHostDevice(): boolean {
    return this.isHost
  }

  /**
   * 销毁会话
   * ⚠️ 必须在组件 aboutToDisappear 时调用
   */
  destroy(): void {
    if (this.dataObject) {
      // 显式解绑监听器 - 防止内存泄漏
      if (this.changeListener) {
        try {
          this.dataObject.off('change', this.changeListener)
        } catch (error) {
          hilog.error(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
            `Unregister change listener failed: ${String(error)}`)
        }
        this.changeListener = null
      }
      if (this.statusListener) {
        try {
          this.dataObject.off('status', this.statusListener)
        } catch (error) {
          hilog.error(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
            `Unregister status listener failed: ${String(error)}`)
        }
        this.statusListener = null
      }
      this.dataObject = null
    }
    this.dataChangeCallback = null
    this.statusChangeCallback = null
    this.currentSessionId = ''
    this.isHost = false

    hilog.info(DistributedSyncManager.DOMAIN, DistributedSyncManager.TAG,
      'Session destroyed')
  }
}

/**
 * 协同管理器单例
 */
export class CollaborationManager {
  private static instance: CollaborationManager | null = null
  private syncManager: DistributedSyncManager | null = null
  private status: CollaborationStatus = CollaborationStatus.DISCONNECTED

  private constructor() {}

  static getInstance(): CollaborationManager {
    if (!CollaborationManager.instance) {
      CollaborationManager.instance = new CollaborationManager()
    }
    return CollaborationManager.instance
  }

  /**
   * 创建会话
   * @param jsonData 初始数据 JSON 字符串
   */
  async createSession(jsonData: string = '{}'): Promise<string> {
    this.syncManager = new DistributedSyncManager()
    this.status = CollaborationStatus.WAITING
    return await this.syncManager.createSession(jsonData)
  }

  /**
   * 加入会话
   * @param sessionId 会话 ID
   * @param jsonData 初始数据 JSON 字符串
   */
  async joinSession(sessionId: string, jsonData: string = '{}'): Promise<void> {
    this.syncManager = new DistributedSyncManager()
    this.status = CollaborationStatus.CONNECTING
    await this.syncManager.joinSession(sessionId, jsonData)
    this.status = CollaborationStatus.CONNECTED
  }

  getSyncManager(): DistributedSyncManager | null {
    return this.syncManager
  }

  getStatus(): CollaborationStatus {
    return this.status
  }

  destroy(): void {
    if (this.syncManager) {
      this.syncManager.destroy()
      this.syncManager = null
    }
    this.status = CollaborationStatus.DISCONNECTED
  }
}
'''


def get_example_model() -> str:
    """生成示例数据模型 Example.ets"""
    return '''/**
 * 示例数据模型
 * 
 * Model 层职责:
 * - 定义数据结构 (interface)
 * - 数据验证
 * - 数据转换
 */

/**
 * 用户信息模型
 */
export interface UserInfo {
  id: string
  name: string
  avatar: string
  phone: string
  email?: string
}

/**
 * 分页请求参数
 */
export interface PageRequest {
  pageIndex: number
  pageSize: number
  keyword?: string
}

/**
 * 分页响应结果
 */
export interface PageResponse<T> {
  items: T[]
  total: number
  pageIndex: number
  pageSize: number
  hasMore: boolean
}

/**
 * API 响应包装
 */
export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}
'''


def get_profile_page() -> str:
    """生成个人中心页面 ProfilePage.ets"""
    return '''/**
 * 个人中心页面
 */
@Component
export struct ProfilePage {
  @State userInfo: UserInfo = {
    name: '用户名',
    avatar: '',
    phone: '138****8888'
  }

  build() {
    Column() {
      // 用户信息卡片
      this.buildUserCard()

      // 菜单列表
      List() {
        ForEach(this.getMenuItems(), (item: MenuItem) => {
          ListItem() {
            this.buildMenuItem(item)
          }
        })
      }
      .backgroundColor($r('app.color.bg_primary'))
      .borderRadius($r('app.float.radius_lg'))
      .margin({ top: 16 })
      .divider({
        strokeWidth: 0.5,
        color: $r('app.color.divider'),
        startMargin: 56,
        endMargin: 16
      })
    }
    .width('100%')
    .height('100%')
    .padding($r('app.float.spacing_lg'))
    .backgroundColor($r('app.color.bg_secondary'))
  }

  @Builder
  buildUserCard() {
    Row() {
      // 头像
      if (this.userInfo.avatar) {
        Image(this.userInfo.avatar)
          .width($r('app.float.avatar_size_lg'))
          .height($r('app.float.avatar_size_lg'))
          .borderRadius($r('app.float.radius_full'))
      } else {
        Column() {
          SymbolGlyph($r('sys.symbol.person'))
            .fontSize(32)
            .fontColor([$r('app.color.text_inverse')])
        }
        .width($r('app.float.avatar_size_lg'))
        .height($r('app.float.avatar_size_lg'))
        .borderRadius($r('app.float.radius_full'))
        .backgroundColor($r('app.color.primary'))
        .justifyContent(FlexAlign.Center)
      }

      // 用户信息
      Column() {
        Text(this.userInfo.name)
          .fontSize($r('app.float.font_size_xl'))
          .fontColor($r('app.color.text_primary'))
          .fontWeight(FontWeight.Bold)

        Text(this.userInfo.phone)
          .fontSize($r('app.float.font_size_sm'))
          .fontColor($r('app.color.text_secondary'))
          .margin({ top: 4 })
      }
      .alignItems(HorizontalAlign.Start)
      .margin({ left: 16 })

      Blank()

      SymbolGlyph($r('sys.symbol.chevron_right'))
        .fontSize(20)
        .fontColor([$r('app.color.icon_secondary')])
    }
    .width('100%')
    .padding(20)
    .backgroundColor($r('app.color.bg_primary'))
    .borderRadius($r('app.float.radius_lg'))
  }

  @Builder
  buildMenuItem(item: MenuItem) {
    Row() {
      SymbolGlyph($r(item.icon))
        .fontSize(24)
        .fontColor([$r('app.color.icon_primary')])

      Text(item.label)
        .fontSize($r('app.float.font_size_lg'))
        .fontColor($r('app.color.text_primary'))
        .margin({ left: 16 })

      Blank()

      if (item.value) {
        Text(item.value)
          .fontSize($r('app.float.font_size_md'))
          .fontColor($r('app.color.text_secondary'))
      }

      SymbolGlyph($r('sys.symbol.chevron_right'))
        .fontSize(20)
        .fontColor([$r('app.color.icon_secondary')])
        .margin({ left: 8 })
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
  }

  private getMenuItems(): MenuItem[] {
    return [
      { id: 'orders', label: '我的订单', icon: 'sys.symbol.doc_text' },
      { id: 'favorites', label: '我的收藏', icon: 'sys.symbol.heart' },
      { id: 'history', label: '浏览历史', icon: 'sys.symbol.clock' },
      { id: 'settings', label: '设置', icon: 'sys.symbol.gearshape' },
      { id: 'about', label: '关于', icon: 'sys.symbol.info_circle' },
    ]
  }
}

/**
 * 用户信息数据模型
 */
interface UserInfo {
  name: string
  avatar: string
  phone: string
}

/**
 * 菜单项数据模型
 */
interface MenuItem {
  id: string
  label: string
  icon: string
  value?: string
}
'''


def get_entry_module_hvigorfile() -> str:
    """生成 entry/hvigorfile.ts"""
    return '''import { hapTasks } from '@ohos/hvigor-ohos-plugin';

export default {
    system: hapTasks,
    plugins:[]
}
'''


def get_entry_oh_package() -> str:
    """生成 entry/oh-package.json5"""
    return '''{
  "name": "entry",
  "version": "1.0.0",
  "description": "Entry module",
  "main": "",
  "author": "",
  "license": "",
  "dependencies": {}
}
'''


def get_entry_build_profile() -> str:
    """生成 entry/build-profile.json5"""
    return '''{
  "apiType": "stageMode",
  "buildOption": {
  },
  "buildOptionSet": [
    {
      "name": "release",
      "arkOptions": {
        "obfuscation": {
          "ruleOptions": {
            "enable": false,
            "files": [
              "./obfuscation-rules.txt"
            ]
          }
        }
      }
    }
  ],
  "targets": [
    {
      "name": "default"
    },
    {
      "name": "ohosTest"
    }
  ]
}
'''


def get_appscope_string() -> dict:
    """生成 AppScope 字符串资源"""
    return {
        "string": [
            {"name": "app_name", "value": "我的应用"}
        ]
    }


def get_module_strings() -> dict:
    """生成模块字符串资源"""
    return {
        "string": [
            {"name": "module_desc", "value": "主模块"},
            {"name": "EntryAbility_desc", "value": "主入口"},
            {"name": "EntryAbility_label", "value": "我的应用"},
            {"name": "start_window_background", "value": "#FFFFFF"}
        ]
    }


# ============================================================================
# 项目生成器
# ============================================================================

class HarmonyProjectGenerator:
    """HarmonyOS 项目生成器"""

    def __init__(self, project_name: str, target_path: str = None):
        self.project_name = project_name
        self.bundle_name = f"{BUNDLE_NAME_PREFIX}.{project_name.lower()}"
        self.target_path = Path(target_path) if target_path else Path.cwd()
        self.project_path = self.target_path / project_name

    def generate(self):
        """生成项目"""
        print(f"\n{'='*60}")
        print(f"  HarmonyOS NEXT Project Initializer")
        print(f"{'='*60}")
        print(f"\n  Project: {self.project_name}")
        print(f"  Bundle:  {self.bundle_name}")
        print(f"  SDK:     {SDK_VERSION}")
        print(f"  Path:    {self.project_path}")
        print(f"\n{'='*60}\n")

        # 创建目录结构
        self._create_directories()

        # 生成配置文件
        self._create_config_files()

        # 生成资源文件
        self._create_resource_files()

        # 生成代码文件
        self._create_code_files()

        print(f"\n{'='*60}")
        print(f"  Project created successfully!")
        print(f"{'='*60}")
        print(f"\n  Next steps:")
        print(f"  1. Open DevEco Studio")
        print(f"  2. File -> Open -> Select: {self.project_path}")
        print(f"  3. Wait for project sync")
        print(f"  4. Run on device/emulator")
        print(f"\n{'='*60}\n")

    def _create_directories(self):
        """创建目录结构"""
        directories = [
            # 根目录
            "hvigor",
            # AppScope
            "AppScope/resources/base/element",
            "AppScope/resources/base/media",
            # Entry 模块
            "entry/src/main/ets/entryability",
            "entry/src/main/ets/pages",
            "entry/src/main/ets/components",
            "entry/src/main/ets/viewmodel",      # MVVM: ViewModel 层
            "entry/src/main/ets/model",          # MVVM: Model 层
            "entry/src/main/ets/database",       # 数据持久化层
            "entry/src/main/ets/collaboration", # 分布式协同层
            "entry/src/main/ets/services",
            "entry/src/main/ets/utils",
            # 资源目录
            "entry/src/main/resources/base/element",
            "entry/src/main/resources/base/media",
            "entry/src/main/resources/base/profile",
            "entry/src/main/resources/dark/element",
            "entry/src/main/resources/rawfile",
            # 测试目录
            "entry/src/ohosTest/ets/test",
            "entry/src/test/ets/test",
        ]

        for dir_path in directories:
            full_path = self.project_path / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"  [DIR]  {dir_path}")

    def _create_config_files(self):
        """创建配置文件"""
        configs = {
            "oh-package.json5": get_oh_package_json5(self.project_name, self.bundle_name),
            "build-profile.json5": get_build_profile_json5(self.project_name),
            "hvigorfile.ts": get_hvigorfile(),
            "hvigor/hvigor-config.json5": get_hvigor_config(),
            "AppScope/app.json5": get_app_json5(self.project_name, self.bundle_name),
            "entry/hvigorfile.ts": get_entry_module_hvigorfile(),
            "entry/oh-package.json5": get_entry_oh_package(),
            "entry/build-profile.json5": get_entry_build_profile(),
            "entry/src/main/module.json5": get_module_json5(self.project_name, self.bundle_name),
            "entry/src/main/resources/base/profile/main_pages.json": get_main_pages(),
        }

        for file_path, content in configs.items():
            self._write_file(file_path, content)

    def _create_resource_files(self):
        """创建资源文件"""
        # 基础颜色 (含启动窗口背景色)
        colors = COLORS_BASE.copy()
        colors["color"].append({"name": "start_window_background", "value": "#FFFFFF"})
        self._write_json("entry/src/main/resources/base/element/color.json", colors)

        # 深色模式颜色
        self._write_json("entry/src/main/resources/dark/element/color.json", COLORS_DARK)

        # 尺寸
        self._write_json("entry/src/main/resources/base/element/float.json", FLOATS_BASE)

        # 字符串 (合并基础字符串和模块字符串)
        module_strings = get_module_strings()
        existing_strings = STRINGS_BASE.copy()
        existing_strings["string"].extend(module_strings["string"])
        self._write_json("entry/src/main/resources/base/element/string.json", existing_strings)

        # AppScope 字符串
        self._write_json("AppScope/resources/base/element/string.json", get_appscope_string())

        # 媒体资源文件
        self._create_media_files()

    def _create_media_files(self):
        """创建媒体资源文件"""
        # layered_image.json - 分层图标配置
        self._write_file("entry/src/main/resources/base/media/layered_image.json", get_layered_image_json())

        # 前景图 (foreground.png)
        self._write_binary("entry/src/main/resources/base/media/foreground.png", 
                          base64.b64decode(FOREGROUND_PNG_BASE64))

        # 背景图 (background.png)
        self._write_binary("entry/src/main/resources/base/media/background.png", 
                          base64.b64decode(BACKGROUND_PNG_BASE64))

        # 启动图标 (startIcon.png)
        self._write_binary("entry/src/main/resources/base/media/startIcon.png", 
                          base64.b64decode(START_ICON_PNG_BASE64))

    def _create_code_files(self):
        """创建代码文件"""
        code_files = {
            # 入口和页面
            "entry/src/main/ets/entryability/EntryAbility.ets": get_entry_ability(),
            "entry/src/main/ets/pages/Index.ets": get_index_page(),
            "entry/src/main/ets/pages/HomePage.ets": get_home_page(),
            "entry/src/main/ets/pages/ProfilePage.ets": get_profile_page(),
            # MVVM 架构基础文件
            "entry/src/main/ets/viewmodel/BaseViewModel.ets": get_base_viewmodel(),
            "entry/src/main/ets/model/Models.ets": get_example_model(),
            # 数据持久化基础文件
            "entry/src/main/ets/database/DatabaseHelper.ets": get_database_helper(),
            "entry/src/main/ets/utils/PreferencesUtil.ets": get_preferences_util(),
            # 分布式协同基础文件
            "entry/src/main/ets/collaboration/CollaborationManager.ets": get_collaboration_manager(),
        }

        for file_path, content in code_files.items():
            self._write_file(file_path, content)

    def _write_file(self, relative_path: str, content: str):
        """写入文件"""
        file_path = self.project_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
        print(f"  [FILE] {relative_path}")

    def _write_json(self, relative_path: str, data: dict):
        """写入 JSON 文件"""
        file_path = self.project_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"  [JSON] {relative_path}")

    def _write_binary(self, relative_path: str, data: bytes):
        """写入二进制文件"""
        file_path = self.project_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(data)
        print(f"  [BIN]  {relative_path}")


# ============================================================================
# 主程序
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Initialize a HarmonyOS NEXT 6.0 project with design system.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python init_harmony_project.py MyApp --sdk "6.0.2(22)"
  python init_harmony_project.py MyApp --sdk "5.0.0(12)" --path E:/projects
  python init_harmony_project.py ShoppingApp --sdk "6.0.2(22)" --bundle com.mycompany

SDK Version Format:
  格式: "主版本.次版本.修订版(API版本)"
  示例: "6.0.2(22)", "5.0.0(12)"
  
  查看当前SDK版本: 在 DevEco Studio 中查看项目的 build-profile.json5
        '''
    )

    parser.add_argument('project_name', help='项目名称 (如 MyApp)')
    parser.add_argument('--sdk', '-s', required=True, 
                        help='SDK版本，格式如 "6.0.2(22)" (必填)')
    parser.add_argument('--path', '-p', default=None, 
                        help='目标目录 (默认: 当前目录)')
    parser.add_argument('--bundle', '-b', default=None, 
                        help='包名前缀 (默认: com.example)')

    args = parser.parse_args()

    # 验证项目名称
    if not args.project_name.replace('_', '').isalnum():
        print("Error: 项目名称只能包含字母、数字和下划线。")
        sys.exit(1)

    # 解析并设置 SDK 版本
    global HARMONY_VERSION, SDK_VERSION, BUNDLE_NAME_PREFIX
    try:
        HARMONY_VERSION, SDK_VERSION = parse_sdk_version(args.sdk)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # 更新包名前缀
    if args.bundle:
        BUNDLE_NAME_PREFIX = args.bundle

    # 生成项目
    generator = HarmonyProjectGenerator(args.project_name, args.path)
    generator.generate()


if __name__ == '__main__':
    main()
