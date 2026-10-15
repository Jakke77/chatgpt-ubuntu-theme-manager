# ChatGPT Ubuntu Theme Manager 1.2.2

Teeman kohdejärjestelmän vieressä on nyt **Hae koneen tiedot** -painike. Se täyttää Ubuntu- ja GNOME-version koneesta, näyttää tarkistettavan versiotietoraportin ja liittää samat tiedot paikallista konetta varten tehtävään ChatGPT-promptiin. Raportin voi myös kopioida erikseen.

**Julkaistu sellaisenaan, käyttö omalla vastuulla.** Ohjelma jaetaan ilman takuuta GPL-3.0-or-later-lisenssin mukaisesti. Jatkuvaa ylläpitoa, tukea, virhekorjauksia tai tulevaa yhteensopivuutta ei luvata. Projektia saa haarauttaa ja jatkaa lisenssin ehdoilla. [Tukikäytäntö](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.2/SUPPORT.md).

## Asenna tai päivitä

Lataa **`chatgpt-ubuntu-theme-manager_1.2.2_all.deb`**, sulje mahdollinen vanha manageri ja avaa paketti kaksoisnapsauttamalla. Asennusohjelma voi pyytää salasanaa. Vaihtoehtoisesti aja ladatun paketin hakemistossa:

```bash
sudo apt install ./chatgpt-ubuntu-theme-manager_1.2.2_all.deb
```

Päivitys säilyttää nykyisen ulkoasun ja alkuperäisen palautuskopion. Ensiasennus yrittää ottaa Hiili-ulkoasun käyttöön aktiiviselle paikalliselle työpöytäkäyttäjälle. Tekninen pakettinimi on `hiili-theme`, jotta aiemmat versiot päivittyvät samana pakettina.

## Muutokset

- **Hae koneen tiedot** päivittää **Teeman kohdejärjestelmä** -kentän koneen Ubuntu- ja GNOME-versiosta.
- Painikkeen alla näkyvä raportti sisältää käyttöjärjestelmän, GNOME Shellin, GTK 4:n, libadwaitan, Yarun GTK-, Shell- ja kuvakepakettien sekä managerin versiot ja istuntotyypin (Wayland/X11). Puuttuva tieto merkitään raporttiin.
- **Kopioi tiedot** kopioi pelkän näkyvän raportin tavallisena tekstinä.
- Koko promptin kopiointipainike ja **Tee uusia teemoja ChatGPT:llä** käyttävät samaa valmista promptia ja samaa haettua raporttia. Uusi haku päivittää raportin; painikkeiden välillä tietoja ei haeta huomaamatta uudelleen.
- Kohdekenttää voi edelleen muokata toista Ubuntu-versiota varten. Paikallisen koneen raportti liitetään promptiin vain, kun kenttä vastaa haettua kohdetta. Muulla kohteella raportti jää katseltavaksi ja erikseen kopioitavaksi mutta jätetään pois promptista. Käyttöliittymä kertoo tästä.
- Uusi **Hae koneen tiedot** palauttaa kohdekenttään tämän koneen version ja päivittää raportin.

Tietojen haku on paikallinen lukutoiminto. Se ei tarvitse verkkopalvelua, API-avainta tai järjestelmänvalvojan salasanaa. Raporttiin ei kerätä käyttäjätunnusta, kotihakemistoa, koneen nimeä, laitteistotunnisteita tai verkkotietoja. Käyttäjä voi tarkistaa tiedot ennen niiden lähettämistä ChatGPT:lle.

Selaimen kirjautumista ja promptin lähettämistä koskeva toimintatapa säilyy: manageri avaa verkkosivun ja kopioi promptin, mutta käyttäjä tarkistaa ja lähettää viestin itse. Jos teksti puuttuu keskustelun kentästä, sen voi liittää leikepöydältä.

## Aiemmat ominaisuudet ja sisältörajaus

Viisi valmista ulkoasua, väripalettien tuonti samaan manageriin ja aiemman ulkoasun palautus säilyvät mukana. Myös version 1.2.1 yleiskäyttöön sopiva prompttiohje ja teemapakettien paikallinen metatietotarkistus säilyvät. Tarkistus voi erehtyä eikä takaa lainmukaisuutta tai hallitse erillistä ChatGPT-keskustelua. Katso [sisältölinjaus](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.2/CONTENT_POLICY.md).

Teemapaketin versio 1 sisältää edelleen vain 13 väriä ja lyhyet metatiedot. Se ei sisällä ohjelmakoodia, vapaata CSS:ää, kuvia tai omia sovellusvalikon käynnistimiä. Tiedostomuoto ja GPL-lisenssi säilyvät ennallaan.

## Yhteensopivuus ja tarkistukset

Version 1.2.2 tarkistukset Ubuntu 26.10 / GNOME 51 -ympäristössä:

- 13 versiotietojen ja promptin testiä sekä aiemmat 16 sisältötarkistuksen
  ja 22 teemapaketin testiä läpäisivät (yhteensä 51). Mukana ovat puuttuvat
  paketit, osittainen kyselytulos, aikakatkaisu, virheelliset versiot,
  yksityisten lisäkenttien torjunta sekä raportin tarkka URL-vastaavuus.
- Rakennetun paketin graafisessa kokeessa Hae koneen tiedot päivitti kentän
  ja raportin. Kopioi tiedot kopioi näkyvän raportin. Koko promptin leikepöytä
  ja ChatGPT-linkki sisälsivät saman haetun raportin. Toisen Ubuntu-version
  kirjoittaminen jätti tämän koneen raportin pois, ja uusi haku palautti sen.
- Samassa yksityisessä Xvfb/dconf-istunnossa teeman tuonti, sisältörajaus,
  käyttöönotto ja aiemman ulkoasun palautus toimivat. Tiedostovalitsin ja
  ulkoisen selaimen avaus korvattiin hallituilla vastauksilla; verkkokeskusteluun
  ei lähetetty viestiä.
- Integraatio-, GTK 3/GTK 4/GNOME Shell -tyyli- ja asennuskoukkutarkistukset
  läpäisivät. Järjestelmänvalvojan oikeuksilla tehtävää asennusta ja muita
  Ubuntu-versioita ei ajettu. Todellisen koneen versiot luettiin paikallisesti.

Projektin testiympäristö on **Ubuntu 26.10 / GNOME 51**. Versiotietoraportti auttaa promptin kohdentamisessa; sen saaminen tai kohdekentän muuttaminen ei osoita managerin tai syntyvän teeman toimivan toisessa ympäristössä.

**Ubuntu 26.04** täyttää kirjastovaatimukset, mutta sitä ei ole testattu. **Ubuntu 24.04 ei ole tuettu** nykyisellä paketilla. Vaatimukset: GTK 4 ≥ 4.18, libadwaita ≥ 1.6 sekä Ubuntu/GNOME/Yaru-osat. Tämä ei ole Kubuntun tai Xubuntun teemanhallinta.

Rakennus- ja tarkistuskomennot ovat [TESTING.md](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.2/TESTING.md)-tiedostossa. Aiemman 1.2.1-julkaisun todennetut tarkistukset säilyvät [käyttöohjeessa](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.2/README.fi.md#julkaisun-tarkistukset) ja [muutoshistoriassa](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.2/CHANGELOG.fi.md).

## Lataukset

- `chatgpt-ubuntu-theme-manager_1.2.2_all.deb`: asennus tai päivitys.
- `Metsayo.ctm-theme.zip` tai `Metsayo.theme.json`: sama esimerkkipaletti; tuo vain toinen managerin **Tuo teema…** -painikkeella.
- `chatgpt-ubuntu-theme-manager-1.2.2-source.tar.gz`: lähdekoodi.
- `chatgpt-ubuntu-theme-manager-1.2.2-jakopaketti.zip`: koko jakopaketti ohjeineen.

[Käyttöohje ja lähdekoodi](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/tree/v1.2.2) · [Teemapaketin tiedostomuoto](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.2/THEME_FORMAT.fi.md)

Version 1.2.2 adds a local system-information button, a visible plain-text report and a separate copy action. The report includes Ubuntu, GNOME, GTK 4, libadwaita, Yaru and manager versions plus the Wayland/X11 session type. Both prompt actions include the same displayed report only when the target still matches the detected machine. Editing the target for another system excludes the host report. No user name, home directory, host name, hardware identifiers or network information is collected. No API or telemetry is used.

Unofficial community project; not an OpenAI or Canonical product. **Provided as is, without warranty under GPL-3.0-or-later. Use at your own risk; no ongoing maintenance or future compatibility is promised.**
