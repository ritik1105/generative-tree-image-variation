import yaml
from itertools import product
import random
from config.config_manager import ConfigManager

class VariationEngine:
    def load_defaults(self):
        with open("config/defaults.yaml","r") as file:
            data = yaml.safe_load(file)
        return data
    def normalize_request(self,request):
        config = self.load_defaults()
        defaults = ConfigManager.defaults()
        normalized = request.copy()
        for field, default_value in defaults.items():

            if (
                field not in normalized
                or normalized[field] is None
                or normalized[field] == []
                ):
                normalized[field] = default_value
        variation_fields = [
            "season",
            "weather",
            "health",
            "camera_angle",
            "lighting",
            "time_of_day"
        ]

        for field in variation_fields:
            if field in normalized and not isinstance(normalized[field], list):
                normalized[field] = [normalized[field]]

        return normalized

    def generate_combinations(self, normalized_request):

        dimensions = [
            "season",
            "weather",
            "health",
            "camera_angle",
            "lighting",
            "time_of_day"
        ]

        dimension_values = [
            normalized_request[dimension]
            for dimension in dimensions
        ]

        all_products = product(*dimension_values)

        combinations = []

        for product_tuple in all_products:

            combination = {
                "species": normalized_request["species"]
            }

            for dimension, value in zip(dimensions, product_tuple):
                combination[dimension] = value

            combinations.append(combination)

        return combinations
    def sample_combinations(self,combinations, requested_images):
        if requested_images >= len(combinations):
            return combinations
        else:
            return random.sample(combinations,requested_images)
        
if __name__ == "__main__":
    request = { 
        "species": "Neem",
        "season": ["summer", "winter"],
        "weather": ["clear", "rainy"]
    }

    engine = VariationEngine()

    normalized = engine.normalize_request(request)

    combinations = engine.generate_combinations(normalized)

    print(f"Total combinations: {len(combinations)}\n")

    for combination in combinations:
        print(combination)

    print("\n------- Sampling Test (requested_images=3) -------\n")

    sampled = engine.sample_combinations(combinations, 3)

    print(f"Sampled combinations ({len(sampled)}):\n")

    for combo in sampled:
        print(combo)
    
