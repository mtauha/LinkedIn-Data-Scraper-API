from typing import Iterable
import scrapy
from Scraper.items import ProfileItem
from Scraper.items import EducationItem
from Scraper.items import ExperienceItem
from Scraper.items import LicensesAndCertificationItem


class Job(scrapy.Spider):
    name = "profile_scraper"
    allowed_domains = ["linkedin.com"]
    start_urls = ["https://www.linkedin.com/jobs/"]
    job_list = [""]

    def start_requests(self):
        for job in self.job_list:
            job_url = self.start_urls[0] + f"{job}/"
            yield scrapy.Request(
                url=job_url,
                callback=self.parse_job,
                meta={"job": job, "url": job_url},
            )
    
    def parse_job(self, response):
        pass
