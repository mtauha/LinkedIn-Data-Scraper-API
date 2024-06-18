from fastapi import FastAPI, BackgroundTasks, Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ..Scraper.Scraper.spiders import profile_scraper

app = FastAPI()

# Configure Scrapy settings
settings = get_project_settings()
process = CrawlerProcess(settings)