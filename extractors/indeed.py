from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class Indeed:
    def __init__(self):
        self.base_url = "https://kr.indeed.com/jobs"
        self.browser = self.__chrome_browser()

    def __chrome_browser(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        return browser

    def get_page_count(self, keyword):
        self.browser.get(f"{self.base_url}?q={keyword}")
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        pagination = soup.find("nav", attrs={"aria-label": "pagination"})

        if pagination is None:
            return 0
        else:
            pages = pagination.find_all("div", recursive=False)
            count = len(pages)

        return 5 if count >= 5 else count

    def extract_indeed_jobs(self, keyword):
        pages = self.get_page_count(keyword)
        results = []

        for page in range(pages):
            url = f"{self.base_url}?q={keyword}&start={page * 10}"
            self.browser.get(url)

            soup = BeautifulSoup(self.browser.page_source, "html.parser")
            job_list = soup.find("ul", class_="jobsearch-ResultsList")
            jobs = job_list.find_all('li', recursive=False)

            for job in jobs:
                zone = job.find("div", class_="mosaic-zone")
                if zone is None:
                    anchor = job.select_one("h2 a")
                    title = anchor['aria-label']
                    link = anchor['href']
                    name = job.find("span", class_="companyName")
                    location = job.find("div", class_="companyLocation")
                    job_data = {
                        "link": f"https://kr.indeed.com{link}",
                        "company": name.string,
                        "location": location.string,
                        "position": title
                    }
                    results.append(job_data)

        return results
