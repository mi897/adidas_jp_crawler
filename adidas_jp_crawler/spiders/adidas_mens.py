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

        output = {
            "title": title,
            "Product Number": None,
            "Product Name": await self.get_product_name(),
            "Product URL": response.url,
            "Breadcrumb": await self.get_product_breadcrumb(),
            "Category": await self.get_product_category(),
            "Image URL": await self.get_product_image_url(),
            "Price": None,
            "Sizes": None,
            "Size Fit": None,
            "Coordinated Products ": None,
            "Description Title": None,
            "Description General": None,
            "Description Itemized": None,
            "Size Chart": None,
            "Special Functions": None,
            "Rating": None,
            "Number of Reviews": None,
            "Reviews": None,
            "Recommended Rate": None,
            "Rating Fit": None,
            "Rating Length": None,
            "Rating Quality": None,
            "Rating Comfort": None,
            "KWs": None,
        }

        await self.details_page.close()
        return output


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

        url = self.details_page.url
        product_number = url

        return product_number
        

    async def get_product_name(self) -> str:
        '''
        Extracts the product name from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The product name
        '''

        product_name = await self.details_page.locator("css=.articleNameHeader").locator("css=.itemTitle").text_content()

        return product_name

    async def get_product_breadcrumb(self) -> str:
        '''
        Extracts the breadcrumb trail from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The product breadcrumb trail
        '''

        breadcrumb_list = await self.details_page.locator("css=.breadcrumbList").get_by_role("listitem").all_text_contents()
        breadcrumb = " / ".join(breadcrumb_list[1:])

        return breadcrumb
    

    async def get_product_category(self) -> str:
        '''
        Extracts the product category from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The product category
        '''

        product_category = await self.details_page.locator("css=.articleNameHeader").locator("css=.categoryName").text_content()

        return product_category

    async def get_product_image_url(self) -> str:
        '''
        Extracts the list of image urls of the product from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The image urls (comma separated string)
        '''

        # click show more button

        more_images_button = self.details_page.get_by_label('もっと見るボタン')

        await more_images_button.click()

        more_images_button.wait_for()

        # get image urls

        product_images = [await img.get_attribute("src") for img in await self.details_page.locator("css=.articleImageWrapper").locator("css=.image").all()]

        return product_images

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

