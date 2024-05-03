import scrapy
from playwright.async_api import Page


class AdidasMensSpider(scrapy.Spider):
    name = "adidas_mens"
    allowed_domains = ["shop.adidas.jp"]
    start_url = "https://shop.adidas.jp/item/?gender=mens&category=wear"
    # start_url = "https://shop.adidas.jp/products/IX6434/"

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_url,
            meta={"playwright": True, "playwright_include_page": True},
        )

    async def parse(self, response, **kwargs):
        page = response.meta["playwright_page"]

        title = await page.title()  # "Example Domain"
        await page.close()
        return {"title": title}


    async def errback_close_page(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
