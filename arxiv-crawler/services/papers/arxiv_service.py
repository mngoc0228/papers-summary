import asyncio
import re

import requests
from bs4 import BeautifulSoup



class ArxivService:
    def __init__(self):
        self.arxiv_uri = "http://export.arxiv.org/api/query"
        self.taxonomy_uri = "https://arxiv.org/category_taxonomy"

    async def fetch_categories(self):
        response = await asyncio.to_thread(requests.get, self.taxonomy_uri)
        response.raise_for_status()

        taxonomy: dict[str, str] = {}
        for category_code, category_name in re.findall(
            r"<h4>\s*([A-Za-z0-9\.-]+)\s*<span>\(([^)]+)\)</span>\s*</h4>",
            response.text,
            flags=re.S,
        ):
            taxonomy[category_code.strip()] = category_name.strip()

        categories_mapping = [
            {
                "code": code,
                "name": name,
            }
            for code, name in taxonomy.items()
        ]

        return categories_mapping
    
    async def fetch_papers(self, category: str, max_results: int = 10):
        params = {
            "search_query": f"cat:{category}",
            "start": 0,
            "max_results": max_results,
        }
        response = await asyncio.to_thread(requests.get, self.arxiv_uri, params=params)
        response.raise_for_status()

        # using beautifulsoup4 to parse the Atom feed response
        soup = BeautifulSoup(response.text, "html.parser")
        
        papers = []
        for entry in soup.find_all("entry"):
            title = entry.find("title")
            title_text = title.text.strip() if title else ""
            
            summary = entry.find("summary")
            summary_text = summary.text.strip() if summary else ""
            
            published = entry.find("published")
            published_text = published.text.strip() if published else ""
            
            arxiv_id = ""
            id_tag = entry.find("id")
            if id_tag:
                id_text = id_tag.text.strip()
                match = re.search(r"(\d+\.\d+)$", id_text)
                if match:
                    arxiv_id = match.group(1)
            
            authors = []
            for author in entry.find_all("author"):
                name = author.find("name")
                if name:
                    authors.append(name.text.strip())
            
            pdf_url = ""
            for link in entry.find_all("link"):
                if link.get("title") == "pdf":
                    pdf_url = link.get("href", "")
                    break

            primary_category = ""
            primary_cat = entry.find("arxiv:primary_category")
            if primary_cat:
                primary_category = primary_cat.get("term", "")
            
            categories = []
            for cat in entry.find_all("category"):
                cat_term = cat.get("term")
                if cat_term:
                    categories.append(cat_term)
            
            papers.append({
                "arxiv_id": arxiv_id,
                "title": title_text,
                "summary": summary_text,
                "authors": authors,
                "published": published_text,
                "primary_category": primary_category,
                "categories": categories,
                "pdf_url": pdf_url,
            })
        
        return papers

