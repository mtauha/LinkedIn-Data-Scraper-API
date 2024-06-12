from typing import Iterable
import scrapy, re
from Scraper.items import (
    ProfileItem,
    EducationItem,
    ExperienceItem,
    LicensesAndCertificationItem,
    RecommendationItem,
    HonorsAndAwardsItem,
    LanguagesItem,
    OrganizationsItem,
    ProjectItem,
)


class Profile(scrapy.Spider):
    name = "profile_scraper"
    allowed_domains = ["linkedin.com,proxy.scrapeops.io"]
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
        education_item["url"] = edu.xpath(".//h3/a/@href").get()
        # Extract organization
        education_item["organization"] = edu.xpath(".//h3/a/text()").get()
        # Extract education
        education_item["education"] = edu.xpath(".//h4/span[1]/text()").get()
        # Extract field
        education_item["field"] = edu.xpath(".//h4/span[2]/text()").get()
        # Extract start date
        education_item["start_date"] = edu.xpath(".//div/p/span/time[1]/text()").get()
        # Extract end date
        education_item["end_date"] = edu.xpath(".//div/p/span/time[2]/text()").get()
        # Extract grade
        education_item["grade"] = edu.xpath(".//h4/span[3]/text()").get()
        return education_item

    def extract_experience_details(self, exp):
        experience_item = ExperienceItem()
        # Extract URL
        experience_item["url"] = exp.xpath(".//h4/a/@href").get()
        # Extract role
        experience_item["role"] = exp.xpath(".//h3/span/text()").get()
        # Extract start date
        experience_item["start_date"] = exp.xpath(".//div/p/span/time[1]/text()").get()
        # Extract end date
        if exp.xpath(
            '//*[@id="main-content"]/section[1]/div/section/section[4]/div/ul/li[1]/div/div/p[1]/span/time[2]/text()'
        ).get():
            experience_item["end_date"] = exp.xpath(
                ".//div/p[1]/span/time[2]/text()"
            ).get()
        else:
            experience_item["end_date"] = "Present"
        # Extract duration
        experience_item["duration"] = exp.xpath(".//div/p/span/span/text()").get()
        # Extract country
        experience_item["country"] = exp.xpath(".//p[2]/text()").get()
        # Extract description
        experience_item["description"] = exp.xpath(".//div/div/div/p/text()").get()
        return experience_item

    def extract_licenses_and_certifications_details(self, lic):
        def extract_credential_id(url):
            pattern = r'\/verify\/([A-Z0-9]+)\?'
            match = re.search(pattern, url)
            if match:
                return match.group(1)
            return None

        lic_item = LicensesAndCertificationItem()
        lic_item["url"] = (
            lic.xpath(".//div/a/@href").get().strip()
            if lic.xpath(".//div/a/@href").get()
            else "None"
        )
        lic_item["name"] = (
            lic.xpath(".//h3/a/text()").get().strip()
            if lic.xpath(".//h3/a/text()").get()
            else "None"
        )
        lic_item["organization"] = (
            lic.xpath(".//h4/a/text()").get().strip()
            if lic.xpath(".//h4/a/text()").get()
            else "None"
        )
        lic_item["organization_url"] = (
            lic.xpath("'.//a/@href'").get().strip()
            if lic.xpath("'.//a/@href'").get()
            else "None"
        )
        lic_item["issue_date"] = (
            lic.xpath(".//div/span[1]/time/text()").get().strip()
            if lic.xpath(".//div/span[1]/time/text()").get()
            else "None"
        )
        lic_item["credential_id"] = (
            extract_credential_id(lic_item["url"])
            if extract_credential_id(lic_item["url"])
            else "None"
        )

        return lic_item

    def extract_recommendations_details(self, rec):
        rec_item = RecommendationItem()
        rec_item["recommender"] = (
            rec.xpath(".//h3/text()").get().strip()
            if rec.xpath(".//h3/text()").get()
            else "None"
        )
        rec_item["url"] = (
            rec.xpath(".//a/@href").get().strip()
            if rec.xpath(".//a/@href").get()
            else "None"
        )
        rec_item["recommendation"] = (
            rec.xpath(".//p/text()").get().strip()
            if rec.xpath(".//p/text()").get()
            else "None"
        )
        return rec_item

    def extract_honors_and_awards_details(self, award):
        award_item = HonorsAndAwardsItem()
        award_item["award"] = (
            award.xpath(".//h3/text()").get().strip()
            if award.xpath(".//h3/text()").get()
            else "None"
        )
        award_item["awarding_date"] = (
            award.xpath(".//span/time/text()").get().strip()
            if award.xpath(".//span/time/text()").get()
            else "None"
        )
        award_item["description"] = (
            award.xpath(".//p/text()").get().strip()
            if award.xpath(".//p/text()").get()
            else "None"
        )
        return award_item

    def extract_languages_details(self, lang):
        lang_item = LanguagesItem()
        lang_item["language"] = (
            lang.xpath(".//h3/text()").get().strip()
            if lang.xpath(".//h3/text()").get()
            else "None"
        )
        lang_item["description"] = (
            lang.xpath(".//h4/text()").get().strip()
            if lang.xpath(".//h4/text()").get()
            else "None"
        )
        return lang_item

    def extract_organizations_details(self, org):
        org_item = OrganizationsItem()
        org_item["organization"] = (
            org.xpath(".//h3/text()").get().strip()
            if org.xpath(".//h3/text()").get()
            else "None"
        )
        org_item["description"] = (
            org.xpath(".//p/text()").get().strip()
            if org.xpath(".//p/text()").get()
            else "None"
        )
        return org_item

    def extract_project_details(self, proj):
        project_item = ProjectItem()
        project_item["name"] = (
            proj.xpath(".//h3/text()").get().strip()
            if proj.xpath(".//h3/text()").get()
            else "None"
        )
        description = proj.xpath('.//*[@class="show-more-less-text__text--more"]/text()') or proj.xpath('.//*[@class="show-more-less-text__text--less"]/text()')
        description = " ".join([text.get().strip() for text in description])
        project_item["description"] = description if description else "None"

        if proj.xpath(".//ul"):
            others = {}
            for other in range(1, len(proj.xpath(".//ul")) + 1):
                others[proj.xpath(f".//li[{other}]/a/@title").get().strip()] = (
                    proj.xpath(f".//li[{other}]/a/@href").get().strip()
                )

            project_item["other_creators"] = others
        else:
            project_item["other_creators"] = "None"

        return project_item

    def parse_profile(self, response):
        item = ProfileItem()

        # Summary Section:
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

        if "followers" in response.xpath(
            '//*[@id="main-content"]/section[1]/div/section/section[1]/div/div[2]/div[1]/h3/div/div[3]/span/text()'
        ):

            item["no_of_followers"] = int(
                response.xpath(
                    '//*[@id="main-content"]/section[1]/div/section/section[1]/div/div[2]/div[1]/h3/div/div[3]/span/text()'
                )
                .get()
                .strip()
                .removesuffix(" followers")
                .replace("K", "000")
            )

            item["no_of_connections"] = (
                response.xpath(
                    '//*[@id="main-content"]/section[1]/div/section/section[1]/div/div[2]/div[1]/h3/div/div[3]/span[2]/text()'
                )
                .get()
                .strip()
                .removesuffix(" connections")
            )
        else:
            item["no_of_connections"] = (
                response.xpath(
                    '//*[@id="main-content"]/section[1]/div/section/section[1]/div/div[2]/div[1]/h3/div/div[3]/span/text()'
                )
                .get()
                .strip()
                .removesuffix(" connections")
            )

        about_response = response.xpath('.//*[@data-section="summary"]')
        item["about"] = ""
        for i in range(1, len(about_response.xpath(".//p/text()")) + 1):
            item["about"] += about_response.xpath(f".//p/text()[{i}]").get()

        """------------------------------------------------------------------------------------"""

        """Education"""

        education = []
        education_response = response.xpath('.//*[@data-section="educationsDetails"]')
        if education_response:
            for edu in range(1, len(education_response.xpath(".//li")) + 1):
                education.append(
                    self.extract_education_details(
                        education_response.xpath(f".//li[{edu}]")
                    )
                )

            item["education"] = education
        else:
            item["education"] = "None"

        """------------------------------------------------------------------------------------"""

        """Experiences"""

        experience = []
        experience_response = response.xpath('.//*[@data-section="experience"]')
        if experience_response:
            for exp in range(1, len(experience_response.xpath(".//li")) + 1):
                experience.append(
                    self.extract_experience_details(
                        experience_response.xpath(f".//li[{exp}]")
                    )
                )
        else:
            experience = "None"

        item["experience"] = experience

        """------------------------------------------------------------------------------------"""

        """Honors and Awards"""

        honors = []
        honors_response = response.xpath('.//*[@data-section="honors-and-awards"]')
        if honors_response:
            for honor in range(1, len(honors_response.xpath(".//li")) + 1):
                honors.append(
                    self.extract_honors_and_awards_details(
                        honors_response.xpath(f".//li[{honor}]")
                    )
                )

            item["honors_and_awards"] = honors
        else:
            item["honors_and_awards"] = "None"

        """------------------------------------------------------------------------------------"""

        """Languages"""

        langs = []
        lang_response = response.xpath('.//*[@data-section="languages"]')
        if lang_response:
            for lang in range(1, len(lang_response.xpath(".//li")) + 1):
                langs.append(
                    self.extract_languages_details(
                        lang_response.xpath(f".//li[{lang}]")
                    )
                )

            item["languages"] = langs
        else:
            item["languages"] = "None"

        """------------------------------------------------------------------------------------"""

        """Organizations"""

        orgs = []
        orgs_response = response.xpath('.//*[@data-section="organizations"]')
        if orgs_response:
            for org in range(1, len(orgs_response.xpath(".//li")) + 1):
                orgs.append(
                    self.extract_organizations_details(
                        orgs_response.xpath(f".//li[{org}]")
                    )
                )

            item["organizations"] = orgs
        else:
            item["organizations"] = "None"

        """------------------------------------------------------------------------------------"""

        """Recommendations"""

        recomms = []
        recom_response = response.xpath('.//*[@data-section="recommendations"]')
        if recom_response:
            for recom in range(1, len(recom_response.xpath(".//li")) + 1):
                recomms.append(
                    self.extract_recommendations_details(
                        recom_response.xpath(f".//li[{recom}]")
                    )
                )

            item["recommendations"] = recomms
        else:
            item["recommendations"] = "None"

        """------------------------------------------------------------------------------------"""

        """Licenses and Certifications"""
        licenses = []
        lic_response = response.xpath(
            './/*[@data-section="certifications"]'
        )
        if lic_response:
            for lic in range(1, len(lic_response.xpath(".//li")) + 1):
                licenses.append(
                    self.extract_licenses_and_certifications_details(
                        lic_response.xpath(f"li[{lic}]")
                    )
                )

            item["licenses_and_certifications"] = licenses
        else:
            item["licenses_and_certifications"] = "None"

        """------------------------------------------------------------------------------------"""

        #! Start From Here
        """Projects"""
        projects = []
        proj_response = response.xpath('.//*[@data-section="projects"]')
        if proj_response:
            for project in range(1, len(proj_response.xpath(".//li")) + 1):
                projects.append(
                    self.extract_project_details(proj_response.xpath(f"li[{project}]"))
                )

        # TODO: Complete all the xpaths of
        # TODO: Licenses and Certifications
        # TODO: Projects
        yield item
