"""Public, editable interview prompts for the manager's data-only theme format."""
import json
from urllib.parse import urlencode
from content_policy import POLICY_PROMPT, validate_content
from system_info import system_target, format_system_info, validate_system_info

PROMPTS = {
    "new": ("Uusi oma teema", "Haluan suunnitella uuden oman tumman Ubuntu-väriteeman."),
    "variant": ("Hiilin uusi väriversio", "Haluan uuden väri- ja kuvakeversion Hiili-teemasta ChatGPT Ubuntu Theme Manageriin."),
    "ubuntu": ("Oma Ubuntu Dark", "Haluan oman Ubuntu Dark -tulkinnan: Ubuntuun sopiva tumma teema, jossa voidaan käyttää oranssia ja munakoison sävyjä. Kysy kuitenkin ensin oma makuni ja anna minun valita värit."),
}


def build_prompt(kind="new", target=None, system_details=None):
    _title, goal = PROMPTS[kind]
    target = " ".join(str(target or system_target()).split())[:160]
    validate_content({"target": target})
    environment = ""
    if system_details is not None:
        details = validate_system_info(system_details)
        for value in details.values():
            validate_content({"target": value})
        environment = ("\nKoneelta haetut teeman yhteensopivuustiedot (asennettujen pakettien versiot):\n"
                       + format_system_info(details)
                       + "\nKäytä näitä kohdeympäristön versiotietoina. Tuntematon tarkoittaa, ettei tietoa voitu hakea; älä arvaa puuttuvia versioita.\n")
    example = {
        "format": "chatgpt-ubuntu-theme",
        "version": 1,
        "id": "metsayo",
        "name": "Metsäyö",
        "description": "Musta metsänvihreä pohja ja hillityt vihreät korostukset",
        "author": "Oma nimi tai nimimerkki",
        "license": "CC0-1.0",
        "target": target,
        "accent": "green",
        "sample": "#264f3d",
        "colors": {
            "#11151a": "#111a15", "#0b0e12": "#0b110d",
            "#171c22": "#1a261e", "#151a20": "#162219",
            "#1e252e": "#25352a", "#191f27": "#203025",
            "#1c232c": "#293b2f", "accent_bg": "#315e45",
            "accent_light": "#b8d8bf", "folder_top": "#3f6650",
            "folder_bottom": "#213a2b", "folder_stroke": "#729d7e",
            "glyph": "#c2dec9",
        },
    }
    example_json = json.dumps(example, ensure_ascii=False, indent=2)
    return f"""Toimi Linux-työpöytäteemojen värisuunnittelijana. Keskustele kanssani suomeksi.

Tavoite: {goal}
Kohdeympäristön lähtötieto: {target}. Voin tehdä paletin myös toiselle Ubuntu-versiolle. Tämä on julkinen versiotieto, ei laitteen tai käyttäjän tunniste.
{environment}

{POLICY_PROMPT}

ALOITA KYSYMÄLLÄ, älä vielä tee teemaa tai koodia. Esitä ensimmäisessä vastauksessa nämä neljä helppoa kysymystä ja odota vastauksiani:
1. Haluanko lähes mustan vai tummanharmaan pohjan, ja mikä olisi teeman nimi?
2. Mitä pää- ja korostusvärejä haluan? Anna esimerkkeinä petrooli, luumu, grafiitti, metsänvihreä ja Ubuntu-oranssi. Voin myös pyytää sinua ehdottamaan.
3. Millaista tunnelmaa haluan: pelkistettyä, pehmeää, teknistä, goottilaista vai jotain muuta? Voin liittää mallikuvan.
4. Onko yllä mainittu Ubuntu- ja työpöytäversio oikea vai teenkö teeman toiseen ympäristöön? Jos versio puuttuu, kysy se; älä oleta kaikkien käyttävän samaa Ubuntua.

Vastausteni jälkeen ehdota yhtenäistä tummaa palettia ja näytä värinäytteet. Säilytä tekstin luettavuus: vaalean #f3f6f6-tekstin kontrastin accent_bg-värillä tulee olla vähintään 4,5:1. Kiinteän #e3e8ec-leipätekstin kontrastin jokaista seitsemää #-alkuisten avainten pintaväriä vasten tulee myös olla vähintään 4,5:1. Manageri tarkistaa nämä kontrastit tuonnissa. Pidä seitsemän pintaväriä tummina ja erota pinnat sekä valinta toisistaan. Tässä pakettimuodossa luodaan värit nykyiseen Hiili-pohjaan; GTK-rakenteen, pyöristysten tai uusien kuvakepiirrosten mielivaltainen muuttaminen ja vaalea teema eivät kuulu versioon 1.

TOIMITA TEEMA NYKYISEEN MANAGERIIN, älä tee erillistä sovellusta. ChatGPT Ubuntu Theme Manager 1.2 tai uudempi tuo dataa sisältävän teemapaketin, näyttää sen omassa teemavalikoimassaan ja hoitaa käyttöönoton sekä palautuksen. Teeman tekeminen ei vaadi Codexia, API-avainta tai maksullista rajapintaa.

Pakettimuoto:
- Ensisijainen ladattava tiedosto on <id>.ctm-theme.zip. ZIP-arkiston juuressa on tasan yksi UTF-8-tiedosto nimeltä theme.json, ei ylimääräistä kansiota.
- Jos et voi tehdä ZIP-tiedostoa, toimita ladattava <id>.json samalla sisällöllä. Manageri hyväksyy myös JSON-tiedoston. Jos et voi luoda tiedostoa lainkaan, anna koko JSON yhtenä koodilohkona ja pyydä tallentamaan se .json-tiedostoksi. Älä väitä puuttuvaa tiedostoa tehdyksi.
- Älä toimita .deb-asentajaa, .desktop-tiedostoa, omaa sovelluskuvaketta valikkoon, GUI-ohjelmaa, komentojonoa, Python-koodia, CSS-tiedostoja tai ulkoisia kuvia. Älä anna sudo-komentoja. Manageri luo GTK 3-, GTK 4-, GNOME Shell-, kuvake- ja taustakuvavärit paikallisesti Hiili/Yaru-pohjastaan.
- Kaikki alla olevan esimerkin 11 ylimmän tason kenttää tarvitaan; muita kenttiä ei sallita. format on aina "chatgpt-ubuntu-theme" ja version on numero 1.
- id on 3–40 merkkiä: alkaa pienellä a–z-kirjaimella ja sisältää vain pieniä a–z-kirjaimia, numeroita tai yhdysmerkkejä. Käytä uudelle teemalle yksilöllistä tunnistetta. Varatut tunnisteet ovat hiili, graphite, petrol, plum ja ubuntu.
- name on 1–80, description 0–600, author 0–120, license 1–128 ja target 0–160 merkkiä. Ne ovat tavallista yhden rivin tekstiä ilman ohjausmerkkejä. Valitse oman uuden paletin lisenssi, esimerkiksi CC0-1.0, ja kysy tekijän nimi tai nimimerkki tarvittaessa.
- target kertoo tarkoitetun Ubuntu/GNOME-ympäristön. Se on ohjetieto, ei väite testatusta yhteensopivuudesta.
- accent on yksi GNOME-korostusvärin nimistä: blue, teal, green, yellow, orange, red, pink, purple, slate.
- sample ja jokainen colors-arvo on tarkalleen #rrggbb-hexväri. colors sisältää täsmälleen esimerkin 13 avainta; älä nimeä avaimia uudelleen tai lisää muita.
- Seitsemän #-alkuista colors-avainta ovat alkuperäisen Hiili-pohjan korvattavia pintavärejä. accent_bg ja accent_light värittävät korostuksia. folder_top, folder_bottom ja folder_stroke värittävät kansioita; glyph värittää kuvakkeiden piirtoja. sample on teemavalikon värinäyte.

Täydellinen kelvollinen esimerkki; korvaa sen nimi, tunniste ja värit toiveideni mukaan:
```json
{example_json}
```

Tarkista JSON-syntaksi, avaimet, väriarvot ja kontrasti käytettävissä olevilla työkaluilla. Anna lyhyt suomenkielinen ohje: avaa ChatGPT Ubuntu Theme Manager → Tuo teema → valitse toimitettu ZIP/JSON → valitse uusi teema → Ota valittu teema käyttöön. Kuvakkeet saavat paletin värit automaattisesti, ja taustakuvan vaihtamisen voi valita managerissa.

Väripaletti voidaan käyttää eri Ubuntu/GNOME-versioissa, jos manageri ja sen vaatimat GTK-, libadwaita-, Yaru- ja GNOME Shell -osat ovat kyseisessä ympäristössä yhteensopivia. Manageri käyttää koneen omaa Yaru-pohjaa. Pelkkä target-kenttä ei tee managerin asentajasta tai Shell-tyyleistä yhteensopivia vanhemman version kanssa. Älä lupaa testaamatonta toimivuutta; kerro täsmällisesti mitä testasit ja mikä jää kohdekoneella tarkistettavaksi.

Aloita nyt vain neljästä kysymyksestä ja odota vastauksiani."""


def chatgpt_url(kind="new", target=None, system_details=None):
    # Sign-in can discard query text; the GUI also copies the public prompt.
    return "https://chatgpt.com/?" + urlencode({"q": build_prompt(kind, target, system_details)})
