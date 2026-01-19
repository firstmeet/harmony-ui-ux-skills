# HarmonyOS NEXT Resource Sync Rules

## Overview

本文档定义资源文件的同步输出规范，确保生成的 UI 代码与资源文件保持一致。

---

## 1. 核心原则

### 强制同步规则

```
当生成包含 $r() 引用的代码时，必须同时输出:

1. string.json  - 所有 $r('app.string.xxx') 的定义
2. color.json   - 所有 $r('app.color.xxx') 的定义  
3. float.json   - 所有 $r('app.float.xxx') 的定义（如有新增）
```

### 资源命名规范

```
格式: 模块名_功能名_属性名

示例:
├── 登录模块
│   ├── login_title            → "欢迎登录"
│   ├── login_button_text      → "登录"
│   ├── login_button_bg        → "#0A59F7"
│   └── login_input_placeholder → "请输入用户名"
│
├── 购物车模块
│   ├── cart_title             → "购物车"
│   ├── cart_empty_text        → "购物车空空如也"
│   ├── cart_badge_bg          → "#E84026"
│   └── cart_total_label       → "合计"
│
└── 通用
    ├── common_confirm         → "确认"
    ├── common_cancel          → "取消"
    └── common_loading         → "加载中..."
```

---

## 2. 输出格式模板

### 完整输出示例

当 AI 生成一个登录页面时，必须按以下格式输出：

#### UI 代码 (LoginPage.ets)

```typescript
@Entry
@Component
struct LoginPage {
  @State username: string = ''
  @State password: string = ''

  build() {
    Column() {
      // 标题
      Text($r('app.string.login_title'))
        .fontSize($r('app.float.font_size_headline'))
        .fontColor($r('app.color.login_title_color'))
        .fontWeight(FontWeight.Bold)

      // 用户名输入
      TextInput({ placeholder: $r('app.string.login_username_placeholder') })
        .height($r('app.float.input_height'))
        .backgroundColor($r('app.color.login_input_bg'))
        .borderRadius($r('app.float.radius_sm'))
        .margin({ top: 32 })
        .onChange((value) => this.username = value)

      // 密码输入
      TextInput({ placeholder: $r('app.string.login_password_placeholder') })
        .type(InputType.Password)
        .height($r('app.float.input_height'))
        .backgroundColor($r('app.color.login_input_bg'))
        .borderRadius($r('app.float.radius_sm'))
        .margin({ top: 16 })
        .onChange((value) => this.password = value)

      // 登录按钮
      Button($r('app.string.login_button_text'))
        .width('100%')
        .height($r('app.float.button_height_lg'))
        .backgroundColor($r('app.color.login_button_bg'))
        .fontColor($r('app.color.login_button_text'))
        .borderRadius($r('app.float.radius_sm'))
        .margin({ top: 32 })

      // 忘记密码
      Text($r('app.string.login_forgot_password'))
        .fontSize($r('app.float.font_size_sm'))
        .fontColor($r('app.color.login_link_color'))
        .margin({ top: 16 })
    }
    .width('100%')
    .height('100%')
    .padding(24)
    .backgroundColor($r('app.color.login_bg'))
  }
}
```

#### 资源文件 - string.json 片段

```json
{
  "string": [
    { "name": "login_title", "value": "欢迎登录" },
    { "name": "login_username_placeholder", "value": "请输入用户名" },
    { "name": "login_password_placeholder", "value": "请输入密码" },
    { "name": "login_button_text", "value": "登录" },
    { "name": "login_forgot_password", "value": "忘记密码？" }
  ]
}
```

#### 资源文件 - color.json 片段

```json
{
  "color": [
    { "name": "login_title_color", "value": "#182431" },
    { "name": "login_input_bg", "value": "#F1F3F5" },
    { "name": "login_button_bg", "value": "#0A59F7" },
    { "name": "login_button_text", "value": "#FFFFFF" },
    { "name": "login_link_color", "value": "#0A59F7" },
    { "name": "login_bg", "value": "#FFFFFF" }
  ]
}
```

#### 资源文件 - float.json 片段 (如有新增)

```json
{
  "float": [
    { "name": "font_size_headline", "value": "32fp" },
    { "name": "font_size_sm", "value": "12fp" },
    { "name": "input_height", "value": "48vp" },
    { "name": "button_height_lg", "value": "48vp" },
    { "name": "radius_sm", "value": "8vp" }
  ]
}
```

---

## 3. 深色模式资源

### 同步输出深色模式颜色

当页面需要支持深色模式时，必须同时输出 `resources/dark/element/color.json`：

#### dark/element/color.json 片段

```json
{
  "color": [
    { "name": "login_title_color", "value": "#E5E8EB" },
    { "name": "login_input_bg", "value": "#2C2C2C" },
    { "name": "login_button_bg", "value": "#317AF7" },
    { "name": "login_button_text", "value": "#FFFFFF" },
    { "name": "login_link_color", "value": "#317AF7" },
    { "name": "login_bg", "value": "#121212" }
  ]
}
```

---

## 4. 资源 Diff 格式

### 增量更新输出

当修改现有页面时，输出增量变更（diff 格式）：

```diff
// resources/base/element/string.json
{
  "string": [
    // ... 现有内容 ...
+   { "name": "cart_checkout_button", "value": "去结算" },
+   { "name": "cart_select_all", "value": "全选" }
  ]
}

// resources/base/element/color.json
{
  "color": [
    // ... 现有内容 ...
+   { "name": "cart_checkout_bg", "value": "#FF6B35" },
+   { "name": "cart_price_color", "value": "#E84026" }
  ]
}
```

---

## 5. main_pages.json 同步

### 新建页面时必须更新

当创建新的 @Entry 页面时，必须同步更新 `main_pages.json`：

```diff
// resources/base/profile/main_pages.json
{
  "src": [
    "pages/Index",
    "pages/HomePage",
    "pages/ProfilePage",
+   "pages/LoginPage",
+   "pages/CartPage"
  ]
}
```

---

## 6. 权限声明同步

### 功能与权限对照表

| 功能 | 所需权限 | 权限名称 |
|------|---------|---------|
| 网络请求 | `ohos.permission.INTERNET` | 网络访问 |
| 定位 | `ohos.permission.LOCATION` | 位置信息 |
| 相机 | `ohos.permission.CAMERA` | 相机访问 |
| 相册 | `ohos.permission.READ_MEDIA` | 读取媒体 |
| 通知 | `ohos.permission.NOTIFICATION` | 发送通知 |
| 存储 | `ohos.permission.READ_WRITE_DOWNLOAD_DIRECTORY` | 下载目录 |

### 权限声明输出

当生成需要权限的功能时，必须同步输出 `module.json5` 更新：

```diff
// entry/src/main/module.json5
{
  "module": {
    // ... 其他配置 ...
    "requestPermissions": [
+     {
+       "name": "ohos.permission.INTERNET",
+       "reason": "$string:internet_permission_reason",
+       "usedScene": {
+         "abilities": ["EntryAbility"],
+         "when": "inuse"
+       }
+     },
+     {
+       "name": "ohos.permission.LOCATION",
+       "reason": "$string:location_permission_reason",
+       "usedScene": {
+         "abilities": ["EntryAbility"],
+         "when": "inuse"
+       }
+     }
    ]
  }
}
```

同时输出权限说明字符串：

```diff
// resources/base/element/string.json
{
  "string": [
+   { "name": "internet_permission_reason", "value": "用于访问网络获取数据" },
+   { "name": "location_permission_reason", "value": "用于获取您的位置信息" }
  ]
}
```

---

## 7. 资源文件结构

### 标准目录结构

```
entry/src/main/resources/
├── base/
│   ├── element/
│   │   ├── color.json      # 颜色资源
│   │   ├── string.json     # 字符串资源
│   │   └── float.json      # 尺寸资源
│   ├── media/
│   │   ├── layered_image.json
│   │   ├── foreground.png
│   │   ├── background.png
│   │   ├── startIcon.png
│   │   └── ic_xxx.svg      # 自定义图标
│   └── profile/
│       └── main_pages.json  # 页面注册
│
├── dark/
│   └── element/
│       └── color.json      # 深色模式颜色
│
└── rawfile/
    └── ...                 # 原始文件
```

---

## 8. 资源同步检查清单

### 生成代码时

- [ ] 所有 `$r('app.string.xxx')` 都有 string.json 定义
- [ ] 所有 `$r('app.color.xxx')` 都有 color.json 定义
- [ ] 新增尺寸使用 `$r('app.float.xxx')` 并定义
- [ ] 资源命名遵循 `模块名_功能名_属性名` 格式

### 创建新页面时

- [ ] 已更新 main_pages.json
- [ ] 已声明所需权限（如有）
- [ ] 已提供权限说明字符串

### 支持深色模式时

- [ ] 已提供 dark/element/color.json 定义
- [ ] 深色模式颜色与浅色模式对应

---

## 9. 输出格式规范

### AI 输出模板

```markdown
## 代码文件

### LoginPage.ets

\`\`\`typescript
// 代码内容
\`\`\`

---

## 资源文件更新

### string.json (新增)

\`\`\`json
{
  "string": [
    { "name": "login_xxx", "value": "xxx" }
  ]
}
\`\`\`

### color.json (新增)

\`\`\`json
{
  "color": [
    { "name": "login_xxx", "value": "#xxx" }
  ]
}
\`\`\`

### dark/element/color.json (新增)

\`\`\`json
{
  "color": [
    { "name": "login_xxx", "value": "#xxx" }
  ]
}
\`\`\`

### main_pages.json (更新)

\`\`\`diff
{
  "src": [
    // 现有页面...
+   "pages/LoginPage"
  ]
}
\`\`\`
```
