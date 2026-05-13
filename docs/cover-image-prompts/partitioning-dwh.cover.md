# Cover image prompt — partitioning-dwh

## Articolo di riferimento

- **Slug**: `partitioning-dwh`
- **Sezione**: `data-warehouse`
- **Titolo IT**: *Partitioning nel DWH: quando 3 anni di dati pesano troppo*

## Descrizione della scena

Illustrazione in stile editoriale vintage con palette calda dominata da marrone, ocra, beige sabbia e accenti di rosso/arancio mattone. Sulla destra, un uomo elegante in completo marrone scuro, camicia bianca e cravatta rossa con fazzoletto da taschino bianco — capelli scuri pettinati indietro, baffi folti — sorride bonariamente con la mano sinistra in tasca e indica con l'indice della mano destra una fila di cassetti. Sullo sfondo, un'enorme parete-archivio composta da decine e decine di cassetti metallici da schedario (stile archivio anni '50-'60), tutti grigio-verde con piccole etichette bianche identiche, organizzati in una griglia regolare a perdita d'occhio. In mezzo alla parete, una riga di tre cassetti spicca perché è di colore rosso/arancio acceso e parzialmente aperta — sono le partizioni "selezionate" dalla query. In basso a sinistra, sul pavimento di legno, una pila disordinata di fogli e documenti cartacei con sopra una lente di ingrandimento — il caos dei dati non partizionati. Atmosfera retro da archivio amministrativo, luce calda, grana di carta vintage, piccoli quadrati decorativi rossi e marroni negli angoli del quadro.

## Metafora visiva

La parete-archivio rappresenta la fact table da 800 milioni di righe: senza partitioning, ogni query è costretta a "guardare in tutti i cassetti". I tre cassetti rossi aperti sono le partizioni mensili interrogate dal report trimestrale: il database non legge tutto l'archivio, ma solo i mesi richiesti. L'archivista che indica i cassetti giusti è il DBA che progetta la strategia di partitioning — sa esattamente dove cercare, e il tempo di risposta passa da minuti a secondi. La pila di carte disordinate in basso ricorda lo stato precedente: tutto in un unico mucchio, senza struttura fisica.

## File output

- **Nome file**: `partitioning-dwh.cover.jpg`
- **Path di destinazione**: `content/posts/data-warehouse/partitioning-dwh/partitioning-dwh.cover.jpg`
- **Formato**: JPG, ratio 3:2 (coerente con il sistema editoriale del blog)
