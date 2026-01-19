"""
HarmonyOS NEXT UI/UX Pro Max Skill - 脚本配置
资源抓取脚本的配置参数
"""

import os
from pathlib import Path

# ============== 路径配置 ==============
# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 输出目录
OUTPUT_DIR = PROJECT_ROOT / "resources"
FIGMA_OUTPUT_DIR = OUTPUT_DIR / "figma"
GITHUB_OUTPUT_DIR = OUTPUT_DIR / "github"
COMPONENTS_OUTPUT_DIR = OUTPUT_DIR / "components"
DOCS_OUTPUT_DIR = OUTPUT_DIR / "docs"

# ============== Figma 配置 ==============
# Figma API Token (从环境变量读取)
FIGMA_TOKEN = os.getenv("FIGMA_TOKEN", "")

# HarmonyOS NEXT Design Library 相关链接
FIGMA_RESOURCES = {
    "harmony_design_library": {
        "name": "HarmonyOS NEXT Design Library",
        "url": "https://www.figma.com/community/file/xxx",  # 需要替换为实际链接
        "description": "社区版 HarmonyOS NEXT 设计库"
    }
}

# ============== GitHub/Gitee 配置 ==============
# 需要抓取的仓库列表
GITHUB_REPOS = [
    {
        "name": "openharmony-app-samples",
        "url": "https://github.com/openharmony/app_samples",
        "branch": "master",
        "description": "OpenHarmony 官方示例应用"
    },
    {
        "name": "agc-template-market",
        "url": "https://github.com/AppGalleryConnect/agc-template-market-harmonyos-demos",
        "branch": "main",
        "description": "华为 AGC 模板市场示例"
    }
]

GITEE_REPOS = [
    {
        "name": "ArkUI_Component",
        "url": "https://gitee.com/example/ArkUI_Component",  # 需要替换为实际链接
        "branch": "master",
        "description": "ArkUI 组件示例"
    }
]

# ============== NPM/OHPM 包配置 ==============
NPM_PACKAGES = [
    {
        "name": "@ibestservices/ibest-ui",
        "registry": "https://registry.npmjs.org",
        "description": "IBest-UI 组件库"
    }
]

# ============== 官方文档配置 ==============
OFFICIAL_DOCS = {
    "arkui_guide": {
        "url": "https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkui-overview-0000001774279970",
        "description": "ArkUI 开发指南"
    },
    "design_guidelines": {
        "url": "https://developer.huawei.com/consumer/cn/design/",
        "description": "HarmonyOS 设计规范"
    }
}

# ============== 抓取配置 ==============
# 请求超时时间 (秒)
REQUEST_TIMEOUT = 30

# 重试次数
MAX_RETRIES = 3

# 请求间隔 (秒) - 避免过于频繁的请求
REQUEST_DELAY = 1

# User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# 请求头
DEFAULT_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# ============== 文件类型过滤 ==============
# 需要提取的源码文件类型
SOURCE_FILE_EXTENSIONS = [
    ".ets",
    ".ts",
    ".js",
    ".json",
    ".json5",
]

# 需要提取的资源文件类型
RESOURCE_FILE_EXTENSIONS = [
    ".svg",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
]

# 需要忽略的目录
IGNORE_DIRS = [
    "node_modules",
    ".git",
    ".idea",
    "build",
    "dist",
    "__pycache__",
]
