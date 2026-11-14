# Career Radar — Italia & Spagna

Dashboard personale per opportunità in **Milano/Monza, Barcellona, Madrid, Valencia e Siviglia**.

## Sito
Dopo aver abilitato GitHub Pages in **Settings → Pages → Build and deployment → Source: GitHub Actions**, apri:

**https://masinisa99-debug.github.io/career-radar/**

## Funzioni
- 35 annunci e 69 aziende target iniziali, filtri e scoring orientativo
- Pipeline candidature, shortlist, note, follow-up e contatti
- Import da JSON/CSV ed export backup JSON
- Salvataggio **nel browser (localStorage)**; non c'è un account o un database
- Aggiornamento automatico da una selezione di board pubblici Ashby / Greenhouse: GitHub Actions produce `feed/jobs.json` ogni giorno

## Attivazione aggiornamenti
1. Settings → Pages → Build and deployment → seleziona **GitHub Actions**.
2. Settings → Actions → General: verifica i permessi di scrittura, se il job segnala un errore.
3. Actions → **Aggiorna Career Radar** → Run workflow (facoltativo: viene anche eseguito su push e una volta al giorno).
4. Il feed viene letto automaticamente dalla dashboard quando apri il sito pubblicato; oppure premi “Controlla feed”.

Il collector controlla solo i seguenti board pubblici: Perk, Lexroom, fonio, Pillar e Scalapay. **Non esegue scraping di LinkedIn**. Gli annunci e le condizioni linguistiche vanno verificati sui siti ufficiali. La verifica automatica NON copre tutte le aziende, né aggiorna istantaneamente gli annunci.

## Privacy
**Questo repository è pubblico.** Non caricare CV, note private, email, backup delle candidature o informazioni personali. Le note vengono salvate nel singolo browser e non sono sincronizzate tra computer e telefono. Usa periodicamente “Dati & backup” per esportare un JSON; importalo su un altro dispositivo se necessario.

## Struttura
- `index.html`: app completa autonoma con dati iniziali embedded
- `feed/jobs.json`: feed ATS aggiornabile
- `scripts/refresh_jobs.py`: collezione e filtro ATS
- `.github/workflows/update-jobs.yml`: job giornaliero / deploy Pages

Creato il 14 novembre 2026.
