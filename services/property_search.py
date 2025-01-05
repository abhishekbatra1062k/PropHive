from models.property import Property
from services.property_manager import PropertyManager

class PropertySearch:
    def __init__(self, manager: PropertyManager):
        self.manager = manager

    def search_properties(self, criteria: dict):
        min_price = criteria.get("min_price", float("-inf"))
        max_price = criteria.get("max_price", float("inf"))
        location = criteria.get("location")

        results = []
        for prop in self.manager.properties.values():
            if (min_price <= prop.details.get("price", 0) <= max_price) and (location is None or prop.details.get("location") == location):
                results.append(prop)
        return results

    def shortlist_property(self, user_id: str, property_id: str) -> bool:
        if property_id not in self.manager.properties:
            raise ValueError("Property not found")

        user_shortlist = self.manager.user_portfolios.get(user_id, [])
        if property_id in user_shortlist:
            return False

        self.manager.user_portfolios[user_id].append(property_id)
        return True

    def get_shortlisted(self, user_id: str):
        shortlisted_ids = self.manager.user_portfolios.get(user_id, [])
        return [self.manager.properties[prop_id] for prop_id in shortlisted_ids if self.manager.properties[prop_id].status == "available"]

