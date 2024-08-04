BOT_NAME = 'ticket_scraper'

SPIDER_MODULES = ['ticket_scraper.spiders']
NEWSPIDER_MODULE = 'ticket_scraper.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    # 'ticket_scraper.pipelines.TicketScraperPipeline': 300,
    'ticket_scraper.pipelines.TicketPipeline': 300,
    'ticket_scraper.pipelines.MysqlTicketPipeline': 300,
}

MYSQL_SETTINGS = {
    'host': 'localhost:3306',
    'user': 'root',
    'password': 'hrn77799.',
    'db': 'ticket-data',
    'charset': 'utf8mb4',
}

REDIS_SETTINGS = {
    'host': 'localhost',
    'port': 6379,
    'redis_password': None,  # 如果 Redis 服务器有设置密码，需要设置密码
    'redis_db': 0  # 数据库编号，默认为 0
}
