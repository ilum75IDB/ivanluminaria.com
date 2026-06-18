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

---

## Riferimenti

- File live target: `content/resumes/project-manager/index.it.md` (sezione `## Profilo Professionale`, riga 17)
- Diff finale verrà applicato qui solo dopo l'approvazione esplicita della variante scelta.
- Pagina renderizzata in locale: <http://ilum.local:1313/it/resumes/project-manager/>
- Branch di lavoro: `claude/resumes-refactor` (creata da `main` il 2026-06-18, isolata dal lavoro Bonjour LAN che vive su `claude/work-in-progress`).
