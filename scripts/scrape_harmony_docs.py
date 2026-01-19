"""
HarmonyOS NEXT UI/UX Pro Max Skill - 文档爬取脚本
从华为开发者文档和社区资源抓取 UI/UX 知识
"""

import os
import sys
import csv
import json
import time
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse

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
REQUEST_DELAY = 2

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# 知识来源 URL
KNOWLEDGE_SOURCES = {
    "arkui_components": [
        "https://developer.huawei.com/consumer/cn/doc/harmonyos-references-V5/4_2_u57fa-u7840-u7ec4-u4ef6-0000001884757586-V5",
        "https://developer.huawei.com/consumer/cn/doc/harmonyos-references-V5/4_3_u5bb9-u5668-u7ec4-u4ef6-0000001884917718-V5",
    ],
    "design_guidelines": [
        "https://developer.huawei.com/consumer/cn/design/",
    ]
}


@dataclass
class ScrapedKnowledge:
    """爬取的知识"""
    title: str
    category: str
    content: str
    code_example: str
    url: str
    scraped_at: str


class HarmonyDocsScraper:
    """华为开发者文档爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.knowledge_list: List[ScrapedKnowledge] = []
    
    def fetch_page(self, url: str) -> Optional[str]:
        """获取网页内容"""
        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            log_warning(f"获取页面失败 {url}: {e}")
            return None
    
    def scrape_segmentfault_articles(self):
        """从 SegmentFault 抓取 HarmonyOS 相关文章"""
        log_info("正在从 SegmentFault 抓取 HarmonyOS 文章...")
        
        search_urls = [
            "https://segmentfault.com/search?q=HarmonyOS+ArkUI+%E7%BB%84%E4%BB%B6",
            "https://segmentfault.com/search?q=HarmonyOS+NEXT+%E5%B8%83%E5%B1%80",
        ]
        
        for url in search_urls:
            html = self.fetch_page(url)
            if not html:
                continue
            
            soup = BeautifulSoup(html, 'lxml')
            
            # 查找文章列表
            articles = soup.find_all('div', class_='list-group-item')
            
            for article in articles[:5]:  # 只取前5篇
                title_elem = article.find('a', class_='title')
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href', '')
                    
                    if 'HarmonyOS' in title or 'ArkUI' in title:
                        self._scrape_article_content(title, link, 'SegmentFault')
            
            time.sleep(REQUEST_DELAY)
    
    def scrape_csdn_articles(self):
        """从 CSDN 抓取 HarmonyOS 相关文章"""
        log_info("正在从 CSDN 抓取 HarmonyOS 文章...")
        
        # CSDN HarmonyOS 专区
        search_url = "https://so.csdn.net/so/search?q=HarmonyOS%20NEXT%20ArkUI&t=blog"
        
        html = self.fetch_page(search_url)
        if not html:
            return
        
        soup = BeautifulSoup(html, 'lxml')
        
        # 查找搜索结果
        results = soup.find_all('div', class_='limit_width')
        
        for result in results[:5]:
            title_elem = result.find('a')
            if title_elem:
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')
                
                if link and ('HarmonyOS' in title or 'ArkUI' in title or '鸿蒙' in title):
                    self._scrape_article_content(title, link, 'CSDN')
        
        time.sleep(REQUEST_DELAY)
    
    def scrape_juejin_articles(self):
        """从掘金抓取 HarmonyOS 相关文章"""
        log_info("正在从掘金抓取 HarmonyOS 文章...")
        
        # 掘金 API 搜索
        api_url = "https://api.juejin.cn/search_api/v1/search"
        
        try:
            response = self.session.post(
                api_url,
                json={
                    "id_type": 0,
                    "key_word": "HarmonyOS ArkUI 组件",
                    "cursor": "0",
                    "limit": 10,
                    "search_type": 2,
                    "sort_type": 0
                },
                timeout=REQUEST_TIMEOUT
            )
            data = response.json()
            
            for item in data.get('data', [])[:5]:
                result_model = item.get('result_model', {})
                title = result_model.get('article_info', {}).get('title', '')
                article_id = result_model.get('article_info', {}).get('article_id', '')
                
                if article_id:
                    link = f"https://juejin.cn/post/{article_id}"
                    self._scrape_article_content(title, link, '掘金')
            
        except Exception as e:
            log_warning(f"掘金 API 请求失败: {e}")
        
        time.sleep(REQUEST_DELAY)
    
    def _scrape_article_content(self, title: str, url: str, source: str):
        """抓取文章内容并提取知识"""
        if not url.startswith('http'):
            return
        
        log_info(f"  抓取: {title[:40]}...")
        
        html = self.fetch_page(url)
        if not html:
            return
        
        soup = BeautifulSoup(html, 'lxml')
        
        # 提取文章正文
        content = ""
        code_examples = []
        
        # 不同网站的内容选择器
        content_selectors = [
            'article',
            '.article-content',
            '.markdown-body',
            '#article_content',
            '.post-content',
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                # 提取文本
                content = content_elem.get_text(separator='\n', strip=True)[:2000]
                
                # 提取代码块
                code_blocks = content_elem.find_all('code')
                for code in code_blocks[:3]:  # 最多取3个代码块
                    code_text = code.get_text(strip=True)
                    if len(code_text) > 50 and len(code_text) < 1000:
                        code_examples.append(code_text)
                break
        
        if content:
            # 确定分类
            category = self._determine_category(title, content)
            
            knowledge = ScrapedKnowledge(
                title=title,
                category=category,
                content=content[:1000],  # 限制内容长度
                code_example='\n---\n'.join(code_examples[:2]) if code_examples else '',
                url=url,
                scraped_at=time.strftime('%Y-%m-%d %H:%M:%S')
            )
            self.knowledge_list.append(knowledge)
            log_success(f"  已提取: {title[:30]}... [{category}]")
        
        time.sleep(REQUEST_DELAY)
    
    def _determine_category(self, title: str, content: str) -> str:
        """根据标题和内容确定分类"""
        text = (title + content).lower()
        
        if any(k in text for k in ['button', '按钮', 'text', '文本', 'image', '图片', 'input', '输入']):
            return 'component'
        elif any(k in text for k in ['row', 'column', 'flex', 'grid', '布局', 'layout']):
            return 'layout'
        elif any(k in text for k in ['color', '颜色', 'theme', '主题', '样式']):
            return 'style'
        elif any(k in text for k in ['animation', '动画', '动效', 'transition']):
            return 'animation'
        elif any(k in text for k in ['navigation', '导航', 'tab', 'router', '路由']):
            return 'navigation'
        elif any(k in text for k in ['form', '表单', 'checkbox', 'switch', '开关']):
            return 'form'
        else:
            return 'general'
    
    def scrape_github_awesome_list(self):
        """从 GitHub Awesome 列表抓取资源"""
        log_info("正在从 GitHub 抓取 Awesome HarmonyOS 资源...")
        
        # 搜索 GitHub 上的 HarmonyOS 相关仓库
        api_url = "https://api.github.com/search/repositories"
        params = {
            "q": "HarmonyOS ArkUI component",
            "sort": "stars",
            "order": "desc",
            "per_page": 10
        }
        
        try:
            response = self.session.get(api_url, params=params, timeout=REQUEST_TIMEOUT)
            data = response.json()
            
            for item in data.get('items', [])[:5]:
                name = item.get('name', '')
                description = item.get('description', '') or ''
                url = item.get('html_url', '')
                stars = item.get('stargazers_count', 0)
                
                if description:
                    knowledge = ScrapedKnowledge(
                        title=f"[GitHub] {name} (⭐{stars})",
                        category='resource',
                        content=description,
                        code_example='',
                        url=url,
                        scraped_at=time.strftime('%Y-%m-%d %H:%M:%S')
                    )
                    self.knowledge_list.append(knowledge)
                    log_success(f"  已添加: {name}")
            
        except Exception as e:
            log_warning(f"GitHub API 请求失败: {e}")
        
        time.sleep(REQUEST_DELAY)
    
    def export_to_csv(self, output_path: Path):
        """导出爬取的知识到 CSV"""
        if not self.knowledge_list:
            log_warning("没有爬取到任何知识")
            return
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            fields = ['title', 'category', 'content', 'code_example', 'url', 'scraped_at']
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            
            for item in self.knowledge_list:
                writer.writerow(asdict(item))
        
        log_success(f"已导出 {len(self.knowledge_list)} 条知识到: {output_path}")


def main():
    """主函数"""
    log_info("=" * 60)
    log_info("HarmonyOS NEXT UI/UX Pro Max Skill - 网络知识爬取")
    log_info("=" * 60)
    
    scraper = HarmonyDocsScraper()
    
    # 从各个来源抓取知识
    log_info("\n开始抓取网络资源...\n")
    
    # GitHub Awesome 列表
    scraper.scrape_github_awesome_list()
    
    # 技术社区文章 (可能因为网站限制而失败)
    try:
        scraper.scrape_juejin_articles()
    except Exception as e:
        log_warning(f"掘金抓取失败: {e}")
    
    # 导出到 CSV
    log_info("\n正在导出知识...")
    output_path = OUTPUT_DIR / "scraped_knowledge.csv"
    scraper.export_to_csv(output_path)
    
    # 打印统计
    log_info("\n" + "=" * 60)
    log_info(f"抓取完成! 共获取 {len(scraper.knowledge_list)} 条知识")
    log_info("=" * 60)


if __name__ == "__main__":
    main()
