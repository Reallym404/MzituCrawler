import random
from scrapy.conf import settings
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class RandomUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        ua  = random.choice(settings.get('USER_AGENT_LIST'))
        if ua:
            request.headers.setdefault('User-Agent', ua)