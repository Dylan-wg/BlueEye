class Language:

    def __init__(self, name):
        self.name: str = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Language):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == str
        else:
            return False

    def __hash__(self):
        return self.name.__hash__()


ENGLISH = Language("English")
SIMPLIFIED_CHINESE = Language("中文(简体)")
TRADITIONAL_CHINESE = Language("中文(繁體)")
GERMAN = Language("Deutsch")
LANGUAGE_LIST = [ENGLISH, SIMPLIFIED_CHINESE, TRADITIONAL_CHINESE, GERMAN]
