import scrapy
from playwright.async_api import Page

from typing import List, Dict

class AdidasMensSpider(scrapy.Spider):
    name = "adidas_mens"
    allowed_domains = ["shop.adidas.jp"]
    # start_url = "https://shop.adidas.jp/item/?gender=mens&category=wear"
    start_url = "file:///home/irfan/Documents/adidas_jp_crawler/samples/product_details_page.mhtml"
    # start_url = "https://shop.adidas.jp/products/IX6434/"

    details_page: Page = None

    def start_requests(self):
        print("START URL: {}".format(self.start_url))
        yield scrapy.Request(
            url=self.start_url,
            meta={"playwright": True, "playwright_include_page": True},
        )

    async def parse(self, response, **kwargs):
        self.details_page: Page = response.meta["playwright_page"]

        # Click on each coordinated product
        # Get div for each of them
        # Send each to another function to parse

        # Get page body

        # Parse each column separately

        # combine into a dict

        # add try catch

        # write csv

        title = await self.details_page.title()  # "Example Domain"

        await self.details_page.close()
        return {"title": title}


    async def errback_close_page(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()


    def get_coordinated_products(self) -> List[Dict]:
            
        # in self.details_page

        # locate coordinateRecommend class

        # for all li items in ul
        # click on the div with role button
        # extract the coordinate_time_container below

        # parse each coordinated product
        
        pass

    def get_product_number(self) -> str:
        '''
        Extracts the product number from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The product number
        '''
        
        pass

    def get_product_name(self) -> str:
        pass

    def get_product_url(self) -> str:
        pass

    def get_product_breadcrumb(self) -> str:
        pass

    def get_product_category(self) -> str:
        pass

    def get_product_image_url(self) -> str:
        pass

    def get_product_price(self) -> str:
        pass

    def get_product_sizes(self) -> List[str]:
        pass

    def get_product_size_fit(self) -> str:
        pass

    def get_product_description_title(self) -> str:
        pass

    def get_product_description_general(self) -> str:
        pass

    def get_product_description_itemized(self) -> str:
        pass

    def get_product_size_chart(self):
        pass

    def get_product_special_functions(self):
        pass

    def get_product_rating(self) -> str:
        pass

    def get_product_num_reviews(self) -> str:
        pass

    def get_product_reviews(self):
        pass

    def get_product_recommended_rate(self) -> str:
        pass

    def get_product_rating_fit(self) -> str:
        pass

    def get_product_rating_length(self) -> str:
        pass

    def get_product_rating_quality(self) -> str:
        pass

    def get_product_rating_comfort(self) -> str:
        pass

    def get_product_kws(self) -> List[str]:
        pass

    def get_product_rating(self):
        pass

    def get_product_rating(self):
        pass

