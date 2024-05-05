import scrapy
from playwright.async_api import Page, expect, Locator
import logging
from scrapy.utils.log import configure_logging 

from typing import List, Dict
from urllib.parse import urljoin


class AdidasMensSpider(scrapy.Spider):
    name = "adidas_mens"
    allowed_domains = ["shop.adidas.jp"]

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    start_url = "https://shop.adidas.jp/item/?gender=mens&category=wear&order=1"
    # start_url = "file:///home/irfan/Documents/adidas_jp_crawler/samples/product_details_page.mhtml"
    # start_url = "https://shop.adidas.jp/products/IX6434/"
    # start_url = "https://shop.adidas.jp/products/IN4769/"

    details_page: Page = None

    def start_requests(self):
        print("START URL: {}".format(self.start_url))
        yield scrapy.Request(
            url=self.start_url,
            meta={"playwright": True, "playwright_include_page": True},
            callback=self.parse
        )

    async def parse(self, response, **kwargs):
        details_page: Page = response.meta["playwright_page"]

        # find all products

        product_cards = await details_page.locator('.itemCardArea-cards.test-card.css-dhpxhu').all()

        logging.info("number of products on page: {}".format(len(product_cards)))

        
        for card in product_cards:

            product_page = await card.get_by_role('link').get_attribute('href')

            url = response.urljoin(product_page)

            print("product url: {}".format(url))
            logging.info("product url: {}".format(url))

            yield scrapy.Request(
                url=url,
                meta={"playwright": True, "playwright_include_page": True},
                callback=self.parse_page
            )
                    

        # go to next page

        next_page_link = details_page.locator('.viewSwitcher').locator('.pageSelector').get_by_role('link')
        if await next_page_link.is_visible():
            next_page = next_page_link.get_attribute('href')
            if next_page:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(
                url=self.start_url,
                meta={"playwright": True, "playwright_include_page": True},
                callback=self.parse
            )
            


    async def parse_page(self, response, *kwargs):

        details_page: Page = response.meta["playwright_page"]

        # combine into a dict

        title = await details_page.title()

        output = {
            "title": title,
            # "Product Number": self.get_product_number(details_page),
            # "Product Name": await self.get_product_name(details_page),
            # "Product URL": response.url,
            # "Breadcrumb": await self.get_product_breadcrumb(details_page),
            # "Category": await self.get_product_category(details_page),
            # "Image URL": await self.get_product_image_url(details_page),
            # "Price": await self.get_product_price(details_page),
            # "Sizes": await self.get_product_sizes(details_page),
            # "Size Fit": await self.get_product_size_fit(details_page),
            # "Coordinated Products ": await self.get_coordinated_products(details_page),
            # "Description Title": await self.get_product_description_title(details_page),
            # "Description General": await self.get_product_description_general(details_page),
            # "Description Itemized": await self.get_product_description_itemized(details_page),
            # # "Size Chart": await self.get_product_size_chart(details_page),
            # "Special Functions": await self.get_product_special_functions(details_page),
            # "Rating": await self.get_product_rating(details_page),
            # "Number of Reviews": await self.get_product_num_reviews(details_page),
            # # "Reviews": await self.get_product_reviews(details_page),
            # "Recommended Rate": await self.get_product_recommended_rate(details_page),
            # "Rating Fit": await self.get_product_rating_fit(details_page),
            # "Rating Length": await self.get_product_rating_length(details_page),
            # "Rating Quality": await self.get_product_rating_quality(details_page),
            # "Rating Comfort": await self.get_product_rating_comfort(details_page),
            # "KWs": await self.get_product_kws(details_page),
        }

        await details_page.close()
        yield output

    async def errback_close_page(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()


    async def get_coordinated_products(self, details_page) -> List[Dict]:
        '''
        Extracts coordinate products from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The list of coordinated products
        '''

        products = []

        coordinate_items: List[Locator] = await details_page.locator('.coordinateItems').get_by_role("listitem").all()
        coordinate_item_container = details_page.locator(".coordinate_item_container.add-open")
        
        for item in coordinate_items:
            await item.locator("div").first.click()

            await coordinate_item_container.wait_for()

            product_image_wrapper = coordinate_item_container.locator('.image_wrapper')

            product_name = coordinate_item_container.locator(".info_wrapper > span > span")

            product_price = coordinate_item_container.locator(".info_wrapper > .mdl-price > p > span")

            url = product_image_wrapper.get_by_role("link")

            await expect(product_name).not_to_contain_text(products[-1]['product_name']) if products else None

            product_url = urljoin(details_page.url, await url.get_attribute("href"))
            product = {
                "product_id": product_url.split("/")[-1],
                "product_name": await product_name.text_content(),
                "product_url": product_url,
                "image_url": urljoin(details_page.url, await product_image_wrapper.get_by_role('img').get_attribute('src')),
                "price": await product_price.text_content(),
            }

            products.append(product)

            await item.locator("div").first.click()
            await coordinate_item_container.wait_for(state="hidden")


        return products

    def get_product_number(self, details_page) -> str:
        '''
        Extracts the product number from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The product number
        '''

        url = details_page.url
        product_number = url.split('/')[-2]

        return product_number
        

    async def get_product_name(self, details_page) -> str:
        '''
        Extracts the product name from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The product name
        '''

        product_name = await details_page.locator("css=.articleNameHeader").locator("css=.itemTitle").text_content()

        return product_name

    async def get_product_breadcrumb(self, details_page) -> str:
        '''
        Extracts the breadcrumb trail from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The product breadcrumb trail
        '''

        breadcrumb_list = await details_page.locator("css=.breadcrumbList").get_by_role("listitem").all_text_contents()
        breadcrumb = " / ".join(breadcrumb_list[1:])

        return breadcrumb
    

    async def get_product_category(self, details_page) -> str:
        '''
        Extracts the product category from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The product category
        '''

        product_category = await details_page.locator("css=.articleNameHeader").locator("css=.categoryName").text_content()

        return product_category

    async def get_product_image_url(self, details_page) -> str:
        '''
        Extracts the list of image urls of the product from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The image urls (comma separated string)
        '''

        # click show more button

        # get image wrapper

        extended_image_wrapper = details_page.locator("css=.article_image_wrapper.isExpand")

        # click expand button

        more_images_button = details_page.get_by_label('もっと見るボタン')

        await more_images_button.click()

        # wait for image wrapper to extend

        await extended_image_wrapper.wait_for()

        # get image urls

        product_images = await details_page.locator("css=.articleImageWrapper").locator("css=.image").all()

        image_urls = []
        for image in product_images:
            # expect()
            # (await image.get_attribute("src")).startswith("/static")
            await image.scroll_into_view_if_needed()
            image_urls.append(await image.get_attribute("src"))

        # image_urls = [await img.get_attribute("src") for img in product_images]

        return image_urls

    async def get_product_price(self, details_page) -> str:
        '''
        Extracts the product price from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The product price
        '''

        product_price = await details_page.locator("css=.articlePrice").locator("css=.price-value").text_content()

        return product_price

    async def get_product_sizes(self, details_page) -> List[str]:
        '''
        Extracts the product sizes from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The product sizes
        '''

        product_sizes_locators = await details_page.locator("css=.sizeSelectorList").get_by_role("listitem").all()

        product_sizes = [await size.text_content() for size in product_sizes_locators]

        return product_sizes

    async def get_product_size_fit(self, details_page) -> str:
        '''
        Extracts the size fit from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The size fit (out of 5)
        '''

        size_fit_bar_class = await details_page.locator("css=.sizeFitBar").locator("css=.marker").get_attribute("class")
        size_fit = size_fit_bar_class[-3]

        return size_fit

    async def get_product_description_title(self, details_page) -> str:
        '''
        Extracts the title of the product description from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The description title
        '''

        description_title = await details_page.locator("css=.heading.itemFeature").text_content()
        
        return description_title

    async def get_product_description_general(self, details_page) -> str:
        '''
        Extracts the general product description from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The general product description
        '''

        general_description = await details_page.locator("css=.description").locator("css=.description_part.details").text_content()
        
        return general_description

    async def get_product_description_itemized(self, details_page) -> str:
        '''
        Extracts the itemized product description from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The itemized description
        '''

        itemized_description_locators = await details_page.locator("css=.description").locator("css=.articleFeatures").get_by_role("listitem").all()
        itemized_description = [await item.text_content() for item in itemized_description_locators]

        return itemized_description

    async def get_product_size_chart(self, details_page):
        '''
        Extracts the size chart of the product from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The size chart
        '''
        
        size_chart = details_page.locator("css=.sizeChart")
        size_chart.scroll_into_view_if_needed()
        
        properties_rows = await size_chart.get_by_role('table')

        properties = []

        for row in properties_rows:
            row.wait_for()
            properties.append(await row.text_content())

        return {
            "properties": properties
        }
        


    async def get_product_special_functions(self, details_page):
        '''
        Extracts any special function that the product might have from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The special function title and description
        '''

        special_function = None

        selector = '.contentsWrapper > main > div > div > .css-j2pp63 > div > div > .details'
        if await details_page.locator(selector=selector).is_visible():

            special_function_wrapper = details_page.locator(selector)

            title = await special_function_wrapper.locator('a').text_content()
            description = (await special_function_wrapper.text_content())[len(title):]

            special_function = {
                "title": title,
                "description": description,
            }

        return special_function


    async def get_product_rating(self, details_page) -> str:
        '''
        Extracts the product rating from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The product rating (out of 5)
        '''

        product_rating_container = details_page.locator("#BVRRContainer")

        await details_page.mouse.wheel(0, 1000)
        await details_page.mouse.wheel(0, -1000)
        await details_page.mouse.wheel(0, 1200)

        await product_rating_container.locator('#BVRRWidgetID').wait_for()
        
        rating_div = product_rating_container.locator('//*[@id="BVRRRatingOverall_"]/div[3]/span[1]')

        await rating_div.scroll_into_view_if_needed()
        
        await rating_div.wait_for()
        product_rating = await rating_div.text_content()

        return product_rating

    async def get_product_num_reviews(self, details_page) -> str:
        '''
        Extracts the number of ratings from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The number of ratings
        '''

        num_rating = await details_page.locator("css=.BVRRNumber.BVRRBuyAgainTotal").text_content()

        return num_rating

    async def get_product_reviews(self, details_page):
        pass

    async def get_product_recommended_rate(self, details_page) -> str:
        '''
        Extracts the rate of recommendations from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The percentage rate of recommendations
        '''

        recommendations_rate = await details_page.locator("css=.BVRRBuyAgainPercentage").locator("css=.BVRRNumber").text_content()

        return recommendations_rate

    async def get_product_rating_fit(self, details_page) -> str:
        '''
        Extracts the fit rating from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The fit rating (out of 5)
        '''

        fit_rating = await details_page.locator('//*[@id="BVRRQuickTakeSummaryID"]/div/div/div/div[2]/div[5]/div/div[1]/div[1]/div[2]/div[2]/img').get_attribute("alt")
        fit_rating = fit_rating.strip(" / 5")

        return fit_rating


    async def get_product_rating_length(self, details_page) -> str:
        '''
        Extracts the length rating from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The length rating (out of 5)
        '''

        length_rating = await details_page.locator('//*[@id="BVRRQuickTakeSummaryID"]/div/div/div/div[2]/div[5]/div/div[1]/div[2]/div[2]/div[2]/img').get_attribute("alt")
        length_rating = length_rating.strip(" / 5")

        return length_rating

    async def get_product_rating_quality(self, details_page) -> str:
        '''
        Extracts the quality rating from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The quality rating (out of 5)
        '''

        quality_rating = await details_page.locator('//*[@id="BVRRQuickTakeSummaryID"]/div/div/div/div[2]/div[5]/div/div[2]/div[1]/div[2]/div[2]/img').get_attribute("alt")
        quality_rating = quality_rating.strip(" / 5")

        return quality_rating

    async def get_product_rating_comfort(self, details_page) -> str:
        '''
        Extracts the comfort rating from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The comfort rating (out of 5)
        '''

        comfort_rating = await details_page.locator('//*[@id="BVRRQuickTakeSummaryID"]/div/div/div/div[2]/div[5]/div/div[2]/div[2]/div[2]/div[2]/img').get_attribute("alt")
        comfort_rating = comfort_rating.strip(" / 5")

        return comfort_rating

    async def get_product_kws(self, details_page) -> List[str]:
        '''
        Extracts the KWs from the details page

        Expects:
            A class variable "details_page" which is a playwright page
        
        Returns:
            The list of KWs
        '''

        await details_page.mouse.wheel(0, 5000)
        kws = await details_page.locator('.itemTagsPosition').get_by_role("link").all_text_contents()        

        return kws

