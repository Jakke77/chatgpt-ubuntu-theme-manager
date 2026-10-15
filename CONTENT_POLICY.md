# Sisältörajaus / Content policy

ChatGPT Ubuntu Theme Managerin 1.2.1-julkaisuun sisältyy paikallinen,
yleiskäyttöön sopiva sisältörajaus. Tavoite on ehkäistä teemapakettien
käyttämistä huijausten, toisena esiintymisen, hyväksikäytön, pornografian,
vihasisällön tai raa'an väkivallan esittämiseen tai mainostamiseen.
Tämä on projektin oma sisältölinjaus ja rajallinen tekninen tarkistus.
Se ei ole arvio yksittäisen teeman lainmukaisuudesta eikä lupaus siitä,
että kaikki haitallinen sisältö tunnistetaan.

## Mitä pakettimuoto sallii?

Version 1 teemapaketti sisältää vain 13 väriä, korostusvärin valinnan,
värinäytteen ja lyhyet metatiedot. Manageri muodostaa niistä ulkoasun
omiin pohjiinsa. Paketti ei voi sisältää ulkoisia kuvia, logoja, vapaata
CSS:ää, HTML-sivuja, kirjautumislomakkeita, ohjelmakoodia, asennusskriptejä
tai sovellusvalikon käynnistimiä. Se ei myöskään muuta GDM-kirjautumisruutua.

Tämä rajaus estää paketin mukana toimitettavat kalastelusivut ja muut
teemaksi naamioidut sovellukset. Pelkkä väripaletti ei kuitenkaan kerro
tekijän tarkoitusta, eikä värien samankaltaisuus yksin merkitse huijausta.

## Mitä paikallinen tarkistus tekee?

Manageri tarkistaa teeman kuusi tekstikenttää: `id`, `name`, `description`,
`author`, `license` ja `target`. Niiden on oltava tavallista tekstiä;
URL-osoitteita ja merkkauskieltä ei hyväksytä. Lisäksi paikalliset
sanasto- ja hahmosäännöt torjuvat tunnistamiaan viittauksia seuraaviin:

- huijaukset, tietojenkalastelu, identiteettivarkaus ja harhaanjohtava
  toisena henkilönä tai virallisena palveluna esiintyminen;
- seksuaalinen hyväksikäyttö ja pornografia;
- ihmisryhmiin kohdistuva vihasisältö;
- raaka väkivalta ja sen ihannointi.

Samaa tarkistusta käytetään uuden tiedoston tuonnissa, omien teemojen
valikoimaa luettaessa ja teeman käyttöönotossa. Aiemmin tuotu teema, jonka
metatiedot eivät läpäise tarkistusta, jätetään pois omien teemojen
valikoimasta. Sen tiedostoja ei poisteta. Alkuperäisen ulkoasun palautus
pysyy käytettävissä. Komentorivi käyttää samoja tarkistuksia, eikä
ohjelmassa ole sisältörajoituksen ohitusvalintaa.

ChatGPT:n aloituspromptit sisältävät saman yleiskäyttöön sopivan rajauksen.
Manageri avaa kuitenkin erillisen verkkopalvelun: se ei hallitse myöhemmin
käytävää ChatGPT-keskustelua, sen vastauksia tai käyttäjän siellä muokkaamaa
promptia.

## Tavalliset tyylit ja identiteetin ilmaisu ovat sallittuja

Sisältörajaus ei kiellä tavallisia synkkiä, goottilaisia tai kauhuun
viittaavia väripaletteja. Esimerkiksi **Metsäyö**, **Goottilainen luumu**,
**Kallot ja kuut** sekä **Sateenkaari / Pride** voivat olla tavallisia
teeman aiheita. Ei-seksuaalinen taide, omaan identiteettiin liittyvät värit
ja normaali brändin väreistä saatu inspiraatio ovat sallittuja.

Vastaavasti pankin tai viranomaisen nimissä tehtävä huijaus tai väärennetty
kirjautumisnäkymä ei kuulu ohjelman käyttötarkoitukseen. Pakettimuoto ei
tue sellaisen käyttöliittymän tai lomakkeen tuontia.

## Rajat ja virheelliset hylkäykset

Tarkistus on deterministinen paikallinen suodatin, ei yleinen sisällön tai
tarkoituksen tunnistava luokittelija. Se ei ymmärrä kaikkia kieliä,
kiertoilmauksia, kirjoitusasun muunnelmia tai asiayhteyksiä. Se voi sekä
päästää läpi sopimatonta tekstiä että hylätä asiallista tekstiä. Väreistä
ei voi päätellä, millaiseen tarkoitukseen niitä käytetään.

Jos tavallinen teema hylätään virheellisesti, muotoile sen nimi ja kuvaus
selkeästi ja neutraalisti kuvaamaan itse väripalettia. Tarkista myös muut
metatiedot ja poista URL-osoitteet sekä merkkauskieli. Älä lisää pakettiin
ohituskomentoja tai muita tiedostoja. Teeman tekijä vastaa metatietojensa
paikkansapitävyydestä.

Tarkistus ei käytä verkkoyhteyttä, API-avaimia tai maksullista
moderointipalvelua. Metatietoja ei lähetetä moderointipalveluun, eikä
tarkistus lisää telemetriaa. Käyttäjän erikseen avaama ChatGPT toimii oman
verkkopalvelunsa ehtojen mukaisesti.

## Lisenssi ja ylläpito

Tämä asiakirja kuvaa julkaistun ohjelman toimintaa ja projektin
sisältölinjausta. Se ei muuta [GPL-3.0-or-later-lisenssin](LICENSE)
myöntämiä oikeuksia. Avointa lähdekoodia tai sen muokattuja versioita ei
voi teknisesti pakottaa noudattamaan samaa suodatinta. Ohjelma jaetaan
edelleen sellaisenaan ilman lupausta jatkuvasta ylläpidosta; katso
[SUPPORT.md](SUPPORT.md).

## English

This release aims to keep themes suitable for general audiences. Its local
metadata rules reject recognized patterns related to fraud, phishing,
identity theft, deceptive impersonation, exploitation, pornography, hate
content and graphic violence. The version 1 format accepts only colors and
short metadata, not external images, logos, scripts, HTML, forms or desktop
launchers. Metadata must be plain text without URLs or markup.

The same rules apply during import, catalog loading and application. Old
themes that fail validation are omitted from the custom-theme catalog;
their files are not deleted, and restoring the previous appearance remains
available. Normal gothic or horror styles, skull motifs, Pride and other
identity expression, non-explicit art and ordinary brand-color inspiration
are allowed.

This is a limited deterministic filter, not a universal content classifier
or a legal-compliance guarantee. It can miss harmful wording and reject
innocent wording, especially across languages and contexts. It cannot
control a separate ChatGPT conversation or modified open-source forks.
The local check requires no network service, API key or paid moderation
and adds no telemetry. This policy does not alter rights granted by the GPL.
