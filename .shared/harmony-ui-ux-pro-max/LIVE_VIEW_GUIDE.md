HarmonyOS NEXT 实况窗 (Live View) 开发指南 - LiveViewKit 版
1. 核心优势
开发简化：不再需要手动构建复杂的通知请求，直接使用 LiveViewManager。

类型安全：通过 LiveViewData 结构化定义胶囊、扩展态内容。

系统级集成：更好的功耗管理和多端同步。

2. 核心代码模板 (Standard Implementation)
AI 必须使用 @kit.LiveViewKit 进行开发：

A. 导入与初始化
TypeScript

import { LiveViewManager, liveView } from '@kit.LiveViewKit';
import { wantAgent } from '@kit.AbilityKit';

// 定义实况窗数据
let liveViewData: liveView.LiveViewData = {
  primaryId: 1001, // 业务 ID
  primaryStatus: liveView.LiveViewStatus.ONGOING,
  // 1. 胶囊状态（状态栏）
  capsule: {
    type: liveView.CapsuleType.CAPSULE_TYPE_TEXT,
    icon: $r('app.media.food_icon'),
    backgroundColor: '#FF6600',
    title: $r('app.string.delivering'),
    content: '15 min'
  },
  // 2. 扩展态（通知中心/锁屏）
  contents: {
    title: $r('app.string.order_status'),
    content: $r('app.string.courier_nearby'),
    layoutType: liveView.LayoutType.LAYOUT_TYPE_PROGRESS, // 进度条布局
    progress: 60,
    additionalInfo: '距离您 1.2km'
  },
  // 3. 点击动作
  clickAction: await wantAgent.getWantAgent({
    wants: [{ bundleName: 'com.example.app', abilityName: 'EntryAbility' }],
    operationType: wantAgent.OperationType.START_ABILITY,
    requestCode: 0
  })
};
B. 生命周期管理
TypeScript

// 启动/创建实况窗
await LiveViewManager.startLiveView(liveViewData);

// 更新进度
liveViewData.contents.progress = 85;
await LiveViewManager.updateLiveView(liveViewData);

// 结束实况窗
liveViewData.primaryStatus = liveView.LiveViewStatus.FINISHED;
await LiveViewManager.stopLiveView(liveViewData);
3. AI 强制检查清单 (Rules)
模块导入：必须使用 import { LiveViewManager } from '@kit.LiveViewKit'。

布局选择：必须根据场景选择 LayoutType（如 LAYOUT_TYPE_PICKUP 用于打车，LAYOUT_TYPE_PROGRESS 用于外卖）。

权限检查：提醒用户在 module.json5 中配置 ohos.permission.KEEP_ALIVE（如果需要长时运行）及通知相关权限。