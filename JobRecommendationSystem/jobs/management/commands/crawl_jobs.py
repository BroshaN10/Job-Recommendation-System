# jobs/management/commands/crawler.py
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from jobs.models import Job

class Command(BaseCommand):
    help = 'Crawl LinkedIn jobs'

    def handle(self, *args, **options):
        url = 'https://www.linkedin.com/jobs/search/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        job_listings = soup.find_all('li', class_='result-card')

        for job in job_listings:
            title = job.find('h3', class_='result-card__title').text.strip()
            company = job.find('h4', class_='result-card__subtitle').text.strip()
            location = job.find('span', class_='job-result-card__location').text.strip()
            description = job.find('p', class_='job-result-card__snippet').text.strip() if job.find('p', class_='job-result-card__snippet') else ''

            Job.objects.create(title=title, company=company, location=location, description=description)

            self.stdout.write(self.style.SUCCESS(f'Saved job: {title}'))

        self.stdout.write(self.style.SUCCESS('Job crawling completed'))