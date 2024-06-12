# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProfileItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    about = scrapy.Field()
    country = scrapy.Field()
    current_institute = scrapy.Field()
    current_organization = scrapy.Field()
    no_of_connections = scrapy.Field()
    no_of_followers = scrapy.Field()
    education = scrapy.Field()
    project = scrapy.Field()
    experience = scrapy.Field()
    licenses_and_certifications = scrapy.Field()
    recommendations = scrapy.Field()
    honors_and_awards = scrapy.Field()
    languages = scrapy.Field()
    organizations = scrapy.Field()


class ProjectItem(scrapy.Item):
    name = scrapy.Field()
    description= scrapy.Field()
    other_creators = scrapy.Field()

class EducationItem(scrapy.Item):
    url = scrapy.Field()
    organization = scrapy.Field()
    education = scrapy.Field()
    field = scrapy.Field()
    grade = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()

class ExperienceItem(scrapy.Item):
    url = scrapy.Field()
    role = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    duration = scrapy.Field()
    country = scrapy.Field()
    description = scrapy.Field()

class LicensesAndCertificationItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    organization = scrapy.Field()
    organization_url = scrapy.Field()
    issue_date = scrapy.Field()
    credential_id = scrapy.Field()

class RecommendationItem(scrapy.Item):
    recommender = scrapy.Field()
    url = scrapy.Field()
    recommendation = scrapy.Field()

class HonorsAndAwardsItem(scrapy.Field):
    award = scrapy.Field()
    awarding_date = scrapy.Field()
    description = scrapy.Field()

class LanguagesItem(scrapy.Item):
    language = scrapy.Field()
    description = scrapy.Field()

class OrganizationsItem(scrapy.Item):
    organization = scrapy.Field()
    description = scrapy.Field()
