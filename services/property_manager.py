from models.property import Property

class PropertyManager:
    def __init__(self):
        self.properties = {}
        self.user_portfolios = {}
        self.search_indices = {"price": {}, "location": {}}

    def add_property(self, user_id: str, property_details: dict) -> str:
        property_id = f"prop-{len(self.properties) + 1}"
        new_property = Property(property_id, user_id, property_details)
        self.properties[property_id] = new_property

        if user_id not in self.user_portfolios:
            self.user_portfolios[user_id] = []
        self.user_portfolios[user_id].append(property_id)

        self.update_indices(new_property)
        return property_id

    def update_property_status(self, property_id: str, status: str, user_id: str) -> bool:
        if property_id not in self.properties:
            raise ValueError("Property not found")
        property_obj = self.properties[property_id]

        if property_obj.user_id != user_id:
            raise PermissionError("Permission denied")

        property_obj.status = status
        return True

    def get_user_properties(self, user_id: str):
        if user_id not in self.user_portfolios:
            return []
        return [self.properties[prop_id] for prop_id in self.user_portfolios[user_id]]

    def update_indices(self, property_obj: Property):
        price = property_obj.details.get("price")
        location = property_obj.details.get("location")

        if price is not None:
            self.search_indices["price"].setdefault(price, []).append(property_obj.property_id)
        if location is not None:
            self.search_indices["location"].setdefault(location, []).append(property_obj.property_id)

