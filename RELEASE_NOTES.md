# ChatGPT Ubuntu Theme Manager 1.2.3

## 1.2.4 · Veri Aika · Veriyö

- Kuudes sisäänrakennettu paletti: lähes musta, viininpunainen ja ruusunpunainen.
- GTK 3/4, GNOME Shell ja kuvakkeet käyttävät samoja teemasävyjä.
- Alkuperäiset Veriyö · Otava ja Veriyö · Hiillos -taustakuvat mukana;
  taustakuvavalinta säilyy vapaaehtoisena. Oletus on Otava.
- Vanhemmille managereille erillinen JSON/ZIP-väripaketti.
- Painikkeiden tummempi korostusväri täyttää nykyisen tuontimuodon tekstikontrastin.


**Tee uusia teemoja ChatGPT:llä** kopioi koko aloituspromptin leikepöydälle ja avaa tavallisen `https://chatgpt.com/`-sivun. Odota sivun latautumista, liitä prompti **Ctrl+V**, tarkista se ja lähetä itse. Prompti tai koneen versiotiedot eivät enää ole avattavassa verkko-osoitteessa.

Prompti ei myöskään enää pakota verkkokeskustelun kieleksi suomea. Se pyytää käyttämään käyttäjän tunnettua ChatGPT-oletus- tai keskustelukieltä ja kysymään kielen ensin, jos se ei ole tiedossa. Managerin käyttöliittymä säilyy suomenkielisenä.

**Julkaistu sellaisenaan, käyttö omalla vastuulla.** Ohjelma jaetaan ilman takuuta GPL-3.0-or-later-lisenssin mukaisesti. Jatkuvaa ylläpitoa, tukea, virhekorjauksia tai tulevaa yhteensopivuutta ei luvata. Projektia saa haarauttaa ja jatkaa lisenssin ehdoilla. [Tukikäytäntö](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.3/SUPPORT.md).

## Asenna tai päivitä

Lataa **`chatgpt-ubuntu-theme-manager_1.2.3_all.deb`**, sulje mahdollinen vanha manageri ja avaa paketti kaksoisnapsauttamalla. Asennusohjelma voi pyytää salasanaa. Vaihtoehtoisesti aja ladatun paketin hakemistossa:

```bash
sudo apt install ./chatgpt-ubuntu-theme-manager_1.2.3_all.deb
```

Päivitys säilyttää nykyisen ulkoasun ja alkuperäisen palautuskopion. Ensiasennus yrittää ottaa Hiili-ulkoasun käyttöön aktiiviselle paikalliselle työpöytäkäyttäjälle. Tekninen pakettinimi on `hiili-theme`, jotta aiemmat versiot päivittyvät samana pakettina.

## Muutokset

- ChatGPT-painike avaa aina osoitteen `https://chatgpt.com/` ilman kyselyparametreja. Automaattinen promptin esitäyttö verkko-osoitteen kautta on poistettu.
- Molemmat promptipainikkeet kopioivat edelleen saman kokonaisen promptin. Selaimen avaava painike kertoo liittämään tekstin **Ctrl+V** sivun latauduttua; kopiointikuvake kopioi tekstin avaamatta selainta.
- Paikallista kohdetta käytettäessä kopiossa on sama koneen versiotietoraportti, joka näkyy managerissa. **Kopioi tiedot** kopioi edelleen pelkän raportin. Tietoja ei haeta uudelleen näiden painikkeiden välillä.
- Toiselle koneelle muokattu kohde jättää paikallisen raportin pois promptista. Uusi **Hae koneen tiedot** päivittää raportin ja palauttaa paikallisen kohteen.
- Aloitusprompti pyytää ChatGPT:tä käyttämään käyttäjän oletuskieltä, jos se on tiedossa, tai keskustelussa jo käytettyä kieltä. Jos kumpikaan ei ole tiedossa, kieli kysytään ensin. Sen jälkeen esitetään neljä teeman aloituskysymystä ja annetaan myös asennusohjeet valitulla kielellä.
- Prompti ohjeistaa olemaan päättelemättä käyttäjän kieltä teknisen mallin suomen kielestä. Manageri ei lue ChatGPT-tilin kieliasetuksia eikä takaa, että verkkokeskustelu tuntee ne.

Käyttäjän kuvissa ChatGPT näytti vahvistusvirheen ja teksti tuli näkyviin sivun päivittämisen jälkeen. Virheen tarkkaa syytä ei ole varmistettu. Tämä päivitys muuttaa managerin avaustapaa; se ei väitä korjaavansa ChatGPT:n verkkopalvelua tai takaavansa kirjautumatta toimimista.

Jos sivulla näkyy vahvistusvirhe tai kirjoituskenttä ei toimi, päivitä sivu (**F5**) tai valitse sivun **Yritä uudelleen**. Liitä prompti uudelleen vasta, kun sivu toimii. Kirjautumisesta ja saatavilla olevista toiminnoista päättää ChatGPT-palvelu. Käyttäjä tarkistaa ja lähettää viestin itse.

## Aiemmat ominaisuudet ja sisältörajaus

Viisi valmista ulkoasua, väripalettien tuonti samaan manageriin, koneen versiotietoraportti ja aiemman ulkoasun palautus säilyvät mukana. Myös version 1.2.1 yleiskäyttöön sopiva prompttiohje ja teemapakettien paikallinen metatietotarkistus säilyvät. Tarkistus voi erehtyä eikä takaa lainmukaisuutta tai hallitse erillistä ChatGPT-keskustelua. Katso [sisältölinjaus](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.3/CONTENT_POLICY.md).

Teemapaketin versio 1 sisältää edelleen vain 13 väriä ja lyhyet metatiedot. Se ei sisällä ohjelmakoodia, vapaata CSS:ää, kuvia tai omia sovellusvalikon käynnistimiä. Tiedostomuoto ja GPL-lisenssi säilyvät ennallaan. Manageri ei tarvitse Codexia tai OpenAI API -avainta.

## Yhteensopivuus ja tarkistusten rajaus

Projektin testiympäristö on **Ubuntu 26.10 / GNOME 51**. Versiotietoraportti auttaa promptin kohdentamisessa; sen saaminen tai kohdekentän muuttaminen ei osoita managerin tai syntyvän teeman toimivan toisessa ympäristössä.

**Ubuntu 26.04** täyttää kirjastovaatimukset, mutta sitä ei ole testattu. **Ubuntu 24.04 ei ole tuettu** nykyisellä paketilla. Vaatimukset: GTK 4 ≥ 4.18, libadwaita ≥ 1.6 sekä Ubuntu/GNOME/Yaru-osat. Tämä ei ole Kubuntun tai Xubuntun teemanhallinta.

Rakennus- ja tarkistuskomennot ovat [TESTING.md](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.3/TESTING.md)-tiedostossa. Graafisessa kokeessa ulkoisen selaimen avaus korvataan hallitulla vastauksella: sillä voidaan tarkistaa avattava osoite ja leikepöytä, mutta ei ChatGPT-verkkopalvelun toimintaa, kirjautumista tai vastauksen kieltä. Aiempien 1.2.2- ja 1.2.1-julkaisujen todennetut tarkistukset säilyvät [käyttöohjeessa](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.3/README.fi.md#julkaisun-tarkistukset) ja [muutoshistoriassa](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.3/CHANGELOG.fi.md).

Version 1.2.3 tarkistuksissa läpäisivät kaikki **53 yksikkötestiä** sekä paketin GTK 3-, GTK 4-, GNOME Shell -tyyli- ja asennuskoukkutarkistukset. Rakennetun paketin graafinen koe yksityisessä Xvfb/dconf-istunnossa vahvisti puhtaan verkko-osoitteen, koko promptin ja konetietojen leikepöytäkopion, muokatun kohteen käsittelyn sekä kopion säilymisen selaimen avausvirheessä. Samassa kokeessa teeman tuonti, käyttöönotto ja palautus toimivat. Kieliohje tarkistettiin kaikista kolmesta prompttivaihtoehdosta. ChatGPT:hen ei lähetetty viestiä, joten mallin kielivalintaa tai sivuston vahvistuksen toimintaa ei testattu.

## Lataukset

- `chatgpt-ubuntu-theme-manager_1.2.3_all.deb`: asennus tai päivitys.
- `Metsayo.ctm-theme.zip` tai `Metsayo.theme.json`: sama esimerkkipaletti; tuo vain toinen managerin **Tuo teema…** -painikkeella.
- `chatgpt-ubuntu-theme-manager-1.2.3-source.tar.gz`: lähdekoodi.
- `chatgpt-ubuntu-theme-manager-1.2.3-jakopaketti.zip`: koko jakopaketti ohjeineen.

[Käyttöohje ja lähdekoodi](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/tree/v1.2.3) · [Teemapaketin tiedostomuoto](https://github.com/Jakke77/chatgpt-ubuntu-theme-manager/blob/v1.2.3/THEME_FORMAT.fi.md)

Version 1.2.3 copies the full prompt and opens the plain `https://chatgpt.com/` page without query parameters. Wait for the page to load, paste with **Ctrl+V**, review and send. The opened address contains no prompt or local version report. The app changes its browser entry method; it does not fix the web service or guarantee availability without signing in. If the site reports a verification error, refresh or retry and paste again once it works.

The prompt asks ChatGPT to use the user's known default or conversation language, including the four style questions and installation instructions. If that language is unknown, it asks the user first. The manager cannot read ChatGPT account language settings. Its interface remains Finnish, and the Finnish technical template does not establish the user's preferred language.

Unofficial community project; not an OpenAI or Canonical product. **Provided as is, without warranty under GPL-3.0-or-later. Use at your own risk; no ongoing maintenance or future compatibility is promised.**
