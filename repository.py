from __future__ import annotations
import json
from pathlib import Path
from studium import Studium
from semester import Semester
from modul import Modul
from pruefungsleistung import Pruefungsleistung

class StudiumRepository:
    def __init__(self, dateipfad: str):
        self.dateipfad = Path(dateipfad)
        
    def lade_studium(self) -> Studium:
        """Lädt die Klasse Studium aus der JSON Datei"""
        with self.dateipfad.open("r", encoding="utf-8") as f:
            daten = json.load(f)
        studium = Studium(
            start_datum=daten["start_datum"],
            ziel_monate=daten["ziel_monate"],
            ziel_ects=daten["ziel_ects"]
        )
        for s in daten["semester"]:
            semester = Semester(nummer=s["nummer"], ziel_ects=s["ziel_ects"])
            for m in s["module"]:
                modul = Modul(name=m["name"], ects=m["ects"])
                if m["pruefungsleistung"]:
                    modul.pruefung_hinzufuegen(
                        Pruefungsleistung(note=m["pruefungsleistung"]["note"]) if m["pruefungsleistung"] else None
                            )
                semester.modul_hinzufuegen(modul)
            studium.semester_hinzufuegen(semester)
        return studium

    def speichere_studium(self, studium: Studium) -> None:
        """Speichert die Klasse Studium in der JSON Datei"""
        daten = {
            "start_datum": studium.start_datum,
            "ziel_monate": studium.ziel_monate,
            "ziel_ects": studium.ziel_ects,
            "semester": [
                {
                    "nummer": s.nummer,
                    "ziel_ects": s.ziel_ects,
                    "module":[
                        {
                            "name": m.name,
                            "ects": m.ects,
                            "pruefungsleistung": {"note": m.pruefungsleistung.note}
                            if m.pruefungsleistung else None
                        }
                        for m in s.module
                    ]
                }
                for s in studium.semester
             ]
           }
        with self.dateipfad.open("w", encoding="utf-8") as f:
            json.dump(daten, f, ensure_ascii=False, indent=4)
            
    def reset(self) -> None:
        """Setzt alle Daten in der JSON Datei zurück. Aufruf über Dashboard reset Button"""
        daten = {
            "start_datum": "",
            "ziel_monate": 0,
            "ziel_ects": 180,
            "semester": []
        }
        with self.dateipfad.open("w", encoding="utf-8") as f:
          json.dump(daten, f, ensure_ascii=False, indent=4)         

            