### ADR-057 : Les clés et les rôles des fiches — les liens visent la fiche, le rôle vit sur la fiche ou sur `system_role`

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 15/10/2026
* **Statut :** ✅ accepté (Sébastien, Discord, 15/10/2026 : 11 questions tranchées aux boutons, après discussion avec Gabriel et Laurence). Remplace **ADR-056**.
* **État du code :** ✅ codé le 15/10/2026, chantier PRF (`context AI/16-refacto-profils.md`, fiches PRF1 à PRF9). Le trigger du point 5 pose aussi un 4ᵉ déclencheur, sur `"user".system_role`.
* **Décideurs :** Sébastien ; proposition « drapeaux sur `user` » de Gabriel ; questions de Laurence sur `is_admin` et `is_reader` (Discord, 15/10/2026) ; découpage d'origine de Robin HOTTON (prof, 14/10/2026).
* **Voir aussi :** ADR-056 (remplacé) ; ADR-027 (droits, « le sien ») ; ADR-052 (jeton JWT) ; ADR-058 (chasseur IA)

**Contexte**

* ADR-056 a gardé les liens par `id_user` et prévu une refacto, le découpage de Robin HOTTON. Sébastien l'a lancée le 15/10/2026, sans attendre l'avis de Robin.
* Comptés le 14/10/2026 dans le schéma v3 (dépôt Fil-Rouge-API) : **11** clés étrangères visent `client(id_user)`, `hunter(id_user)` ou `real_estate_manager(id_user)`, **0** visent leur `id`.
* Les noms `id_client`, `id_hunter`, `id_realestatemanager` laissent croire qu'elles portent le numéro de la fiche. Elles portent le numéro du compte, `user.id`, qui est le `sub` du jeton (`API/src/app/utils/security.py:143`).
* Le rôle vit sur le compte : `user.id_role`, lu par `get_principal` (`API/src/app/utils/roles.py`). Un compte Client peut donc avoir une fiche `hunter`, et rien ne l'empêche.
* Admin et Reader n'ont pas de fiche. Le schéma de Robin ne dit pas où vit leur rôle.

**Options**

*Où vivent les rôles Admin et Reader*

1. **Garder `user.id_role`** pour tout le monde. Écartée : le rôle reste séparé de la fiche, et rien n'empêche l'écart entre les deux.
2. **Deux booléens sur `user`**, `is_admin` et `is_reader` (Gabriel). Écartée : deux cases pour un seul choix, et les deux pourraient être vraies ensemble.
3. **Une colonne `user.system_role`**, `'Admin'` ou `'Reader'`, vide sinon. **Retenue.**

*Comment une fiche porte son rôle*

1. **`id_role` + CHECK** sur chaque fiche. Écartée : un numéro à retenir, et le CHECK doit connaître ce numéro.
2. **`role_wording`**, le nom du rôle, avec une clé vers `role(wording)` et un CHECK sur la seule valeur permise. **Retenue.**

*Un compte et ses fiches*

1. **Plusieurs fiches par compte** (un client qui est aussi chasseur). Écartée : « le sien » devrait savoir quelle fiche est en jeu à chaque requête.
2. **Une fiche au plus par compte**, et pas de fiche pour un compte à `system_role`. **Retenue.**

*Le nom du rôle de gestionnaire* : `'RealEstateManager'` écarté, **`'Manager'` gardé** (le JSON de l'API ne change pas).

*Quand changer les valeurs de l'API* : avec une v4 du schéma, écartée ; **maintenant**, avant qu'un front appelle l'API, retenue.

**Décision**

1. **Les 11 clés visent la PK de la fiche** : `client(id)`, `hunter(id)`, `real_estate_manager(id)`. Les noms des colonnes et du JSON ne changent pas. Leurs **valeurs** changent : un `id_client` attend un `client.id`.
2. **`user` ne sert qu'à la connexion.** Son `id` ne reste que dans les 3 `id_user` des fiches et dans les 4 `id_author` (`search_request`, `criteria`, `estate`, `estate_contact`) : un auteur peut être un Admin sans fiche.
3. **`user.id_role` disparaît.** `user.system_role VARCHAR(10) CHECK (system_role IN ('Admin', 'Reader'))`, vide pour un compte qui a une fiche.
4. **Chaque fiche porte son rôle** : `role_wording VARCHAR(20) NOT NULL DEFAULT '<Rôle>' CHECK (role_wording = '<Rôle>') REFERENCES role(wording)`. La table `role` garde 3 lignes : `'Client'`, `'Hunter'`, `'Manager'`.
5. **Une fiche au plus par compte**, et aucune pour un compte à `system_role`. Un **trigger** le garantit en base, sur les trois tables.
6. **Le rôle se lit** sur `system_role`, sinon sur la fiche du compte. Ni l'un ni l'autre : **403**.
7. **« Le sien »** compare au numéro de la fiche connectée, lu en base à chaque requête. Le jeton ne porte que `sub` (ADR-052).
8. **`AbstractPerson`** : une classe SQLModel sans table. Champs : `created_at`, `id_user`, `first_name`, `last_name`, `phone_number`, `country_iso`, `gender`. `country_iso` y est facultatif ; `Client` le redéclare obligatoire. Les tables SQL ne changent pas.
9. **Le rôle de lecture PostgreSQL `fil_rouge_reader`** suit : `id_role` sort de ses colonnes ouvertes sur `"user"` (`docker/init-v3/04_role-lecture-seule.sql`). Ce rôle n'est **pas** le Reader de l'API, qui est une personne avec un compte.

**Conséquences**

* Trois migrations neuves mènent une base existante au nouveau schéma : 45 (les clés), 46 (les rôles des fiches), 47 (retrait de `id_role`).
* **Après le pull qui clôt le chantier**, chacun refait sa base de dev et rejoue le seed de démo.
* Un client de l'API qui envoyait un `user.id` dans `id_client` reçoit désormais une erreur ou une autre ligne. Il n'y a pas encore de front : le coût est nul aujourd'hui.
* À l'oral, deux phrases suffisent :
  * « le compte sert à se connecter ; la fiche porte la personne, son rôle et ses liens » ;
  * « Admin et Reader n'ont pas de fiche : leur rôle est sur le compte, dans `system_role` ».
* Le MPD (`vrac/v9.drawio`) reçoit le même changement (à faire par le groupe).

**Ce que cet ADR ne tranche pas**

* 🟡 Les droits du chasseur IA (une fiche `hunter` avec `is_hunter_ai`) : ADR-058.
* 🟡 L'avis de Robin HOTTON sur ces choix : pas demandé, risque assumé par Sébastien.

**Sources**

| Affirmation | Source |
|---|---|
| Les 11 questions et leurs réponses | Sébastien, Discord, 15/10/2026 (questions `q15-1` à `q15-8`, `cad-1` à `cad-3`) |
| Proposition « drapeaux sur `user` » | Gabriel, Discord, 15/10/2026 |
| `is_admin` et `is_reader` questionnés | Laurence, Discord, 15/10/2026 |
| Maquette avant / après | https://claude.ai/artifact/YNT5ANwbWYKp6SERVvvn9K |
| 11 clés vers `id_user`, 0 vers `id` | schéma v3, grep du 14/10/2026 (ADR-056) |
| `user.id` = `sub` du JWT | `API/src/app/utils/security.py:143` |
| Le découpage d'origine | Robin HOTTON, relayé par Sébastien, 14/10/2026 ; ADR-056, « Refacto à venir » |
