from zapv2 import ZAPv2
from src.config import Config
from src.logger import logger


def run_zap_scan():
    zap = ZAPv2(apikey=Config.ZAP_API_KEY, proxies={'http': Config.ZAP_PROXY, 'https': Config.ZAP_PROXY})

    logger.info('Accessing target {}'.format(Config.TARGET_URL))
    zap.urlopen(Config.TARGET_URL)

    logger.info('Starting Spider scan')
    scan_id = zap.spider.scan(Config.TARGET_URL)
    while int(zap.spider.status(scan_id)) < 100:
        logger.info('Spider progress %: {}'.format(zap.spider.status(scan_id)))

    logger.info('Starting Active scan')
    scan_id = zap.ascan.scan(Config.TARGET_URL)
    while int(zap.ascan.status(scan_id)) < 100:
        logger.info('Active Scan progress %: {}'.format(zap.ascan.status(scan_id)))

    logger.info('Scan completed')

    alerts = zap.core.alerts()
    return alerts