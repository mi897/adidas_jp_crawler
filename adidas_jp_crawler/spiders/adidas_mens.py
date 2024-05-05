import scrapy
from playwright.async_api import Page, expect


from typing import List, Dict

class AdidasMensSpider(scrapy.Spider):
    name = "adidas_mens"
    allowed_domains = ["shop.adidas.jp"]
    # start_url = "https://shop.adidas.jp/item/?gender=mens&category=wear"
    # start_url = "file:///home/irfan/Documents/adidas_jp_crawler/samples/product_details_page.mhtml"
    start_url = "https://shop.adidas.jp/products/IX6434/"

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
            "Product Number": self.get_product_number(), # parse url
            "Product Name": await self.get_product_name(),
            "Product URL": response.url,
            "Breadcrumb": await self.get_product_breadcrumb(),
            "Category": await self.get_product_category(),
            "Image URL": await self.get_product_image_url(), # need to wait after click
            "Price": await self.get_product_price(),
            "Sizes": await self.get_product_sizes(),
            "Size Fit": await self.get_product_size_fit(),
            "Coordinated Products ": None,
            "Description Title": await self.get_product_description_title(),
            "Description General": await self.get_product_description_general(),
            "Description Itemized": await self.get_product_description_itemized(),
            "Size Chart": await self.get_product_size_chart(),
            "Special Functions": await self.get_product_special_functions(),
            "Rating": await self.get_product_rating(),
            "Number of Reviews": await self.get_product_num_reviews(),
            "Reviews": await self.get_product_reviews(),
            "Recommended Rate": await self.get_product_recommended_rate(),
            "Rating Fit": await self.get_product_rating_fit(),
            "Rating Length": await self.get_product_rating_length(),
            "Rating Quality": await self.get_product_rating_quality(),
            "Rating Comfort": await self.get_product_rating_comfort(),
            "KWs": await self.get_product_kws(),
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
        product_number = url.split('/')[-2]

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

        # get image wrapper

        extended_image_wrapper = self.details_page.locator("css=.article_image_wrapper.isExpand")

        # click expand button

        more_images_button = self.details_page.get_by_label('もっと見るボタン')

        await more_images_button.click()

        # wait for image wrapper to extend

        await extended_image_wrapper.wait_for()

        # get image urls

        product_images = await self.details_page.locator("css=.articleImageWrapper").locator("css=.image").all()

        image_urls = []
        for image in product_images:
            # expect()
            # (await image.get_attribute("src")).startswith("/static")
            await image.scroll_into_view_if_needed()
            image_urls.append(await image.get_attribute("src"))

        # image_urls = [await img.get_attribute("src") for img in product_images]

        return image_urls

    async def get_product_price(self) -> str:
        '''
        Extracts the product price from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The product price
        '''

        product_price = await self.details_page.locator("css=.articlePrice").locator("css=.price-value").text_content()

        return product_price

    async def get_product_sizes(self) -> List[str]:
        '''
        Extracts the product sizes from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The product sizes
        '''

        product_sizes_locators = await self.details_page.locator("css=.sizeSelectorList").get_by_role("listitem").all()

        product_sizes = [await size.text_content() for size in product_sizes_locators]

        return product_sizes

    async def get_product_size_fit(self) -> str:
        '''
        Extracts the size fit from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The size fit (out of 5)
        '''

        size_fit_bar_class = await self.details_page.locator("css=.sizeFitBar").locator("css=.marker").get_attribute("class")
        size_fit = size_fit_bar_class[-3]

        return size_fit

    async def get_product_description_title(self) -> str:
        '''
        Extracts the title of the product description from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The description title
        '''

        description_title = await self.details_page.locator("css=.heading.itemFeature").text_content()
        
        return description_title

    async def get_product_description_general(self) -> str:
        '''
        Extracts the general product description from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The general product description
        '''

        general_description = await self.details_page.locator("css=.description").locator("css=.description_part.details").text_content()
        
        return general_description

    async def get_product_description_itemized(self) -> str:
        '''
        Extracts the itemized product description from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The itemized description
        '''

        itemized_description_locators = await self.details_page.locator("css=.description").locator("css=.articleFeatures").get_by_role("listitem").all()
        itemized_description = [await item.text_content() for item in itemized_description_locators]

        return itemized_description

    async def get_product_size_chart(self):
        pass

    async def get_product_special_functions(self):
        pass

    async def get_product_rating(self) -> str:
        '''
        Extracts the product rating from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The product rating (out of 5)
        '''

        product_rating_container = self.details_page.locator("#BVRRContainer")

        await self.details_page.mouse.wheel(0, 1000)
        await self.details_page.mouse.wheel(0, -1000)
        await self.details_page.mouse.wheel(0, 1200)

        await product_rating_container.locator('#BVRRWidgetID').wait_for()
        
        rating_div = product_rating_container.locator('//*[@id="BVRRRatingOverall_"]/div[3]/span[1]')

        await rating_div.scroll_into_view_if_needed()
        
        await rating_div.wait_for()
        product_rating = await rating_div.text_content()

        return product_rating

    async def get_product_num_reviews(self) -> str:
        '''
        Extracts the number of ratings from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The number of ratings
        '''

        num_rating = await self.details_page.locator("css=.BVRRNumber.BVRRBuyAgainTotal").text_content()

        return num_rating

    async def get_product_reviews(self):
        pass

    async def get_product_recommended_rate(self) -> str:
        '''
        Extracts the rate of recommendations from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The percentage rate of recommendations
        '''

        recommendations_rate = await self.details_page.locator("css=.BVRRBuyAgainPercentage").locator("css=.BVRRNumber").text_content()

        return recommendations_rate

    async def get_product_rating_fit(self) -> str:
        '''
        Extracts the fit rating from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The fit rating (out of 5)
        '''

        fit_rating = await self.details_page.locator('//*[@id="BVRRQuickTakeSummaryID"]/div/div/div/div[2]/div[5]/div/div[1]/div[1]/div[2]/div[2]/img').get_attribute("alt")
        fit_rating = fit_rating.strip(" / 5")

        return fit_rating


    async def get_product_rating_length(self) -> str:
        '''
        Extracts the length rating from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The length rating (out of 5)
        '''

        length_rating = await self.details_page.locator('//*[@id="BVRRQuickTakeSummaryID"]/div/div/div/div[2]/div[5]/div/div[1]/div[2]/div[2]/div[2]/img').get_attribute("alt")
        length_rating = length_rating.strip(" / 5")

        return length_rating

    async def get_product_rating_quality(self) -> str:
        '''
        Extracts the quality rating from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The quality rating (out of 5)
        '''

        quality_rating = await self.details_page.locator('//*[@id="BVRRQuickTakeSummaryID"]/div/div/div/div[2]/div[5]/div/div[2]/div[1]/div[2]/div[2]/img').get_attribute("alt")
        quality_rating = quality_rating.strip(" / 5")

        return quality_rating

    async def get_product_rating_comfort(self) -> str:
        '''
        Extracts the comfort rating from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The comfort rating (out of 5)
        '''

        comfort_rating = await self.details_page.locator('//*[@id="BVRRQuickTakeSummaryID"]/div/div/div/div[2]/div[5]/div/div[2]/div[2]/div[2]/div[2]/img').get_attribute("alt")
        comfort_rating = comfort_rating.strip(" / 5")

        return comfort_rating

    async def get_product_kws(self) -> List[str]:
        '''
        Extracts the KWs from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The list of KWs
        '''

        await self.details_page.mouse.wheel(0, 5000)
        kws = await self.details_page.locator('.itemTagsPosition').get_by_role("link").all_text_contents()        

        return kws

