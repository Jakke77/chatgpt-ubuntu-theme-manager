"""Small, offline metadata checks for the manager's general-audience catalog.

These deliberately narrow Finnish/English rules are a visible guardrail, not a
semantic moderation service, a legal assessment, or a guarantee about intent.
They check text only: palette files contain no supplied images, CSS or code.
No request, rejected content, or personal data is sent away or logged here.
"""

import re
import unicodedata


POLICY_SUMMARY = (
    "Teemat on tarkoitettu yleiskäyttöön. Huijauksia, toisena esiintymistä, "
    "lasten hyväksikäyttöä, pornografiaa, vihasisältöä, terrorismin ihannointia "
    "ja raakaa väkivaltaa ei sallita. Tavalliset synkät, goottilaiset ja omaa "
    "identiteettiä ilmaisevat teemat ovat sallittuja. Paikallinen rajattu "
    "suomen- ja englanninkielinen tekstitarkistus ei tunnista kaikkea sisältöä "
    "eikä takaa lainmukaisuutta."
)

POLICY_PROMPT = (
    "Tee yleiskäyttöön sopiva teema. Älä tuota huijausta, identiteettivarkautta, "
    "toisena henkilönä tai virallisena palveluna esiintymistä, salasanojen "
    "kalastelua, lasten hyväksikäyttöä, pornografiaa, vihasisältöä, terrorismin "
    "ihannointia tai raakaa väkivaltaa. Älä käytä metatiedoissa linkkejä, "
    "HTML:ää tai Markdown-linkkejä. Nimet, kuvaukset, tekijä, lisenssitunnus "
    "ja kohdejärjestelmä ovat pelkkää tekstiä. Synkät ja goottilaiset aiheet "
    "sekä oman identiteetin, uskonnon tai poliittisen näkemyksen tavallinen "
    "ilmaisu ovat sallittuja. Älä väitä paikallista tarkistusta kattavaksi "
    "moderoinniksi tai lainmukaisuuden takeeksi."
)


class ContentPolicyError(ValueError):
    """Metadata matches one of the manager's limited local content rules."""


_FIELDS = ("id", "name", "description", "author", "license", "target")
_DIRECTION_CONTROLS = frozenset("\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069")
_LINK_OR_MARKUP = re.compile(
    r"\b[a-z][a-z0-9+.-]*://|\b(?:mailto|javascript|data):|\bwww\."
    r"|<\s*/?\s*[a-z][^<>]*>|<!--|<!doctype\b|<\?xml\b"
    r"|\[[^\]]*\]\s*\([^)]*\)|\[[^\]]+\]\s*\[[^\]]*\]"
    r"|\[(?:url|img)(?:\s*=|\])",
    re.IGNORECASE,
)


def _normalize(text):
    # Strip format characters for matching, rather than banning scripts that
    # legitimately use joiners. Fold accents too, so "väärennetty" and a
    # trivially accented/zero-width obfuscation are checked alike.
    folded = unicodedata.normalize("NFKC", text).casefold()
    folded = "".join(char for char in folded if unicodedata.category(char) != "Cf")
    folded = "".join(char for char in unicodedata.normalize("NFKD", folded)
                     if unicodedata.category(char) not in ("Mn", "Me"))
    return re.sub(r"\s+", " ", folded)


def _words(text):
    # Treat Unicode dashes, underscores and punctuation as separators; O'Neill
    # remains ordinary text. Word boundaries keep e.g. Pornainen and Sussex.
    return re.sub(r"[\W_]+", " ", text, flags=re.UNICODE).strip()


def _patterns(*patterns):
    return tuple(re.compile(pattern, re.UNICODE) for pattern in patterns)


# Remove only specific educational/prevention phrases before the fraud scan.
# A second, harmful phrase in the same field still gets checked.
_FRAUD_EDUCATION = _patterns(
    r"\bidentity theft (?:prevention|awareness|protection|education)\b",
    r"\b(?:anti|preventing|avoiding|against) identity theft\b",
    r"\banti phishing(?: (?:awareness|education|training))?\b",
    r"\bphishing (?:awareness|prevention|protection|training|education)\b",
    r"\b(?:identiteettivarkauden|identiteettivarkauksien|henkilollisyysvarkauden) "
    r"(?:ehkaisy|ehkaiseminen|torjunta|estaminen)\b",
    r"\b(?:tietojenkalastelun|salasanakalastelun) (?:esto|ehkaisy|torjunta)\b",
)

_FRAUD = _patterns(
    r"\b(?:identity theft|identity stealing|credential theft|credential stealer|"
    r"password theft|password stealer|phishing)\b",
    r"\b(?:steal|harvest|capture) (?:users? |your |their )?(?:passwords?|credentials|bank details)\b",
    r"\b(?:fake|spoofed|fraudulent) (?:bank |government |support )?(?:login|sign in|signin)\b",
    r"\b(?:impersonate|impersonating) (?:a real person|someone else|a bank|the police|official support)\b",
    r"\b(?:pretend|pretending) to be (?:a bank|the police|official support|another person)\b",
    r"\b(?:identiteettivarkaus|identiteettivarkaudet|henkilollisyysvarkaus|"
    r"tietojenkalastelu|salasanakalastelu|toisena esiintyminen)\b",
    r"\b(?:salasanojen|tunnusten|pankkitunnusten) (?:varastaminen|varastaja|kalastelu)\b",
    r"\b(?:salasanoja|pankkitunnuksia) (?:varastava|keraava|kalasteleva)\b",
    r"\b(?:vaarennetty|vale|huijaus) (?:pankin )?(?:kirjautuminen|kirjautumissivu)\b",
    r"\b(?:esiinny|esiintyy|esiintyminen) (?:pankkina|poliisina|virallisena tukena|toisena henkilona)\b",
)

_CHILD_ABUSE = _patterns(
    r"\b(?:child pornography|child porn|child sexual abuse|child sexual exploitation|"
    r"sexualized children|sexualised children|sexualized child|sexualised child|"
    r"csam|lolicon|shotacon)\b",
    r"\b(?:lapsiporno\w*|(?:lapsen|lasten|alaikaisen|alaikaisten) "
    r"(?:seksuaalinen hyvaksikaytto|seksuaalinen riisto|seksualisointi))\b",
)

_SEXUAL_EXPLICIT = _patterns(
    r"\b(?:porn|porno|pornography|pornographic)(?:theme|teema)?\b",
    r"\b(?:anal sex|oral sex|explicit sexual acts|explicit sexual content|"
    r"blowjob|handjob|cumshot|gangbang|rape porn|incest porn)\b",
    r"\b(?:pornoteema|pornografia|pornografinen|sukupuoliyhdynta|"
    r"seksikohtaus|seksikohtaukset|suuseksi|anaaliseksi)\b",
)

_GROUP = (
    r"(?:muslims?|jews?|christians?|immigrants?|refugees?|gays?|lesbians?|"
    r"trans people|transgender people|black people|white people|asians?|"
    r"muslimit|juutalaiset|kristityt|maahanmuuttajat|pakolaiset|homot|lesbot|"
    r"transihmiset|mustat|valkoiset)"
)
_GROUP_PARTITIVE = (
    r"(?:muslimit|juutalaiset|kristityt|maahanmuuttajat|pakolaiset|homot|lesbot|"
    r"transihmiset|mustat|valkoiset)"
)
_HATE = _patterns(
    r"\b(?:nigger|niggers|faggot|faggots|kike|kikes|neekeri|neekerit|mutiainen|mutiaiset)\b",
    r"\b(?:white supremacy|racial supremacy|ethnic cleansing|valkoinen ylivalta|rotupuhtaus|etninen puhdistus)\b",
    rf"\b(?:kill|exterminate|eliminate) (?:all |the |all the )?{_GROUP}\b",
    rf"\bdeath to (?:all |the |all the )?{_GROUP}\b",
    rf"\b{_GROUP} (?:must die|should die|must be killed|should be killed)\b",
    rf"\b(?:tapa|tappakaa|tuhoa|tuhotkaa) (?:kaikki )?{_GROUP_PARTITIVE}\b",
    rf"\b{_GROUP_PARTITIVE} (?:pitaa|taytyy|tulee) (?:tappaa|tuhota|havittaa)\b",
)

_TERROR_PRAISE = _patterns(
    r"\b(?:heil hitler|sieg heil|glory to isis|glory to isil|long live isis|"
    r"join isis|support isis|praise al qaeda|glory to al qaeda)\b",
    r"\b(?:kunnia isisille|elakoon isis|liity isisiin|tue isisia|elakoon hitler)\b",
)

_GRAPHIC_VIOLENCE = _patterns(
    r"\b(?:graphic gore|graphic violence|gore porn|dismembered bodies|"
    r"decapitated bodies|mutilated corpses|disembowelment|torture victims)\b",
    r"\b(?:raaka vakivalta|raakaa vakivaltaa|veriset sisaelimet|"
    r"irtileikatut paat|silvotut ruumiit|silpominen|kidutusuhrit)\b",
)


def _reject(field, category):
    # Always use fixed field/category strings; never echo rejected metadata.
    raise ContentPolicyError(
        f"Teeman kenttä {field} ei sovi yleiskäyttöiseen teemavalikoimaan "
        f"({category})."
    )


def validate_content(metadata):
    """Raise ContentPolicyError on a limited local rule match; otherwise None.

    Call after structural manifest validation. This function does not mutate the
    supplied metadata and intentionally does not inspect colors as content.
    """
    for field in _FIELDS:
        value = metadata.get(field, "")
        if not isinstance(value, str):
            # Structural validation owns type/bounds errors, but fail closed if
            # the content guard is accidentally called before that validation.
            _reject(field, "virheellinen tekstikenttä")
        if any(char in _DIRECTION_CONTROLS or
               unicodedata.category(char) in ("Cc", "Cs", "Zl", "Zp")
               for char in value):
            _reject(field, "harhaanjohtava muotoilu tai ohjausmerkki")
        normalized = _normalize(value)
        if _LINK_OR_MARKUP.search(normalized):
            _reject(field, "linkki tai merkintäkieli")
        words = _words(normalized)
        fraud_words = words
        for rule in _FRAUD_EDUCATION:
            fraud_words = rule.sub(" ", fraud_words)
        if any(rule.search(fraud_words) for rule in _FRAUD):
            _reject(field, "huijaus tai toisena esiintyminen")
        for category, rules in (
            ("lasten hyväksikäyttö", _CHILD_ABUSE),
            ("pornografia tai seksuaalisesti eksplisiittinen sisältö", _SEXUAL_EXPLICIT),
            ("vihasisältö tai väkivaltaan yllyttäminen", _HATE),
            ("terrorismin tai natsismin ihannointi", _TERROR_PRAISE),
            ("raaka väkivalta", _GRAPHIC_VIOLENCE),
        ):
            if any(rule.search(words) for rule in rules):
                _reject(field, category)
