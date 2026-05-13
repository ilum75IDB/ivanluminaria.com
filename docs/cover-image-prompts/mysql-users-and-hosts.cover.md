# Cover image prompt — mysql-users-and-hosts.cover.jpg

## Articolo di riferimento

- **Slug**: `mysql-users-and-hosts`
- **Sezione**: `mysql`
- **Titolo IT**: *Utenti MySQL: perché 'mario' e 'mario'@'localhost' non sono la stessa persona*

## Descrizione della scena

Illustrazione in stile retro-vintage anni '50, con bordi a cornice color crema e palette dominata da toni seppia, ocra caldo e marrone scuro, con qualche tocco di rosso e verde oliva. La scena è ambientata nell'**atrio di una banca d'epoca**. In primo piano, **due uomini in giacca scura, cravatta rossa, cappello a tesa larga (fedora)** sono in piedi, identici nei tratti del viso (stessa persona, ma due "istanze"): il primo porta un **badge rettangolare rosso** appuntato sul bavero con la scritta "ADMIN", il secondo un **badge verde** con la scritta "USER". Sullo sfondo, due ingressi distinti che richiamano i diversi "host": a sinistra una **porta** sovrastata dall'insegna luminosa "**localhost**"; al centro, una **porta a vetri scura** con sopra l'indicazione "**192.168.1.12**". Da ciascuna porta entra un altro uomo identico in giacca e fedora, mostrando che la stessa persona può arrivare da ingressi diversi. Sulla destra, davanti a una **grande porta blindata di caveau** con ruota e congegni in ottone, un **funzionario di banca con divisa e berretto** consegna due **chiavi-cartellino** etichettate "USR" (verde) e "READONLY" (rossa) all'utente con badge "USER". Texture leggermente sporca e color carta invecchiata su tutta la scena, illuminazione calda da lampade interne.

## Metafora visiva

La scena traduce il concetto centrale dell'articolo: in MySQL l'identità non è "il nome utente", ma la coppia `'utente'@'host'`. I due uomini identici con badge diversi sono la stessa persona "mario" che diventa due entità distinte a seconda dell'host da cui si collega — `'mario'@'localhost'` e `'mario'@'192.168.1.12'` non sono la stessa identità, e quindi possono avere GRANT diversi (USER vs ADMIN). Le porte d'ingresso rappresentano gli host, il caveau della banca è il database, e le chiavi che il funzionario consegna sono i GRANT — privilegi assegnati alla coppia utente+host, non al solo nome. È una scena di portineria/banca, non di eroismo: il DBA è il funzionario che fa il suo lavoro di controllo accessi.

## File output

- **Nome file**: `mysql-users-and-hosts.cover.jpg`
- **Path di destinazione**: `content/posts/mysql/mysql-users-and-hosts/mysql-users-and-hosts.cover.jpg`
- **Formato**: JPG, ratio 3:2 (coerente con il sistema editoriale del blog)
