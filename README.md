# adidas_jp_crawler

A web crawler to get product details from https://shop.adidas.jp/


## Installation

Install the python requirements:

    pip install -r requirements.txt



## Exported Fields

| Field Name | Description |
| :--------- | :---------- |
| Product Name | Name of the product |
| Product URL | Link to the product details page |
| Breadcrumb | Breadcrumb trail to the product |
| Category | Product category |
| Image URL | Links to the product images (comma separated) |
| Price | Product price |
| Sizes | List of offered sizes (comma separated) |
| Size Fit | Size sense out of 5. 1 being smallest, 5 being largest |
| Coordinated Products | List of coordinated products. The data structure is described below in [Custom Fields](#coordinated-product) |
| Description Title | Title of the product description |
| Description General | General description of the product |
| Description Itemized | Itemized description of the product |
| Size Chart | Measurements from the size chart. The data structure is described below in [Custom Fields](#size-chart) |
| Special Functions | List of special functions. The data structure is described below in [Custom Fields](#special-function) |
| Rating | Product rating |
| Number of Reviews | Number of reviews the product received |
| Reviews | List of user reviews. The data structure is described below in [Custom Fields](#review) |
| Recommended Rate | Product recommendation rate (0-100%) |
| Rating Fit | Rating of the fit of the product (0: Too tight , 5: Too loose) |
| Rating Length | Rating of the length of the product (0: Too short, 5: Too long) |
| Rating Quality | Rating of the quality of the product (0: Low, 5: High) |
| Rating Comfort | Rating of the comfort of the product (0: Not comfortable, 5: Very comfortable) |
| KWs | List of KWs (comma separated) |




### Custom Fields

Custom fields are used to handle nested data. They are encapsulated within curly braces {} in the exported document. They are structured as follows:
{
    "field_name_1": field_value,
    "field_name_1": field_value
}

This structure is used to be both readable and able to easily convert back to python dictionaries using the json.loads function.

#### Coordinated Product

| Field Name | Description |
| :--------- | :---------- |
| product_id | Product ID |
| product_name | Coordinated product name |
| product_url | Link to the product details page |
| image_url | Link to the product image |
| price | Product price |


#### Size Chart

On the webpage, the size chart is a table where the columns represent the different offered sizes of the product and the rows are measurements such as "Chest Size", "Back Length", "Sleeve Length", etc. The rows present differ product to product. Hence the size of this custom field will be dynamic in the sense that it will have varying number of fields but each field value will be an array of measurements. This array will be correspond to the sizes as present in the [Sizes field](#exported-fields).


#### Special Function

| Field Name | Description |
| :--------- | :---------- |
| function | Name of the special function |
| description | Description of special function |


#### Review

| Field Name | Description |
| :--------- | :---------- |
| date | Name of the special function |
| rating | Description of special function |
| title | Description of special function |
| description | Description of special function |
| reviewer_id | Description of special function |