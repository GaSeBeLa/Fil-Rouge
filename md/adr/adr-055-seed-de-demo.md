### ADR-055 : Le seed de démo — des données fausses, hors des tests

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 14/10/2026
* **Statut :** 💡 proposé (Sébastien, Discord, 14/10/2026, choix A). Pas de report Confluence pour l'instant.
* **Décideurs :** Sébastien (questions Q1 à Q4 du chantier DEM, Discord, 14/10/2026).
* **Voir aussi :** ADR-016 (mot de passe haché) ; ADR-027 et ADR-028 (rôles) ; ADR-035 et ADR-038 (paiement et note du chasseur)

**Contexte**

* Au 14/10/2026, 7 tables de la base de dev sont vides : `estate_proposed`, `estate_searchrequest`, `visit`, `sale`, `payment`, `hunter_performance`, `review_media`.
* Aucun compte de la base n'est actif : les 25 comptes repris n'ont pas de vrai mot de passe (DRO8).
* La démo et la soutenance ont besoin d'un parcours complet à montrer dans le Swagger.

**Décision**

1. **Un script qui appelle les services** (Q2) : `API/src/app/scripts/seed_demo.py`, dans le dépôt Fil-Rouge-API. Aucun appel HTTP, aucun SQL écrit à la main : chaque ligne passe par les règles de l'API, comme un vrai utilisateur.
2. **Des données fausses** (Q3) : Faker `fr_FR`, graine fixe ; **aucune personne réelle**. Emails en `example.com`, domaine réservé à la documentation (RFC 2606). Aucune date tirée du jour.
3. **Les montants ne viennent jamais du hasard** : honoraires et paiement sortent du calcul (`calculer_honoraires`, `PaymentCalculationService.build_payment`).
4. **Quatre comptes neufs** (Q4), un par rôle sauf `Admin`, activés. Mot de passe : `DEMO_PASSWORD`, lu dans `docker/.env`, jamais dans git, jamais affiché.
5. **Le seed n'entre jamais dans les tests** : aucun test ne dépend de ses données, et il refuse d'écrire dans `fil_rouge_test`. Le seed est le décor, les tests sont la preuve.
6. **`faker` à version fixe** dans `requirements.txt`, comme les autres paquets depuis le chantier BAN.

**Conséquences**

* Pour l'équipe, après le pull : `DEMO_PASSWORD=` dans `docker/.env`, puis `docker compose up -d --build`, puis la commande du script (`API/README.md`, « Seed de démo »).
* Le script ne sème qu'une fois par base ; resemer = refaire la base.
* Écart au sujet : en base, l'avis est la note du **chasseur** sur un bien de la sélection, et seul ce chasseur y ajoute un média (ADR-051). Le client n'a pas d'avis à lui.

**Sources**

| Affirmation | Source |
|---|---|
| Q1 à Q4, choix A de l'ADR | Sébastien, Discord, 14/10/2026 |
| Les 7 tables vides | base de dev, comptée le 14/10/2026 (`context AI/15-seed-demo.md`) |
| `.invalid` refusé par l'API | `UserCreate` (email-validator), essayé le 14/10/2026 (`context AI/08-etat.md`) |
| Le média d'avis réservé au chasseur | ADR-051 ; `services/review_media_service.py` |
