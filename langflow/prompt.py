def get_classification_prompt(document_text: str):
    return f"""Ton but est de classifier le document suivant en fonction de son contenu.  
Réponds uniquement en JSON ({{"category": "XXX"}}), sans explication ni texte supplémentaire.  

### **Catégories possibles** :  
- **ATTESTATION_AFFILIATION_URSSAF** : Attestation officielle d'affiliation à l'URSSAF, mentionnant l'affiliation d'une entreprise ou d'un indépendant. Recherchez des termes comme "Attestation d'affiliation", "URSSAF", "cotisations sociales", "numéro SIRET".  
- **RIB** : Document contenant des informations bancaires comme un IBAN, un BIC, un numéro de compte ou le titre "Relevé d'Identité Bancaire".  
- **CARTE_IDENTITE_PASSEPORT** : Document officiel d'identité comme une carte nationale d’identité ou un passeport. Recherchez "Carte nationale d'identité", "Passeport", une photo d'identité et des champs comme "Nom", "Prénom", "Date de naissance".  
- **JUSTIFICATIF_DOMICILE** : Facture ou attestation prouvant le domicile (facture EDF, téléphone, quittance de loyer, attestation d’hébergement). Recherchez "Adresse", "Facture", "Quittance", "EDF", "Free", "Orange", etc.  
- **EXTRAIT_ACTE_NAISSANCE** : Document officiel d’état civil contenant les informations de naissance d’une personne. Recherchez "Extrait d’acte de naissance", "Mairie", "Naissance de".  
- **AVIS_IMPOSITION** : Document fiscal émis par l’administration fiscale, indiquant les revenus et l’impôt à payer. Recherchez "Avis d'imposition", "Impôt sur le revenu", "Direction générale des finances publiques (DGFIP)".  
- **FICHE_DE_PAIE** : Bulletin de salaire contenant des informations sur le revenu et les cotisations sociales. Recherchez "Salaire brut", "Salaire net", "Cotisations sociales", "Employeur".  
- **PERMIS_DE_CONDUIRE** : Document officiel attestant du droit de conduire. Recherchez "Permis de conduire", une photo d’identité et des champs comme "Nom", "Prénom", "Catégorie".  
- **INCONNU** : Si le document ne correspond à aucune catégorie ci-dessus.  
- **CARTE_GRISE** : Certificat d’immatriculation d’un véhicule, mentionnant des informations comme le numéro d’immatriculation, le titulaire du véhicule et les caractéristiques du véhicule. Recherchez des termes comme "Certificat d’immatriculation", "Immatriculation", "Carte grise", "Titulaire", "D.1", "D.2", "D.3", "E".

Voici le document
---
{document_text}
---


Quel est sa catégorie?"""