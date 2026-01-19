// ==========================================
// HarmonyBaby Care - 数据模型定义
// ==========================================

/**
 * 喂养类型枚举
 */
export enum FeedingType {
  BREAST = 'breast',      // 母乳
  BOTTLE = 'bottle',      // 奶瓶
  BABY_FOOD = 'baby_food' // 辅食
}

/**
 * 母乳喂养侧边枚举
 */
export enum BreastSide {
  LEFT = 'left',
  RIGHT = 'right'
}

/**
 * 睡眠质量枚举
 */
export enum SleepQuality {
  STABLE = 'stable',      // 安稳
  NORMAL = 'normal',      // 正常
  RESTLESS = 'restless'   // 易醒
}

/**
 * 尿布状态枚举
 */
export enum DiaperStatus {
  WET = 'wet',       // 尿湿
  DIRTY = 'dirty',   // 便便
  BOTH = 'both',     // 混合
  DRY = 'dry'        // 干爽
}

/**
 * 便便颜色枚举
 */
export enum PoopColor {
  YELLOW = 'yellow',
  GREEN = 'green',
  BROWN = 'brown',
  BLACK = 'black',
  RED = 'red'
}

/**
 * 家庭成员角色
 */
export enum FamilyRole {
  PARENT = 'parent',
  GRANDPARENT = 'grandparent'
}

/**
 * 权限级别
 */
export enum Permission {
  FULL = 'full',
  READONLY = 'readonly'
}

// ==========================================
// 数据接口定义
// ==========================================

/**
 * 宝宝信息
 */
export interface BabyInfo {
  id: string
  name: string
  birthday: string  // ISO 日期格式
  gender: 'boy' | 'girl'
  avatarUrl: string
}

/**
 * 喂养记录
 */
export interface FeedingRecord {
  id: string
  babyId: string
  type: FeedingType
  timestamp: number
  duration: number      // 秒数（母乳）
  side: BreastSide | null  // 母乳侧边
  amount: number | null    // ml（奶瓶/辅食）
  brand: string | null     // 品牌
  temperature: number | null  // 水温
  ingredients: string[]    // 辅食食材
  allergyMark: boolean     // 过敏标记
  note: string
}

/**
 * 睡眠记录
 */
export interface SleepRecord {
  id: string
  babyId: string
  startTime: number
  endTime: number | null
  nightWakings: number[]  // 夜醒时间戳列表
  quality: SleepQuality
  roomTemp: number | null
  humidity: number | null
  note: string
}

/**
 * 尿布记录
 */
export interface DiaperRecord {
  id: string
  babyId: string
  timestamp: number
  status: DiaperStatus
  poopColor: PoopColor | null
  poopTexture: string | null
  note: string
}

/**
 * 健康记录
 */
export interface HealthRecord {
  id: string
  babyId: string
  timestamp: number
  temperature: number | null
  medicine: string | null
  dosage: string | null
  note: string
}

/**
 * 生长记录
 */
export interface GrowthRecord {
  id: string
  babyId: string
  timestamp: number
  height: number | null   // cm
  weight: number | null   // kg
  headCircumference: number | null  // cm
}

/**
 * 里程碑记录
 */
export interface MilestoneRecord {
  id: string
  babyId: string
  timestamp: number
  milestone: string
  photoUrl: string | null
  note: string
}

/**
 * 今日统计数据
 */
export interface TodayStats {
  feedingCount: number
  feedingTotalMl: number
  sleepTotalMinutes: number
  diaperCount: number
  lastTemperature: number | null
  nextFeedingEstimate: number | null
  nextSleepEstimate: number | null
}

/**
 * 快速记录项
 */
export interface QuickRecordItem {
  id: string
  icon: Resource
  label: Resource
  color: Resource
  bgColor: Resource
}

/**
 * 计时器状态
 */
export interface TimerState {
  isRunning: boolean
  isPaused: boolean
  startTime: number
  pausedTime: number
  totalPausedDuration: number
  currentSide: BreastSide
}

/**
 * 家庭成员
 */
export interface FamilyMember {
  id: string
  name: string
  avatarUrl: string
  role: FamilyRole
  permission: Permission
  lastActive: number
}

/**
 * 用药提醒
 */
export interface MedicineReminder {
  id: string
  babyId: string
  medicineName: string
  dosage: string
  frequency: string       // 如 "每日1次"
  nextReminderTime: number
  isActive: boolean
}
