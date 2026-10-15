# ChatGPT Ubuntu Theme Manager 1.2.0

Tumma teemanhallinta Ubuntu/GNOME-työpöydälle. Omia paletteja voi nyt tuoda managerin samaan valikoimaan ilman erillistä sovelluskuvaketta.

**Julkaistu sellaisenaan, käyttö omalla vastuulla.** Ohjelma jaetaan ilman takuuta GPL-3.0-or-later-lisenssin mukaisesti. Jatkuvaa ylläpitoa, tukea, virhekorjauksia tai tulevaa yhteensopivuutta ei luvata. Projektia saa haarauttaa ja jatkaa lisenssin ehdoilla. [Tukikäytäntö](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.0/SUPPORT.md).

## Asenna

Lataa **`chatgpt-ubuntu-theme-manager_1.2.0_all.deb`**, sulje mahdollinen vanha manageri ja avaa paketti kaksoisnapsauttamalla. Asennusohjelma voi pyytää salasanaa. Vaihtoehtoisesti aja ladatun paketin hakemistossa:

```bash
sudo apt install ./chatgpt-ubuntu-theme-manager_1.2.0_all.deb
```

Päivitys säilyttää nykyisen ulkoasun ja alkuperäisen palautuskopion. Ensiasennus yrittää ottaa Hiili-ulkoasun käyttöön aktiiviselle paikalliselle työpöytäkäyttäjälle. Tekninen pakettinimi on `hiili-theme`, jotta aiemmat versiot päivittyvät samana pakettina.

## Mukana

- Viisi valmista tummaa ulkoasua: Hiili / Musta, Grafiitti, Petrooli, Luumu ja Ubuntu Dark.
- Omien `.ctm-theme.zip`- tai `.json`-palettien tuonti manageriin, esikatselu, käyttöönotto ja palautus.
- Kuvakkeiden sekä haluttaessa taustakuvan väritys valitun paletin mukaan.
- ChatGPT-promptit, jotka kysyvät toiveet ja tuottavat manageriin sopivan teematiedoston. Kohde-Ubuntu/GNOME-version voi muuttaa. Codexia tai API-avainta ei tarvita.
- Metsäyö-esimerkkipaletti: tuo **`Metsayo.ctm-theme.zip`** tai **`Metsayo.theme.json`** managerin **Tuo teema…** -painikkeella; tiedostot sisältävät saman teeman.
- Lähdearkisto sekä koko jakopaketti ohjeineen.

Teemapaketin versio 1 sisältää vain tumman väripaletin ja metatiedot. Vapaa CSS, uudet kuvakepiirrokset, omat taustakuvat ja vaaleat teemat eivät kuulu tähän pakettimuotoon.

## Yhteensopivuus ja tarkistukset

Julkaisun testiympäristö on **Ubuntu 26.10 / GNOME 51**. Validointi, teemojen vaihto ja alkuperäisten asetusten palautus, GTK 3/GTK 4/GNOME Shell -tyylit sekä graafinen tuonti, käyttöönotto ja palautus tarkistettiin erillisillä testiasetuksilla. Graafisessa kokeessa tiedostovalitsin ja selaimen avaus korvattiin hallituilla vastauksilla. ChatGPT-keskusteluun ei lähetetty viestiä. Paketin sisältö ja asennuskoukut tarkistettiin; järjestelmänvalvojan oikeuksilla tehtävää asennusta ei ajettu julkaisun valmistelussa.

**Ubuntu 26.04** täyttää kirjastovaatimukset, mutta sitä ei ole testattu. **Ubuntu 24.04 ei ole tuettu** nykyisellä paketilla. Vaatimukset: GTK 4 ≥ 4.18, libadwaita ≥ 1.6 sekä Ubuntu/GNOME/Yaru-osat. Tämä ei ole Kubuntun tai Xubuntun teemanhallinta.

[Käyttöohje ja lähdekoodi](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/tree/v1.2.0) · [Teemapaketin tiedostomuoto](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.0/THEME_FORMAT.fi.md)

Unofficial community project; not an OpenAI or Canonical product. **Provided as is, without warranty under GPL-3.0-or-later. Use at your own risk; no ongoing maintenance or future compatibility is promised.**
