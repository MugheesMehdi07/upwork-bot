

# Job Fetcher and Broadcaster

This script fetches job listings from an RSS feed, filters them based on specified keywords, and posts new jobs to a Discord channel using a webhook.

## Prerequisites

Before running the script, ensure you have the following:

- Python 3.x installed on your system
- The `python-dotenv` library installed
- The `discordwebhook` library installed
- The `feedparser` library installed

You can install the required Python libraries using pip:

```sh
pip install python-dotenv discordwebhook feedparser
```

## Setup

1. **Clone the repository** (or copy the script files) to your local machine.

2. **Create a `.env` file** in the root directory of the project. This file will store your sensitive data.

3. **Add your sensitive data** to the `.env` file. Your `.env` file should look like this:

    ```plaintext
    WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_id/your_webhook_token
    WEBHOOK_URL_TEST=https://discord.com/api/webhooks/your_test_webhook_id/your_test_webhook_token
    RSS_URL=https://www.upwork.com/ab/feed/jobs/rss?your_rss_feed_parameters
    DB_PATH=jobs.db
    ```

    - Replace `your_webhook_id` and `your_webhook_token` with your actual Discord webhook ID and token.
    - Replace `your_test_webhook_id` and `your_test_webhook_token` with your actual test Discord webhook ID and token.
    - Replace `your_rss_feed_parameters` with your actual RSS feed parameters.

4. **Run the script** using Python:

    ```sh
    python your_script_name.py
    ```

## Getting Your Keys

### Discord Webhook URL

1. Go to your Discord server and create a new webhook in one of your channels. 
2. Copy the webhook URL. It should look something like this: `https://discord.com/api/webhooks/your_webhook_id/your_webhook_token`
3. Replace the placeholder values in the `.env` file with this URL.

### RSS Feed URL

1. Obtain your RSS feed URL from the service you are using (e.g., Upwork).
2. Ensure you have the correct parameters for your feed.
3. Replace the placeholder values in the `.env` file with this URL.

## Configuration

### Exclude Keywords

The script uses a list of keywords to filter out unwanted jobs. You can modify the `exclude_keywords` list in the script to suit your needs:

```python
exclude_keywords = ['shopify', 'wordpress', 'woocommerce', 'unreal', 'wix', 'webflow', 'cms', 'ui/ux',
                    'clickup', 'react native', 'laravel', 'salesforce', 'Ruby on Rails', 'ROR',
                    'ecommerce', 'crm', 'bigcommerce', 'nopcommerce', 'ux/ui', 'bubble.io', 'test', 'tester',
                    'testing', 'sqaurespace', 'Sharepoint', 'Perl', 'Squarespace', 'Data Entry', 'Typing',
                    'Word press', 'Php', 'Vba', 'Airtable', '[$500]']
```

You can add or remove keywords as needed.

## Logging

The script uses logging to provide information about its operations. Logs are printed to the console and include timestamps, log levels, and messages.

## Database

The script uses a SQLite database to store job links and their posting dates. The database file is specified in the `.env` file (`DB_PATH`). The script maintains a database of the last 100 jobs to avoid posting duplicate jobs.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [discordwebhook](https://pypi.org/project/discordwebhook/)
- [feedparser](https://pypi.org/project/feedparser/)
