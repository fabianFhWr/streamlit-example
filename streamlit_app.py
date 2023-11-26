from datetime import datetime
from collections import Counter
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import re
import math
from itertools import groupby

def WNT():
    st.markdown('### 1.	WNT-Nutzung (Wochentag Nutzungs-Trend)')
    # Load data
    dateipfad_resource_logs = r"C:\Users\fabia\Documents\FH\Industrieprojekt\Daten\resource_logs.csv"
    df_resource_logs = pd.read_csv(dateipfad_resource_logs, encoding='latin-1')

    # Filter data and process datetime
    df_WNT = df_resource_logs[df_resource_logs['type'] != 'offline']['createdAt'].tolist()
    df_WNT = [timestamp.split('T')[0] for timestamp in df_WNT]
    df_WNT = [datetime.strptime(datum, '%Y-%m-%d') for datum in df_WNT]

    start_date = min(df_WNT)
    end_date = max(df_WNT)

    # Calculate the difference in days
    difference_days = (end_date - start_date).days
    number_of_weeks = difference_days // 7

    # Create a list with the names of the weekdays
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Count occurrences of each weekday
    weekday_counter = Counter(date.weekday() for date in df_WNT)

    # Calculate occurrence percentage of each weekday
    weekday_percentages = []
    for idx, day in enumerate(weekdays):
        weekday_percentages.append(weekday_counter[idx] / number_of_weeks)

    # Create a DataFrame for Plotly
    data = {'Weekday': weekdays, 'Percentage': weekday_percentages}
    df_plotly = pd.DataFrame(data)

    # Create an interactive bar chart using Plotly Express
    fig = px.bar(df_plotly, x='Weekday', y='Percentage',
                 labels={'Percentage': 'Percentage', 'Weekday': 'Weekday'})

    # Customize hover information
    fig.update_traces(hovertemplate='Percentage: %{y}<extra></extra>')

    # Display the chart using Plotly in Streamlit
    st.plotly_chart(fig)

    # Checkbox to select individual weekdays
    selected_weekdays = st.multiselect('Select weekdays', weekdays)

    if selected_weekdays:
        selected_weekday_indices = [weekdays.index(day) for day in selected_weekdays]

        # Create bar charts for the selected weekdays
        for idx in selected_weekday_indices:
            selected_weekday_data = {'Weekday': [weekdays[idx]], 'Percentage': [weekday_percentages[idx]]}
            df_selected_weekday = pd.DataFrame(selected_weekday_data)

            fig_selected_weekday = px.bar(df_selected_weekday, x='Weekday', y='Percentage',
                                           labels={'Percentage': 'Percentage', 'Weekday': 'Weekday'},
                                           title=f'Percentage of {weekdays[idx]}')

            fig_selected_weekday.update_traces(hovertemplate='Percentage: %{y}<extra></extra>')

            st.plotly_chart(fig_selected_weekday)
            
def ZNT():
    st.markdown('### Kleine Überschrift')
def KWN():
    st.markdown('### KWN (Kalenderwochen-Nutzungsanalyse)')    
    
    # Dateipfad zur CSV-Datei für members
    dateipfad_members = r"C:\Users\fabia\Documents\FH\Industrieprojekt\Daten\members.csv"
    df_members = pd.read_csv(dateipfad_members, encoding='latin-1')
    
    # Dateipfad zur CSV-Datei für packages
    dateipfad_packages = r"C:\Users\fabia\Documents\FH\Industrieprojekt\Daten\packages.csv"
    df_packages = pd.read_csv(dateipfad_packages, encoding='latin-1')
    
    # Dateipfad zur CSV-Datei für resource_logs
    dateipfad_resource_logs = r"C:\Users\fabia\Documents\FH\Industrieprojekt\Daten\resource_logs.csv"
    df_resource_logs = pd.read_csv(dateipfad_resource_logs, encoding='latin-1')
    
    
    
    # Überprüfen, ob 'member' nicht gleich 'offline' ist und 'NaN'-Werte in 'member' entfernen
    filtered_df = df_resource_logs[(df_resource_logs['type'] != 'offline') & (~df_resource_logs['member'].isnull())]
    
    # 'member'-Spalte ohne NaN-Werte in eine Liste umwandeln
    df_member = filtered_df['member'].tolist()
    
    df_start_time = filtered_df['createdAt'].tolist()
    df_start_time = [timestamp.split('T')[0] for timestamp in df_start_time]
    # Anzeigen der ersten paar Zeilen des gefilterten DataFrames df_WNT
    df_start_time = [datetime.strptime(datum, '%Y-%m-%d') for datum in df_start_time]
    
    # Liste, um die 'packages'-Spalte für jedes Mitglied zu speichern
    member_packages = []
    
    for member_id in df_member:
        # Filtern der Zeilen in df_members für jedes Mitglied
        temp_data = df_members[df_members['id'] == member_id]
        
        # Überprüfen, ob Daten für das Mitglied vorhanden sind
        if not temp_data.empty:
            # Wert der 'packages'-Spalte für das Mitglied hinzufügen
            member_packages.append(temp_data['package'].values[0])
        else:
            # Wenn keine Daten für das Mitglied vorhanden sind, füge np.nan zur Liste hinzu
            member_packages.append(np.nan)
    
    df_package_id = []
    
    
    for item in member_packages:
        if isinstance(item, str):
            # Trennen des Strings anhand des Kommas, Entfernen der Klammern und Leerzeichen, und Aufteilen der Teile
            parts = item.split(',')[0].replace('(', '').strip("' ").split("'")
            
            # Filtern der numerischen Teile und Hinzufügen zur Liste
            for part in parts:
                if part.isdigit():
                    df_package_id.append(int(part))
                elif part.lower() == 'nan':
                    df_package_id.append(np.nan)
                else:
                    df_package_id.append(np.nan)
    
        else:
            df_package_id.append(np.nan)
            
    df_package_info1 = []
    df_package_info2 = []
    for package_id in df_package_id:
        # Filtern der Zeilen in df_members für jedes Mitglied
        temp_data = df_packages[df_packages['id'] == package_id]
        
        # Überprüfen, ob Daten für das Mitglied vorhanden sind
        if not temp_data.empty:
            # Wert der 'packages'-Spalte für das Mitglied hinzufügen
            df_package_info1.append(temp_data['name'].values[0])
            df_package_info2.append(temp_data['type_of_user'].values[0])
    
        else:
            # Wenn keine Daten für das Mitglied vorhanden sind, füge np.nan zur Liste hinzu
            df_package_info1.append(np.nan)
            df_package_info2.append(np.nan)
    
    
    # Wandele die Werte in Ganzzahlen um und speichere sie zurück in der Liste
    df_Infomartion = [[start_time, package_info1, package_info2] for start_time, package_info1, package_info2 in zip(df_start_time, df_package_info1, df_package_info2)]

    df_Infomartion = [
        eintrag for eintrag in df_Infomartion
        if all(value is not None and not pd.isna(value) and value != 'nan' for value in eintrag)
    ]

    # Konvertierung des bearbeiteten Arrays in einen DataFrame
    df_Infomartion = pd.DataFrame(df_Infomartion, columns=['Datum', 'Package_Info1', 'Package_Info2'])

    # Filtern der Daten für die 'FHWN Abteilungen' innerhalb des angegebenen Zeitraums
    start_date = st.date_input("Startdatum", datetime(2023, 3, 21))
    end_date = st.date_input("Enddatum", datetime(2023, 9, 21))

    # Widget zur Auswahl der Kategorien (Mehrfachauswahl)
    categories = df_Infomartion['Package_Info1'].unique()
    selected_categories = st.multiselect('Kategorien auswählen', categories)

    # Filtern der Daten basierend auf den ausgewählten Werten
    filtered_data = df_Infomartion[(df_Infomartion['Package_Info1'].isin(selected_categories)) & 
                                   (df_Infomartion['Datum'] >= pd.to_datetime(start_date)) & 
                                   (df_Infomartion['Datum'] <= pd.to_datetime(end_date))]

    # Gruppieren der Daten nach Datum und Kategorie und Zählen der Vorkommnisse pro Tag und Kategorie
    daily_counts = filtered_data.groupby(['Datum', 'Package_Info1']).size().reset_index(name='Anzahl')

    # Erstellung des interaktiven Plots mit Plotly Express
    fig = px.line(daily_counts, x='Datum', y='Anzahl', color='Package_Info1', title='Anzahl der FHWN Abteilungen pro Tag', markers=True)
    fig.update_xaxes(title='Datum')
    fig.update_yaxes(title='Anzahl')
    fig.update_layout(showlegend=True)

    # Anzeigen des Plots in Streamlit
    st.plotly_chart(fig)
    


def Anzahl_Besucher():
    st.markdown('### Anzahl Besucher ')    

    # Dateipfad zur CSV-Datei für resource_logs
    dateipfad_resource_logs = r"C:\Users\fabia\Documents\FH\Industrieprojekt\Daten\resource_logs.csv"
    df_resource_logs = pd.read_csv(dateipfad_resource_logs, encoding='latin-1')

    # Überprüfen, ob 'member' nicht gleich 'offline' ist und 'NaN'-Werte in 'member' entfernen
    filtered_df = df_resource_logs[(df_resource_logs['type'] != 'offline') & (~df_resource_logs['member'].isnull())]

    # 'member'-Spalte ohne NaN-Werte in eine Liste umwandeln
    df_start_time = filtered_df['createdAt'].tolist()
    df_end_time = filtered_df['stoppedAt'].tolist()

    # Liste zur Speicherung der umgewandelten Zeitstempel
    converted_timestamps = []

    # Umwandlung der Zeichenfolgen in datetime-Objekte
    for timestamp in df_start_time:
        # Entfernen des 'Z' am Ende, da es die Z-Zeitzonenkennung ist
        timestamp = timestamp.replace('Z', '')
        # Parsen der Zeichenfolge in ein datetime-Objekt
        dt = datetime.fromisoformat(timestamp)
        converted_timestamps.append(dt)

    df_start_time = converted_timestamps

    converted_timestamps = []

    # Umwandlung der Zeichenfolgen in datetime-Objekte
    for timestamp in df_end_time:
        # Entfernen des 'Z' am Ende, da es die Z-Zeitzonenkennung ist
        timestamp = timestamp.replace('Z', '')
        # Parsen der Zeichenfolge in ein datetime-Objekt
        dt = datetime.fromisoformat(timestamp)
        converted_timestamps.append(dt)

    df_end_time = converted_timestamps

    df_time = [[ start_time, end_time] for start_time, end_time in zip( df_start_time,df_end_time)]

    # Eingabe des Datums im Streamlit-Dashboard
    chosen_date = st.date_input("Datum auswählen:", datetime(2023, 9, 19))

    filtered_data = [(start, end) for start, end in df_time if start.date() == chosen_date]

    # Erstellen einer Liste der Besuchszeiten für die Darstellung
    visit_times = [visit.time() for start, end in filtered_data for visit in (start, end)]

    # Konvertieren der Besuchszeiten in Minuten seit Mitternacht
    visit_times_minutes = [(visit.hour * 60) + visit.minute + (visit.second / 60) for visit in visit_times]

    # Erstellen des Graphen
    # Erstellen eines DataFrame für die Besuchszeiten in Minuten seit Mitternacht
    visit_df = pd.DataFrame({'Visit_Times_Minutes': visit_times_minutes})

    # Erstellen des Histogramms mit Plotly Express
    fig = px.histogram(visit_df, x='Visit_Times_Minutes', nbins=20,
                       labels={'Visit_Times_Minutes': 'Uhrzeit', 'count': 'Anzahl der Besuche'},
                       title=f'Besucher am {chosen_date.strftime("%Y-%m-%d")}')

    # Anzeigen des interaktiven Diagramms in Streamlit
    st.plotly_chart(fig)

def GültigkeitDerPakete():
    st.markdown('### Anzahl Besucher ')    
    # Dateipfad zur CSV-Datei für members
    dateipfad_members = r"C:\Users\fabia\Documents\FH\Industrieprojekt\Daten\members.csv"
    df_members = pd.read_csv(dateipfad_members, encoding='latin-1')
    
    df_packages = df_members['package'].tolist()
    
    # Extrahiere die Booleschen Werte aus den Strings mithilfe von regulären Ausdrücken
    boolean_values = [True if re.search(r'True', item) else False for item in df_packages]
    
    # Zähle die Anzahl von True und False
    count_true = boolean_values.count(True)
    count_false = boolean_values.count(False)
    sumPakete = count_false + count_true
    
    # Kreisdiagramm zur Verteilung der aktiven und inaktiven Pakete
    data = {'Status': ['Aktive Pakete', 'Inaktive Pakete'], 'Anzahl': [count_true, count_false]}
    df_status = pd.DataFrame(data)

    fig = px.pie(df_status, values='Anzahl', names='Status')
    st.plotly_chart(fig)
    
    show_info = st.button("Klicke hier für Details")
    if show_info:
        st.write(f'<b>Anzahl der Aktiven Pakete:</b>  {count_true}', unsafe_allow_html=True)
        st.write(f'<b>Prozentualen Anteil der Aktiven Pakete:</b> {round((count_true/sumPakete)*100,2)}%', unsafe_allow_html=True)
        st.write(f'<b>Anzahl der Inaktive/ausgelaufene Pakete:</b> {count_false}', unsafe_allow_html=True)
        st.write(f'<b>Prozentualen Anteil der Inaktive/ausgelaufene Pakete:</b> {round((count_false/sumPakete)*100,2)}%', unsafe_allow_html=True)
    else:
        st.write("")
    

def NutzerpaketeHäufigkeit():
    st.markdown('### Nutzerpakete – Häufigkeit ')    

    # Dateipfad zur CSV-Datei für members
    dateipfad_members = r"C:\Users\fabia\Documents\FH\Industrieprojekt\Daten\members.csv"
    df_members = pd.read_csv(dateipfad_members, encoding='latin-1')
    
    # Dateipfad zur CSV-Datei für packages
    dateipfad_packages = r"C:\Users\fabia\Documents\FH\Industrieprojekt\Daten\packages.csv"
    df_packages = pd.read_csv(dateipfad_packages, encoding='latin-1')
    
    
    df_package = df_members['package'].tolist()
    
    df_package_id = []
    
    
    for item in df_package:
        if isinstance(item, str):
            # Trennen des Strings anhand des Kommas, Entfernen der Klammern und Leerzeichen, und Aufteilen der Teile
            parts = item.split(',')[0].replace('(', '').strip("' ").split("'")
            
            # Filtern der numerischen Teile und Hinzufügen zur Liste
            for part in parts:
                if part.isdigit():
                    df_package_id.append(int(part))
                elif part.lower() == 'nan':
                    df_package_id.append(np.nan)
                else:
                    df_package_id.append(np.nan)
    
        else:
            df_package_id.append(np.nan)
            
    df_package_id = [value for value in df_package_id if not isinstance(value, float) or not math.isnan(value)]
    
    df_package_name = []
    
    
    for package_id in df_package_id:
        
        # Filtern der Zeilen in df_packages für jedes Paket anhand der ID
        temp_data = df_packages[df_packages['id'] == package_id]
        
        # Überprüfen, ob Daten für das Paket vorhanden sind
        if not temp_data.empty:
            # Wert der 'name'-Spalte für das Paket hinzufügen
            df_package_name.append(temp_data['name'].values[0])
    
    count_package= len(df_package_name);
    
    # Sortiere die Einträge nach ihrer Häufigkeit absteigend
    sorted_entries = sorted(df_package_name, key=lambda x: -df_package_name.count(x))
    
    # Gruppiere die Einträge
    grouped_entries = [list(group) for key, group in groupby(sorted_entries)]
    
    # Erstelle ein DataFrame, das die Anzahl der Vorkommen jedes Pakets enthält
    package_counts = pd.DataFrame({'Package': sorted_entries})
    package_counts['Count'] = package_counts.groupby('Package')['Package'].transform('count')
    package_counts = package_counts.drop_duplicates()
    
       # Erstelle ein Kreisdiagramm mit Plotly Express
    fig = px.pie(package_counts, values='Count', names='Package')
       
       # Anzeige des Kreisdiagramms in Streamlit
    st.plotly_chart(fig)
    show_info = st.button("Klicke hier für Details")
    if show_info:
        for i in grouped_entries:
            st.write(f"<b style='font-size: 20px'>{i[0]}</b>", unsafe_allow_html=True)
            st.write(f'<b>Anzahl des Paketes {i[0]}</b>: {len(i)}', unsafe_allow_html=True)
            st.write(f'<b>Prozentualen Anteil des Paketes {i[0]}</b>: {round((len(i)/count_package)*100,2)}%', unsafe_allow_html=True)
            st.write("")
    
def NutzungDesInnoLabsNachAltersgruppen():
    st.markdown('### Nutzung des InnoLabs nach Altersgruppen ')
    # Dateipfad zur CSV-Datei für members
    dateipfad_members = r"C:\Users\fabia\Documents\FH\Industrieprojekt\Daten\members.csv"
    df_members = pd.read_csv(dateipfad_members, encoding='latin-1')
    
    df_birth = df_members['dateOfBirth'].tolist()
    
    df_birth = [value for value in df_birth if not isinstance(value, float) or not math.isnan(value)]
    
    
    count_all =len(df_birth)
    # Aktuelles Datum
    heute = datetime.now()
    df_age =[]
    df_birth = sorted(df_birth, key=lambda x: (heute - datetime.strptime(x, "%Y-%m-%d")).days)
    # Berechnung des Alters für jede Person in der Liste
    for geburtsjahr in df_birth:
        geburtsdatum = datetime.strptime(geburtsjahr, "%Y-%m-%d")
        
        alter = heute.year - geburtsdatum.year - ((heute.month, heute.day) < (geburtsdatum.month, geburtsdatum.day))
        df_age.append(alter)
    
    
    df_birth = sorted(df_birth, key=lambda x: (heute - datetime.strptime(x, "%Y-%m-%d")).days)
    
    count_only_age = len(df_birth)


    # Definition der Altersgruppen
    age_groups = {
        '0-18': range(0, 19),
        '19-25': range(19, 26),
        '26-35': range(26, 36),
        '36-50': range(36, 51),
        '50-60': range(51, 60),
        '60+': range(61, 150),# Das obere Ende könnte je nach Anforderung angepasst werden
    }
    
    # Zähler für jede Altersgruppe initialisieren
    age_group_counts = {group: 0 for group in age_groups}
    
    # Durchlaufen der Altersdaten und Zuordnen zu den Altersgruppen
    for geburtsjahr in df_birth:
        geburtsdatum = datetime.strptime(geburtsjahr, "%Y-%m-%d")
        alter = heute.year - geburtsdatum.year - ((heute.month, heute.day) < (geburtsdatum.month, geburtsdatum.day))
        
        for group, age_range in age_groups.items():
            if alter in age_range:
                age_group_counts[group] += 1
                break  # Sobald das Alter in einer Gruppe gefunden wurde, den Loop beenden
    # Erstellen eines DataFrame für die Altersgruppen und deren Zählungen
    data = {'Altersgruppe': list(age_group_counts.keys()), 'Anzahl': list(age_group_counts.values())}
    df_age_groups = pd.DataFrame(data)
    
    # Plot des Kreisdiagramms (Pie Chart)
    fig = px.pie(df_age_groups, values='Anzahl', names='Altersgruppe')
    
    # Anzeige des Kreisdiagramms in Streamlit
    st.plotly_chart(fig)
    
    show_info = st.button("Klicke hier für Details")
    if show_info:
    # Ausgabe der Anzahl von Personen in jeder Altersgruppe
        for group, count in age_group_counts.items():
            st.write(f'<b>Anzahl von der Altersgruppe {group}:</b> {count} ', unsafe_allow_html=True)
            st.write(f'<b>Prozentualen Anteil der Altersgruppe {group}:</b> {round((count/count_only_age)*100,2)} ', unsafe_allow_html=True)

    
def main():
    st.title('InnoLAB')
    KPI = ["WNT", "ZNT", "KWN", "Anzahl Besucher", "Gültigkeit der Pakete", "Nutzerpakete – Häufigkeit", "Nutzung des InnoLabs nach Altersgruppen"]
    selected_KPIs = st.multiselect('Select KPIs', KPI)

    if "WNT" in selected_KPIs:
        WNT()  # Execute WNT function and display its output

    if "ZNT" in selected_KPIs:
        ZNT()  # Execute ZNT function and display its output

    if "KWN" in selected_KPIs:
        KWN()  # Execute KWN function and display its output
        
    if "Anzahl Besucher" in selected_KPIs:
        Anzahl_Besucher() 
    
    if "Gültigkeit der Pakete" in selected_KPIs:
        GültigkeitDerPakete()
        
    if "Nutzerpakete – Häufigkeit" in selected_KPIs:
        NutzerpaketeHäufigkeit() 

    if "Nutzung des InnoLabs nach Altersgruppen" in selected_KPIs:
        NutzungDesInnoLabsNachAltersgruppen() 
if __name__ == '__main__':
    main()
