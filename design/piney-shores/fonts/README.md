# Aptos

The deck's typography is Microsoft's **Aptos** family. The font files are
Microsoft property and are not redistributed in this repository.

You very likely do not need them. `tokens.css` declares every face with
`local()` before `url()`, so a machine with **Microsoft 365 installed already
renders the deck in real Aptos** — Aptos is the Office default and ships with
it.

If you do need to bundle the files (a rendering box, a CI PDF export), drop
them here under these names:

```
Aptos.ttf                     Aptos-Display.ttf              Aptos-Narrow.ttf
Aptos-Italic.ttf              Aptos-Display-Bold.ttf         Aptos-Narrow-Bold.ttf
Aptos-SemiBold.ttf            Aptos-Display-Italic.ttf       Aptos-Narrow-Italic.ttf
Aptos-Bold.ttf
Aptos-ExtraBold.ttf           Aptos-Mono.ttf                 Aptos-Serif.ttf
Aptos-Black.ttf               Aptos-Mono-Bold.ttf            Aptos-Serif-Bold.ttf
```

Only four of these carry the deck: **Aptos Display** (headings), **Aptos**
(body), **Aptos Narrow** (eyebrows, labels, table headers) and **Aptos Mono**
(every currency figure, ratio and percentage). Aptos Serif is optional and
unused here.

Without either source, the deck falls back to a humanist sans with close
metrics. Layout holds; only the typeface differs.
