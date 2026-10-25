"""Shared palette catalog for the GTK, Shell, icon and wallpaper variants."""
import re

VERSION = "1.2.4"
APP_NAME = "ChatGPT Ubuntu Theme Manager"
PALETTES = {
    "hiili": {"name": "Hiili / Musta", "theme": "Hiili", "accent": "teal", "sample": "#11151a",
              "description": "Alkuperäinen Hiili: lähes musta ja hillitty petrooli", "colors": {}},
    "graphite": {"name": "Grafiitti", "theme": "Hiili-Grafiitti", "accent": "slate", "sample": "#30343a",
                 "description": "Neutraalit harmaat ja hopeiset korostukset",
                 "colors": {"#11151a": "#151719", "#0b0e12": "#101113", "#171c22": "#202326", "#151a20": "#1a1d20", "#1e252e": "#292d31", "#191f27": "#25292d", "#1c232c": "#2b3035", "accent_bg": "#535e68", "accent_light": "#c4cbd2", "folder_top": "#4a535e", "folder_bottom": "#2a313a", "folder_stroke": "#72808c", "glyph": "#ced4db"}},
    "petrol": {"name": "Petrooli", "theme": "Hiili-Petrooli", "accent": "teal", "sample": "#315e65",
               "description": "Tummat sinivihreät pinnat ja petrooliset korostukset",
               "colors": {"#11151a": "#0e171b", "#0b0e12": "#091114", "#171c22": "#15242a", "#151a20": "#122025", "#1e252e": "#1b3037", "#191f27": "#182b32", "#1c232c": "#1d333b", "accent_bg": "#356e75", "accent_light": "#a4d2d1", "folder_top": "#386c74", "folder_bottom": "#1c3a45", "folder_stroke": "#668f99", "glyph": "#b2d7d9"}},
    "plum": {"name": "Luumu", "theme": "Hiili-Luumu", "accent": "purple", "sample": "#67465f",
             "description": "Luumun ja munakoison sävyt mustalla pohjalla",
             "colors": {"#11151a": "#191219", "#0b0e12": "#100c12", "#171c22": "#271c29", "#151a20": "#211823", "#1e252e": "#332438", "#191f27": "#2d2031", "#1c232c": "#35263b", "accent_bg": "#76516f", "accent_light": "#d9b6d5", "folder_top": "#694b69", "folder_bottom": "#39273e", "folder_stroke": "#9c7a9c", "glyph": "#ddc0dc"}},
    "ubuntu": {"name": "Ubuntu Dark", "theme": "Hiili-UbuntuDark", "accent": "orange", "sample": "#c6532d",
               "description": "Ubuntun oranssi ja munakoiso tummana Hiili-tulkintana",
               "colors": {"#11151a": "#181418", "#0b0e12": "#100d11", "#171c22": "#282029", "#151a20": "#211a23", "#1e252e": "#342935", "#191f27": "#2d232e", "#1c232c": "#352a37", "accent_bg": "#b64a26", "accent_light": "#f3b597", "folder_top": "#8d512f", "folder_bottom": "#4d2d25", "folder_stroke": "#bb805a", "glyph": "#f1c5a6"}},

    "veriyo": {"name": "Veri Aika · Veriyö", "theme": "Hiili-Veriyo", "accent": "pink", "sample": "#f0788b",
               "description": "Veri Ajan lähes musta, viininpunainen ja ruusunpunainen Otava-taivaan alla",
               "wallpaper": "veriyo-otava.png",
               "colors": {"#11151a": "#070508", "#0b0e12": "#050306", "#171c22": "#160b12",
                          "#151a20": "#10080d", "#1e252e": "#25121c", "#191f27": "#1c0e16",
                          "#1c232c": "#2d1722", "accent_bg": "#92344d", "accent_light": "#f0788b",
                          "folder_top": "#56303c", "folder_bottom": "#160b12", "folder_stroke": "#b8657a",
                          "glyph": "#f5eaf0"}},
}


def all_palettes():
    from theme_packs import catalog
    return {**PALETTES, **catalog()}


def palette(variant="hiili"):
    choices = PALETTES if variant in PALETTES else all_palettes()
    if variant not in choices:
        raise ValueError("Tuntematon ulkoasu: " + variant)
    return choices[variant]


def recolor(text, variant="hiili", icons=False):
    values = palette(variant)["colors"]
    if not values:
        return text
    mapping = {key: value for key, value in values.items() if key.startswith("#")}
    for color in ("#3d5e67", "#476b73", "#496b72", "#547c80", "#344e58", "#344b56", "#344750", "#263c42", "#405e66"):
        mapping[color] = values["accent_bg"]
    for color in ("#a1c3c5", "#779fa4", "#7da7aa", "#7da8a8", "#577a82", "#bad2d2"):
        mapping[color] = values["accent_light"]
    # Extend the shared GTK palette to equivalent Shell and wallpaper shades.
    for source, equivalent in {"#171d24": "#171c22", "#1b222b": "#1e252e", "#151c25": "#11151a", "#141a21": "#11151a", "#1a232d": "#171c22"}.items():
        if equivalent in mapping:
            mapping[source] = mapping[equivalent]
    if icons:
        mapping.update({"#334c58": values["folder_top"], "#1c303c": values["folder_bottom"],
                        "#526c76": values["folder_stroke"], "#4c6672": values["folder_stroke"],
                        "#adc7ce": values["glyph"], "#849fa7": values["glyph"]})
        for color in ("#a9c4ca", "#bcc2d1", "#c0afc4", "#afc3b8"):
            mapping[color] = values["glyph"]
    return re.sub(r"#[0-9a-fA-F]{6}\b", lambda match: mapping.get(match[0].lower(), match[0]), text)


def variant_for_theme(theme):
    return next((key for key, value in all_palettes().items() if value["theme"] == theme), None)
