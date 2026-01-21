BOT_NAME = "agents"

SPIDER_MODULES = ["agents.spiders"]
NEWSPIDER_MODULE = "agents.spiders"

ROBOTSTXT_OBEY = True

# Gentle crawling (good for portfolio + real clients)
DOWNLOAD_DELAY = 0.8
AUTOTHROTTLE_ENABLED = True
RETRY_TIMES = 3

# Pipeline: export to CSV + JSONL


# A realistic UA helps many sites; keep it simple
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
