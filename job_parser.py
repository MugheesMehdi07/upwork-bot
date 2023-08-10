import os
from dotenv import load_dotenv
import sqlite3
from discordwebhook import Discord
import feedparser
from datetime import datetime
import time
import logging

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
webhook_url = os.getenv('WEBHOOK_URL')
webhook_url_test = os.getenv('WEBHOOK_URL_TEST')
rss_url = os.getenv('RSS_URL')
db_path = os.getenv('DB_PATH')

add_keywords = ['']
exclude_keywords = ['shopify', 'wordpress', 'woocommerce', 'unreal', 'wix', 'webflow', 'cms', 'ui/ux',
                    'clickup', 'react native', 'laravel', 'salesforce', 'Ruby on Rails', 'ROR',
                    'ecommerce', 'crm', 'bigcommerce', 'nopcommerce', 'ux/ui', 'bubble.io', 'test', 'tester',
                    'testing', 'sqaurespace', 'Sharepoint', 'Perl', 'Squarespace', 'Data Entry', 'Typing',
                    'Word press', 'Php', 'Vba', 'Airtable', '[$500]']

TEST = False

if TEST:
    webhook_url = webhook_url_test

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Discord
discord = Discord(url=webhook_url)

# Database Operations
def db_setup():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs (link TEXT PRIMARY KEY, posted_on DATETIME)''')
    conn.commit()
    conn.close()
    logging.info("Database setup completed.")

def insert_job(link, posted_on):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO jobs (link, posted_on) VALUES (?, ?)", (link, posted_on))
        conn.commit()
    except sqlite3.IntegrityError:
        logging.info("Job already exists in the database.")
    finally:
        conn.close()

def is_job_new(link):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT link FROM jobs WHERE link = ?", (link,))
    result = c.fetchone()
    conn.close()
    return result is None

def cleanup_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM jobs WHERE link IN (SELECT link FROM jobs ORDER BY posted_on DESC LIMIT -1 OFFSET 100)")
    conn.commit()
    conn.close()
    logging.info("Database cleanup completed.")

# Job Fetching and Processing
def fetch_and_broadcast_jobs():
    logging.info('Fetching Jobs...')
    rss = feedparser.parse(rss_url)
    for entry in rss.entries:
        title = entry.title
        link = entry.link
        posted_on = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z').isoformat()

        if not any(exclude_word.lower() in title.lower() for exclude_word in exclude_keywords) and is_job_new(link):
            insert_job(link, posted_on)  # Insert job into DB
            job_data = {"Job Title": title, "Job Link": link, "Job Posted": posted_on}
            broadcast_to_discord(job_data)
            time.sleep(5)  # Delay of 5 seconds between posts

def broadcast_to_discord(job_dict):
    final_str = f"Job Title: {job_dict['Job Title']}\nJob Link: {job_dict['Job Link']}\nJob Posted: {job_dict['Job Posted']}"
    discord.post(content=final_str)
    logging.info(f"Job posted to Discord: {job_dict['Job Title']}")

# Main Logic
def main():
    db_setup()  # Setup database
    fetch_and_broadcast_jobs()
    cleanup_db()  # Cleanup database to maintain 100 rows

if __name__ == "__main__":
    main()
