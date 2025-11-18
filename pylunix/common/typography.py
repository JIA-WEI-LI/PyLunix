from enum import Enum

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QFont

class TypographyStyle(Enum):
    CAPTION = "Caption"
    BODY = "Body"
    BODY_STRONG = "BodyStrong"
    BODY_LARGE = "BodyLarge"
    BODY_LARGE_STRONG = "BodyLargeStrong"
    SUBTITLE = "Subtitle"
    TITLE = "Title"
    TITLE_LARGE = "TitleLarge"
    DISPLAY = "Display"

class PyLnuixTypography:
    _DEFAULT_FAMILY = "Segoe UI"
    _FALLBACK_FAMILY = "Microsoft YaHei UI"

    _RAMP = {
        "Caption":             {"size": 12, "weight": QFont.Weight.Normal},
        "Body":                {"size": 14, "weight": QFont.Weight.Normal},
        "BodyStrong":          {"size": 14, "weight": QFont.Weight.DemiBold},
        "BodyLarge":           {"size": 18, "weight": QFont.Weight.Normal},
        "BodyLargeStrong":     {"size": 18, "weight": QFont.Weight.DemiBold},
        "Subtitle":            {"size": 20, "weight": QFont.Weight.DemiBold},
        "Title":               {"size": 28, "weight": QFont.Weight.DemiBold},
        "TitleLarge":          {"size": 40, "weight": QFont.Weight.DemiBold},
        "Display":             {"size": 68, "weight": QFont.Weight.DemiBold},
    }

    @classmethod
    def get_font(cls, style: TypographyStyle) -> QFont:
        style_key = style.value
        if style_key not in cls._RAMP:
            style_key = "Body" 

        settings = cls._RAMP[style_key]
        
        font = QFont(cls._DEFAULT_FAMILY)
        font.setPixelSize(settings["size"])
        font.setWeight(settings["weight"])
        
        return font

    @classmethod
    def get_family(cls):
        return cls._DEFAULT_FAMILY