from grifon.enums import AutoName


class SexEnum(str, AutoName):
    male = "male"
    female = "female"


class RaceEnum(str, AutoName):
    white = "white"
    black = "black"
    asian = "asian"
    indian = "indian"
    others = "others"


class EmotionEnum(str, AutoName):
    negative = "negative"
    neutral = "neutral"
    positive = "positive"
