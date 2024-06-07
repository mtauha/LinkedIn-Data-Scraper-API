from typing import Iterable
import scrapy
from Scraper.items import ProfileItem
from Scraper.items import EducationItem
from Scraper.items import ExperienceItem
from Scraper.items import LicensesAndCertificationItem


class Profile(scrapy.Spider):
    name = "profile_scraper"
    allowed_domains = ["linkedin.com"]
    start_urls = ["https://www.linkedin.com/in/"]
    profile_list = ["muhammad-tauha-"]

    def start_requests(self):
        for profile in self.profile_list:
            profile_url = self.start_urls[0] + f"{profile}/"
            yield scrapy.Request(
                url=profile_url,
                callback=self.parse_profile,
                meta={"profile": profile, "url": profile_url},
            )

    def extract_education_details(self, edu):
        education_item = EducationItem()

        # Extract URL
        url = edu.xpath(
            '//*[@id="main-content"]/section[1]/div/section/section[5]/div/ul/li[1]/div/h3/a/@href'
        ).get()
        education_item["url"] = url.strip() if url else None

        # Extract organization
        organization = edu.xpath(
            '//*[@id="main-content"]/section[1]/div/section/section[5]/div/ul/li[1]/div/h3/a/text()'
        ).get()
        education_item["organization"] = organization.strip() if organization else None

        # Extract education
        education = edu.xpath(
            '//*[@id="main-content"]/section[1]/div/section/section[5]/div/ul/li[1]/div/h4/span[1]/text()'
        ).get()
        education_item["education"] = education.strip() if education else None

        # Extract field
        field = edu.xpath(
            '//*[@id="main-content"]/section[1]/div/section/section[5]/div/ul/li[1]/div/h4/span[2]/text()'
        ).get()
        education_item["field"] = field.strip() if field else None

        # Extract start date
        start_date = edu.xpath(
            '//*[@id="main-content"]/section[1]/div/section/section[5]/div/ul/li[1]/div/div/p/span/time[1]/text()'
        ).get()
        education_item["start_date"] = start_date.strip() if start_date else None

        # Extract end date
        end_date = edu.xpath(
            '//*[@id="main-content"]/section[1]/div/section/section[5]/div/ul/li[1]/div/div/p/span/time[2]/text()'
        ).get()
        education_item["end_date"] = end_date.strip() if end_date else None

        # Extract grade
        grade = edu.xpath(
            '//*[@id="main-content"]/section[1]/div/section/section[5]/div/ul/li[2]/div/h4/span[3]/text()'
        ).get()
        education_item["grade"] = grade.strip() if grade else None

        return education_item

    def parse_profile(self, response):
        item = ProfileItem()
        item["profile"] = response.meta["profile"]
        item["url"] = response.meta["url"]

        # * Summary Section:

        summary_box = response.css("section.top-card-layout")
        item["name"] = summary_box.css("h1::text").get().strip()
        item["description"] = summary_box.css("h2::text").get().strip()
        item["country"] = (
            summary_box.xpath(
                '//*[@id="main-content"]/section[1]/div/section/section[1]/div/div[2]/div[1]/h3/div/div[1]/span[1]/text()'
            )
            .get()
            .strip()
        )

        if summary_box.xpath(
                '//*[@id="main-content"]/section[1]/div/section/section[1]/div/div[2]/div[3]/div/div[2]/a/span/text()'
            ):
            item["current_institute"] = (
                summary_box.xpath(
                    '//*[@id="main-content"]/section[1]/div/section/section[1]/div/div[2]/div[2]/div/div[2]/a/span/text()'
                )
                .get()
                .strip()
            )

            item["current_organization"] = (
                summary_box.xpath(
                    '//*[@id="main-content"]/section[1]/div/section/section[1]/div/div[2]/div[2]/div/div[1]/a/span/text()'
                )
                .get()
                .strip()
            )
        else:
            item["current_institute"] = (
                summary_box.xpath(
                    '//*[@id="main-content"]/section[1]/div/section/section[1]/div/div[2]/div[2]/div/div[1]/a/span/text()'
                )
                .get()
                .strip()
            )

        item["no_of_connections"] = (
            response.xpath(
                '//*[@id="main-content"]/section[1]/div/section/section[1]/div/div[2]/div[1]/h3/div/div[3]/span/text()'
            )
            .get()
            .strip()
        )

        """Education Section Parser"""
        education = []
        education_response = response.xpath(
            '//*[@id="main-content"]/section[1]/div/section/section[5]'
        ).get()

        if education_response:
            for edu in education_response.strip():
                education.append(self.extract_education_details(edu))

        item['education'] = education if education is not None else None

        #! Start From Here

        yield item

# * Jobs Scraper


class Jobs(scrapy.Spider):
    pass
