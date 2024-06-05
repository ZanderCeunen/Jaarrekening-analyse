import re
import PyPDF2


def haal_waarde_na_identificatie_code(pdf_path, target_code):
    try:
        # Open het PDF-bestand
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)

            # Doorloop alle pagina's in het PDF-bestand
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()

                # Zoek naar de specifieke code
                match = re.search(f"{target_code}(.+)", text)
                if match:
                    resultaat = match.group(1).strip()
                    resultaten = resultaat.split()
                    if len(resultaten) >= 2:
                        resultaat_huidig_boekjaar = re.search(r'-?[\d\.,]+', resultaten[0]).group()
                        resultaat_vorig_boekjaar = re.search(r'-?[\d\.,]+', resultaten[1]).group()
                        return resultaat_huidig_boekjaar.replace('.', '').replace(',', '.'), resultaat_vorig_boekjaar.replace('.', '').replace(',', '.')
                    else:
                        return f"Niet genoeg data gevonden na '{target_code}' in het PDF-bestand."
        # Als de code niet wordt gevonden, geef een foutmelding
        return f"De tekstcode '{target_code}' werd niet gevonden in het PDF-bestand."

    except Exception as e:
        return f"Fout bij het verwerken van het PDF-bestand: {str(e)}"


def berekenen_liquiditeit(pdf_path):
    vlottende_activa = (haal_waarde_na_identificatie_code(pdf_path, "29/58"))
    vreemd_vermogen_korte_termijn = (haal_waarde_na_identificatie_code(pdf_path, "42/48"))
    vreemd_vermogen_korte_termijn_huidig_boekjaar = vreemd_vermogen_korte_termijn[0]
    vreemd_vermogen_korte_termijn_vorig_boekjaar = vreemd_vermogen_korte_termijn[1]
    vlottende_activa_huidige_boekjaar = vlottende_activa[0]
    vlottende_activa_vorige_boekjaar = vlottende_activa[1]
    liquiditeit_huidige_boekjaar = int(vlottende_activa_huidige_boekjaar) / int(vreemd_vermogen_korte_termijn_huidig_boekjaar)
    liquiditeit_vorige_boekjaar = int(vlottende_activa_vorige_boekjaar) / int(vreemd_vermogen_korte_termijn_vorig_boekjaar)
    return liquiditeit_huidige_boekjaar, liquiditeit_vorige_boekjaar


def solvabiliteit(pdf_path):
    totaal_vermogen = (haal_waarde_na_identificatie_code(pdf_path, "10/49"))
    eigen_vermogen_korte_termijn = (haal_waarde_na_identificatie_code(pdf_path, "10/15"))
    eigen_vermogen_korte_termijn_huidig_boekjaar = eigen_vermogen_korte_termijn[0]
    eigen_vermogen_korte_termijn_vorig_boekjaar = eigen_vermogen_korte_termijn[1]
    totaal_vermogen_huidige_boekjaar = totaal_vermogen[0]
    totaal_vermogen_vorige_boekjaar = totaal_vermogen[1]
    solvabiliteit_huidige_boekjaar = int(eigen_vermogen_korte_termijn_huidig_boekjaar) / int(totaal_vermogen_huidige_boekjaar) *100
    solvabiliteit_vorige_boekjaar = int(eigen_vermogen_korte_termijn_vorig_boekjaar) / int(totaal_vermogen_vorige_boekjaar) *100
    return solvabiliteit_huidige_boekjaar, solvabiliteit_vorige_boekjaar


def rendabiliteit(pdf_path):
    resultaat_boekjaar_na_belasting = (haal_waarde_na_identificatie_code(pdf_path, "9904"))
    eigen_vermogen = (haal_waarde_na_identificatie_code(pdf_path, "10/15"))
    eigen_vermogen_huidige_boekjaar = eigen_vermogen[0]
    eigen_vermogen_vorige_boekjaar = eigen_vermogen[1]
    rendabiliteit_huidige_boekjaar = int(resultaat_boekjaar_na_belasting[0]) / int(eigen_vermogen_huidige_boekjaar) * 100
    rendabiliteit_vorige_boekjaar = int(resultaat_boekjaar_na_belasting[1]) / int(eigen_vermogen_vorige_boekjaar) * 100
    return rendabiliteit_huidige_boekjaar, rendabiliteit_vorige_boekjaar


pdf_path = input("Naam van pdf bestand: ")
print(f"De liquiditeit van het huidige boekjaar is: {round(berekenen_liquiditeit(pdf_path)[0],3)}")
print(f"De liquiditeit van het vorige boekjaar is: {round(berekenen_liquiditeit(pdf_path)[1],3)}")
print(f"De solvabiliteit van het huidige boekjaar is: {round(solvabiliteit(pdf_path)[0],3)}%")
print(f"De solvabiliteit van het vorige boekjaar is: {round(solvabiliteit(pdf_path)[1],3)}%")
print(f"De rendabilitheid van het huidige boekjaar is: {round(rendabiliteit(pdf_path)[0],3)}%")
print(f"De rendabiliteit van het vorige boekjaar is: {round(rendabiliteit(pdf_path)[1],3)}%")

