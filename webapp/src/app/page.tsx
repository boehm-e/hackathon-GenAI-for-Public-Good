"use client"
import { Upload } from "@codegouvfr/react-dsfr/Upload";
import { useState } from "react";
import { CircularProgress } from "@mui/material";
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';


const categoryMap = {
  "ATTESTATION_AFFILIATION_URSSAF": "Attestation d'affiliation URSSAF",
  "RIB": "Relevé d'identité bancaire",
  "CARTE_IDENTITE_PASSEPORT": "Carte d'identité ou passeport",
  "JUSTIFICATIF_DOMICILE": "Justificatif de domicile",
  "EXTRAIT_ACTE_NAISSANCE": "Extrait d'acte de naissance",
  "AVIS_IMPOSITION": "Avis d'imposition",
  "FICHE_DE_PAIE": "Fiche de paie",
  "PERMIS_DE_CONDUIRE": "Permis de conduire",
  "INCONNU": "Document inconnu",
  "CARTE_GRISE": "Carte grise",
}

const getCategoryName = (cat: string): string => {
  return cat in categoryMap ? categoryMap[cat as keyof typeof categoryMap] : "INVALID"
}

const UploadDocumentChecker = (props: { category: string }) => {
  const { category } = props;

  const [success, setSuccess] = useState(false);
  const [documentType, setDocumentType] = useState("");
  const [loading, setLoading] = useState(false);

  return (
    <div className="flex flex-row gap-8 items-center">
      <Upload
        hint="Taille maximale : 10 Mo. Formats supportés : jpg, png, pdf. Un seul fichier possible."
        label={<h3>{getCategoryName(category)}</h3>}
        state={success ? "success" : "default"}
        stateRelatedMessage={success ? "Document téléversé avec succès" : `Il semblerait que votre document soit de type ${getCategoryName(documentType)}`}
        nativeInputProps={{
          multiple: false,
          accept: ".jpg, .png, .pdf",
          onChange: async (e) => {
            const file = e.target.files?.[0];
            if (file) {
              setLoading(true);
              const formData = new FormData();
              formData.append('file', file);
              try {
                const response = await fetch('http://localhost:8000/upload', {
                  method: 'POST',
                  body: formData,
                });
                if (!response.ok) {
                  throw new Error('Upload failed');
                }
                const data = await response.json();
                if (data.category === category) {
                  setSuccess(true);
                } else {
                  setSuccess(false);
                }
                setDocumentType(data.category)
              } catch (error) {
                console.error('Error uploading file:', error);
              } finally {
                setLoading(false);
              }
            }
          }
        }}
      />
      {loading && <CircularProgress />}
      {!loading && documentType && (
        success ? <CheckCircleIcon color="success" /> : <div className="flex flex-col gap-2">
          <CancelIcon color="error" />
          <p className="m-0">Document attendu: <b>{getCategoryName(category)}</b> </p>
          <p className="m-0">Document fourni: <b>{getCategoryName(documentType)}</b> </p>
        </div>
      )}
    </div>
  );
}


export default function Home() {
  return (
    <div className="w-full fr-grid-row fr-grid-row--gutters fr-grid-row--center">
      <div className="fr-col-12 fr-col-md-8 main-content-item my-24">
        <div className="flex flex-col gap-24">
          <UploadDocumentChecker category="CARTE_GRISE" />
          <UploadDocumentChecker category="CARTE_IDENTITE_PASSEPORT" />
          <UploadDocumentChecker category="JUSTIFICATIF_DOMICILE" />
        </div>

      </div>
    </div >
  );
}