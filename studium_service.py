from __future__ import annotations
from studium import Studium
from semester import Semester
from modul import Modul
from datetime import datetime
class StudiumService:

    def berechne_durchschnitt(self, studium: Studium) -> float:
        """Berechnet den Durchschnitt aller Noten, wird im Dashboard als String ausgegeben"""
        noten = [
            m.pruefungsleistung.note
            for s in studium.semester
            for m in s.module
            if m.pruefungsleistung is not None
        ]
        return round(sum(noten) / len(noten), 1) if noten else 0.0
    
    
    def berechne_semester_durchschnitt(self, semester: Semester) -> float:
        """Berechnet den Durchschnitt der einzelnen Semester, wird innerhalb der Semester Donutcharts ausgegeben"""
        noten = [
            m.pruefungsleistung.note
            for m in semester.module
            if m.pruefungsleistung is not None
        ]
        return round(sum(noten) / len(noten), 1) if noten else 0.0
   
    
    def berechne_gesamt_ects(self, module: list[Modul]) -> int:
        """Berechnet Gesamt ECTS, wird innerhalb des Gesamt ECTS Charts ausgegeben"""
        return sum(m.ects for m in module)
    

def berechne_monate() -> float:
    """Berechnet die Monate seit Beginn des Studiums. Datum hardcoded aufgrund Reset json Funktion"""
    start = datetime(2026, 4, 14)
    jetzt = datetime.now()
    tage = (jetzt - start).days 
    return tage / 30.44   



        