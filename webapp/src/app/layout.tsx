import "./globals.css";
import { DsfrHead } from "@codegouvfr/react-dsfr/next-appdir/DsfrHead";
import { DsfrProvider } from "@codegouvfr/react-dsfr/next-appdir/DsfrProvider";
import { getHtmlAttributes } from "@codegouvfr/react-dsfr/next-appdir/getHtmlAttributes";
import { defaultColorScheme } from "./defaultColorScheme";
import { addDisplayTranslations, headerFooterDisplayItem } from "@codegouvfr/react-dsfr/Display";
import { Footer } from "@codegouvfr/react-dsfr/Footer";
import { getScriptNonceFromHeader } from "next/dist/server/app-render/get-script-nonce-from-header"; // or use your own implementation
import { headers } from "next/headers";
import Link from "next/link";
import { JSX } from "react";
import { NextAppDirEmotionCacheProvider } from "tss-react/next";
import Header from "@codegouvfr/react-dsfr/Header";

export default async function RootLayout({ children }: { children: JSX.Element; }) {
  const csp = (await headers()).get("Content-Security-Policy");

  let nonce: string | undefined;
  if (csp) {
    nonce = getScriptNonceFromHeader(csp);
  }

  //NOTE: If we had i18n setup we would get lang from the props.
  //See https://github.com/vercel/next.js/blob/canary/examples/app-dir-i18n-routing/app/%5Blang%5D/layout.tsx
  const lang = "fr";

  return (
    <html {...getHtmlAttributes({ defaultColorScheme, lang })} >
      <head>
        <title></title>
        <DsfrHead
          Link={Link}
          preloadFonts={[
            //"Marianne-Light",
            //"Marianne-Light_Italic",
            "Marianne-Regular",
            //"Marianne-Regular_Italic",
            "Marianne-Medium",
            //"Marianne-Medium_Italic",
            "Marianne-Bold"
            //"Marianne-Bold_Italic",
            //"Spectral-Regular",
            //"Spectral-ExtraBold"
          ]}
          nonce={nonce}
        />

      </head>
      <body>
        <DsfrProvider lang={lang}>
          <NextAppDirEmotionCacheProvider options={{ "key": "css", nonce, prepend: true }}>

            <Header
              className="z-[1]"
              brandTop={<>DEMARCHES SIMPLIFIEES</>}
              // operatorLogo={{
              //   alt: 'logo science infuse',
              //   // imgUrl: '/images/science_infuse_logo.jpg',
              //   // imgUrl: '/images/science_infuse_logo.svg',
              //   orientation: 'horizontal'
              // }}
              quickAccessItems={[]}
              homeLinkProps={{
                "href": "/",
                "title": "Accueil - Science Infuse"
              }}
              serviceTitle="Science Infuse"
              // serviceTagline={<>Contenus multimédias gratuits<br />par la Cité des sciences et de l'industrie et le Palais de la découverte</>}
              // serviceTagline="Création de cours pour les enseignants de SVT au collège"
              // navigation={<Navigation />}
            />

            {children}

            <Footer
              accessibility="partially compliant"
              contentDescription={`
                `}
              bottomItems={[
                headerFooterDisplayItem,
              ]}
            />
          </NextAppDirEmotionCacheProvider>
        </DsfrProvider>
      </body>
    </html >
  );
}

addDisplayTranslations({
  "lang": "fr",
  "messages": {
    "dark theme": "Thème sombre 🤩",
  }
});