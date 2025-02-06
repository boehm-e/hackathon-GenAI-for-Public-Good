# demarches-simplifiees.fr

![Demo](demo.gif)

## Validateur de fichiers HTML

Une solution pour valider automatiquement les documents des utilisateurs dans les champs de saisie. 
Ce projet permet de gagner du temps en s'assurant que le bon type de document est téléchargé avant la soumission du formulaire.

## Fonctionnalités

- Validation en temps réel du type de fichier
- Repose sur le DSFR 
- Intégration facile avec les formulaires HTML existants
- Restrictions personnalisables des types de fichiers
- Ajout d'un type de document facile, en modifiant `langflow/prompt.py`

## Comment ça marche

Le système utilise un modèle d'OCR open source ([Florence-2](https://huggingface.co/microsoft/Florence-2-base)) et un LLM ([Llama 3.1:8b](https://huggingface.co/meta-llama/Llama-3.1-8B)) pour classifier automatiquement les documents.

