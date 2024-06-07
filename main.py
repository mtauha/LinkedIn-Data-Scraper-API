from fastapi import FastAPI
from pydantic import BaseModel
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from Scraper.Scraper.spiders import spider

app = FastAPI()


class ScrapyRequest(BaseModel):
    url: str


process = CrawlerProcess(get_project_settings())

# New intro endpoint
@app.get("/")
def intro():
    return {"message": "Hello!"}

@app.post("/profile")
def scrape_profile(request: ScrapyRequest):
    process.crawl(spider.Profile)

