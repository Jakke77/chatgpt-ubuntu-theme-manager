# ChatGPT Ubuntu Theme Manager 1.2.0

> Projekti jaetaan sellaisenaan. Käyttö on omalla vastuulla. Jatkuvaa ylläpitoa,
> tukea tai tulevaa yhteensopivuutta ei luvata. Katso [ylläpitolinjaus](SUPPORT.md).

Tumma teemanhallinta Ubuntu/GNOME-työpöydälle. Voit vaihtaa viiden valmiin
ulkoasun välillä ja tuoda ChatGPT:llä suunniteltuja omia väripaletteja
samaan teemavalikoimaan. Oma teema ei tee sovellusvalikkoon uutta kuvaketta.

Ohjelma on epävirallinen yhteisöprojekti, ei OpenAI:n tai Canonicalin tuote.

## Asennus ja päivitys klikkaamalla

1. Sulje aiemmin avoinna oleva Hiili- tai Theme Manager -ikkuna.
2. Avaa `chatgpt-ubuntu-theme-manager_1.2.0_all.deb` kaksoisnapsauttamalla sitä.
3. Valitse paketin asennusohjelmassa **Asenna** tai **Päivitä** ja anna pyydetty salasana.
4. Avaa sovellusvalikosta **ChatGPT Ubuntu Theme Manager**.

Paketti päivittää aiemman Hiili 1.0:n tai managerin 1.1:n. Päivitys säilyttää
nykyisen ulkoasun ja alkuperäisen palautuspisteen. Tekninen Debian-paketin
nimi on edelleen `hiili-theme`, jotta vanha asennus päivittyy samana pakettina.

Ensimmäinen asennus ilman aiempaa Hiiliä yrittää ottaa Hiili-ulkoasun käyttöön
aktiiviselle paikalliselle työpöytäkäyttäjälle. Teeman voi aina ottaa käyttöön
myös managerin omalla painikkeella.

## Valitse ja ota käyttöön

Valmiit vaihtoehdot ovat **Hiili / Musta**, **Grafiitti**, **Petrooli**,
**Luumu** ja **Ubuntu Dark**. Teemakortin valinta näyttää esikatselun managerissa.
Työpöydän värit ja kuvakkeet vaihtuvat, kun painat **Ota valittu teema käyttöön**.

**Vaihda myös taustakuva** ottaa samalla käyttöön paletin mukaan väritetyn
Hiili-taustakuvan. Sulje ja avaa jo käynnissä olevat sovellukset tarvittaessa,
jotta niiden värit päivittyvät.

## Tuo oma teema samaan valikoimaan

Voit kokeilla tuontia mukana toimitetulla **Metsäyö**-esimerkillä:

1. Paina **Tuo teema…**.
2. Valitse `Metsayo.ctm-theme.zip` tai `Metsayo.theme.json`.
3. Metsäyö ilmestyy managerin teemavalikoimaan ja sen esikatselu avautuu.
4. Paina **Ota valittu teema käyttöön**.

ZIP ja JSON sisältävät saman esimerkkiteeman, joten tuo niistä vain toinen.
Teema säilyy valikoimassa managerin sulkemisen ja avaamisen jälkeen.
Tuonti on käyttäjäkohtainen eikä tarvitse järjestelmänvalvojan salasanaa.

Jos saman tunnisteen teema on jo tuotu, manageri ei korvaa sitä. Käytä oman
paletin uudessa versiossa eri `id`-tunnistetta, esimerkiksi `metsayo-v2`.
Tällöin myös edellinen versio jää kokeiltavaksi.

Version 1 pakettimuoto sisältää **tumman väripaletin ja teeman tiedot**.
Manageri muodostaa niistä GTK 3-, GTK 4-, GNOME Shell-, kuvake- ja
taustakuvavärit omien pohjiensa avulla. Tuotavassa paketissa ei ole
asennuskomentoja tai omaa sovellusta. Tässä versiossa ei voi tuoda vapaasti
kirjoitettua CSS:ää, uusia kuvakepiirroksia, omia taustakuvatiedostoja tai
vaaleaa teemaa.

Hyväksytty ZIP sisältää juuressaan täsmälleen yhden tiedoston nimeltä
`theme.json`. Vaihtoehtoisesti saman sisällön voi tuoda suoraan
UTF-8-muotoisesta `.json`-tiedostosta. Esimerkin JSON toimii mallina.

## Suunnittele uusi paletti ChatGPT:llä

1. Valitse **ChatGPT:n aloitusprompti**: uusi oma teema, Hiilin väriversio
   tai oma Ubuntu Dark.
2. Tarkista kohdeympäristön kenttä. Ohjelma täyttää siihen paikallisen
   Ubuntu- ja GNOME-version; voit kirjoittaa myös toisen kohteen,
   esimerkiksi `Ubuntu 26.04 / GNOME`.
3. Paina **Tee uusia teemoja ChatGPT:llä**.
4. ChatGPT avautuu oletusselaimessa. Prompti kopioidaan myös leikepöydälle.
   Jos teksti ei näy kirjoituskentässä tai kirjautuminen kadottaa sen,
   liitä se komennolla **Ctrl+V** ja lähetä itse.
5. Vastaa ChatGPT:n neljään aloituskysymykseen. Prompti pyytää lopuksi
   manageriin tuotavan `.ctm-theme.zip`- tai `.json`-tiedoston.
6. Tallenna valmis tiedosto ja tuo se managerin **Tuo teema…** -painikkeella.

Kopiointipainikkeella saat saman promptin avaamatta selainta.
Jos verkkokeskustelu ei pysty tekemään ladattavaa tiedostoa, se voi antaa
koko JSONin, jonka tallennat tekstieditorilla `.json`-tiedostoksi.

**Codexia tai OpenAI API -avainta ei tarvita.** Manageri ei lähetä viestiä
ChatGPT-keskusteluun automaattisesti. Selaimeen valmistellaan yleinen prompti
ja kohdeympäristön julkinen versiotieto, jonka voit tarkistaa ja muokata.
Paikallisia tiedostoja tai palautuskopioita ei liitetä keskusteluun.

Aiemmalla promptilla tehtyä erillistä `.deb`-teemasovellusta ei voi tuoda
suoraan. Pyydä ChatGPT:tä muuntamaan sen väripaletti uuden promptin
`theme.json`-muotoon. Vanhan sovelluksen mahdollinen poistaminen tehdään
erikseen sen omilla ohjeilla.

## Muut Ubuntu-versiot

Tämän julkaisun vertailu- ja testiympäristö on **Ubuntu 26.10 / GNOME 51**.
Managerin asennuspaketti vaatii GTK 4:n version vähintään 4.18 ja
libadwaitan version vähintään 1.6 sekä Ubuntu Yarun ja GNOME Shellin osat.

- **Ubuntu 26.04:** GTK 4.22 ja libadwaita 1.9 täyttävät kirjastovaatimukset,
  mutta toimintaa tällä Ubuntu-versiolla ei ole vielä vahvistettu.
  [Ubuntun GTK-paketti](https://packages.ubuntu.com/da/resolute/gir1.2-gtk-4.0),
  [Ubuntun libadwaita-paketti](https://packages.ubuntu.com/uk/resolute/gir1.2-adw-1).
- **Ubuntu 24.04:** nykyinen asennuspaketti ei ole yhteensopiva sen GTK 4.14:n
  ja libadwaita 1.5:n kanssa. Vanhempi versio tarvitsee erillisen sovituksen;
  käytettyjen CSS-muuttujien tuki alkaa GTK 4.16:sta.
  [Ubuntun GTK-versiot](https://packages.ubuntu.com/eu/gir1.2-gtk-4.0),
  [24.04:n libadwaita](https://packages.ubuntu.com/eu/noble/gir1.2-adw-1),
  [GTK:n CSS-tuki](https://docs.gtk.org/gtk4/css-properties.html).

Kohdeympäristön tekstikenttä ja teeman `target`-tieto auttavat suunnittelussa.
Niiden vaihtaminen ei itsessään lisää manageriin tukea toiselle versiolle.
Kubuntu, Xubuntu ja muut työpöytäympäristöt tarvitsevat omiin teemaosiinsa
sopivan toteutuksen.

## Palautus ja poistaminen

**Palauta aiempi ulkoasu** palauttaa ensimmäistä käyttöönottoa edeltäneet
asetukset. Teemojen vaihtelu tai oman paletin tuominen ei korvaa tätä
palautuspistettä. Myös Hiili 1.0:n ja managerin 1.1:n palautuskopiot säilyvät
yhteensopivina. Ne ovat käyttäjäkohtaisesti `~/.config/hiili-theme/`-kansiossa.

Manageri säilyttää muut GNOME-laajennukset ja huomioi asetustiedostojen
myöhemmät käsin tehdyt muutokset palautuksessa. Palauta aiempi ulkoasu
ennen ohjelman poistamista pakettienhallinnasta.

Kaikki sovellukset eivät seuraa työpöydän teemaa. Omia ulkoasujaan käyttävät
tai eristetyt sovellukset voivat säilyttää osan omista väreistään.
GDM-kirjautumisruutua ei muokata.

## Komentorivikäyttö

Aja komennot tavallisena työpöytäkäyttäjänä:

```bash
chatgpt-ubuntu-theme-manager --import-theme Metsayo.ctm-theme.zip
chatgpt-ubuntu-theme-manager --list-themes
chatgpt-ubuntu-theme-manager --apply --variant user:metsayo
chatgpt-ubuntu-theme-manager --restore
chatgpt-ubuntu-theme-manager --print-prompt new --prompt-target 'Ubuntu 26.04 / GNOME'
```

`--import-theme` lisää teeman valikoimaan. `--apply` ottaa sen käyttöön.
`--no-wallpaper` jättää taustakuvan vaihtamatta, kun se annetaan
`--apply`-komennon yhteydessä. Vanha `hiili-theme`-komentonimi toimii edelleen.

## Lähdekoodi ja jakaminen

Lähdekoodi on paketissa `chatgpt-ubuntu-theme-manager-1.2.0-source.tar.gz`.
Koko jakopaketti on `chatgpt-ubuntu-theme-manager-1.2.0-jakopaketti.zip`.
Ohjelma ja sen omat pohjat ovat GPL 3 tai uudempi -lisenssillä.
Metsäyö-esimerkkipaletti on CC0-1.0-lisenssillä. Omassa paletissa lisenssi
ja tekijä ilmoitetaan sen JSON-tiedoissa.

Yarun pohjat luetaan koneeseen asennetuista Ubuntu-paketeista ja ne
säilyttävät omat lisenssinsä. [Yarun lähdekoodi](https://github.com/ubuntu/yaru).
Rakentaminen lähdepaketista: `python3 build.py`; valmis `.deb` syntyy
projektin `dist/`-kansioon. Rakennus tarvitsee Pythonin lisäksi
`dpkg-deb`-, `gtk-update-icon-cache`- ja `desktop-file-validate`-työkalut.

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
