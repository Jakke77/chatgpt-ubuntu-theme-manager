# ChatGPT Ubuntu Theme Manager 1.2.1

Tämä päivitys lisää yleiskäyttöön sopivan sisältörajauksen ChatGPT-promptteihin ja teemapakettien metatietojen paikalliseen validointiin. Nykyiset viisi ulkoasua, väripalettien tuonti samaan manageriin ja aiemman ulkoasun palautus säilyvät mukana.

**Julkaistu sellaisenaan, käyttö omalla vastuulla.** Ohjelma jaetaan ilman takuuta GPL-3.0-or-later-lisenssin mukaisesti. Jatkuvaa ylläpitoa, tukea, virhekorjauksia tai tulevaa yhteensopivuutta ei luvata. Projektia saa haarauttaa ja jatkaa lisenssin ehdoilla. [Tukikäytäntö](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.1/SUPPORT.md).

## Asenna tai päivitä

Lataa **`chatgpt-ubuntu-theme-manager_1.2.1_all.deb`**, sulje mahdollinen vanha manageri ja avaa paketti kaksoisnapsauttamalla. Asennusohjelma voi pyytää salasanaa. Vaihtoehtoisesti aja ladatun paketin hakemistossa:

```bash
sudo apt install ./chatgpt-ubuntu-theme-manager_1.2.1_all.deb
```

Päivitys säilyttää nykyisen ulkoasun ja alkuperäisen palautuskopion. Ensiasennus yrittää ottaa Hiili-ulkoasun käyttöön aktiiviselle paikalliselle työpöytäkäyttäjälle. Tekninen pakettinimi on `hiili-theme`, jotta aiemmat versiot päivittyvät samana pakettina.

## Muutokset

- ChatGPT:n aloituspromptit pyytävät yleiskäyttöön sopivaa teemaa. Ne rajaavat pois huijaukset, identiteettivarkauden ja harhaanjohtavan toisena esiintymisen, hyväksikäytön, pornografian, vihasisällön ja raa'an väkivallan.
- Paikallinen deterministinen tarkistus käy läpi teeman `id`-, `name`-, `description`-, `author`-, `license`- ja `target`-kentät. URL-osoitteet, merkkauskieli ja tunnistettuihin kiellettyihin aiheisiin viittaavat ilmaukset hylätään.
- Tarkistus koskee uuden teeman tuontia, omien teemojen valikoiman lukua ja käyttöönottoa sekä ikkunasta että komentoriviltä.
- Aiemmin tuotu, nyt tarkistuksessa hylätty paletti jää pois omien teemojen valikoimasta. Sen tiedostoja ei poisteta, ja aiemman ulkoasun palautus pysyy käytettävissä.
- Tavalliset synkät, goottilaiset ja kauhuun viittaavat tyylit, kallot, Pride ja muu identiteetin ilmaisu, ei-seksuaalinen taide sekä tavallinen brändiväreistä saatu inspiraatio ovat sallittuja.
- Uusi [sisältölinjaus](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.1/CONTENT_POLICY.md) kertoo tarkistuksen toiminnan, esimerkit ja rajat. Se ei muuta GPL-lisenssin myöntämiä oikeuksia.

Tarkistus ei tarvitse verkkoyhteyttä, API-avainta tai maksullista moderointipalvelua eikä lisää telemetriaa. Selaimen avauksen ja promptin kopioinnin toimintatapaa ei muuteta tässä päivityksessä.

## Sisältörajauksen käytännön rajat

Tämä on metatietosuodatin, ei yleinen sisällöntunnistin tai lainmukaisuuden tae. Kieli, kirjoitusasun muunnelmat ja asiayhteys voivat aiheuttaa sekä vääriä hylkäyksiä että tunnistamatta jäävää sisältöä. Väärin hylätyn tavallisen teeman metatiedot voi muotoilla selkeästi ja neutraalisti kuvaamaan itse väripalettia.

Teemapaketin versio 1 sallii edelleen vain 13 väriä ja lyhyet metatiedot. Se ei tue ulkoisia kuvia, logoja, vapaata CSS:ää, HTML-sivuja, kirjautumislomakkeita, skriptejä tai erillisiä sovellusvalikon käynnistimiä. Manageri ei hallitse erillisessä verkkopalvelussa käytävää ChatGPT-keskustelua tai avoimen lähdekoodin muokattuja versioita.

## Yhteensopivuus ja tarkistukset

Version 1.2.1 tarkistukset Ubuntu 26.10 / GNOME 51 -ympäristössä:

- 16 paikallisen sisältötarkistuksen testiä ja 22 teemapaketin validointitestiä
  läpäisivät. Mukana ovat estetyt ilmaukset, tavalliset sallitut aiheet,
  Unicode-muunnelmat, kaikki tekstikentät, verkottomuus ja JSON/ZIP-tuonti.
- Integraatiokokeessa käsin hylättäväksi muutettu metadata poistui valikoimasta
  eikä teemaa voinut ottaa uudelleen käyttöön. Sen tiedostot ja alkuperäisen
  ulkoasun palautus säilyivät. Viiden valmiin teeman ja Metsäyön vaihto,
  tiedostojen palautus sekä virhetilanteen peruminen tarkistettiin myös.
- Rakennetun paketin graafisessa kokeessa sisältöohje avautui, hylättävä tuonti
  estettiin ja hylättävä kohdeteksti esti selaimen avauksen. Sallitun teeman
  tuonti, käyttöönotto, palautus sekä URL:n ja leikepöydän vastaavuus toimivat
  yksityisessä Xvfb/dconf-istunnossa. Tiedostovalitsin ja ulkoinen selain
  korvattiin hallituilla vastauksilla; ChatGPT-viestiä ei lähetetty.
- GTK 3-, GTK 4- ja GNOME 51:n Shell-jäsentimet hyväksyivät valmiiden teemojen
  ja tuodun paletin tyylit. Asennuskoukun koe vahvisti päivityksen säilyttävän
  ulkoasun. Järjestelmänvalvojan oikeuksilla tehtävää asennusta tai muita
  Ubuntu-versioita ei kokeiltu.

Nämä kokeet osoittavat määriteltyjen sääntöjen toiminnan testitapauksissa.
Ne eivät osoita kattavaa sisällöntunnistusta tai lainmukaisuutta.

Projektin testiympäristö on **Ubuntu 26.10 / GNOME 51**. Version 1.2.0 aiemmat eristettyjen asetusten tuonti-, käyttöönotto-, palautus- ja käyttöliittymätarkistukset on kuvattu [käyttöohjeessa](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.1/README.fi.md#julkaisun-tarkistukset).

**Ubuntu 26.04** täyttää kirjastovaatimukset, mutta sitä ei ole testattu. **Ubuntu 24.04 ei ole tuettu** nykyisellä paketilla. Vaatimukset: GTK 4 ≥ 4.18, libadwaita ≥ 1.6 sekä Ubuntu/GNOME/Yaru-osat. Tämä ei ole Kubuntun tai Xubuntun teemanhallinta.

## Lataukset

- `chatgpt-ubuntu-theme-manager_1.2.1_all.deb`: asennus tai päivitys.
- `Metsayo.ctm-theme.zip` tai `Metsayo.theme.json`: sama esimerkkipaletti; tuo vain toinen managerin **Tuo teema…** -painikkeella.
- `chatgpt-ubuntu-theme-manager-1.2.1-source.tar.gz`: lähdekoodi.
- `chatgpt-ubuntu-theme-manager-1.2.1-jakopaketti.zip`: koko jakopaketti ohjeineen.

[Käyttöohje ja lähdekoodi](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/tree/v1.2.1) · [Teemapaketin tiedostomuoto](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.1/THEME_FORMAT.fi.md)

Version 1.2.1 adds general-audience prompt boundaries and local checks of theme metadata. This limited filter can produce false positives and false negatives; it does not guarantee legal compliance or control a separate ChatGPT conversation. No network moderation, API key or telemetry is used. Normal gothic themes and identity expression remain allowed. See the content policy for details.

Unofficial community project; not an OpenAI or Canonical product. **Provided as is, without warranty under GPL-3.0-or-later. Use at your own risk; no ongoing maintenance or future compatibility is promised.**
