# ADR-025 — proposition à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À coller dans le *Journal de décisions
> (ADR)* de Confluence une fois relu par le groupe. Rien ne s'écrit sur
> Confluence depuis le dépôt.
>
> ⚠️ **Numéro à vérifier.** Il suit `ADR-024` (21/09/2026), lui-même encore au
> statut « proposé ». Même réserve de numérotation que pour l'ADR-024.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

**ADR-025 : Chaque chasseur est rattaché à un manager**

**Date :** 22/09/2026
**Statut :** proposé
**Décideurs :** L'équipe projet

**Contexte**

Le MPD 03 relie déjà le manager (`real_estate_manager`) à la demande de
recherche (`search_request.id_realestatemanager`), mais rien ne relie un
chasseur à un manager. Le rôle `Manager` existe en base sans qu'aucun chasseur
ne lui soit rattaché.

Le sujet parle pourtant du manager **d'un** chasseur : « L'accès aux données
de rémunération est restreint au chasseur concerné et à son manager »
(`CAHIER-DES-CHARGES-TECHNIQUE.md` l. 97, exemple ENF-03 ; repris dans
`REGLES-CALCUL-REMUNERATION.md` l. 296 et 763). Ce lien est nécessaire pour
appliquer ce contrôle d'accès.

⚠️ ENF-03 est un **exemple rempli dans un modèle de document**, pas une
exigence du client. Les user stories ne citent jamais de manager, et les
fixtures n'ont que deux rôles (`client`, `chasseur`). La décision est donc un
choix de modélisation de l'équipe, pas l'application d'une règle du sujet.

**Options envisagées**

- Option 1 : ne rien ajouter — le manager d'un chasseur se déduit des demandes
  qu'il traite. Rejetée : un chasseur sans demande n'a alors aucun manager, et
  deux demandes peuvent donner deux managers.
- Option 2 : `hunter.id_realestatemanager` **nullable** (0,1). Rejetée pour
  l'instant : la base ne garantit pas la règle, tout repose sur l'API.
- Option 3 : `hunter.id_realestatemanager` **NOT NULL** (1,1), FK vers
  `real_estate_manager(id_user)`, `ON DELETE RESTRICT`. **Retenue.**

**Décision**

Option 3. Relation Hunter (1,1) — RealEstateManager (0,n), libellée
« Manages » sur le MPD 03 4. Même convention que toutes les FK du schéma : la
colonne pointe vers `id_user`.

Pas d'historique des changements de manager : seul le manager courant est
connu. Suffisant pour le contrôle d'accès ENF-03.

**Conséquences**

- `real_estate_manager` est créée avant `hunter` dans le script de schéma.
- Les 6 chasseurs des fixtures n'ont aucun manager dans la source : la
  migration crée un **manager placeholder** (compte bloqué, nom bidon) et les
  lui rattache. Hypothèse de migration, documentée
  (`docker/init-v2/README.md` §3.6). Le seed devra le remplacer.
- Base déjà créée : `docker/migrations/2026-09-22_hunter_manager.sql`,
  rejouable.
- API : `Hunter.id_realestatemanager` obligatoire.
- Deux liens « Manages » coexistent sur le MPD : le manager **de la demande**
  et le manager **du chasseur**. Rien n'impose qu'ils coïncident. À assumer, ou
  renommer le second « Supervises ».

**Vérification (22/09/2026)**

PostgreSQL 16, base neuve et base migrée : 7 cas adverses sur 7 identiques
(`NOT NULL`, FK, `RESTRICT`, 0,n, changement de manager). Détail :
`docker/init-v2/README.md` §9.3.

---

**À corriger dans le drawio, hors ADR :** `criteria.budget_max NUMERIC (12.2)`
— un point au lieu d'une virgule. Le script lit `(12, 2)`.
