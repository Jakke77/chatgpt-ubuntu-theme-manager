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
