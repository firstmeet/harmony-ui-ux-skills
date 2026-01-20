# HarmonyOS NEXT AI Kit 开发指南

> 基于 [华为开发者文档中心](https://developer.huawei.com/consumer/cn/doc/) AI 相关文档整理

## AI Kit 概览

HarmonyOS NEXT 提供了丰富的端侧 AI 能力，无需依赖云端即可实现智能化功能。

| Kit | 能力 | 典型场景 |
|-----|------|---------|
| **Core Vision Kit** | OCR、人脸检测、图像分类 | 证件识别、人脸解锁 |
| **Core Speech Kit** | 语音识别、语音合成 | 语音输入、语音播报 |
| **Vision Kit** | 文档扫描、卡证识别 | 扫描仪、银行卡识别 |
| **Speech Kit** | 朗读控件、AI 字幕 | 文章朗读、视频字幕 |
| **Natural Language Kit** | 分词、实体识别 | 智能搜索、文本分析 |
| **Agent Framework Kit** | 智能体调用 | AI 助手、智能客服 |
| **Intents Kit** | 意图识别 | 小艺建议、智能推荐 |
| **MindSpore Lite Kit** | 模型推理 | 自定义 AI 模型 |
| **Data Augmentation Kit** | 知识库、RAG | 本地问答、知识检索 |

---

## 一、Core Vision Kit (基础视觉)

### 1.1 文字识别 (OCR)

```typescript
import { textRecognition } from '@kit.CoreVisionKit';
import { image } from '@kit.ImageKit';

@Component
struct OcrDemo {
  @State recognizedText: string = ''

  async recognizeText(imageSource: image.ImageSource): Promise<void> {
    const pixelMap = await imageSource.createPixelMap();
    
    // 调用文字识别
    const result = await textRecognition.recognizeText(pixelMap);
    
    if (result && result.value) {
      this.recognizedText = result.value;
    }
  }

  build() {
    Column() {
      Image($r('app.media.sample_image'))
        .width('100%')
        .height(200)
      
      Button('识别文字')
        .onClick(() => this.recognizeFromCamera())
      
      Text(this.recognizedText)
        .fontSize(14)
        .padding(16)
    }
  }
}
```

### 1.2 人脸检测

```typescript
import { faceDetector } from '@kit.CoreVisionKit';

async function detectFaces(pixelMap: image.PixelMap): Promise<faceDetector.Face[]> {
  const result = await faceDetector.detect(pixelMap, {
    detectMode: faceDetector.DetectMode.DETECT_MODE_PHOTO
  });
  
  return result.faces;
}

// 人脸信息包含：
// - boundingBox: 人脸边界框
// - landmarks: 关键点（眼睛、鼻子、嘴巴）
// - headPose: 头部姿态（俯仰、偏转、翻滚角度）
// - emotion: 表情（微笑、惊讶等）
```

### 1.3 图像分类

```typescript
import { imageClassifier } from '@kit.CoreVisionKit';

async function classifyImage(pixelMap: image.PixelMap): Promise<string[]> {
  const result = await imageClassifier.classify(pixelMap);
  
  // 返回识别的类别列表
  return result.categories.map(cat => cat.label);
}
```

---

## 二、Core Speech Kit (基础语音)

### 2.1 语音识别 (ASR)

```typescript
import { speechRecognizer } from '@kit.CoreSpeechKit';

@Component
struct VoiceInputDemo {
  private recognizer: speechRecognizer.SpeechRecognizer | null = null
  @State isListening: boolean = false
  @State recognizedText: string = ''

  async initRecognizer(): Promise<void> {
    const options: speechRecognizer.CreateEngineParams = {
      language: 'zh-CN',
      scene: speechRecognizer.RecognitionScene.SCENE_CONVERSATION
    };
    
    this.recognizer = await speechRecognizer.createEngine(options);
    
    // 监听识别结果
    this.recognizer.on('result', (result) => {
      if (result.isLast) {
        this.recognizedText = result.result;
        this.isListening = false;
      }
    });
  }

  async startListening(): Promise<void> {
    if (!this.recognizer) {
      await this.initRecognizer();
    }
    
    await this.recognizer?.startListening({
      vadBegin: 2000,  // 静音检测开始时间
      vadEnd: 3000     // 静音检测结束时间
    });
    
    this.isListening = true;
  }

  async stopListening(): Promise<void> {
    await this.recognizer?.stopListening();
    this.isListening = false;
  }

  aboutToDisappear(): void {
    this.recognizer?.shutdown();
  }

  build() {
    Column({ space: 20 }) {
      TextArea({ text: this.recognizedText })
        .height(150)
      
      Button(this.isListening ? '停止' : '开始语音输入')
        .onClick(() => {
          if (this.isListening) {
            this.stopListening();
          } else {
            this.startListening();
          }
        })
    }
    .padding(20)
  }
}
```

### 2.2 语音合成 (TTS)

```typescript
import { textToSpeech } from '@kit.CoreSpeechKit';

@Component
struct TtsDemo {
  private ttsEngine: textToSpeech.TextToSpeechEngine | null = null
  @State isSpeaking: boolean = false

  async initTts(): Promise<void> {
    const options: textToSpeech.CreateEngineParams = {
      language: 'zh-CN',
      person: textToSpeech.VoiceType.VOICE_TYPE_FEMALE_GENTLE
    };
    
    this.ttsEngine = await textToSpeech.createEngine(options);
    
    this.ttsEngine.on('finish', () => {
      this.isSpeaking = false;
    });
  }

  async speak(text: string): Promise<void> {
    if (!this.ttsEngine) {
      await this.initTts();
    }
    
    const params: textToSpeech.SpeakParams = {
      requestId: Date.now().toString(),
      speed: 1.0,    // 语速 0.5-2.0
      volume: 1.0,   // 音量 0.0-1.0
      pitch: 1.0     // 音调 0.5-2.0
    };
    
    await this.ttsEngine?.speak(text, params);
    this.isSpeaking = true;
  }

  async stop(): Promise<void> {
    await this.ttsEngine?.stop();
    this.isSpeaking = false;
  }

  aboutToDisappear(): void {
    this.ttsEngine?.shutdown();
  }

  build() {
    Column({ space: 20 }) {
      TextInput({ placeholder: '输入要朗读的文本' })
        .onChange((value) => this.textToSpeak = value)
      
      Button(this.isSpeaking ? '停止' : '朗读')
        .onClick(() => {
          if (this.isSpeaking) {
            this.stop();
          } else {
            this.speak(this.textToSpeak);
          }
        })
    }
    .padding(20)
  }
}
```

---

## 三、Vision Kit (场景化视觉)

### 3.1 文档扫描

```typescript
import { documentScanner } from '@kit.VisionKit';

async function scanDocument(): Promise<string> {
  // 启动文档扫描界面
  const result = await documentScanner.startDocumentScanner({
    maxPages: 10,
    pageMode: documentScanner.PageMode.MULTI_PAGE
  });
  
  if (result && result.uri) {
    return result.uri;  // 返回扫描后的 PDF/图片路径
  }
  
  return '';
}
```

### 3.2 卡证识别

```typescript
import { cardRecognition } from '@kit.VisionKit';

// 身份证识别
async function recognizeIdCard(pixelMap: image.PixelMap): Promise<IdCardInfo> {
  const result = await cardRecognition.recognizeIdCard(pixelMap);
  
  return {
    name: result.name,
    gender: result.gender,
    nationality: result.nationality,
    birthday: result.birthday,
    address: result.address,
    idNumber: result.idNumber
  };
}

// 银行卡识别
async function recognizeBankCard(pixelMap: image.PixelMap): Promise<BankCardInfo> {
  const result = await cardRecognition.recognizeBankCard(pixelMap);
  
  return {
    cardNumber: result.cardNumber,
    expiryDate: result.expiryDate,
    cardType: result.cardType
  };
}
```

---

## 四、Speech Kit (场景化语音)

### 4.1 朗读控件

```typescript
import { ReadAloud } from '@kit.SpeechKit';

@Entry
@Component
struct ArticleReadPage {
  @State articleContent: string = '这是一篇文章的内容...'

  build() {
    Column() {
      // 文章标题
      Text('文章标题')
        .fontSize(20)
        .fontWeight(FontWeight.Bold)
      
      // 朗读控件 - 系统提供的开箱即用组件
      ReadAloud({
        text: this.articleContent,
        config: {
          language: 'zh-CN',
          speed: 1.0,
          voiceType: ReadAloud.VoiceType.FEMALE
        }
      })
      
      // 文章内容
      Text(this.articleContent)
        .fontSize(16)
        .lineHeight(24)
    }
    .padding(16)
  }
}
```

### 4.2 AI 字幕

```typescript
import { AiCaption } from '@kit.SpeechKit';

@Entry
@Component
struct VideoWithCaptionPage {
  @State videoUrl: string = 'xxx.mp4'

  build() {
    Stack() {
      // 视频播放器
      Video({ src: this.videoUrl })
        .width('100%')
        .height('100%')
      
      // AI 字幕控件 - 自动识别视频音频生成字幕
      AiCaption({
        bindVideoId: 'video_player',
        config: {
          language: 'zh-CN',
          position: AiCaption.Position.BOTTOM,
          fontSize: 16
        }
      })
    }
  }
}
```

---

## 五、Natural Language Kit (自然语言)

### 5.1 文本分词

```typescript
import { textProcessing } from '@kit.NaturalLanguageKit';

async function segmentText(text: string): Promise<string[]> {
  const result = await textProcessing.segment(text);
  return result.words;
}

// 示例
// 输入: "今天天气真好"
// 输出: ["今天", "天气", "真", "好"]
```

### 5.2 实体识别

```typescript
import { textProcessing } from '@kit.NaturalLanguageKit';

interface Entity {
  type: string;   // PERSON, LOCATION, ORGANIZATION, TIME, etc.
  value: string;
  offset: number;
}

async function extractEntities(text: string): Promise<Entity[]> {
  const result = await textProcessing.extractEntities(text);
  return result.entities;
}

// 示例
// 输入: "明天下午3点我和张三在北京见面"
// 输出: [
//   { type: "TIME", value: "明天下午3点" },
//   { type: "PERSON", value: "张三" },
//   { type: "LOCATION", value: "北京" }
// ]
```

---

## 六、Agent Framework Kit (智能体框架)

### 6.1 调用智能体

```typescript
import { agentFramework } from '@kit.AgentFrameworkKit';

@Component
struct AiAssistantDemo {
  @State userInput: string = ''
  @State aiResponse: string = ''
  @State isProcessing: boolean = false

  async askAgent(): Promise<void> {
    this.isProcessing = true;
    
    try {
      // 创建智能体会话
      const session = await agentFramework.createSession({
        agentId: 'your_agent_id',
        context: {
          userId: 'user_123'
        }
      });
      
      // 发送消息
      const response = await session.sendMessage({
        content: this.userInput,
        type: 'text'
      });
      
      this.aiResponse = response.content;
      
    } finally {
      this.isProcessing = false;
    }
  }

  build() {
    Column({ space: 16 }) {
      // 对话历史
      List() {
        // ... 对话消息列表
      }
      .layoutWeight(1)
      
      // 输入区
      Row() {
        TextInput({ placeholder: '输入您的问题' })
          .layoutWeight(1)
          .onChange((value) => this.userInput = value)
        
        Button('发送')
          .enabled(!this.isProcessing)
          .onClick(() => this.askAgent())
      }
    }
    .padding(16)
  }
}
```

---

## 七、Intents Kit (意图框架)

### 7.1 注册意图

```typescript
// 在 module.json5 中注册意图
{
  "module": {
    "abilities": [{
      "name": "EntryAbility",
      "skills": [{
        "actions": ["ohos.want.action.viewData"],
        "entities": ["entity.system.default"],
        "uris": [{
          "scheme": "myapp",
          "host": "order",
          "path": "/detail"
        }]
      }]
    }],
    "extensionAbilities": [{
      "name": "InsightIntentExecutor",
      "type": "insightIntent",
      "srcEntry": "./ets/insightintent/InsightIntentExecutor.ets"
    }]
  }
}
```

### 7.2 实现意图执行器

```typescript
import { InsightIntentExecutor, insightIntent } from '@kit.IntentsKit';

export default class MyIntentExecutor extends InsightIntentExecutor {
  
  async onExecute(name: string, param: Record<string, Object>): Promise<insightIntent.ExecuteResult> {
    switch (name) {
      case 'queryOrder':
        return this.queryOrder(param);
      case 'createOrder':
        return this.createOrder(param);
      default:
        return { code: -1, result: { message: '未知意图' } };
    }
  }

  private async queryOrder(param: Record<string, Object>): Promise<insightIntent.ExecuteResult> {
    const orderId = param['orderId'] as string;
    const order = await OrderService.getOrder(orderId);
    
    return {
      code: 0,
      result: {
        orderId: order.id,
        status: order.status,
        amount: order.amount
      }
    };
  }
}
```

---

## 八、Data Augmentation Kit (数据增强)

### 8.1 本地知识库

```typescript
import { knowledgeBase } from '@kit.DataAugmentationKit';

// 创建知识库
async function createKnowledgeBase(): Promise<void> {
  const kb = await knowledgeBase.create({
    name: 'product_faq',
    description: '产品常见问题'
  });
  
  // 添加文档
  await kb.addDocuments([
    { content: '如何退款？答：在订单详情页点击申请退款...' },
    { content: '配送时间？答：一般1-3个工作日...' }
  ]);
}

// 检索知识
async function searchKnowledge(query: string): Promise<string[]> {
  const kb = await knowledgeBase.open('product_faq');
  
  const results = await kb.search({
    query: query,
    topK: 3
  });
  
  return results.map(r => r.content);
}
```

### 8.2 端侧 RAG

```typescript
import { ragEngine } from '@kit.DataAugmentationKit';

async function askWithRag(question: string): Promise<string> {
  const engine = await ragEngine.create({
    knowledgeBase: 'product_faq',
    model: 'local_llm'  // 使用端侧模型
  });
  
  const response = await engine.generate({
    query: question,
    context: await searchKnowledge(question)
  });
  
  return response.answer;
}
```

---

## AI Kit 选择决策树

```
用户需求
    │
    ├─ 识别类
    │   ├─ 文字识别 → Core Vision Kit (textRecognition)
    │   ├─ 人脸检测 → Core Vision Kit (faceDetector)
    │   ├─ 证件识别 → Vision Kit (cardRecognition)
    │   └─ 文档扫描 → Vision Kit (documentScanner)
    │
    ├─ 语音类
    │   ├─ 语音转文字 → Core Speech Kit (speechRecognizer)
    │   ├─ 文字转语音 → Core Speech Kit (textToSpeech)
    │   ├─ 文章朗读 → Speech Kit (ReadAloud 控件)
    │   └─ 视频字幕 → Speech Kit (AiCaption 控件)
    │
    ├─ 文本处理类
    │   ├─ 分词 → Natural Language Kit
    │   └─ 实体识别 → Natural Language Kit
    │
    ├─ 智能交互类
    │   ├─ AI 对话 → Agent Framework Kit
    │   └─ 智能推荐 → Intents Kit
    │
    └─ 知识问答类
        └─ 本地问答 → Data Augmentation Kit (RAG)
```

---

## 权限配置

| Kit | 所需权限 |
|-----|---------|
| Core Vision Kit | 无（端侧处理） |
| Core Speech Kit | `ohos.permission.MICROPHONE`（语音识别） |
| Vision Kit | `ohos.permission.CAMERA`（扫描） |
| Speech Kit | 无（端侧处理） |
| Natural Language Kit | 无（端侧处理） |
| Agent Framework Kit | `ohos.permission.INTERNET`（如需云端） |

```json5
// module.json5
{
  "module": {
    "requestPermissions": [
      {
        "name": "ohos.permission.MICROPHONE",
        "reason": "$string:microphone_reason",
        "usedScene": {
          "abilities": ["EntryAbility"],
          "when": "inuse"
        }
      }
    ]
  }
}
```
