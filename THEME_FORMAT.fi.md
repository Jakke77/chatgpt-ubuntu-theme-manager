# Managerin teemapaketti, versio 1

ChatGPT Ubuntu Theme Manager 1.2 tai uudempi hyväksyy UTF-8 JSON-tiedoston tai
`.ctm-theme.zip`-arkiston, jonka juuressa on täsmälleen yksi `theme.json`.
Teema lisätään managerin omaan valikoimaan Tuo teema… -painikkeella.

Tämä on tumman väripaletin muoto. Manageri tuottaa GTK 3-, GTK 4-, GNOME Shell-,
kuvake- ja taustakuvatyylit omista Hiili/Yaru-pohjistaan. Pakettiin ei lisätä
CSS:ää, kuvatiedostoja, asennusskriptejä tai .desktop-tiedostoja. Näin jokainen
paletti ei tarvitse omaa sovellusta valikkoon.

Kaikki esimerkin ylimmän tason kentät ja 13 colors-avainta ovat pakollisia;
ylimääräisiä tai toistettuja avaimia ei hyväksytä. `format` ja `version`
pysyvät esimerkin mukaisina. Jokainen väri on `#rrggbb`.

- `id`: 3–40 merkkiä, alkaa pienellä a–z-kirjaimella, sisältää vain pieniä
  a–z-kirjaimia, numeroita ja yhdysmerkkejä. Varatut nimet ovat hiili,
  graphite, petrol, plum ja ubuntu. Uusi versio tarvitsee uuden tunnisteen.
- `name`: 1–80, `description`: 0–600, `author`: 0–120, `license`: 1–128 ja
  `target`: 0–160 merkkiä. Teksti on yhdellä rivillä ilman ohjausmerkkejä.
- `target`: tarkoitettu Ubuntu/GNOME-kohde; ei todistus yhteensopivuudesta.
- `accent`: blue, teal, green, yellow, orange, red, pink, purple tai slate.
- `sample`: managerin teemakortissa näkyvä värinäyte.
- Seitsemän #-alkuista colors-avainta korvaavat Hiili-pohjan pintavärejä.
  `accent_bg` ja `accent_light` värittävät korostukset. `folder_top`,
  `folder_bottom` ja `folder_stroke` värittävät kansiot; `glyph` kuvakkeiden viivat.

Versiosta 1.2.1 alkaen kaikki kuusi tekstikenttää (`id`, `name`,
`description`, `author`, `license`, `target`) ovat tavallista tekstiä ilman
URL-osoitteita tai merkkauskieltä, kuten HTML:ää. Paikalliset sisältösäännöt
tarkistavat nämä kentät ja hylkäävät tunnistamansa huijaus-, identiteettivarkaus-,
harhaanjohtavaan toisena esiintymiseen, hyväksikäyttöön, pornografiaan,
vihasisältöön tai raakaan väkivaltaan liittyvät ilmaukset. Tarkistus ei ole
yleinen luokittelija: kieli, asiayhteys ja kirjoitusasun muunnelmat voivat
aiheuttaa sekä vääriä hylkäyksiä että tunnistamatta jäävää sisältöä.
Tavalliset goottilaiset tyylit, Pride ja muu identiteetin ilmaisu ovat
sallittuja. Katso [sisältörajaus ja esimerkit](CONTENT_POLICY.md).

Sama validointi koskee tuontia, tallennettujen palettien lukua ja
käyttöönottoa. Aiemmin tuodun paletin hylkäys poistaa sen vain valikoimasta,
ei levyltä; aiemman ulkoasun palautus säilyy käytettävissä.

Manageri tarkistaa, että kiinteän leipätekstin `#e3e8ec` kontrasti on vähintään
4,5:1 jokaisella seitsemällä pintavärillä ja että korostuksen tekstin `#f3f6f6`
kontrasti `accent_bg`-värillä on vähintään 4,5:1. Koko teeman jokaisen elementin
saavutettavuutta nämä kaksi tarkistusta eivät yksin takaa.

JSONin enimmäiskoko on 256 KiB ja ZIPin 512 KiB. ZIPin linkit, suoritusbitit,
salaus ja ylimääräiset tiedostot hylätään. Tuonti ei suorita koodia, käytä
sudoa tai ota teemaa heti käyttöön. Jo tuotua tunnistetta ei ylikirjoiteta.

Esimerkki (Metsäyö, CC0-1.0):

```json
{
  "format": "chatgpt-ubuntu-theme",
  "version": 1,
  "id": "metsayo",
  "name": "Metsäyö",
  "description": "Tumma metsä: mustaa, havunvihreää ja pehmeitä vihreitä korostuksia.",
  "author": "Yhteisön esimerkkiteema",
  "license": "CC0-1.0",
  "target": "Ubuntu / GNOME (väripaletti; kohdeversio tarkistetaan erikseen)",
  "accent": "green",
  "sample": "#315447",
  "colors": {
    "#11151a": "#111914",
    "#0b0e12": "#0a100c",
    "#171c22": "#1b261f",
    "#151a20": "#162119",
    "#1e252e": "#26352b",
    "#191f27": "#202e25",
    "#1c232c": "#2b3b30",
    "accent_bg": "#3e6b50",
    "accent_light": "#b4d6bd",
    "folder_top": "#3c6750",
    "folder_bottom": "#1e3828",
    "folder_stroke": "#719e7e",
    "glyph": "#c4ddca"
  }
}
```

Tallenna tämä JSON sellaisenaan `.json`-tiedostoksi tai ZIPin juureen
`theme.json`-nimellä. Avaa manageri → Tuo teema… → valitse tiedosto →
Ota valittu teema käyttöön. Palauta aiempi ulkoasu -painike palauttaa
alkuperäiset asetukset.

Käyttäjän omat paletit tallentuvat XDG_DATA_HOME-hakemiston
`hiili-theme/imported/`-alihakemistoon (oletuksena `~/.local/share/`).
``target``-kentän vaihtaminen ei lisää manageriin tukea vanhalle Ubuntulle.
Ohjelman tämän julkaisun vaatimukset ovat GTK ≥ 4.18 ja libadwaita ≥ 1.6,
sekä Ubuntu/GNOME/Yaru-ympäristö. Toiminta on testattu Ubuntu 26.10:ssä.
