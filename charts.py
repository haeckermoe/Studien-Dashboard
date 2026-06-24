from __future__ import annotations
import plotly.graph_objects as go
from semester import Semester


def erstelle_ects_chart(erreichte_ects: int, ziel_ects: int) -> go.Figure:
    """Funktion um ECTS Chart nach dash.py zu holen. 
    Erstellt ein Donut Diagramm mit dem Gesamtfortschritt in ECTS in der Mitte. 
    Bei 180/180 ECTS erscheint eine Glückwunschnachricht."""
    rest_ects = ziel_ects - erreichte_ects
    prozent = (erreichte_ects / ziel_ects) * 100

    annotations = [
        dict(text=f"{prozent:.0f}%", font=dict(size=20),
             x=0.5, y=0.5, showarrow=False),
        dict(text="Gesamtfortschritt ECTS", font=dict(size=20),
             x=0.5, y=1.3, showarrow=False)
    ]
    if prozent == 100:
        annotations.append(dict(
            text="Glückwunsch, Studium erfolgreich abgeschlossen!",
            font=dict(size=16, color="darkgreen"),
            x=0.5, y=-0.2, showarrow=False))
    else:
        annotations.append(dict(
            text=f"{erreichte_ects} von {ziel_ects} ECTS erreicht!",
            font=dict(size=16), x=0.5, y=-0.2, showarrow=False))

    fig = go.Figure(data=go.Pie(
        values=(erreichte_ects, rest_ects),
        showlegend=False, hole=0.5, textinfo="none", sort=False,
        marker=dict(colors=("steelblue", "lightgrey"))
    ))
    fig.update_layout(annotations=annotations)
    return fig
    

def erstelle_semester_chart(semester: Semester, ziel_ects: int) -> go.Figure:
    """Funktion um Semester Charts nach dash.py zu holen.
    Erstellt ein Donutchart pro Semester. Der Notendurchschnitt ist in der Mitte.
    Die ist und ziel ECTS werden als String ausgegeben.
    Bei 30/30 ECTS erscheint eine Glückwunschnachricht."""
    erreichte_ects = semester.erreichte_ects()
    rest_ects = ziel_ects - erreichte_ects

    noten = [m.pruefungsleistung.note for m in semester.module
             if m.pruefungsleistung is not None]
    schnitt = f"{sum(noten) / len(noten):.1f}" if noten else "X.X"

    annotations = [
        dict(text=f"Ø{schnitt}", font=dict(size=20),
             x=0.5, y=0.5, showarrow=False),
        dict(text=f"Semester {semester.nummer}", font=dict(size=20),
             x=0.5, y=1.3, showarrow=False)
    ]
    if erreichte_ects >= ziel_ects:
        annotations.append(dict(
            text="Glückwunsch, Semester bestanden!",
            font=dict(color="green", size=16),
            x=0.5, y=-0.2, showarrow=False))
    else:
        annotations.append(dict(
            text=f"{erreichte_ects} von {ziel_ects} ECTS erreicht!",
            font=dict(size=16), x=0.5, y=-0.2, showarrow=False))

    fig = go.Figure(data=go.Pie(
        values=(erreichte_ects, rest_ects),
        showlegend=False, hole=0.5, textinfo="none", sort=False,
        marker=dict(colors=("steelblue", "lightgrey"))
    ))
    fig.update_layout(annotations=annotations)
    return fig
   

def erstelle_tachometer(erreichte_ects: int, monate_seit_start: int, ziel_ects: int) -> go.Figure:
    """Funktion um Gauge Chart nach dash.py zu holen.
    Rechnet die Geschwindigkeit des Studienfortschritts aus und zeigt sie in Tachoformat an.
    Es wird mit 48 Monaten gerechnet, was 3,75 ECTS Pro Monat entspricht.
    Die prozentuale Geschwindigkeit wird in der Mitte ausgegeben. Als String werden
    ECTS / Monat ausgegeben.
    """
    ects_pro_monat = erreichte_ects / monate_seit_start if monate_seit_start > 0 else 0
    prozent = (ects_pro_monat / 3.75) * 100
    verbleibende_ects = ziel_ects - erreichte_ects
    verbleibende_monate = round(verbleibende_ects / ects_pro_monat) if ects_pro_monat > 0 else 0

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prozent,
        title={"text": "Studiengeschwindigkeit"},
        number={"suffix": "%"},
        gauge={
            "axis": {"range": [0, 200]},
            "bar": {"color": "black", "thickness": 0.1},
            "steps": [
                {"range": [0, 70], "color": "darkred"},
                {"range": [70, 100], "color": "orange"},
                {"range": [100, 130], "color": "green"},
                {"range": [130, 200], "color": "gold"}
            ],
            "threshold": {"line": {"color": "black", "width": 4},
                          "thickness": 0.9, "value": prozent}
        }
    ))
    fig.update_layout(annotations=[dict(
        text=f"{ects_pro_monat:.2f} von 3,75 ECTS pro Monat",
        x=0.5, y=-0.1, showarrow=False, font=dict(size=14)),
        dict(text=f"In der aktuellen Geschwindigkeit wirst du dein Studium in {verbleibende_monate} Monaten abschließen!",
             x=0.5, y=-0.25, showarrow= False, font = dict(size=16))
             ])
    return fig
    