#!/usr/bin/env python3
"""
HarmonyOS NEXT UI/UX Pro Max Skill - Search Script

Provides design intelligence search for HarmonyOS NEXT UI/UX development.
"""

import os
import sys
import json
import csv
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

# Get the script directory
SCRIPT_DIR = Path(__file__).parent
KNOWLEDGE_BASE_DIR = SCRIPT_DIR.parent.parent.parent / "knowledge_base"
SHARED_DIR = SCRIPT_DIR.parent


@dataclass
class SearchResult:
    """Search result item"""
    category: str
    title: str
    content: str
    relevance: float


class HarmonyDesignSearch:
    """HarmonyOS NEXT Design Intelligence Search"""
    
    def __init__(self):
        self.knowledge = self._load_knowledge()
    
    def _load_knowledge(self) -> Dict:
        """Load knowledge from CSV files"""
        knowledge = {
            "components": [],
            "layouts": [],
            "colors": [],
            "typography": [],
            "spacing": [],
            "animations": [],
            "page_templates": []
        }
        
        # Load from CSV files if they exist
        csv_files = {
            "components": KNOWLEDGE_BASE_DIR / "components.csv",
            "layouts": KNOWLEDGE_BASE_DIR / "layouts.csv",
            "colors": KNOWLEDGE_BASE_DIR / "colors.csv",
            "typography": KNOWLEDGE_BASE_DIR / "typography.csv",
            "spacing": KNOWLEDGE_BASE_DIR / "spacing.csv",
            "animations": KNOWLEDGE_BASE_DIR / "animations.csv",
            "page_templates": KNOWLEDGE_BASE_DIR / "page_templates.csv"
        }
        
        for key, filepath in csv_files.items():
            if filepath.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8-sig') as f:
                        reader = csv.DictReader(f)
                        knowledge[key] = list(reader)
                except Exception as e:
                    print(f"Warning: Failed to load {filepath}: {e}", file=sys.stderr)
        
        return knowledge
    
    def search(self, query: str, domain: str = "all") -> List[SearchResult]:
        """
        Search for design intelligence
        
        Args:
            query: Search query
            domain: Search domain (all, component, layout, style, animation)
        
        Returns:
            List of search results
        """
        results = []
        query_lower = query.lower()
        
        # Search components
        if domain in ["all", "component"]:
            for comp in self.knowledge["components"]:
                score = self._calculate_relevance(query_lower, comp.get("name", ""), comp.get("description", ""))
                if score > 0:
                    results.append(SearchResult(
                        category="component",
                        title=comp.get("name", ""),
                        content=f"{comp.get('description', '')}\n\nUsage:\n{comp.get('usage_example', '')}",
                        relevance=score
                    ))
        
        # Search layouts
        if domain in ["all", "layout"]:
            for layout in self.knowledge["layouts"]:
                score = self._calculate_relevance(query_lower, layout.get("name", ""), layout.get("description", ""))
                if score > 0:
                    results.append(SearchResult(
                        category="layout",
                        title=layout.get("name", ""),
                        content=f"{layout.get('description', '')}\n\nCode:\n{layout.get('code_example', '')}",
                        relevance=score
                    ))
        
        # Search colors
        if domain in ["all", "style", "color"]:
            for color in self.knowledge["colors"]:
                score = self._calculate_relevance(query_lower, color.get("name", ""), color.get("usage", ""))
                if score > 0:
                    results.append(SearchResult(
                        category="color",
                        title=f"{color.get('name', '')} ({color.get('value', '')})",
                        content=f"Usage: {color.get('usage', '')}\nLight: {color.get('light_mode', '')}\nDark: {color.get('dark_mode', '')}",
                        relevance=score
                    ))
        
        # Search typography
        if domain in ["all", "style", "typography"]:
            for typo in self.knowledge["typography"]:
                score = self._calculate_relevance(query_lower, typo.get("name", ""), typo.get("use_case", ""))
                if score > 0:
                    results.append(SearchResult(
                        category="typography",
                        title=typo.get("name", ""),
                        content=f"Font: {typo.get('font_family', '')}, Size: {typo.get('font_size', '')}, Weight: {typo.get('font_weight', '')}\nUse case: {typo.get('use_case', '')}",
                        relevance=score
                    ))
        
        # Search page templates
        if domain in ["all", "template", "page"]:
            for template in self.knowledge["page_templates"]:
                score = self._calculate_relevance(query_lower, template.get("name", ""), template.get("description", ""))
                if score > 0:
                    results.append(SearchResult(
                        category="page_template",
                        title=template.get("name", ""),
                        content=f"{template.get('description', '')}\n\nComponents: {template.get('components_used', '')}\n\nStructure:\n{template.get('layout_structure', '')}",
                        relevance=score
                    ))
        
        # Sort by relevance
        results.sort(key=lambda x: x.relevance, reverse=True)
        
        return results[:10]  # Return top 10 results
    
    def _calculate_relevance(self, query: str, title: str, content: str) -> float:
        """Calculate relevance score"""
        score = 0.0
        query_terms = query.split()
        
        for term in query_terms:
            if term in title.lower():
                score += 2.0
            if term in content.lower():
                score += 1.0
        
        return score
    
    def generate_design_system(self, query: str, project_name: str = "MyApp") -> str:
        """
        Generate a design system based on the query
        
        Args:
            query: Design requirements query
            project_name: Project name
        
        Returns:
            Design system in markdown format
        """
        output = []
        output.append(f"# {project_name} Design System")
        output.append(f"\n> Generated for: {query}\n")
        
        # Colors
        output.append("## Color Palette\n")
        output.append("| Token | Value | Usage |")
        output.append("|-------|-------|-------|")
        for color in self.knowledge["colors"][:8]:
            output.append(f"| `{color.get('name', '')}` | `{color.get('value', '')}` | {color.get('usage', '')} |")
        
        # Typography
        output.append("\n## Typography\n")
        output.append("| Style | Size | Weight | Use Case |")
        output.append("|-------|------|--------|----------|")
        for typo in self.knowledge["typography"][:6]:
            output.append(f"| `{typo.get('name', '')}` | {typo.get('font_size', '')} | {typo.get('font_weight', '')} | {typo.get('use_case', '')} |")
        
        # Spacing
        output.append("\n## Spacing\n")
        output.append("| Token | Value | Use Case |")
        output.append("|-------|-------|----------|")
        for space in self.knowledge["spacing"][:8]:
            output.append(f"| `{space.get('name', '')}` | {space.get('value', '')} | {space.get('use_case', '')} |")
        
        # Recommended Components
        output.append("\n## Recommended Components\n")
        search_results = self.search(query, domain="component")
        for result in search_results[:5]:
            output.append(f"### {result.title}\n")
            output.append(f"{result.content[:500]}\n")
        
        return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="HarmonyOS NEXT UI/UX Pro Max Skill - Design Intelligence Search"
    )
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--domain", "-d", default="all", 
                        choices=["all", "component", "layout", "style", "color", "typography", "template"],
                        help="Search domain")
    parser.add_argument("--design-system", action="store_true",
                        help="Generate a complete design system")
    parser.add_argument("-p", "--project", default="MyApp",
                        help="Project name for design system generation")
    parser.add_argument("-f", "--format", default="ascii",
                        choices=["ascii", "markdown", "json"],
                        help="Output format")
    parser.add_argument("--persist", action="store_true",
                        help="Save design system to file")
    
    args = parser.parse_args()
    
    if not args.query:
        parser.print_help()
        return
    
    searcher = HarmonyDesignSearch()
    
    if args.design_system:
        # Generate design system
        result = searcher.generate_design_system(args.query, args.project)
        
        if args.persist:
            output_dir = Path("design-system")
            output_dir.mkdir(exist_ok=True)
            output_file = output_dir / "MASTER.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"Design system saved to: {output_file}")
        else:
            print(result)
    else:
        # Regular search
        results = searcher.search(args.query, args.domain)
        
        if args.format == "json":
            print(json.dumps([{
                "category": r.category,
                "title": r.title,
                "content": r.content,
                "relevance": r.relevance
            } for r in results], ensure_ascii=False, indent=2))
        else:
            if not results:
                print("No results found.")
                return
            
            print(f"\n{'='*60}")
            print(f"Search Results for: {args.query}")
            print(f"{'='*60}\n")
            
            for i, result in enumerate(results, 1):
                print(f"[{i}] [{result.category.upper()}] {result.title}")
                print(f"    Relevance: {'★' * int(result.relevance)}")
                print(f"    {result.content[:200]}...")
                print()


if __name__ == "__main__":
    main()
