from __future__ import annotations
from repository import StudiumRepository
from studium_service import StudiumService
from studium import Studium
from semester import Semester
from modul import Modul
from pruefungsleistung import Pruefungsleistung

class DashboardController:
    def __init__(self, studium_service: StudiumService, studium_repository: StudiumRepository):
        self.studium_service = studium_service
        self.studium_repository = studium_repository
        
    def lade_daten(self) -> dict:
        """Lädt Daten aus dem Repository"""
        studium = self.studium_repository.lade_studium()
        return {
            "studium": studium,
            "gesamt_ects": studium.erreichte_ects(),
            "durchschnitt": self.studium_service.berechne_durchschnitt(studium)
        }

    def modul_hinzufuegen(self, semester_nummer: int, name: str, ects: int, note=None) -> None:
        """Fügt ein neues Modul hinzu, ordnet es einem Semester zu und fügt name, ects und eine Prüfungsleistung hinzu"""
        studium = self.studium_repository.lade_studium()
        semester = next(
            (s for s in studium.semester if s.nummer == semester_nummer),
            None
        )

        if semester is None:
            semester = Semester(nummer=semester_nummer, ziel_ects=30)
            studium.semester_hinzufuegen(semester)
        modul = Modul(name = name, ects = ects)
        if note is not None:
            modul.pruefung_hinzufuegen(Pruefungsleistung(note))
        semester.modul_hinzufuegen(modul)
        self.studium_repository.speichere_studium(studium)

    def semester_hinzufuegen(self, nummer: int, ziel_ects: int) -> None:
        """Fügt der Studium Klasse ein Semester hinzu"""
        studium = self.studium_repository.lade_studium()
        semester = Semester(nummer = nummer, ziel_ects = ziel_ects)
        studium.semester_hinzufuegen(semester)
        self.studium_repository.speichere_studium(studium)

        
        
        