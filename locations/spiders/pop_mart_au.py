from locations.storefinders.stockist import StockistSpider


class PopMartAUSpider(StockistSpider):
    name = "pop_mart_au"
    item_attributes = {"brand": "Pop Mart", "brand_wikidata": "Q97180096"}
    key = "u12357"
