# Appunti — refactor "Profilo Professionale" del CV Project Manager

**Branch**: `claude/resumes-refactor`
**File target**: `content/resumes/project-manager/index.it.md`
**Sezione**: `## Profilo Professionale` (paragrafo unico subito dopo, riga 17 del file)
**Lingua master**: italiano (le traduzioni EN/ES/RO seguiranno solo dopo aver chiuso la versione IT)
**Tono richiesto da Ivan**: stile Borzacchiello — diretto, pragmatico, ritmo serrato, frasi corte, andate a capo come strumento di ritmo, niente filler, risalto a esperienza/numeri/aziende/mercati/metodologie.

Questo file raccoglie l'originale + le 3 prime proposte. Lo aggiorniamo via via che convergiamo sulla versione finale (o un ibrido). Non è un draft di pubblicazione: vive solo qui finché la versione scelta non viene applicata al file `.md` reale della roadmap PM.

---

## Originale (versione live al 2026-06-18)

> Project Manager con quasi 30 anni di esperienza IT e un solido background tecnico in ambienti Data Warehouse e Oracle. Oltre 10 progetti completati con consegne quasi sempre rispettate, gestendo team di 3-7 persone in contesti multiculturali e remoti su progetti con budget nell'ordine di €100K-€500K. Competenze concrete in pianificazione, gestione del rischio, coordinamento delle risorse e interfaccia con gli stakeholder — maturate sul campo coordinando attività di sviluppo, rilascio e manutenzione per clienti nei settori Banking, Telco, Assicurativo e Pubblica Amministrazione. Metodologie Agile (Scrum) applicate nella gestione quotidiana dei progetti, con formazione certificata. Background tecnico approfondito (architettura DWH, Oracle DBA, PL/SQL, ETL/ELT) che consente di parlare la stessa lingua del team di sviluppo, valutare la fattibilità delle soluzioni e identificare i rischi tecnici prima che diventino problemi.

**Diagnosi rapida**:

- Un unico paragrafo, molto denso (~140 parole, una sola pausa logica).
- Tono CV-burocratico classico: "Competenze concrete in pianificazione, gestione del rischio..." — costruzione tipica da template.
- Tutti i numeri ci sono (30 anni, 10+ progetti, team 3-7, budget €100K-€500K) ma annegano nel testo.
- Le aziende reali (Atradius, Generali, TIM/Huawei, Telepass, Banca d'Italia, CDP) **non sono mai nominate**.
- Chiude con il punto-forza giusto ("parlare la stessa lingua del team di sviluppo... rischi tecnici prima che diventino problemi") ma senza enfasi, mescolato a tutto il resto.

---

## Versione A — Identità tecnica come differenziatore

> Trent'anni nei database. Oracle, PostgreSQL, MySQL.
>
> Architetto Data Warehouse. DBA. Sviluppatore PL/SQL.
> Poi Project Manager. Non in alternativa. In aggiunta.
>
> Oltre 10 progetti chiusi tra il 2013 e il 2020. Team da 3 a 7 persone. Budget tra €100K e €500K.
> Multi-paese, full-remote, multilingua.
>
> Banking. Telco. Assicurazioni. Pubblica Amministrazione.
> Atradius, Generali, TIM via Huawei, Telepass, Banca d'Italia, Cassa Depositi e Prestiti, PA via Auselda.
>
> Metodo: Agile e Scrum. Formazione certificata 2024.
> Sprint planning, retrospective, backlog refinement. Non rito. Strumento.
>
> Differenza rispetto a un PM puro: leggo il piano architetturale, capisco la stima di sviluppo, vedo il rischio tecnico prima che diventi un ticket.

**Asse**: chi sono → cosa ho fatto → con chi → come lavoro → cosa porto in più. ~95 parole.

---

## Versione B — Numeri e clienti come ariete

> Project Manager con background tecnico.
> Oracle, PL/SQL, Data Warehouse, performance tuning. Trent'anni.
>
> 10+ progetti delivered tra il 2013 e il 2020. Team 3-7 persone. Budget €100K-€500K. Consegne quasi sempre rispettate.
>
> Settori reali: Banking, Telco, Assicurazioni, Pubblica Amministrazione.
> Clienti reali: Atradius (Surety multi-paese EU), Generali (database 500GB-8TB), TIM/Huawei (Exadata, 70+ istanze, reperibilità 24/7), Telepass, Banca d'Italia, Cassa Depositi e Prestiti.
>
> Numeri che ricordo dei progetti che ho gestito:
> Batch portati da 4 ore a 30 minuti. Pipeline ETL da 15+ sorgenti su 2 miliardi di righe. Ingestione DWH giornaliera completa in meno di 2 ore. 60.000 righe di codice PL/SQL coordinate end-to-end.
>
> Metodologia: Agile, Scrum, formazione certificata 2024.
> Strumenti: Jira, MS Project, Git/GitHub, Excel/Sheets a livello avanzato.
>
> Approccio: la roadmap è un piano. Non un'opera d'arte. Va eseguita.

**Asse**: numeri concreti prima, contesto dopo. Più "marketing-ready" per recruiter che fanno screening rapido. ~140 parole.

---

## Versione C — PM tecnico come ruolo distinto

> Esiste il PM che gestisce il progetto. E il PM che capisce il progetto.
> Io sono il secondo.
>
> Trent'anni dentro Oracle, PL/SQL, Data Warehouse, performance tuning.
> Da dieci ne uso per fare anche il Project Manager.
>
> Cosa vedo che un PM puro fa fatica a vedere:
> quando un requisito non è implementabile come scritto.
> Quando una stima dello sviluppatore è ottimistica per pressione, non per dati.
> Quando il vero rischio non è la deadline. È l'architettura.
>
> 10+ progetti chiusi tra il 2013 e il 2020. Team 3-7 persone. Budget €100K-€500K. Multi-paese, full-remote.
> Settori: Banking, Telco, Assicurativo, Pubblica Amministrazione.
> Clienti: Atradius, Generali, TIM/Huawei, Telepass, Banca d'Italia, Cassa Depositi e Prestiti.
>
> Scrum e Agile, formazione certificata.
> Sprint, backlog, retrospective. Strumenti. Non rituali.
>
> Cosa porto in un progetto: traduzione tecnica dei requisiti, scoperta precoce dei rischi, una sola lingua per il team e per gli stakeholder.

**Asse**: dichiara subito il posizionamento ("PM tecnico, non PM puro") e lo difende con esempi concreti di cosa significa. ~145 parole.

---

## Tabella di confronto

| | Originale | Versione A | Versione B | Versione C |
|---|---|---|---|---|
| **Apertura** | "Project Manager con quasi 30 anni..." | Identità in 2 frasi nominali | Etichetta professionale | Dichiarazione di posizionamento ("io sono il secondo") |
| **Punto forte** | Punto-chiusura tecnico | Naturalezza narrativa | Densità di numeri/clienti | Differenziatore esplicito |
| **Rischio** | Annega tutto in un blocco unico | Aggressiva quanto basta | Può sembrare LinkedIn-style | Apertura provocatoria — non a tutti piace |
| **Lunghezza** | ~140 parole | ~95 parole | ~140 parole | ~145 parole |
| **A chi parla meglio** | Tutti, ma senza colpire nessuno | HR/cliente che vuole capire il profilo | Recruiter in screening rapido | Cliente diretto che ti compra come consulente |
| **Cita clienti reali** | No | Sì (6 nomi) | Sì (6 nomi) | Sì (6 nomi) |
| **Cita metriche tecniche** | No | No | Sì (4 metriche) | No |

---

## Round 2 — versioni compattate (3 paragrafi ciascuna)

**Feedback Ivan 2026-06-18**: le versioni round-1 (sparse, con a-capo a ogni 2-3 parole) occupavano troppo spazio verticale sulla pagina della roadmap. Lo stile Borzacchiello si può mantenere riducendo gli a-capo: il ritmo viene dalla punteggiatura (punti fermi frequenti, frasi corte, antitesi binarie, frasi nominali), non dal layout. 3 paragrafi tematici è l'equilibrio tra "compatto" e "non monolitico come l'originale".

### Versione A — Identità tecnica (compatta)

> Trent'anni nei database — Oracle, PostgreSQL, MySQL. Architetto Data Warehouse, DBA, sviluppatore PL/SQL. Poi Project Manager. Non in alternativa: in aggiunta.
>
> Oltre 10 progetti chiusi tra il 2013 e il 2020, team da 3 a 7 persone, budget €100K-€500K, multi-paese, full-remote, multilingua. Banking, Telco, Assicurazioni, Pubblica Amministrazione: Atradius, Generali, TIM via Huawei, Telepass, Banca d'Italia, Cassa Depositi e Prestiti.
>
> Metodo: Agile e Scrum, formazione certificata 2024. Sprint planning, retrospective, backlog refinement — strumenti, non riti. Differenza rispetto a un PM puro: leggo il piano architetturale, capisco la stima di sviluppo, vedo il rischio tecnico prima che diventi un ticket.

(~115 parole, 3 paragrafi)

### Versione B — Numeri e clienti (compatta)

> Project Manager con background tecnico. Oracle, PL/SQL, Data Warehouse, performance tuning. Trent'anni.
>
> 10+ progetti delivered tra il 2013 e il 2020, team 3-7 persone, budget €100K-€500K, consegne quasi sempre rispettate. Settori: Banking, Telco, Assicurazioni, Pubblica Amministrazione. Clienti: Atradius (Surety multi-paese EU), Generali (database 500GB-8TB), TIM/Huawei (Exadata, 70+ istanze, reperibilità 24/7), Telepass, Banca d'Italia, Cassa Depositi e Prestiti.
>
> Numeri che ricordo dei progetti gestiti: batch portati da 4 ore a 30 minuti, pipeline ETL da 15+ sorgenti su 2 miliardi di righe, ingestione DWH giornaliera completa in meno di 2 ore, 60.000 righe di codice PL/SQL coordinate end-to-end. Metodologia Agile/Scrum, formazione certificata 2024. Strumenti: Jira, MS Project, Git/GitHub. Approccio: la roadmap è un piano, non un'opera d'arte. Va eseguita.

(~145 parole, 3 paragrafi)

### Versione C — PM tecnico come ruolo distinto (compatta)

> Esiste il PM che gestisce il progetto. E il PM che capisce il progetto. Io sono il secondo. Trent'anni dentro Oracle, PL/SQL, Data Warehouse, performance tuning — da dieci ne uso per fare anche il Project Manager.
>
> Cosa vedo che un PM puro fa fatica a vedere: quando un requisito non è implementabile come scritto. Quando una stima dello sviluppatore è ottimistica per pressione, non per dati. Quando il vero rischio non è la deadline, è l'architettura.
>
> 10+ progetti chiusi tra il 2013 e il 2020, team 3-7 persone, budget €100K-€500K, multi-paese e full-remote. Settori: Banking, Telco, Assicurativo, Pubblica Amministrazione. Clienti: Atradius, Generali, TIM/Huawei, Telepass, Banca d'Italia, Cassa Depositi e Prestiti. Scrum e Agile, formazione certificata. Cosa porto: traduzione tecnica dei requisiti, scoperta precoce dei rischi, una sola lingua per team e stakeholder.

(~140 parole, 3 paragrafi)

### Confronto round-1 vs round-2

| Versione | Round 1 (sparso) | Round 2 (compatto) | Riduzione righe |
|---|---|---|---|
| A | 13 righe verticali | ~9 righe (3 paragrafi) | ~30% |
| B | 18 righe verticali | ~10 righe (3 paragrafi) | ~45% |
| C | 19 righe verticali | ~11 righe (3 paragrafi) | ~40% |

Tutte e 3 le versioni round-2 occupano spazio verticale **comparabile all'originale** (che era 1 paragrafo di ~8 righe renderizzate), pur con tono e densità informativa completamente diversi.

---

## Versione finale scelta (2026-06-18) — APPLICATA AL FILE LIVE

Variante adottata: **C compatta** (3 paragrafi) con due micro-aggiustamenti rispetto al draft:

1. Apertura del paragrafo 2: passato da "Cosa vedo che un PM puro fa fatica a vedere:" a **"Quello che riconosco subito su un progetto:"** (round 3, C.3) — eliminato il posizionamento per contrasto col PM puro, sostituito da un'apertura affermativa che non si appoggia sulla debolezza altrui. Coerente con le linee guida anti-eroe del blog.
2. Paragrafo 2, secondo esempio: "una stima dello sviluppatore" → **"una stima"** — accorciato senza perdere il punto.

### Testo applicato (IT, master)

> Esiste il PM che gestisce il progetto. E il PM che capisce il progetto. Io sono il secondo. Trent'anni dentro Oracle, PL/SQL, Data Warehouse, performance tuning — da dieci ne uso per fare anche il Project Manager.
>
> Quello che riconosco subito su un progetto: quando un requisito non è implementabile come scritto. Quando una stima è ottimistica per pressione, non per dati. Quando il vero rischio non è la deadline, è l'architettura.
>
> 10+ progetti chiusi tra il 2013 e il 2020, team 3-7 persone, budget €100K-€500K, multi-paese e full-remote. Settori: Banking, Telco, Assicurativo, Pubblica Amministrazione. Clienti: Atradius, Generali, TIM/Huawei, Telepass, Banca d'Italia, Cassa Depositi e Prestiti. Scrum e Agile, formazione certificata. Cosa porto: traduzione tecnica dei requisiti, scoperta precoce dei rischi, una sola lingua per team e stakeholder.

Tradotto contestualmente in tutte e 4 le lingue (IT/EN/ES/RO). ES e RO mantengono la convenzione "no diacritics nel body" del file preesistente, per coerenza visiva con il resto della pagina.

---

## Decisioni chiuse

- [x] Scelta variante: **C compatta + C.3 sull'apertura del paragrafo 2**.
- [x] Mantenere nomi clienti diretti: **sì** (Atradius, Generali, TIM/Huawei, Telepass, Banca d'Italia, CDP).
- [x] Metriche tecniche dei progetti gestiti nel paragrafo: **no** (mantenuto stile asciutto C, niente numeri batch/righe/sorgenti che invece appartengono a B).

## Decisioni ancora aperte (per cicli futuri)

- [ ] Stile Borzacchiello applicato anche agli altri 3 profili (DWH Architect, Oracle DBA, PL/SQL) o solo a PM? — Decisione architetturale: se sì serve coerenza, se no il PM diventa il pezzo "speciale" della sezione.
- [ ] PDF `CV_Project_Manager_Ivan_Luminaria_202603_EN.pdf`: aggiornare anche il PDF EN con un'introduzione coerente con il nuovo paragrafo web, o lasciare il PDF allineato al vecchio profilo CV-classico?
- [ ] Lo stesso paragrafo aggiornato va portato anche nella **card sulla landing** (`_index.it.md` shortcode `kh-role`)? Oggi la card landing mostra un testo introduttivo separato.
- [ ] Le 4 occorrenze di "PM" nel paragrafo "Profilo Professionale" (usate come **concetto generico**, non come titolo di ruolo) sono state lasciate intatte. Decidere se sostituirle con "Responsabile tecnico di progetto" / "Technical Project Manager" / equivalenti, o se mantenerle perché lì "PM" è la formulazione più naturale per il ritmo della frase.

---

## Round 4 — Esperienza IDEA DB CONSULTING (sotto-blocchi 2022–Presente)

**Sessione 2026-06-18**: refactor del primo blocco "Esperienza Professionale" della pagina PM. Quattro trasformazioni applicate in un'unica modifica:

1. **Riordino dei 3 sotto-incarichi**: ATRADIUS in alto, Banking/Telepass al centro, GENERALI in fondo — riflette il peso strategico (ATRADIUS è il progetto più ampio: 4 paesi EU, 60K righe PL/SQL) e cronologico (ATRADIUS è iniziato per primo).
2. **Date specifiche → durate sintetiche**: `Feb 2024 – Mag 2025`, `2022 – 2026` → `4 anni`, `1 anno`, `1 anno`. Più asciutto, focus sulla durata utile per il lettore.
3. **Bullet → prosa orientata al risultato**: ogni sotto-incarico passa da 3 bullet tecnici a 1-2 frasi che dichiarano il risultato ottenuto. Stile coerente con il "Profilo Professionale" (frasi corte, ritmo punctuated, niente filler).
4. **Sostituzione titolo ruolo**: `PM` → `Responsabile tecnico di progetto` (IT) / `Technical Project Manager` (EN) / `Responsable tecnico de proyecto` (ES, no diacritics per coerenza body) / `Responsabil tehnic de proiect` (RO, no diacritics).

### Testo applicato (IT, master)

```markdown
- **Responsabile tecnico di progetto & DWH Lead** (per ATRADIUS) | 4 anni:
  Data Warehouse della divisione Surety consolidato su 4 paesi europei. Ingestione giornaliera completa sotto le 2 ore.

- **Project Coordinator** (Banking, Telepass e altri clienti) | 1 anno:
  Batch analitici portati da 4 ore a meno di 30 minuti su dataset oltre i 2 miliardi di righe.

- **Responsabile tecnico di progetto & DWH Lead** (per GENERALI Assicurazioni) | 1 anno:
  Team di sviluppo Oracle coordinato su database assicurativi da 500GB a 8TB. Scope gestito dai requisiti al rilascio.
```

### Info informativa caduta consapevolmente

Le seguenti metriche/dettagli erano nei bullet originali e sono stati rimossi nella prosa orientata al risultato:

- "60.000 righe di codice PL/SQL ETL" (ATRADIUS) — il risultato chiave è il DWH consolidato + ingestione <2h, il volume di codice non aggiunge segnale per il lettore
- "15+ sorgenti eterogenee" (Banking/Telepass) — mezzo non fine: il risultato è il 4h→30min
- "Rilasci in Oracle OCI/Autonomous DB" (Banking/Telepass) — tecnologia specifica non rilevante per il punto
- "Tracking, reporting, dipendenze tra team" (ATRADIUS) — attività implicite nel ruolo "Responsabile tecnico di progetto & DWH Lead"
- "Raccolta requisiti, scope, presentazione soluzioni" (GENERALI) — compresso in "Scope gestito dai requisiti al rilascio"

### Layout fix (round 5)

Subito dopo l'applicazione, layout aggiustato: rimosso `:` finale dopo le durate (era residuo del formato bullet), e aggiunta riga vuota tra l'header del sotto-incarico e la prosa risultato. Goldmark ora rende la prosa come paragrafo separato dentro il `<li>`, invece di farla apparire in continuità con la riga del bullet.

---

## Round 6 — Esperienza NIMIS CONSULTING (TIM/HUAWEI, 2020-2022)

**Sessione 2026-06-18**: stesso metodo dei round precedenti applicato al secondo blocco "Esperienza Professionale" della pagina PM. Differenza strutturale rispetto a IDEA DB CONSULTING: NIMIS non aveva sotto-incarichi multipli, era un singolo ruolo (DBA per TIM/HUAWEI) con 3 bullet di attività. Quindi niente riordino, solo trasformazione bullet→prosa + durata sintetica.

Trasformazioni applicate:

1. **Date specifiche → durata sintetica**: `2020 – 2022` → `2 anni`. Coerente con il round IDEA DB CONSULTING (4 anni / 1 anno / 1 anno).
2. **3 bullet → 1 prosa risultato (2 frasi)**: focus sulla scala tecnica gestita (30+ DB, 70+ istanze Exadata, 20M abbonati, 800M record/giorno).
3. **Layout**: stessa struttura della precedente (durata senza `:`, prosa come paragrafo separato sotto l'header del ruolo).

### Testo applicato (IT, master)

```markdown
### NIMIS CONSULTING S.R.L. — Roma, Italia (Full Remote)
**Senior Oracle DBA & Performance Tuning Expert** (per TIM / HUAWEI) | 2 anni

Parco di 30+ database Oracle critici (70+ istanze su cluster Exadata) a supporto di oltre 20 milioni di abbonati mobile prepagati. Tuning e patching su tabelle dei fatti con ingestione fino a 800 milioni di record di traffico telefonico al giorno.
```

### Scelte editoriali

- **Titolo del ruolo invariato**: "Senior Oracle DBA & Performance Tuning Expert" è il titolo nominale del contratto NIMIS. Nel CV PM non viene rinominato retroattivamente — la scelta è ammettere onestamente che il ruolo era DBA, ed enfatizzare gli aspetti che hanno valore anche in un CV PM (scala del progetto gestito, criticità mission-critical, interfaccia con team di sviluppo).
- **Numeri 20M abbonati e 800M record/giorno**: presi dal CV DWH Architect dello stesso periodo NIMIS/TIM/HUAWEI (sono ufficiali, già usati altrove). Riportarli qui amplifica il segnale "wow" rispetto ai soli 30+ DB / 70+ istanze, e rinforza il positioning "PM tecnico" già dichiarato nel Profilo Professionale.
- **Variante 2 scartata**: c'era anche un'opzione più PM-oriented ("Interfaccia tecnica al team di sviluppo per prioritizzazione degli interventi e patching pianificato in 24/7"). Scartata perché meno asciutta, più descrittiva e meno coerente con il pattern dei sotto-incarichi ATRADIUS/GENERALI (numeri-wow secchi).

### Info caduta consapevolmente

- "Pianificazione ed esecuzione manutenzione/patching" → "patching" basta (la pianificazione è implicita)
- "Coordinamento con team di sviluppo" / "supporto tecnico specializzato" / "prioritizzazione degli interventi" → tutti compressi (impliciti nel ruolo)
- "Gestione autonoma del proprio carico di lavoro" → dropped (caratteristica generica del ruolo senior)
- "Reportistica verso il responsabile di progetto" → dropped (attività gestionale standard)

---

## Round 7 — Esperienza LIBERO PROFESSIONISTA / CONSULENTE INDIPENDENTE (2013-2020)

**Sessione 2026-06-18**: rifacimento del terzo blocco "Esperienza Professionale" della pagina PM. Stesso pattern dei round precedenti, con due novità rispetto a NIMIS:

1. **Esteso il rinome ruolo** "Project Manager" → "Responsabile tecnico di progetto" (IT) / "Technical Project Manager" (EN) / "Responsable tecnico de proyecto" (ES) / "Responsabil tehnic de proiect" (RO) anche all'header del ruolo, perché qui "Project Manager" era scritto per esteso (non come acronimo "PM"). Decisione presa per coerenza con il positioning del CV.
2. **Aggiunta precisazione tra parentesi sul ruolo**: `(Società di consulenza e Clienti diretti)` — esplicita le due tipologie di acquisizione cliente durante il periodo freelance. Pattern di parentesi mutuato da NIMIS `(per TIM / HUAWEI)`.

### Testo applicato (IT, master)

```markdown
### LIBERO PROFESSIONISTA / CONSULENTE INDIPENDENTE — Roma, Italia (Full Remote Europa)
**Responsabile tecnico di progetto & Senior DWH Consultant** (Società di consulenza e Clienti diretti) | 7 anni

10 progetti delivered in 7 anni per clienti nei settori Banking, Telco e servizi, con budget €100K-€500K. Team 3-7 persone in contesti multiculturali e distribuiti, coordinati con approccio Agile.
```

### Scelte editoriali

- **Header datore invariato**: l'utente ha esplicitamente confermato di non sostituire `LIBERO PROFESSIONISTA / CONSULENTE INDIPENDENTE` con `SOCIETÀ DI CONSULENZA E CLIENTI DIRETTI`. La precisazione va in parentesi sul ruolo, non come header.
- **Durata 7 anni** coerente con i round precedenti (4/1/1 anni IDEA DB CONSULTING, 2 anni NIMIS).
- **Numeri mantenuti**: i numeri del Profilo Professionale (10 progetti, 7 anni, settori, €100K-€500K, team 3-7, multiculturale/distribuito, Agile) vengono ripetuti qui come "dettaglio dell'esperienza specifica". Non ridondanza nociva, perché il Profilo Professionale è sintesi mentre questa sezione è il dettaglio del periodo.

### Decisione aperta scartata (per ora)

- **Scope-creep IDEA DB CONSULTING**: il blocco IDEA DB CONSULTING ha ancora "Project Manager & Senior DWH Architect" come header del ruolo. L'utente ha esplicitamente detto di NON includere il rinome in questo commit. Ripreso eventualmente in un ciclo separato.

### Info caduta consapevolmente

- "Consegne quasi sempre rispettate" → già nel Profilo Professionale, ridondante qui
- "Assegnazione dei compiti / facilitazione collaborazione / gestione priorità" → attività standard di team coordination, implicite nel ruolo
- "Interfaccia diretta con clienti per requisiti/scope/avanzamenti/aspettative" → compresso in "coordinati con approccio Agile" (la raccolta requisiti è parte di Agile)
- "**Formazione tecnica e mentoring**" — l'utente ha esplicitamente confermato di non reintrodurla come 3a frase. Lasciata fuori per asciuttezza.

---

## Riferimenti

- File live target: `content/resumes/project-manager/index.it.md` (sezione `## Profilo Professionale`, riga 17)
- Diff finale verrà applicato qui solo dopo l'approvazione esplicita della variante scelta.
- Pagina renderizzata in locale: <http://ilum.local:1313/it/resumes/project-manager/>
- Branch di lavoro: `claude/resumes-refactor` (creata da `main` il 2026-06-18, isolata dal lavoro Bonjour LAN che vive su `claude/work-in-progress`).
