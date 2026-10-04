# BRIEF: BONTRIVO

Feldtest des Skills `product-launch-motion` (Pipeline-Schritt 1 + 3).
Quelle aller Fakten: der vom Nutzer am 2026-10-04 eingefügte Seitentext, das HTML und
`brand.css` von bontrivo.de sowie das vom Nutzer gelieferte Logo-PNG. Die Seite selbst war aus
der Arbeitsumgebung nicht erreichbar (Netzwerk-Richtlinie). Belegstellen: `source/SOURCES.md`.

## Das Produkt

- **Was es ist:** Restaurant-Websites mit Speisekarte, Reservierung und Vorbestellung, fertig
  eingerichtet und gehostet, im Monatsabo.
- **Kategorie:** B2B-SaaS für die Gastronomie.
- **Was es ersetzt:** die Reservierung über Drittportale („ohne Umweg über Drittportale“,
  „ohne Provisionen an Drittportale“), die Agentur, den Baukasten, den man selbst bauen müsste
  („ohne technisches Vorwissen“).

## Das Publikum

- **Wer schaut:** Inhaber:innen und Betreiber:innen von Restaurants, Bistros, Bars, Hotels, Cafés,
  Biergärten, Catering. Nicht technisch, wenig Zeit.
- **Was sie heute tun:** Reservierung über Portale, veraltete Website, Speisekarte als PDF oder
  gar keine eigene Seite. (Annahme aus der Positionierung der Seite, nicht belegt.)
- **Wovor sie skeptisch sind:** Aufwand, Technik, versteckte Kosten, lange Projektlaufzeit.
- **Wo es läuft:** Instagram (`instagram.com/bontrivo`) und Facebook-Feed, Website-Hero,
  Demo-Termine. **Konsequenz:** Feeds spielen stumm ab, also muss der Claim in den ersten
  2 Sekunden als Schrift im Bild stehen. Untertitel sind Pflicht, der 9:16-Schnitt ist wichtig.

## Die EINE Aussage

> **Websites, die Appetit machen.**

Die h1 der Seite, wörtlich, mit 4 Wörtern ohne Konjunktion. Damit besteht sie den 7-Wort-Test.

- **Warum sie stimmt (was gezeigt wird):** die drei realen Bausteine (Speisekarte, Reservierung,
  Vorbestellung), die drei realen Schritte (Anfragen, Einrichten, Live gehen), „Tage, nicht
  Monate“, die sieben realen Branchen, der reale Grundpreis.
- **Was NICHT behauptet wird:** keine Gästezahlen, kein Umsatzplus, keine Provisionshöhe, keine
  Ladezeit, kein „Nr. 1“. „Mehr Gäste“ erscheint höchstens als Wortlaut der Marke, nie beziffert.

## Freigegebene Zahlen (Whitelist)

| Zahl | Bedeutung | Quelle |
|---|---|---|
| `29,00 €` | Grundpreis „Website monatlich“ | bontrivo.de `#preise`, `data-base-price="29"` |
| `/ Monat` | Einheit dazu | ebd. |
| `348,00 €` | „Jährliche Zahlweise — 348,00 € / Jahr, im Voraus fällig“ | ebd. Muss **immer** neben 29,00 € stehen, weil der Monatspreis jährlich abgerechnet wird |
| `1` `2` `3` | Schrittnummern „Anfragen / Einrichten / Live gehen“ | „So geht's: Drei Schritte zur eigenen Website.“ |

Jede andere Zahl wird abgelehnt.

**Bewusst NICHT verwendet:**

- `249,00 €`: **Widerspruch auf der Seite.** Die Preiskarte nennt „Einrichtung 249,00 € einmalig.
  Wir stellen Fotos, Speisekarte und Texte für Sie ein.“ (optional, zusätzlich). Die FAQ sagt:
  „Statt 29,00 € im Monat zahlen Sie wahlweise 249,00 € einmalig für Einrichtung und Betrieb.“
  Das sind zwei unvereinbare Bedeutungen derselben Zahl. Das muss Bontrivo klären, bevor die
  Zahl in irgendeinem Film steht.
- `59,00 €` (WhatsApp-Pflege), `149,00 €` / `199,00 €` (Fotografie-Addons): real, aber
  Zusatzleistungen. Sie gehören nicht zur einen Aussage.
- „Sieben Branchen“ als Ziffer: Die Seite nennt keine Zahl, nur die Liste. Wir nennen die Namen.

## Reale Assets

| Asset | Wo | Freigabe |
|---|---|---|
| Logo (PNG 577×186, transparent) | vom Nutzer im Chat geliefert, `source/bontrivo-logo-user-supplied.png` | vom Nutzer bereitgestellt. Für 1080p **originalgetreu vektorisiert** (`assets/brand/`), als Rekonstruktion gekennzeichnet |
| Marken-Tokens | `brand.css` (vom Nutzer eingefügt) | Farben, Radien, Typo 1:1 übernommen |
| Schrift | Montserrat Variable (die Seite nutzt selbst `montserrat-variable.woff2`) | SIL OFL 1.1, lokal eingebettet |
| Icons | SVG-Pfade aus dem Seiten-HTML (Feature- und Branchen-Icons) | Markenmaterial der Seite |
| Produkt-Screens | **keine.** Die App liegt hinter dem Login, Kundenseiten sind unbekannt | → im Film wird **keine** Restaurant-Website gezeigt |
| Fotografie | Die Seite nutzt `/assets/img/stock/…` | **ausgeschlossen** (Stock) |
| Kundenstimme | „Seit unsere Website steht, buchen deutlich mehr Gäste den Tisch direkt online.“ | **ausgeschlossen:** kein Name, kein Betrieb, nicht belegbar |
| Stimme | Piper `de_DE-thorsten-high` (Datensatz CC0), lokal | frei |
| Musik / SFX | selbst synthetisiert mit ffmpeg | keine Fremdlizenz |

## Negativliste

- Keine Stockfotos, keine Gesichter, kein Essen-Foto.
- Keine erfundene Zahl, kein Prozentwert, kein Datum.
- **Keine Restaurant-Website-Attrappe.** Wir kennen Bontrivos echtes Template nicht. Ein
  erfundenes „Restaurant Muster“ mit erfundenen Gerichten und Preisen wäre Fake-UI.
- Kein Wettbewerber im Bild (die Seite hat eine Unterseite „Quandoo-Alternative“, im Film heißt
  es nur „Drittportale“, wie auf der Seite).
- Kein Cursor: Es wird keine UI gezeigt, also gibt es nichts zu klicken.
- Keine unbelegte Kundenstimme, nicht die 249 €.
- Keine Geschwindigkeit über „in wenigen Tagen“ bzw. „Tage, nicht Monate“ hinaus.

## Rahmen

- **Laufzeit:** Ziel 40–50 s, Ergebnis aus der gemessenen Sprachaufnahme.
- **Format:** 1920×1080 @ 30 fps, dazu ein 9:16-Schnitt.
- **Stimme:** lokale Neural-TTS (Thorsten, männlich). Für einen öffentlichen Launch hörbar
  synthetisch (siehe Skill 03, „Choosing a voice“). Für die Veröffentlichung eine echte
  Sprecheraufnahme einplanen.
- **Musik:** keine Partitur; Klangdesign siehe `DIRECTION.md`.
- **Abnahme:** Nutzer (Bontrivo).

## Register-Karte (Kurzform; vollständig in `DIRECTION.md`)

- **Argument-Register:** `#20201E` (`--surface-dark`)
- **Produkt-Register (der Tisch):** `#FFF4E7` (`--surface`)
- **Akzent:** Tomate `#E65F3C` (`--brand`), AA-sichere Variante für kleine Schrift `#BE4020`
  (`--brand-ink`)
- **Signal:** Olive-Lime `#B7CF4A`/`#A3C13A`, laut `brand.css` „seltenes Signal“, nur für den
  Zustand „fertig / live“
