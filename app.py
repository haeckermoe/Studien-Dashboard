from dash import Dash, html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
from dashboard_controller import DashboardController
from repository import StudiumRepository
from studium_service import StudiumService, berechne_monate
from charts import erstelle_ects_chart, erstelle_semester_chart, erstelle_tachometer

repo = StudiumRepository("studium.json")
service = StudiumService()
controller = DashboardController(service, repo)

app = Dash(__name__)
 
_leer = go.Figure()
_leer.update_layout(
    xaxis={"visible": False},
    yaxis={"visible": False},
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

app.layout = html.Div([
    html.H1("Studien Dashboard"),
    html.Div([
        dcc.Graph(id="ects_chart", figure = _leer, style={"flex": "1"}),
        dcc.Graph(id="tachometer", figure = _leer, style={"flex": "1"})
    ], style={"display": "flex"}),
    html.Div([
        dcc.Graph(id=f"semester_chart_{i}", figure = _leer, style={"flex": "1"}) 
        for i in range(1, 7)
    ], style={"display": "flex"}),
    html.Div([
        dcc.Input(id="modul-name", placeholder = "Name des Moduls"),
        dcc.Input(id="modul-ects", placeholder = "ECTS des Moduls", type = "number"),
        dcc.Input(id="modul-note", placeholder = "Erreichte Note", type = "number"),
        dcc.Input(id="semester-nummer", placeholder="Semester"),
        dcc.Checklist(id="angerechnet", options=[{"label": "Angerechnet", "value": "ja"}],value=[]),
        html.Button("Hinzufügen", id="button"),
        html.Div(id="ausgabe"),
        html.Button("Alle Daten zurücksetzen", id="reset"),
        html.Div(id="reset-ausgabe"),
        dcc.ConfirmDialog(id="confirm-reset", message="Möchtest du wirklich alle Module löschen?")
    ])
])
             
@callback(                  
    Output("ects_chart", "figure"),
    Output("tachometer", "figure"),  
    Output("ausgabe", "children"),
    Output("semester_chart_1", "figure"),
    Output("semester_chart_2", "figure"),
    Output("semester_chart_3", "figure"),
    Output("semester_chart_4", "figure"),
    Output("semester_chart_5", "figure"),
    Output("semester_chart_6", "figure"),
    Input("button", "n_clicks"),
    State("modul-name", "value"),
    State("modul-ects", "value"),
    State("modul-note", "value"),
    State("semester-nummer", "value"),
    State("angerechnet", "value"),
    prevent_initial_call= False
)

def aktualisieren(n_clicks, name, ects, note, semester_nummer, angerechnet):
    """Aktualisiert die Charts nach jeder Eingabe"""
    daten = controller.lade_daten()
    studium = daten["studium"]
    
    if n_clicks:
        if angerechnet:
            controller.modul_hinzufuegen(int(semester_nummer), name, int(ects), note=None)
        else:
            controller.modul_hinzufuegen(int(semester_nummer), name, int(ects), float(note))
        daten = controller.lade_daten()
        studium = daten["studium"]

    monate = berechne_monate()
    ects_fig = erstelle_ects_chart(studium.erreichte_ects(), studium.ziel_ects)
    tacho_fig = erstelle_tachometer(studium.erreichte_ects(),monate, studium.ziel_ects)
    semester_figs = []
    for i in range(1, 7):
        semester = next((s for s in studium.semester if s.nummer == i), None)
        if semester:
            fig = erstelle_semester_chart(semester, 30)
        else:
            fig = _leer
        semester_figs.append(fig)
    text = f"ECTS: {daten['gesamt_ects']} | Gesamtschnitt: {daten['durchschnitt']:.1f}"
    return ects_fig, tacho_fig, text, *semester_figs
    
    
@callback(
    Output("confirm-reset", "displayed"),
    Input("reset", "n_clicks"),
    prevent_initial_call = True
)
def zeige_dialog(n_clicks):
    """Reset Dialog"""
    return True


@callback(
    Output("reset-ausgabe", "children"),
    Input("confirm-reset", "submit_n_clicks"),
    prevent_initial_call = True
)
def reset_bestaetigen(n_clicks):
    """Löscht alle Daten nach Bestätigung des Dialogs"""
    repo.reset()
    return "Alle Module gelöscht!"


if __name__ == "__main__":
    app.run(debug=True, port= 8050)