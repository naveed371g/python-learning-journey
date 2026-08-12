import time
import random
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]


def _build_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(f"--user-agent={random.choice(USER_AGENTS)}")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=en-US")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


def _random_delay(min_s=1.5, max_s=3.5):
    time.sleep(random.uniform(min_s, max_s))


def scrape_indeed(query: str, max_results: int = 15) -> list[dict]:
    """Scrape Indeed for Bay Area jobs matching query."""
    jobs = []
    encoded_query = query.replace(" ", "+")
    url = (
        f"https://www.indeed.com/jobs?q={encoded_query}"
        f"&l=San+Francisco+Bay+Area%2C+CA&radius=25&sort=date"
    )
    driver = None
    try:
        driver = _build_driver()
        logger.info(f"Scraping Indeed: {url}")
        driver.get(url)
        _random_delay(2, 4)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-jk]"))
            )
        except Exception:
            logger.warning("Indeed: job cards not found within timeout")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.find_all("div", attrs={"data-jk": True})
        if not cards:
            cards = soup.find_all(
                "li", class_=lambda c: c and "job_seen_beacon" in c)

        for card in cards[:max_results]:
            try:
                title_el = card.find(
                    "h2", class_=lambda c: c and "jobTitle" in c)
                title = title_el.get_text(strip=True) if title_el else "N/A"

                company_el = card.find("span", {"data-testid": "company-name"}) or \
                    card.find("span", class_=lambda c: c and "companyName" in c)
                company = company_el.get_text(
                    strip=True) if company_el else "N/A"

                location_el = card.find("div", {"data-testid": "text-location"}) or \
                    card.find(
                        "div", class_=lambda c: c and "companyLocation" in c)
                location = location_el.get_text(
                    strip=True) if location_el else "Bay Area, CA"

                salary_el = card.find("div", class_=lambda c: c and "salary" in (c or "").lower()) or \
                    card.find("span", class_=lambda c: c and "salary" in (
                        c or "").lower())
                salary = salary_el.get_text(strip=True) if salary_el else ""

                snippet_el = card.find("div", class_=lambda c: c and "job-snippet" in (c or "")) or \
                    card.find("div", attrs={
                              "data-testid": "jobsnippet_footer"})
                snippet = snippet_el.get_text(strip=True) if snippet_el else ""

                jk = card.get("data-jk", "")
                job_url = f"https://www.indeed.com/viewjob?jk={jk}" if jk else "https://www.indeed.com"

                date_el = card.find(
                    "span", class_=lambda c: c and "date" in (c or "").lower())
                date_posted = date_el.get_text(strip=True) if date_el else ""

                if title != "N/A":
                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "salary": salary,
                        "snippet": snippet,
                        "url": job_url,
                        "date_posted": date_posted,
                        "source": "Indeed",
                    })
            except Exception as e:
                logger.debug(f"Indeed card parse error: {e}")
                continue

    except Exception as e:
        logger.error(f"Indeed scrape failed: {e}")
    finally:
        if driver:
            driver.quit()

    logger.info(f"Indeed returned {len(jobs)} jobs")
    return jobs


def scrape_linkedin(query: str, max_results: int = 15) -> list[dict]:
    """Scrape LinkedIn public jobs page for Bay Area jobs."""
    jobs = []
    encoded_query = query.replace(" ", "%20")
    url = (
        f"https://www.linkedin.com/jobs/search/"
        f"?keywords={encoded_query}&location=San+Francisco+Bay+Area"
        f"&f_TPR=r604800&sortBy=DD"
    )
    driver = None
    try:
        driver = _build_driver()
        logger.info(f"Scraping LinkedIn: {url}")
        driver.get(url)
        _random_delay(3, 5)

        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 600);")
            _random_delay(1, 2)

        try:
            WebDriverWait(driver, 12).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".jobs-search__results-list li, .base-card")
                )
            )
        except Exception:
            logger.warning("LinkedIn: job cards not found within timeout")

        soup = BeautifulSoup(driver.page_source, "html.parser")

        cards = soup.select(".jobs-search__results-list li") or \
            soup.select("ul.jobs-search__results-list > li") or \
            soup.select(".base-card--link")

        for card in cards[:max_results]:
            try:
                title_el = card.find("h3", class_=lambda c: c and "base-search-card__title" in (c or "")) or \
                    card.find(
                        "span", class_=lambda c: c and "sr-only" in (c or ""))
                title = title_el.get_text(strip=True) if title_el else "N/A"

                company_el = card.find("h4", class_=lambda c: c and "base-search-card__subtitle" in (c or "")) or \
                    card.find(
                        "a", class_=lambda c: c and "hidden-nested-link" in (c or ""))
                company = company_el.get_text(
                    strip=True) if company_el else "N/A"

                location_el = card.find(
                    "span", class_=lambda c: c and "job-search-card__location" in (c or ""))
                location = location_el.get_text(
                    strip=True) if location_el else "Bay Area, CA"

                link_el = card.find("a", class_=lambda c: c and "base-card__full-link" in (c or "")) or \
                    card.find("a", href=True)
                job_url = link_el["href"] if link_el and link_el.get(
                    "href") else "https://www.linkedin.com/jobs"

                date_el = card.find("time")
                date_posted = date_el.get_text(strip=True) if date_el else ""

                listed_el = card.find(
                    "span", class_=lambda c: c and "job-search-card__listdate" in (c or ""))
                if listed_el:
                    date_posted = listed_el.get_text(strip=True)

                if title != "N/A":
                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "salary": "",
                        "snippet": "",
                        "url": job_url,
                        "date_posted": date_posted,
                        "source": "LinkedIn",
                    })
            except Exception as e:
                logger.debug(f"LinkedIn card parse error: {e}")
                continue

    except Exception as e:
        logger.error(f"LinkedIn scrape failed: {e}")
    finally:
        if driver:
            driver.quit()

    logger.info(f"LinkedIn returned {len(jobs)} jobs")
    return jobs


def scrape_jobs(query: str, max_per_source: int = 15, source_filter: str = "both") -> list[dict]:
    """Scrape Indeed + LinkedIn (or just one), merge, deduplicate, return combined list."""
    indeed_jobs = []
    if source_filter in ("both", "indeed"):
        indeed_jobs = scrape_indeed(query, max_per_source)

    linkedin_jobs = []
    if source_filter in ("both", "linkedin"):
        try:
            linkedin_jobs = scrape_linkedin(query, max_per_source)
        except Exception as e:
            logger.warning(
                f"LinkedIn scrape skipped (will use Indeed only): {e}")

    combined = indeed_jobs + linkedin_jobs
    seen = set()
    unique = []
    for job in combined:
        key = (job["title"].lower()[:40], job["company"].lower()[:30])
        if key not in seen:
            seen.add(key)
            unique.append(job)

    return unique
