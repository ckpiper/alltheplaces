from scrapy import Spider
from scrapy.http import JsonRequest

from locations.categories import Extras, apply_yes_no
from locations.dict_parser import DictParser
from locations.hours import DAYS, OpeningHours
from locations.spiders.kfc_us import KFC_SHARED_ATTRIBUTES


class KfcMYSpider(Spider):
    name = "kfc_my"
    item_attributes = KFC_SHARED_ATTRIBUTES
    allowed_domains = ["kfc.com.my"]
    start_urls = ["https://kfc.com.my/graphql"]

    def start_requests(self):
        gql_query = """query allLocation {
    allLocation {
        locations {
            address
            city
            country
            lat
            ref: locationId
            long
            name
            phone
            selfcollect_close
            selfcollect_open
            state
            zip
            drivethru
        }
    }
}"""
        url = self.start_urls[0] + f"?query={gql_query}"
        yield JsonRequest(url=url)

    def parse(self, response):
        for location in response.json()["data"]["allLocation"]["locations"]:
            item = DictParser.parse(location)
            apply_yes_no(Extras.DRIVE_THROUGH, item, location["drivethru"] == "1", False)
            item["opening_hours"] = OpeningHours()

            if len(location["selfcollect_open"].split(":")) == 2:
                location["selfcollect_open"] = location["selfcollect_open"] + ":00"
            location["selfcollect_open"] = location["selfcollect_open"].replace("::", ":")

            if len(location["selfcollect_close"].split(":")) == 2:
                location["selfcollect_close"] = location["selfcollect_close"] + ":00"
            location["selfcollect_close"] = location["selfcollect_close"].replace("24:00:00", "23:59:00")
            location["selfcollect_close"] = location["selfcollect_close"].replace("::", ":")

            try:
                item["opening_hours"].add_days_range(
                    DAYS, location["selfcollect_open"], location["selfcollect_close"], "%H:%M:%S"
                )
            except Exception as e:
                self.logger.warning(
                    f"Error parsing hours: {location['selfcollect_open']}, {location['selfcollect_close']}, {e}"
                )
                self.crawler.stats.inc_value(f"atp/{self.name}/hours/failed")
            yield item
