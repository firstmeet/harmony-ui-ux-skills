# HarmonyOS UI/UX 知识库

本知识库收集整理了华为开发者联盟官方示例代码和 HarmonyOS NEXT 开发的核心知识点，用于 AI 辅助 UI/UX 设计和代码生成。

**数据来源**: [华为开发者联盟示例代码](https://developer.huawei.com/consumer/cn/samples/)  
**采集日期**: 2026-01-19  
**示例总数**: 约 380 个 (38页 x 10个/页)

## 📚 知识库文件索引 (共26个文件)

### 官方示例代码 (Official Samples)
| 文件 | 描述 | 条目数 |
|------|------|--------|
| `official_samples_full.csv` | 完整示例代码列表 | 50+ |
| `official_samples.csv` | 精选示例代码 | 26 |
| `ai_samples.csv` | AI 功能开发示例 | 14 |

### UI 组件与布局 (Components & Layouts)
| 文件 | 描述 | 条目数 |
|------|------|--------|
| `arkui_components.csv` | ArkUI 组件完整参考 | 35+ |
| `arkui_patterns.csv` | 常用 UI 模式模板 | 15 |
| `components.csv` | 基础组件详细用法 | 13 |
| `layouts.csv` | 布局容器详细用法 | 7 |
| `code_snippets.csv` | 常用代码片段 | 13 |
| `ui_effects.csv` | UI 特效实现方法 | 10 |

### 开发框架与服务 (Kits & Services)
| 文件 | 描述 | 条目数 |
|------|------|--------|
| `kits_reference.csv` | HarmonyOS Kit 服务参考 | 20+ |
| `app_services.csv` | 应用服务开发参考 | 15 |
| `distributed_features.csv` | 分布式特性参考 | 9 |
| `system_capabilities.csv` | 系统能力参考 | 9 |

### 状态管理与导航 (State & Navigation)
| 文件 | 描述 | 条目数 |
|------|------|--------|
| `state_management.csv` | 状态管理装饰器 | 12 |
| `navigation_patterns.csv` | 导航模式参考 | 9 |

### 表单与动画 (Forms & Animations)
| 文件 | 描述 | 条目数 |
|------|------|--------|
| `form_patterns.csv` | 表单验证模式 | 10 |
| `animation_examples.csv` | 动画示例 | 12 |
| `animations.csv` | 动画规范 | 13 |

### 无障碍与国际化 (Accessibility & i18n)
| 文件 | 描述 | 条目数 |
|------|------|--------|
| `accessibility_i18n.csv` | 无障碍与国际化 | 10 |

### 图标使用 (Icons)
| 文件 | 描述 | 条目数 |
|------|------|--------|
| `icons_guide.csv` | 图标使用流程指南 | 6 |
| `harmony_symbols.csv` | HarmonyOS 原生图标完整列表 | 404 (唯一) |

> **注意**: 官方页面显示433个图标符号，但这包含了同一图标在多个类别中出现的重复条目。去重后的实际唯一图标数量为404个。

### 设计规范 (Design Tokens)
| 文件 | 描述 | 条目数 |
|------|------|--------|
| `colors.csv` | 颜色设计规范 | 17 |
| `typography.csv` | 字体排版规范 | 8 |
| `spacing.csv` | 间距规范 | 5 |
| `page_templates.csv` | 页面模板 | 10+ |

## 📊 示例代码分类统计

基于华为开发者联盟 2026-01-19 数据:

| 类别 | 示例数量 | 子类别 |
|------|----------|--------|
| **HarmonyOS特征** | 23 | 一次开发多端部署、自由流转、原生智能 |
| **应用框架开发** | 154 | 程序框架、ArkTS语言、UI框架、NDK、本地数据、Web等 |
| **系统开发** | 54 | 网络、安全、基本功能、硬件、穿戴 |
| **媒体开发** | 20+ | 音频、视频、直播、短视频 |
| **AI功能开发** | 24 | 意图框架、机器学习、计算平台 |
| **应用服务开发** | 38 | 各类 Kit 服务集成 |
| **图形开发** | 15+ | 2D/3D图形、渲染 |
| **技术质量** | 10+ | 性能优化、稳定性 |

## 🔑 核心 Kit 服务速查

### AI & 视觉
| Kit | 主要功能 | 典型场景 |
|-----|---------|----------|
| Core Vision Kit | 文字识别(OCR)、人脸检测、人脸比对、主体分割、骨骼点识别 | 证件识别、人脸验证、抠图 |
| Vision Kit | 文档扫描、卡证识别、表格提取、人脸活体检测 | 文档数字化、身份验证 |
| Core Speech Kit | 语音识别(ASR)、语音合成(TTS) | 语音输入、语音播报 |
| Speech Kit | AI字幕、朗读控件 | 视频字幕、内容朗读 |
| Natural Language Kit | 分词、实体抽取 | 搜索优化、智能客服 |
| CANN Kit | 模型推理、图像分类 | AI应用 |

### 设备协同
| Kit | 主要功能 | 典型场景 |
|-----|---------|----------|
| Share Kit | 隔空传送(gesturesShare)、碰一碰分享(knockShare)、华为分享 | 跨设备文件共享 |
| Service Collaboration Kit | 跨设备互通 | 多设备协同 |
| Wear Engine Kit | 穿戴设备交互、消息通信、传感器信息 | 手表应用 |

### 应用服务
| Kit | 主要功能 | 典型场景 |
|-----|---------|----------|
| Account Kit | 华为账号静默登录、头像昵称授权、快速验证手机号 | 用户登录 |
| Payment Kit | 支付收银台 | 应用内支付 |
| Push Kit | 消息推送 | 通知提醒 |
| Health Kit | 运动健康数据管理 | 健康类应用 |
| Live View Kit | 实况窗服务 | 外卖、快递进度 |
| Reader Kit | 电子书阅读 | 阅读类应用 |
| App Linking Kit | 延迟链接 | 应用跳转 |

### 系统能力
| Kit | 主要功能 | 典型场景 |
|-----|---------|----------|
| CameraKit | 相机预览、拍照、录像、对焦、变焦 | 相机应用 |
| SFFT | 大文件高速并发传输 | 文件上传下载 |
| Network Boost Kit | 网络感知、网络质量预测 | 网络优化 |
| Device Security Kit | 安全相机、安全地理位置、防窥保护 | 隐私安全 |
| AR Engine | 空间感知、平面识别、SLAM | AR应用 |
| Graphics Accelerate Kit | 游戏资源加速下载 | 游戏应用 |

## 🚀 快速使用指南

### 查找组件用法
```
1. arkui_components.csv → 了解组件属性
2. code_snippets.csv → 获取代码模板
3. arkui_patterns.csv → 了解常用模式
```

### 实现特定功能
```
1. official_samples_full.csv → 找到官方示例
2. kits_reference.csv → 了解 API
3. 查看对应 Kit 服务文档
```

### 设计 UI 界面
```
1. colors.csv → 选择配色
2. typography.csv → 确定字体
3. layouts.csv → 选择布局
4. animation_examples.csv → 添加动效
```

### 表单开发
```
1. form_patterns.csv → 验证模式
2. state_management.csv → 状态管理
3. accessibility_i18n.csv → 无障碍支持
```

### 使用图标
```
1. harmony_symbols.csv → 检查原生图标是否存在
2. 存在 → 使用 $r('sys.symbol.xxx')
3. 不存在 → 访问 https://allsvgicons.com/ 下载 SVG
4. 保存到 resources/base/media/ic_xxx.svg
5. 使用 $r('app.media.ic_xxx')
```

## 📝 关键技术要点

### 状态管理优先级
1. `@State` - 组件内部状态
2. `@Prop` - 父到子单向传递
3. `@Link` - 父子双向同步
4. `@Provide/@Consume` - 跨层级共享
5. `@StorageLink` - 持久化存储

### 性能优化
- 使用 `LazyForEach` 实现懒加载
- 使用 `@Observed/@ObjectLink` 观察对象属性变化
- 使用后台任务实现应用保活

### 资源引用规范
```typescript
// 颜色
$r('app.color.primary')

// 字符串
$r('app.string.app_name')

// 尺寸
$r('app.float.font_body')

// 系统图标
$r('sys.symbol.heart_fill')
```

## 📝 更新日志

### 2026-01-19 (Update 3)
- 完整采集 HarmonyOS Symbol 官方图标库
- 官方显示 433 个图标符号，去重后实际 404 个唯一图标
- 数据来源: https://developer.huawei.com/consumer/cn/design/harmonyos-symbol/
- 包含 15 个分类: 系统UI/时间/箭头/相机与照片/办公文件/键盘/媒体/通信/连接/符号标识/编辑/隐私安全/人物/形状/交通出行
- 每个图标包含: 分类/图标名称/中文名称/Unicode/所属模块/使用场景
- 修正图标命名格式: 使用下划线 `_` 而非点号 `.`（如 `chevron_left` 而非 `chevron.left`）

### 2026-01-19 (Update 2)
- 新增图标使用规则 Rule 6: 先检查原生图标是否存在，不存在则从 allsvgicons.com 获取
- 添加 `icons_guide.csv` - 图标使用流程指南
- 添加 `harmony_symbols.csv` - HarmonyOS 原生图标完整列表 (404个唯一图标)
- 更新 CODING_RULES.md 添加图标检查流程
- 知识库文件增至 26 个

### 2026-01-19
- 完整采集华为开发者联盟示例代码 (~380个)
- 按类别整理：应用框架开发、系统开发、媒体开发、AI功能开发等
- 添加 AI 功能、分布式特性、系统能力等分类
- 整理 ArkUI 组件完整参考和代码片段
- 添加表单验证模式、动画示例
- 添加无障碍与国际化指南
- 创建 24 个 CSV 知识库文件
