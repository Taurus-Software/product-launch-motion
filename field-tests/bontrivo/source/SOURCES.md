# Quellen (Truth Pass)

Alles hier wurde am 2026-10-04 vom Nutzer im Chat eingefügt: Seitentext, HTML und `brand.css`
von bontrivo.de sowie das Logo. Die Domain war aus der Arbeitsumgebung nicht abrufbar
(Netzwerk-Richtlinie: CONNECT 403). Im Film steht nur, was hier wörtlich belegt ist.

## Wörtlich verwendete Texte

| Im Film | Wortlaut auf der Seite | Stelle |
|---|---|---|
| WEBSITES, DIE APPETIT MACHEN. | `<h1 class="display-xl">Websites, die Appetit machen.</h1>` | Hero |
| Restaurant-Website, fertig eingerichtet, ohne technisches Vorwissen | „BONTRIVO baut Ihre Restaurant-Website: Speisekarte, Reservierung und Vorbestellung — fertig eingerichtet, ohne technisches Vorwissen.“ | Hero |
| Speisekarte · Gerichte · Preise · selbst aktualisiert | „Gerichte, Preise und Tagesangebote übersichtlich präsentiert — jederzeit von Ihnen selbst aktualisierbar.“ | „Speisekarte, die verkauft“ |
| Reservierung · ohne Umweg über Drittportale | „Gäste reservieren einen Tisch oder bestellen vor — direkt über Ihre eigene Website, ohne Umweg über Drittportale.“ | „Reservierung und Vorbestellung“ |
| Vorbestellung · pünktlich abholen | „Gäste bestellen vor und holen pünktlich ab“ | Lösungen → Pick Up Order System |
| Restaurants … Catering | Branchen-Liste: Restaurants, Bistros, Bars, Hotels, Cafés, Biergärten, Catering | „Anwendungsfälle“ |
| Anfragen · Einrichten · Live gehen | Schritte 1–3 | „So geht's: Drei Schritte zur eigenen Website.“ |
| Tage, nicht Monate | „Von der Anfrage bis zur eigenen Adresse im Netz vergehen Tage, nicht Monate.“ | „In wenigen Tagen live“ |
| 29,00 € / Monat · 348,00 € / Jahr | „29,00 € / Monat — Jährliche Zahlweise — 348,00 € / Jahr, im Voraus fällig“ | `#preise` |
| inklusive: Speisekarte, Reservierung, Vorbestellung, Hosting | „Speisekarte inklusive · Reservierung inklusive · Vorbestellung inklusive · Hosting inklusive“ | `#preise` |
| Website anfragen · bontrivo.de | Button „Website anfragen“ | Hero/CTA |

## Marken-Tokens (aus `brand.css`, wörtlich)

```css
--surface: #FFF4E7;        --surface-sunken: #F6E8D6;  --surface-dark: #20201E;
--brand: #E65F3C;          --brand-ink: #BE4020;       --brand-soft: #FBDCD1;
--accent: #A3C13A;  /* Olive Lime — seltenes Signal */  --surface-accent: #B7CF4A;
--ink: #20201E;            --ink-muted: #55534C;       --ink-subtle: #85817A;
--on-dark: #FFF4E7;        --border: #E4D9C8;
--radius-md: 10px;         --radius-lg: 16px;          --radius-pill: 999px;
--font-display: 'Montserrat';  /* display-xl: 900, uppercase, letter-spacing .005em */
.wordmark { font-weight: 800; letter-spacing: .01em; text-transform: uppercase; }
.eyebrow  { 12.5px; 700; letter-spacing: .14em; uppercase; }
.feature-card .step-number { 40px pill; background: var(--surface-dark); color: var(--on-dark); 900 }
```

## Logo-Messung (`bontrivo-logo-user-supplied.png`)

- 577×186 px, transparent; Buchstaben `#242220`, Ring `#E65F3C` (= `--brand`),
  Bohne `#B7CF4A` (= `--surface-accent`).
- Ring: Bounding-Box x 91–172, y 52–133 (Ø ≈ 81 px); Bohne oben rechts im Ring, x 138–170,
  y 55–89.

## Widersprüche und Lücken (an Bontrivo melden)

1. **249,00 €:** Die Preiskarte sagt „Einrichtung 249,00 € einmalig“ (Zusatzleistung). Die FAQ
   sagt: „Statt 29,00 € im Monat zahlen Sie wahlweise 249,00 € einmalig für Einrichtung und
   Betrieb.“
2. **Kundenstimme ohne Urheber:** „Seit unsere Website steht, buchen deutlich mehr Gäste den
   Tisch direkt online.“ Sie hat weder Namen noch Betrieb.
3. **„Eindrücke“-Galerie:** besteht aus Stockfotos (`/assets/img/stock/gal1–8.jpg`). Es gibt keine
   echten Kundenseiten.
4. Kein öffentlich sichtbares Beispiel eines echten Bontrivo-Kundenauftritts. Deshalb zeigt der
   Film keine Produkt-UI.
