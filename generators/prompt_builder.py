class PromptBuilder:
    QUALITY_DESCRIPTORS = ["botanically accurate",
                            "natural outdoor environment",
                            "high-detail nature photography",
                            "realistic bark texture",
                            "sharp focus",
                            "ultra realistic"]
    def build_prompt(self,combination):
        prompt_parts = []
        prompt_parts.append(f"Photorealistic {combination['species']} tree")
        prompt_parts.append(f"{combination['season']} season")
        prompt_parts.append(f"{combination['weather']} weather")
        prompt_parts.append(f"{combination['health']} foliage")
        prompt_parts.append(f"{combination['camera_angle']} view")
        prompt_parts.append(combination['lighting'].replace("_", " "))
        prompt_parts.append(f"{combination['time_of_day']} atmosphere")
        prompt_parts.extend(self.QUALITY_DESCRIPTORS)
        prompt = ", ".join(prompt_parts)
        return prompt
    
    def prettify(text):
        return text.replace("_", " ")

if __name__=="__main__":
    combination = {
        "species": "Neem",
        "season": "winter",
        "weather": "rainy",
        "health": "healthy",
        "camera_angle": "front",
        "lighting": "natural_daylight",
        "time_of_day": "morning"
    }
    builder = PromptBuilder()
    prompt = builder.build_prompt(combination)
    print(prompt)
        