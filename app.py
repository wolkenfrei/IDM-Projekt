#st.write ersetzt das print
#-->print schreibt ins Terminal - also für sich selber
#-->st.write schreibt in das gewünschte UI

#Start: 
# python -m venv .venv
# .venv\Scripts\activate
# streamlit run app.py


import streamlit as st

if "request_text" not in st.session_state:
        st.session_state.request_text = ""
#import alles von streamlit und sage die kurzform soll st sein

st.set_page_config(page_title="Wolki", layout="wide")
#hier sage ich, dass ich die seite mit einem titel und eime layout configurieren möchte
#page_titel ist der Name des Tabs und das Layout ist die breite - ist standard

st.title("Wolki")#Titel auf der Hauptseite
st.write("IDM Lernprojekt")#Text unter dem Titel
st.sidebar.title("Navigation")#Alles landet Links

auswahl = st.sidebar.selectbox(#Variabel "auswahl"benannt die unter der Sidebar ein Drop down baut
    "Bitte auswählen",#Test über die Auswahl, die man treffen kann
    ["Antrag erstellen", "Antrag anzeigen"])#Auswahl möglichkeiten

if auswahl == "Antrag erstellen":
    st.write("Hier kommt noch ein Formular")#Wenn in der Auswahl "Antrag erstellen" angeklickt wird, kommt die Meldung "hier kommt noch ein Formular"
else:
    st.write("Hier kommt später eine Liste.")#Wenn was anderes als Antrag erstellen genommen wird, kommt die Meldung, dass später eine Liste angbezeigt wird

#VARIABELN
user_id = st.text_input("User-ID")#wir erzeugen nun ein Eingabefeld wo "User-ID" drin steht
request_type = st.selectbox("Request-Typ", ["Einzelberechtigung", "Neuer User (Onboarding)"])#Alle Berechtigungen oder einzelne?
system = None
request_text = ""
ad = mail = servicenow = sap = False
system_1 = system_2 = system_3 = system_4 = False

if request_type == "Einzelberechtigung":#Auswahlmöglichkeiten mit dem oberbegriff "System". Darunter dann die erstellte Liste mit neuen Werten
    st.write("Wähle nun das gewünschte System aus")
    system = st.selectbox("System", ["SAP", "AD", "ServiceNow", "Email"])

    if system == "SAP":#Wenn SAP ausgewählt wird, soll es die System anzeigen - Checkbox. Das gilt für die Einzelberechtigung
        st.write("System auswählen")
        system_1 = st.checkbox("System_1")
        system_2 = st.checkbox("System_2")
        system_3 = st.checkbox("System_3")
        system_4 = st.checkbox("System_4")
    
else:
    st.write("Neuer User - wähle die gewünschten Berechtigungen aus")#Das gilt für neue User (onboarding) - hier müssen die Berechtigungen einzeln angeklickt werden

    ad = st.checkbox("AD / Benutzerkonto")
    mail = st.checkbox("E-Mail / Exchange")
    servicenow = st.checkbox("ServiceNow")
    sap = st.checkbox("SAP")#sobald man SAP auswählt, muss man die gewünschten Systeme auswählen.
    if sap:
        st.write("System auswählen")
        system_1 = st.checkbox("System_1")
        system_2 = st.checkbox("System_2")
        system_3 = st.checkbox("System_3")
        system_4 = st.checkbox("System_4")

button_geklickt = st.button("Request erstellen")#unter dem Eingabefeld erscheint über die Methode ein Button

if button_geklickt:
    request_text = f"User-ID: {user_id}\n" #Nachdem der Button geklickt worden ist, wird die User-ID angezeigt
    
    if request_type == "Einzelberechtigung":
        request_text += "Typ: Einzelberechtigung\n"
        request_text += f"System: {system}\n"

        if system == "SAP":
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
        request_text += "Typ: Neuer User (Onboarding)\n"
        request_text += "Benötigte Systeme:\n"

        if ad:
            request_text += "- AD\n"
        if mail:
            request_text += "- E-Mail\n"
        if servicenow:
            request_text += "- ServiceNow\n"
        if sap:
            request_text += "- SAP\n"

        if sap:
             request_text += "SAP Rollen:\n"
             if system_1: 
                request_text += "- System_1\n"
             if system_2:
                request_text += "- System_2\n"
             if system_3:
                request_text += "- System_3\n"
             if system_4:
                request_text += "- System_4\n"

    st.session_state.request_text = request_text

st.text_area("Request Text", st.session_state.request_text, height=200)

    
