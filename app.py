#st.write ersetzt das print
#-->print schreibt ins Terminal - also für sich selber
#-->st.write schreibt in das gewünschte UI

#Start: 
# python -m venv .venv
# .venv\Scripts\activate
# streamlit run app.py


#Block 0 – Imports
import streamlit as st
import random #Zufallszahlen
from datetime import datetime #Datum und Uhrzeit


#Block 1 – Session State
#Streamlit startet Script ständig neu (Rerun bei jeder Änderung)
if "request_text" not in st.session_state:
    st.session_state.request_text = ""
if "requests" not in st.session_state:
    st.session_state.requests = [] #Liste mit den erstellten Requests
if "request_ok" not in st.session_state:
    st.session_state.request_ok = False #Bei True = Erfolgsmeldung anzeigen, bei False = keine Erfolgsmeldung


#Block 2 – Page Setup & Header
st.set_page_config(page_title="Wolkis Projekt", layout="wide")
#Browser-Tab und nutzt die gesagte Seitenbreite

st.sidebar.title("Wolkis IDM Lernprojekt") #Überschrift der Sidebar
st.sidebar.link_button("Projekt auf GitHub ansehen", "https://github.com/wolkenfrei/IDM-Projekt\n") #Verweis auf GitHub für weitere Informationen
st.sidebar.title("Navigation")



#Block 3 – Navigation
auswahl = st.sidebar.selectbox(  # Navigation - steuert den Seiteninhalt
    "Bitte auswählen",
    ["Antrag erstellen", "Antrag anzeigen"]
)

# Anzeige abhängig von der Auswahl
if auswahl == "Antrag erstellen":
    st.write("Bitte User-ID eingeben und Request-Typ auswählen.")

    #Block 4 – Inputs / Variablen (UI - Werte)
    user_id = st.text_input("User-ID")  # Pflichtfeld der ID
    request_type = st.selectbox(
        "Request-Typ",
        ["Einzelberechtigung", "Neuer User (Onboarding)"]
    )  # Logikpfad der Anwendung

    # Defaults verhindern NameError bei späteren Abfragen
    system = None  # Startwert sonst crash (NameError)
    request_text = ""  # sammelt Ausgabe für den Request Text

    # Checkbox-Defaults (existieren immer, auch wenn UI-Zweig nicht aktiv ist)
    ad = mail = servicenow = sap = False  # boolean
    system_1 = system_2 = system_3 = system_4 = False  # boolean

    #Block 5 – Conditional UI (abhängig vom Request-Typ)
    if request_type == "Einzelberechtigung":  # Logik und UI für Einzelberechtigungen
        st.write("Wähle nun das gewünschte System aus")
        system = st.selectbox(
            "System",
            ["Bitte wählen...", "SAP", "AD", "ServiceNow", "Email"]
        )  # Bitte wählen ist Standard/Platzhalter

        if system == "SAP":  # Zusatzoption aber nur wenn SAP ausgewählt worden ist
            st.write("System auswählen")
            system_1 = st.checkbox("System_1")
            system_2 = st.checkbox("System_2")
            system_3 = st.checkbox("System_3")
            system_4 = st.checkbox("System_4")

    else:
        st.write("Neuer User - wähle die gewünschten Berechtigungen aus")  # Einzeln anwählbar

        ad = st.checkbox("AD / Benutzerkonto")
        mail = st.checkbox("E-Mail / Exchange")
        servicenow = st.checkbox("ServiceNow")
        sap = st.checkbox("SAP")  # Rollen/Optionen nur anzeigen, wenn SAP angehakt ist

        if sap:
            st.write("System auswählen")
            system_1 = st.checkbox("System_1")
            system_2 = st.checkbox("System_2")
            system_3 = st.checkbox("System_3")
            system_4 = st.checkbox("System_4")

    #Block 6 – Request (Button + Text erstellen)
    button_geklickt = st.button("Request erstellen")  # Triggert die Request Generierung

    if button_geklickt:
        request_id = random.randint(1000, 9999)  # Erzeugt eine zufällige Request-ID
        timestamp = datetime.now().strftime("%d.%m.%y - %H:%M Uhr")  # aktuelles Datum und Uhrzeit
        request_text = f"Request-ID: {request_id}\nDatum: {timestamp}\n\nUser-ID: {user_id}\n"

        if user_id == "":
            st.warning("Bitte User-ID eingeben")  # Schutz gegen leeres Pflichtfeld - Gelbe Warnmeldung
            st.session_state.request_ok = False  # Erfolgsmeldung deaktivieren
            st.session_state.request_text = ""  # Optional den Text leeren
            st.stop()  # Stop, hier stoppt der Code

        if request_type == "Einzelberechtigung":  # separater Flow - genau ein System
            if system == "Bitte wählen...":
                st.error("Bitte System auswählen")  # Rote Meldung
                st.session_state.request_ok = False  # Kein Erfolg
                st.session_state.request_text = ""  # Optional den Text leeren
                st.stop()  # Stop, hier stoppt der Code

            request_text += "Typ: Einzelberechtigung\n"
            request_text += f"System: {system}\n"

            if system == "SAP":
                if not (system_1 or system_2 or system_3 or system_4):
                    st.error("Bitte mindestens ein SAP-System auswählen")  # Rote Meldung
                    st.session_state.request_ok = False  # Kein Erfolg
                    st.session_state.request_text = ""  # Optional den Text leeren
                    st.stop()  # Stop, hier stoppt der Code

                request_text += "SAP Systeme:\n"
                if system_1:
                    request_text += "- System_1\n"
                if system_2:
                    request_text += "- System_2\n"
                if system_3:
                    request_text += "- System_3\n"
                if system_4:
                    request_text += "- System_4\n"

        else:
            request_text += "Typ: Neuer User (Onboarding)\n"  # Onboarding - mehrere Systeme gleichzeitig
            request_text += "Benötigte Systeme:\n"

            if not (ad or mail or servicenow or sap):
                st.error("Bitte mindestens ein System auswählen")  # Rote Meldung
                st.session_state.request_ok = False  # Kein Erfolg
                st.session_state.request_text = ""  # Optional den Text leeren
                st.stop()  # Stop, hier stoppt der Code

            if ad:
                request_text += "- AD\n"
            if mail:
                request_text += "- E-Mail\n"
            if servicenow:
                request_text += "- ServiceNow\n"
            if sap:
                request_text += "- SAP\n"

            if sap:
                if not (system_1 or system_2 or system_3 or system_4):
                    st.error("Bitte mindestens ein SAP-System auswählen")  # Rote Meldung
                    st.session_state.request_ok = False  # Kein Erfolg
                    st.session_state.request_text = ""  # Optional den Text leeren
                    st.stop()  # Stop, hier stoppt der Code

                request_text += "SAP Rollen:\n"
                if system_1:
                    request_text += "- System_1\n"
                if system_2:
                    request_text += "- System_2\n"
                if system_3:
                    request_text += "- System_3\n"
                if system_4:
                    request_text += "- System_4\n"

        st.session_state.request_text = request_text  # Speichert den fertigen Request-Text
        st.session_state.request_ok = True  # Erfolgsmeldung aktivieren
        st.session_state.requests.append(request_text)  # Fügt den fertigen Text zur Liste hinzu

    #Block 7 – Output (Anzeige)
    if st.session_state.request_ok:  # Wird nur angezeigt, wenn letzter Klick erfolgreich war
        st.success("Request erfolgreich erstellt")  # Grüne Meldung im UI
        st.write("Erstellter Request")
        st.text(st.session_state.request_text)  # Hier wird der erstellte Request angezeigt


#Block 8 - Antrag unter "Antrag anzeigen"
else:
    st.write("Bisher erstellte Anträge")  # Bereich für die Request-Übersicht

    if not st.session_state.requests:
        st.info("Es wurden noch keine Anträge erstellt.")  # Liste ist leer - nur der Hinweis
    else:
        for nummer, request in enumerate(st.session_state.requests, start=1):
            st.write(f"Request: {nummer}") #Überschrift mit laufender Nummer
            st.text(request)  # Zeigt jeden Request an
            st.divider() #Trennt die einzelnen Anträge

