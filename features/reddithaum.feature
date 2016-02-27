# language: fr

Fonctionnalité: Afficher les nouveaux liens postés
	Scénario: Aucun nouveau lien n’a été posté
		Étant donné que aucun lien n’a été posté
        Et que les nouveaux liens ont été vérifiés "60" secondes auparavant
		Lorsque le programme vérifie les nouveaux liens postés
		Alors il n’envoie aucune notification

	Scénario: Un nouveau lien a été posté
		Étant donné qu’un lien a été posté
        Et que les nouveaux liens ont été vérifiés "60" secondes auparavant
		Lorsque le programme vérifie les nouveaux liens postés
		Alors il envoie une notification avec le nouveau lien

	Scénario: Vérification à rythme insoutenable
		Étant donné que les nouveaux liens ont été vérifiés "59" secondes auparavant
		Lorsque le programme vérifie les nouveaux liens postés
		Alors une sécurité empêche la requête vers l’API
