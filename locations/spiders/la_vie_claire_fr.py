from scrapy.spiders import SitemapSpider

from locations.categories import Categories
from locations.structured_data_spider import StructuredDataSpider


class LaVieClaireFRSpider(SitemapSpider, StructuredDataSpider):
    name = "la_vie_claire_fr"
    item_attributes = {
        "brand": "La Vie Claire",
        "brand_wikidata": "Q3213589",
        "extras": Categories.SHOP_HEALTH_FOOD.value,
    }
    sitemap_urls = ["https://magasins.lavieclaire.com/sitemap.xml"]
    sitemap_rules = [(r"https://magasins.lavieclaire.com/lavieclaire/fr/store/.*/\d+$", "parse_sd")]
    wanted_types = ["LocalBusiness"]
    drop_attributes = {"image"}
