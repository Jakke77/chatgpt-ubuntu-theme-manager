# ChatGPT Ubuntu Theme Manager 1.2.3 — tavallinen ChatGPT-sivu ja keskustelukieli

- **Tee uusia teemoja ChatGPT:llä** kopioi koko promptin ja avaa tavallisen
  `https://chatgpt.com/`-sivun ilman kyselyparametreja. Promptin esitäyttö
  verkko-osoitteesta on poistettu; osoitteessa ei välitetä promptia tai
  koneen versiotietoja.
- Käyttäjä odottaa sivun latautumista, liittää tekstin **Ctrl+V**, tarkistaa
  sen ja lähettää itse. Erillinen kopiointikuvake kopioi edelleen vain tekstin
  leikepöydälle. **Kopioi tiedot** kopioi pelkän näkyvän raportin.
- Molemmissa promptitoiminnoissa käytetään samaa tekstiä ja samaa näkyvää
  raporttia, kun kohde vastaa paikallista konetta. Raportin haku ja toista
  järjestelmää varten muokattavan kohteen käsittely säilyvät.
- Prompti pyytää käyttämään käyttäjän tunnettua ChatGPT-oletus- tai
  keskustelukieltä. Jos kieli ei ole tiedossa, se pyydetään kysymään ensin.
  Teeman neljä aloituskysymystä ja asennusohjeet pyydetään samalla kielellä.
  Teknisen mallin suomen kielestä ei pidä päätellä käyttäjän toivetta.
- Manageri ei lue ChatGPT-tilin kieliasetuksia; käyttöliittymä on edelleen
  suomenkielinen. Sisältörajaus, teeman käyttöönotto ja palautus, tiedostomuoto,
  GPL-lisenssi ja ylläpitolinjaus säilyvät ennallaan.

Verkkopalvelun vahvistusvirheen tarkkaa syytä ei ole varmistettu. Muutos ei
takaa ChatGPT:n toimintaa ilman kirjautumista. Jos verkkosivu näyttää virheen,
päivitä tai yritä uudelleen ja liitä teksti vasta sivun toimiessa.
Tarkistusten rajaus kuvataan [julkaisutiedoissa](RELEASE_NOTES.md).

Alla säilyvät aiempien julkaisujen todennetut tarkistukset. Näissä aiemmissa
versioissa prompti valmisteltiin myös verkko-osoitteen kyselyyn.

# ChatGPT Ubuntu Theme Manager 1.2.2 — koneen versiotiedot

- **Hae koneen tiedot** päivittää teeman kohdejärjestelmän paikallisesta
  Ubuntu- ja GNOME-versiosta ja näyttää kopioitavan raportin.
- Raporttiin tulevat käyttöjärjestelmä, GNOME Shell, GTK 4, libadwaita,
  Yarun GTK-, Shell- ja kuvakepaketit, managerin versio ja Wayland/X11-istuntotyyppi.
  Puuttuva tieto ilmoitetaan raportissa.
- **Kopioi tiedot** kopioi raportin tavallisena tekstinä. Sama näkyvä raportti
  sisältyy koko promptin kopioon ja ChatGPT-linkin promptiin, kun kohdekenttä
  vastaa haettua paikallista kohdetta.
- Toiselle järjestelmälle muokattu kohde jättää tämän koneen raportin pois
  promptista. Raportti säilyy erikseen katseltavana ja kopioitavana.
  Uusi tietojen haku päivittää raportin ja palauttaa paikallisen kohteen.
- Haku toimii paikallisena lukutoimintona ilman verkkopalvelua tai salasanaa.
  Raporttiin ei kerätä käyttäjätunnusta, kotihakemistoa, koneen nimeä,
  laitteistotunnisteita tai verkkotietoja.
- Sisältörajaus, väripaletin tiedostomuoto, teeman käyttöönotto ja palautus,
  GPL-lisenssi ja ylläpitolinjaus säilyvät ennallaan.

51 versiopromptin, sisällön ja tiedostomuodon testiä sekä graafinen
haku-, kopiointi- ja teemanvaihtokoe läpäisivät. Myös integraatio-, tyyli- ja
asennuskoukkutarkistukset läpäisivät Ubuntu 26.10 / GNOME 51 -ympäristössä.

Tämän päivityksen tarkistusten rajaus on [julkaisutiedoissa](RELEASE_NOTES.md).
Alla säilyvät aiempien julkaisujen todennetut tarkistukset.

# ChatGPT Ubuntu Theme Manager 1.2.1 — sisällön rajaus

- Yleiskäyttöön sopivan sisällön ohje lisättiin kaikkiin kolmeen ChatGPT-promptiin.
- Paikallinen, rajallisiin ilmauksiin perustuva tarkistus käsittelee teeman
  tunnisteen, nimen, kuvauksen, tekijän, lisenssin ja kohdejärjestelmän tiedot.
  Se hylkää tunnistamansa huijaus-, hyväksikäyttö-, porno-, viha- ja raakaa
  väkivaltaa kuvaavat ilmaukset sekä linkit ja merkkauskielen tekstitiedoissa.
- Tarkistus koskee tuontia ja jo tuotujen teemojen luettelointia. Käsin muutettu
  hylättävä metadata estää teeman valinnan ja käyttöönoton; alkuperäisen
  ulkoasun palautus ja käyttäjän omat tiedostot säilyvät.
- Yläpalkin kilpipainike kertoo sisältörajauksesta ja sen rajoista.
- Väripaletin tiedostomuoto pysyy versiossa 1. Vanhojen tavallisten palettien
  tiedostot toimivat edelleen. URL- tai merkkauskieltä sisältävät aiemmat
  tekstitiedot vaativat muuttamisen tavalliseksi tekstiksi.
- Tarkistus toimii ilman verkkoa, käyttäjätietojen lähettämistä tai API-avainta.
  Se ei ole kattava sisällönluokittelija, lainmukaisuuden tae tai erillisen
  ChatGPT-keskustelun valvoja. Katso [CONTENT_POLICY.md](CONTENT_POLICY.md).
- Selaimen avaus, leikepöytä ja teeman käyttöönotto säilyvät ennallaan.

### Tarkistukset

38 sisältö- ja tiedostotestiä sekä integraatio-, käyttöliittymä-, tyyli- ja
asennuskoukkukokeet läpäisivät Ubuntu 26.10 / GNOME 51 -ympäristössä.
Tarkempi rajaus on [julkaisutiedoissa](RELEASE_NOTES.md).

# ChatGPT Ubuntu Theme Manager 1.2.0 — muutokset

Omat ChatGPT:llä suunnitellut tummat väripaletit voidaan nyt tuoda samaan
manageriin ja vaihtaa käyttöön sen teemavalikoimasta. Jokainen teema ei enää
tarvitse erillistä sovellusta tai omaa kuvaketta sovellusvalikkoon.

## Uutta

- **Tuo teema…** hyväksyy `.ctm-theme.zip`-paketin tai suoran `.json`-tiedoston.
  Tuotu teema säilyy käyttäjän valikoimassa managerin uudelleenavaamisen jälkeen.
- Tuonti avaa esikatselun. Käyttöönotto tehdään erikseen
  **Ota valittu teema käyttöön** -painikkeella.
- Teemavalikoima mukautuu myös omiin teemoihin. Viisi valmista vaihtoehtoa
  säilyvät: Hiili / Musta, Grafiitti, Petrooli, Luumu ja Ubuntu Dark.
- Mukana on tuotava **Metsäyö**-esimerkki sekä ZIP- että JSON-muodossa.
- ChatGPT-promptit pyytävät managerin ymmärtämää teemapakettia erillisen
  `.deb`-asentajan ja sovelluskuvakkeen sijaan. Aluksi ChatGPT:tä pyydetään
  edelleen kysymään käyttäjän toiveet.
- Promptin kohdeympäristö tunnistetaan julkisista Ubuntu- ja GNOME-versiotiedoista.
  Kenttää voi muokata esimerkiksi toista Ubuntu-versiota varten.
- Komentoriville lisättiin `--import-theme`, `--list-themes` ja `--prompt-target`.

## Teemapaketin rajat

Pakettimuodon versio 1 sisältää paletin värit ja teeman tiedot. ZIPin juuressa
on vain `theme.json`. Manageri muodostaa GTK-, Shell-, kuvake- ja
taustakuvavärit omista pohjistaan. Tuonti ei suorita paketin toimittamaa koodia.

Vapaasti kirjoitettu CSS, kokonaan uudet kuvakkeet, omat taustakuvat ja vaaleat
teemat eivät kuulu tähän pakettimuotoon. Aiemmin erillisenä `.deb`-sovelluksena
tehty teema täytyy muuntaa paletin JSON-muotoon ennen tuontia.

Saman `id`-tunnisteen tuonti uudelleen estetään, jotta aiemmin tuotu teema
ei muutu huomaamatta. Anna uudelle versiolle uusi tunniste.

## Päivitys ja yhteensopivuus

Asenna `chatgpt-ubuntu-theme-manager_1.2.0_all.deb` vanhan version päälle.
Tekninen pakettinimi `hiili-theme` säilyy. Päivitys säilyttää nykyisen
ulkoasun ja Hiili 1.0:n tai managerin 1.1:n alkuperäisen palautuspisteen.
Sulje aiempi manageri ennen päivitystä.

Julkaisu tehdään Ubuntu 26.10 / GNOME 51 -ympäristössä. Paketti vaatii
GTK ≥ 4.18 ja libadwaita ≥ 1.6. Ubuntu 26.04 täyttää nämä kirjastovaatimukset,
mutta toimivuutta siinä ei ole vahvistettu. Ubuntu 24.04:n GTK 4.14 ei tue
käytettyjä moderneja CSS-muuttujia, joten nykyinen asennuspaketti ei tue sitä.
[Ubuntun GTK-versiot](https://packages.ubuntu.com/eu/gir1.2-gtk-4.0),
[26.04:n libadwaita](https://packages.ubuntu.com/uk/resolute/gir1.2-adw-1),
[GTK:n CSS-muuttujien vaatimukset](https://docs.gtk.org/gtk4/css-properties.html).

Promptin kohdeversio tai teeman `target`-kenttä on suunnittelutieto. Se ei ole
todistus teeman tai managerin testatusta yhteensopivuudesta kyseisessä ympäristössä.

Codexia tai API-avainta ei tarvita. Selain avataan ja prompti kopioidaan
leikepöydälle; käyttäjä tarkistaa ja lähettää viestin itse ChatGPT:ssä.

## Julkaisun tarkistukset

Versio 1.2.0 tarkistettiin Ubuntu 26.10 / GNOME 51 -koneella:

- 20 teemapaketin luku- ja validointitestiä läpäisi.
- Viisi valmista teemaa ja tuotu Metsäyö vaihtuivat käyttöön ja palautuivat
  alkuperäisiin asetuksiin erillisillä testiasetuksilla. Palautuksessa
  varmistettiin alkuperäiset tiedostot tavu tavulta, symlinkit, käyttäjän
  myöhemmät muutokset ja muiden GNOME-laajennusten säilyminen.
- GTK 3-, GTK 4- ja GNOME 51:n Shell-jäsentimet hyväksyivät sekä valmiiden
  teemojen että tuodun paletin tyylit.
- Rakennetun paketin graafisessa kokeessa tuontipainike, ZIP-tiedoston
  valmistumisen käsittely, valikoiman päivitys, käyttöönotto ja palautus
  toimivat yksityisessä Xvfb/dconf-istunnossa. Järjestelmän tiedostovalitsin
  ja ulkoisen selaimen avaus korvattiin testissä hallituilla vastauksilla;
  ChatGPT-keskusteluun ei lähetetty viestiä. Valittua kohdeversiota sisältävän
  URL:n ja leikepöydän promptin vastaavuus tarkistettiin.
- Asennuskoukkujen kokeessa ensiasennus kutsui käyttöönottoa ja päivitys
  säilytti valitun ulkoasun. Valmiista .deb:stä puretut ohjelmatiedostot
  vastasivat testattuja lähteitä, tuonti toimi ja paketissa oli yksi
  sovellusvalikon käynnistin.

Paketin asennusta järjestelmänvalvojan oikeuksilla ei suoritettu tämän
päivityksen valmistelussa. Muita Ubuntu-versioita ei ajettu testikoneella.
Virtuaali-ikkunan portaalin ja PipeWiren käynnistys antoivat ympäristövaroituksia;
GTK:n teematarkistuksissa ei löytynyt tyylivirheitä.
