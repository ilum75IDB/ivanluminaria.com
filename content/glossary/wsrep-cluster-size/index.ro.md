---
title: "wsrep_cluster_size"
description: "Variabilă de stare Galera care indică numărul de noduri active din cluster. Scăderea sub quorum blochează scrierile pe toate nodurile rămase."
translationKey: "glossary_wsrep_cluster_size"
aka: "Galera cluster size status variable"
articles:
  - "/posts/mysql/galera-cluster-quorum-split-brain-e-bootstrap-di-emergenza-con-due-nodi-giu"
---

`wsrep_cluster_size` este o variabilă de stare expusă de plugin-ul wsrep (Galera) care raportează câte noduri sunt conectate și sincronizate în cluster la un moment dat. Nu este un parametru de configurare: valoarea sa este dinamică și se modifică în timp real pe măsură ce topologia clusterului se schimbă.

## Cum funcționează

Valoarea se citește printr-o interogare simplă:

```sql
SHOW STATUS LIKE 'wsrep_cluster_size';
```

Într-un cluster cu 3 noduri funcțional, rezultatul așteptat este `3`. Galera calculează quorum-ul folosind formula `⌊N/2⌋ + 1`: pentru 3 noduri, quorum-ul minim este 2. Dacă `wsrep_cluster_size` scade la `1`, nodul supraviețuitor nu atinge quorum-ul, setează `wsrep_cluster_status` la `non-Primary` și refuză scrierile pentru a preveni split-brain.

## Context operațional

Verificarea `wsrep_cluster_size` este primul pas atunci când o aplicație raportează erori de scriere pe un cluster Galera. O valoare mai mică decât numărul total de noduri așteptate nu indică neapărat o întrerupere critică: două din trei noduri mențin quorum-ul, iar clusterul rămâne în starea `Primary`. Problema apare doar când se pierde majoritatea.

În clusterele cu 2 noduri (configurație descurajată în producție), pierderea oricărui nod aduce `wsrep_cluster_size` la `1` și blochează imediat scrierile, necesitând fie un bootstrap manual, fie utilizarea unui nod arbitru (garbd).

## Note

`wsrep_cluster_size` reflectă dimensiunea vederii curente a clusterului (Primary Component), nu numărul total de noduri configurate. Un nod în starea `Donor/Desynced` sau `Joiner` poate să nu apară temporar în număr, sau să îl reducă, în timpul unui transfer SST/IST.
