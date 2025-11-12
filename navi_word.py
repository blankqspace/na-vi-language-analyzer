import re
from typing import Dict, List, Optional


class NaviWord:
    """Base class for all Na'vi words"""

    def __init__(self, text: str, position: int = 0):
        self.text = text
        self.position = position
        self.normalized = text.lower().strip()

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.text}')"

    @property
    def is_valid(self) -> bool:
        return bool(re.match(r"^[a-zA-ZàèìòùÀÈÌÒÙäëïöüÄËÏÖÜ\'-]+$", self.text))


class NaviNoun(NaviWord):
    """It describes noun in Na'vi: case, number and lenition"""

    def __init__(
        self,
        text: str,
        position: int = 0,
        ends_with_vowel: bool = True,
        ends_with_diphthong: bool = False,
        ends_with_pseudovowel: bool = False,
    ):
        super().__init__(text, position)
        self.ends_with_vowel = ends_with_vowel
        self.ends_with_diphthong = ends_with_diphthong
        self.ends_with_pseudovowel = ends_with_pseudovowel
        self._lenition_applied = False

    def get_case(self, case: str) -> str:

        case_endings = {
            "subjective": "",
            "agentive": self._get_agentive(),
            "patientive": self._get_patientive(),
            "dative": self._get_dative(),
            "genitive": self._get_genitive(),
            "topical": self._get_topical(),
        }
        return self.text + case_endings.get(case, "")

    def _get_agentive(self) -> str:
        if self.ends_with_vowel:
            return "l"
        else:
            return "il"

    def _get_patientive(self) -> str:
        if self.ends_with_vowel or self.ends_with_diphthong:
            return "ti"
        else:
            return "it"

    def _get_dative(self) -> str:
        if self.ends_with_vowel or self.ends_with_diphthong:
            return "ru"
        else:
            return "ur"

    def _get_genitive(self) -> str:
        if self.ends_with_vowel:
            if self.text.endswith(("o", "u")):
                return "ä"
            elif self.text.endswith("a"):
                return "yä"
            else:
                return "yä"
        else:
            return "ä"

    def _get_topical(self) -> str:
        if self.ends_with_vowel:
            return "ri"
        else:
            return "iri"

    def get_number(self, number: str) -> str:

        number_prefixes = {"singular": "", "dual": "me", "trial": "pxe", "plural": "ay"}
        prefix = number_prefixes.get(number, "")

        if prefix:
            lenited_base = self._apply_lenition(self.text)
            result = prefix + lenited_base
            self._lenition_applied = True
            return result
        return self.text

    def _apply_lenition(self, word: str) -> str:

        lenition_rules = {
            "px": "p",
            "tx": "t",
            "kx": "k",
            "p": "p",
            "t": "t",
            "k": "k",
            "ts": "s",
        }
        for from_sound, to_sound in lenition_rules.items():
            if word.startswith(from_sound):
                return to_sound + word[len(from_sound) :]
        return word

    def get_number_with_case(self, number: str, case: str) -> str:

        numbered_form = self.get_number(number)

        # Create a temporary Noun object for the number form
        # Determine if the new form ends in a vowel
        vowels = ("a", "e", "i", "ì", "o", "u", "ä")
        ends_with_vowel = numbered_form.endswith(vowels)

        temp_noun = NaviNoun(numbered_form, ends_with_vowel=ends_with_vowel)
        return temp_noun.get_case(case)

    def make_indefinite(self) -> str:
        return self.text + "o"

    @property
    def has_lenition(self) -> bool:
        return self._lenition_applied


class NaviPronoun(NaviWord):
    """It describes pronoun in Na'vi: person, number, animacy and inclusivity/exclusivity"""

    def __init__(
        self,
        text: str,
        position: int = 0,
        person: str = "third",
        number: str = "singular",
        animacy: str = "animate",
        inclusivity: str = "exclusive",  # for 1st person: "inclusive" or "exclusive"
        gender: str = "neutral",  # for 3rd person: "neutral", "male", "female"
        is_honorific: bool = False,
    ):
        super().__init__(text, position)
        self.person = person
        self.number = number
        self.animacy = animacy
        self.inclusivity = inclusivity
        self.gender = gender
        self.is_honorific = is_honorific

    def get_case(self, case: str) -> str:
        # Pronouns follow same case rules as nouns ending in vowels
        ends_with_vowel = self.text.endswith(("a", "e", "i", "ì", "o", "u", "ä"))
        noun = NaviNoun(self.text, ends_with_vowel=ends_with_vowel)
        return noun.get_case(case)

    def get_genitive(self) -> str:
        irregular_genitives = {
            "fko": "fkeyä",  # one, they (unspecified agent)
            "nga": "ngeyä",  # you
            "po": "peyä",  # he/she (animate)
            "sno": "sneyä",  # himself, herself, itself, themselves, oneself
            "tsa'u": "tseyä",  # that
            "ayla": "ayleyä",  # others
            "fo": "feyä",  # they
            "awnga": "awngeyä",  # we, us (inclusive), short form
            "ayoeng": "ayoengeyä",  # we, us (inclusive)
            "oe": "oeyä",
            "moe": "moeyä",
            "pxoe": "pxoeyä",
            "ayoe": "ayoeyä",
            "oeng": "oengeyä",
            "pxoeng": "pxoengeyä",
        }

        # Derived pronouns (frapo - everyone, 'awpo - one individual, apo - another one, fìpo - this one, tsapo - that one)
        if self.text.startswith(
            ("fra", "'aw", "la", "fì", "tsa")
        ) and self.text.endswith("po"):
            base = self.text[:-2]  # remove 'po'
            return base + "peyä"

        return irregular_genitives.get(self.text, self.text + "ä")

    def get_honorific_form(self) -> str:

        honorific_forms = {
            # 1st person exclusive
            "oe": "ohe",
            "moe": "mohe",
            "pxoe": "pxohe",
            "ayoe": "ayohe",
            # 1st person inclusive
            "oeng": "oheng",
            "pxoeng": "pxoheng",
            "ayoeng": "ayoheng",
            # 2nd person
            "nga": "ngenga",
            "menga": "mengenga",
            "pxenga": "pxengenga",
            "aynga": "ayngenga",
            # 3rd person animate
            "po": "poho",
        }

        # Gender in 3rd person honorifics
        if self.gender == "male":
            return "pohan"
        elif self.gender == "female":
            return "pohe"

        return honorific_forms.get(self.text, self.text)

    def get_basic_forms(self) -> Dict[str, str]:
        basic_pronouns = {
            # 1st person exclusive
            "1st_excl_sg": "oe",
            "1st_excl_du": "moe",
            "1st_excl_tr": "pxoe",
            "1st_excl_pl": "ayoe",
            # 1st person inclusive
            "1st_incl_du": "oeng",
            "1st_incl_tr": "pxoeng",
            "1st_incl_pl": "ayoeng",  # or "awnga"
            # 2nd person
            "2nd_sg": "nga",
            "2nd_du": "menga",
            "2nd_tr": "pxenga",
            "2nd_pl": "aynga",
            # 3rd person animate
            "3rd_anim_sg": "po",
            "3rd_anim_du": "mefo",
            "3rd_anim_tr": "pxefo",
            "3rd_anim_pl": "ayfo",  # or "fo"
            # 3rd person inanimate
            "3rd_inan_sg": "tsa'u",  # or "tsaw"
            "3rd_inan_du": "mesa'u",
            "3rd_inan_tr": "pxesa'u",
            "3rd_inan_pl": "aysa'u",  # or "sa'u"
            # Special pronouns
            "reflexive": "sno",
            "indeterminate": "fko",
        }
        return basic_pronouns

    def get_gendered_form(self) -> str:
        if (
            self.person == "third"
            and self.number == "singular"
            and self.animacy == "animate"
        ):
            if self.gender == "male":
                return "poan"
            elif self.gender == "female":
                return "poe"
        return self.text

    def get_question_forms(self, gender: str = "common") -> Dict[str, str]:
        # Who
        question_forms = {
            "common": {
                "singular": ["pesu", "tupe"],
                "dual": ["pemsu", "mesupe"],
                "trial": ["pepxsu", "pxesupe"],
                "plural": ["paysu", "aysupe"],
            },
            "male": {
                "singular": ["pestan", "tutampe"],
                "dual": ["pemstan", "mestampe"],
                "trial": ["pepxstan", "pxestampe"],
                "plural": ["paystan", "aystampe"],
            },
            "female": {
                "singular": ["peste", "tutepe"],
                "dual": ["pemste", "mestepe"],
                "trial": ["pepxste", "pxestepe"],
                "plural": ["payste", "aystepe"],
            },
        }
        return question_forms.get(gender, question_forms["common"])

    def make_short_plural(self) -> str:
        # short plural form (ay+ with lenition)
        if self.text in ["po", "fo"]:
            return self._apply_lenition("ay" + self.text)
        return "ay" + self.text

    def _apply_lenition(self, word: str) -> str:

        lenition_rules = {
            "px": "p",
            "tx": "t",
            "kx": "k",
            "p": "p",
            "t": "t",
            "k": "k",
        }
        for from_sound, to_sound in lenition_rules.items():
            if word.startswith(from_sound):
                return to_sound + word[len(from_sound) :]
        return word

    def get_lahe_forms(self) -> Dict[str, str]:
        # Lahe is a big exeption
        lahe_forms = {
            "full": {
                "subjective": "aylahe",
                "agentive": "aylahel",
                "patientive": "aylaheti",
                "dative": "aylaheru",
                "genitive": "aylaheyä",
                "topical": "aylaheri",
            },
            "short": {
                "subjective": "ayla",
                "agentive": "aylal",
                "patientive": "aylat",
                "dative": "aylar",
                "genitive": "ayleyä",  # irregular vowel change
                "topical": "aylari",
            },
        }
        return lahe_forms

    @property
    def is_animate(self) -> bool:
        return self.animacy == "animate"

    @property
    def is_inclusive(self) -> bool:
        return self.inclusivity == "inclusive"

    @property
    def has_short_form(self) -> bool:
        short_form_pronouns = ["ayoeng", "ayfo", "aysa'u"]
        return self.text in short_form_pronouns

    def get_short_form(self) -> str:
        short_forms = {"ayoeng": "awnga", "ayfo": "fo", "aysa'u": "sa'u"}
        return short_forms.get(self.text, self.text)


class NaviVerb(NaviWord):
    """It describes verb in Na'vi: infixes and transitivity"""

    def __init__(
        self,
        text: str,
        position: int = 0,
        transitivity: str = "transitive",
        is_compound: bool = False,
    ):
        super().__init__(text, position)
        self.transitivity = transitivity
        self.is_compound = is_compound

    def add_infix(
        self,
        pre_first: Optional[str] = None,
        first: Optional[str] = None,
        second: Optional[str] = None,
    ) -> str:
        """
        Add infixes to verb
        pre_first: eyk, äp (causative, reflexive)
        first: iv, er, ol, us, awn (tense, aspect, mood, participles)
        second: ei, äng, ats (affect, evidence)
        """
        result = self.text

        syllables = self._split_syllables(result)

        if pre_first and len(syllables) >= 2:
            result = self._insert_infix(result, pre_first, -2)

        if first:
            result = self._insert_infix(result, first, -2)

        if second:
            result = self._insert_infix(result, second, -1)

        return result

    def _split_syllables(self, word: str) -> List[str]:
        vowels = "aeiìouä"
        syllables = []
        current = ""

        for char in word:
            current += char
            if char in vowels:
                syllables.append(current)
                current = ""

        if current:
            if syllables:
                syllables[-1] += current
            else:
                syllables.append(current)

        return syllables

    def _insert_infix(self, word: str, infix: str, syllable_index: int) -> str:

        syllables = self._split_syllables(word)

        if abs(syllable_index) > len(syllables):
            syllable_index = -1 if syllable_index < 0 else 0

        target_syllable = syllables[syllable_index]

        for i, char in enumerate(target_syllable):
            if char in "aeiìouä":
                new_syllable = target_syllable[:i] + infix + target_syllable[i:]
                syllables[syllable_index] = new_syllable
                break

        return "".join(syllables)

    def make_participle(self, voice: str = "active") -> str:

        if voice == "active":
            return self.add_infix(first="us")
        else:  # passive
            return self.add_infix(first="awn")

    def make_causative(self) -> str:
        return self.add_infix(pre_first="eyk")

    def make_reflexive(self) -> str:
        return self.add_infix(pre_first="äp")

    @property
    def is_transitive(self) -> bool:
        return self.transitivity == "transitive"


class NaviAdjective(NaviWord):
    """It describes adjective in Na'vi: attribution and comparison"""

    def __init__(
        self,
        text: str,
        position: int = 0,
        derived_with_le: bool = False,
        is_color: bool = False,
    ):
        super().__init__(text, position)
        self.derived_with_le = derived_with_le
        self.is_color = is_color

    def make_attributive(self, position: str = "before") -> str:
        """
        Create attributive form with suffix -a-
        position: 'before' or 'after' noun
        """
        if self.derived_with_le and position == "after":
            return self.text
        else:
            if self.text.endswith("a"):
                return self.text  # apxa tute, not apxaa tute
            return self.text + "a"

    def make_adverb(self) -> str:
        return "ni" + self.text

    def make_comparative(
        self, comparison: str = "standard", compared_to: Optional[str] = None
    ) -> str:
        if comparison == "standard":
            return f"to {compared_to}" if compared_to else "to"
        elif comparison == "superlative":
            return "frato"
        elif comparison == "equality":
            return f"niftxan {self.text} na {compared_to}"
        return self.text

    def make_color_noun(self) -> str:
        if self.is_color:
            if self.text.endswith("n"):
                return self.text[:-1] + "mpin"  # nasal assimilation
            return self.text + "pin"
        return self.text


class NaviNumber(NaviWord):
    """Na'vi number - octal, or base eight, number system.
    The numbers are calculated from (m × 8) + n formula"""

    def __init__(self, text: str, position: int = 0, value: Optional[int] = None):
        super().__init__(text, position)
        self.value = value

    def get_cardinal(self) -> str:

        numbers = {
            1: "'aw",
            2: "mune",
            3: "pxey",
            4: "tsing",
            5: "mrr",
            6: "pukap",
            7: "kinä",
            8: "vol",
        }
        if self.value and self.value in numbers:
            return numbers[self.value]
        return self.text

    def get_ordinal(self) -> str:

        cardinal = self.get_cardinal()
        stem_changes = {
            "'aw": "'aw",
            "mune": "mu",
            "pxey": "pxey",
            "tsing": "tsi",
            "mrr": "mrr",
            "pukap": "pu",
            "kinä": "ki",
            "vol": "vol",
        }
        stem = stem_changes.get(cardinal, cardinal)
        return stem + "ve"

    def get_fraction(self) -> str:

        if self.value == 2:
            return "mawl"  # half
        elif self.value == 3:
            return "pan"  # third

        ordinal_stem = self.get_ordinal()[:-2]  # remove -ve
        return ordinal_stem + "pxi"

    def make_adverbial(self) -> str:
        """Create adverbial form with alo (time, turn)"""
        if self.value == 1:
            return "'awlo"  # once
        elif self.value == 2:
            return "melo"  # twice
        elif self.value == 3:
            return "pxelo"  # three times
        else:
            return f"alo a{self.get_cardinal()}"  # 4 and more


class NaviParticle(NaviWord):
    """It describes particle in Na'vi"""

    def __init__(self, text: str, position: int = 0, particle_type: str = "general"):
        super().__init__(text, position)
        self.particle_type = (
            particle_type  # 'question', 'focus', 'vocative', 'negative'
        )

    def use_in_context(self, context: str) -> str:
        """Use particle in context"""
        if self.particle_type == "question":
            return f"{self.text} {context}"
        elif self.particle_type == "vocative":
            return f"ma {context}"
        elif self.particle_type == "negative":
            return f"{context} {self.text}"
        else:
            return f"{context} {self.text}"

    def is_question_particle(self) -> bool:
        return self.particle_type == "question"

    def is_vocative(self) -> bool:
        return self.particle_type == "vocative"


class NaviPrenoun(NaviWord):
    """It describes prenoun in Na'vi (adjective-like noun prefixes)"""

    def __init__(self, text: str, position: int = 0, prenoun_type: str = "deictic"):
        super().__init__(text, position)
        self.prenoun_type = prenoun_type  # 'deictic', 'question', 'universal'

    def combine_with_noun(self, noun: str) -> str:
        # Vowel contraction: tsa- + atan -> tsatan
        if self.text.endswith("a") and noun.startswith("a"):
            return self.text[:-1] + noun
        return self.text + noun

    def causes_lenition(self) -> bool:
        leniting_prenouns = ["pe"]  # pe+ causes lenition
        return any(self.text.startswith(p) for p in leniting_prenouns)

