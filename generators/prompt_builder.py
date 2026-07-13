from config.config_manager import ConfigManager


class PromptBuilder:
    """
    Prompt Builder V2

    Goals:
        • Short, structured prompts
        • Better SDXL prompt adherence
        • Descriptor deduplication
        • Backward compatible with existing YAML files
    """

    def __init__(self):

        # --------------------------------------------------
        # Load Configurations
        # --------------------------------------------------

        self.templates = ConfigManager.prompt_templates()

        self.species_profiles = ConfigManager.species_profiles()

        self.season_profiles = ConfigManager.season_profiles()

        self.weather_profiles = ConfigManager.weather_profiles()

        self.camera_profiles = ConfigManager.camera_profiles()

        self.lighting_profiles = ConfigManager.lighting_profiles()

        self.realism_profiles = ConfigManager.realism_profiles()

        self.composition_profiles = ConfigManager.composition_profiles()

        # --------------------------------------------------
        # Generic profile lookup
        # --------------------------------------------------

        self.profile_map = {
            "season": self.season_profiles,
            "weather": self.weather_profiles,
            "lighting": self.lighting_profiles,
            "camera_angle": self.camera_profiles,
        }

    # ======================================================
    # Utility Methods
    # ======================================================

    @staticmethod
    def prettify(text):

        if text is None:
            return ""

        return str(text).replace("_", " ")

    @staticmethod
    def deduplicate(items):
        """
        Removes duplicate descriptors while preserving order.
        """

        seen = set()

        output = []

        for item in items:

            if not item:
                continue

            text = str(item).strip()

            if not text:
                continue

            key = text.lower()

            if key in seen:
                continue

            seen.add(key)

            output.append(text)

        return output

    # ======================================================
    # Profile Readers
    # ======================================================

    def get_species_profile(self, species):

        return self.species_profiles.get(
            species,
            {}
        )

    def get_profile_descriptors(
        self,
        profiles,
        key,
    ):

        if key is None:
            return []

        profile = profiles.get(
            key,
            {}
        )

        return profile.get(
            "descriptors",
            []
        )

    # ======================================================
    # Species Helpers
    # ======================================================

    def get_scientific_name(
        self,
        species_profile,
    ):

        return species_profile.get(
            "scientific_name",
            ""
        )

    def get_species_descriptors(
        self,
        species_profile,
    ):

        return species_profile.get(
            "descriptors",
            []
        )

    def get_appearance_descriptors(
        self,
        species_profile,
    ):

        appearance = species_profile.get(
            "appearance",
            {}
        )

        descriptors = []

        for value in appearance.values():

            if isinstance(value, list):
                descriptors.extend(value)

        return descriptors

    # ======================================================
    # Composition
    # ======================================================

    def get_composition(self):

        profile = self.composition_profiles.get(
            "single_tree",
            {}
        )

        return profile.get(
            "descriptors",
            []
        )

    # ======================================================
    # Realism
    # ======================================================

    def get_realism(
        self,
        realism,
    ):

        profile = self.realism_profiles.get(
            realism,
            {}
        )

        return profile.get(
            "descriptors",
            []
        )

    # ======================================================
    # Environment
    # ======================================================

    def get_environment_descriptors(
        self,
        variation,
    ):

        descriptors = []

        order = [
            "season",
            "weather",
            "lighting",
            "camera_angle",
        ]

        for field in order:

            descriptors.extend(

                self.get_profile_descriptors(

                    self.profile_map[field],

                    variation.get(field),

                )

            )

        return descriptors

    # ======================================================
    # Prompt Formatting
    # ======================================================

    @staticmethod
    def sentence(items):

        items = [
            i.strip()
            for i in items
            if i and str(i).strip()
        ]

        if not items:
            return ""

        return ", ".join(items)
    

    def build_prompt(
        self,
        variation,
        template="photorealistic",
        realism="photorealistic",
    ):
        """
        Builds a concise natural-language prompt optimized for SDXL.
        """

        species = variation["species"]

        health = self.prettify(
            variation.get("health", "healthy")
        )

        season = self.prettify(
            variation.get("season", "")
        )

        weather = self.prettify(
            variation.get("weather", "")
        )

        lighting = self.prettify(
            variation.get("lighting", "")
        )

        camera = self.prettify(
            variation.get("camera_angle", "")
        )

        time_of_day = self.prettify(
            variation.get("time_of_day", "")
        )

        # --------------------------------------------------
        # Species Profile
        # --------------------------------------------------

        species_profile = self.species_profiles.get(
            species,
            {}
        )

        scientific_name = species_profile.get(
            "scientific_name",
            ""
        )

        appearance = []

        appearance.extend(
            species_profile.get(
                "descriptors",
                []
            )[:2]
        )

        appearance_data = species_profile.get(
            "appearance",
            {}
        )

        for value in appearance_data.values():

            if isinstance(value, list):

                appearance.extend(value[:1])

        appearance = self.deduplicate(appearance)

        # --------------------------------------------------
        # Weather
        # --------------------------------------------------

        weather_desc = self.get_profile_descriptors(
            self.weather_profiles,
            variation.get("weather"),
        )[:1]

        # --------------------------------------------------
        # Lighting
        # --------------------------------------------------

        lighting_desc = self.get_profile_descriptors(
            self.lighting_profiles,
            variation.get("lighting"),
        )[:1]

        # --------------------------------------------------
        # Camera
        # --------------------------------------------------

        camera_desc = self.get_profile_descriptors(
            self.camera_profiles,
            variation.get("camera_angle"),
        )[:1]

        # --------------------------------------------------
        # Realism
        # --------------------------------------------------

        realism_desc = self.get_realism(
            realism
        )[:3]

        realism_desc = self.deduplicate(
            realism_desc
        )

        # --------------------------------------------------
        # Prompt
        # --------------------------------------------------

        prompt = (
            f"A single mature {health} {species} tree"
        )

        if scientific_name:

            prompt += f" ({scientific_name})"

        if appearance:

            prompt += (
                " with "
                + ", ".join(appearance)
            )

        prompt += "."

        # --------------------------------------------------
        # Environment
        # --------------------------------------------------

        env = []

        if season:
            env.append(f"during {season}")

        if weather:
            env.append(weather)

        if time_of_day:
            env.append(time_of_day)

        if env:

            prompt += (
                " Growing outdoors "
                + " ".join(env)
                + "."
            )

        # --------------------------------------------------
        # Weather Details
        # --------------------------------------------------

        extra = []

        extra.extend(weather_desc)

        extra.extend(lighting_desc)

        if extra:

            prompt += (
                " Environment features "
                + ", ".join(extra)
                + "."
            )

        # --------------------------------------------------
        # Composition
        # --------------------------------------------------

        prompt += (
            " Exactly one tree is present."
            " The tree occupies the center of the frame."
            " The entire tree is visible from trunk to canopy."
        )

        # --------------------------------------------------
        # Camera
        # --------------------------------------------------

        if camera:

            prompt += (
                f" Captured from a {camera} view."
            )

        if camera_desc:

            prompt += (
                " "
                + ", ".join(camera_desc)
                + "."
            )

        # --------------------------------------------------
        # Style
        # --------------------------------------------------

        style = []

        style.extend(realism_desc)

        style.extend([
            "photorealistic",
            "natural colors",
            "real bark texture",
            "real leaf texture",
            "sharp focus"
        ])

        style = self.deduplicate(style)

        prompt += (
            " "
            + ", ".join(style)
            + "."
        )

        # --------------------------------------------------
        # Print prompt for debugging
        # --------------------------------------------------

        print("\n" + "=" * 80)
        print("POSITIVE PROMPT")
        print(prompt)
        print("=" * 80)

        return prompt