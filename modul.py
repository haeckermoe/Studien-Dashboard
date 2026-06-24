from __future__ import annotations
from dataclasses import dataclass
from pruefungsleistung import Pruefungsleistung

@dataclass
class Modul:
    """Repräsentiert ein Modul, enthält eine Prüfungsleistung"""
    name: str
    ects: int
    pruefungsleistung: "Pruefungsleistung" | None = None

    def pruefung_hinzufuegen(self, pruefungsleistung):
        """Fügt eine Prüfungsleistung hinzu"""
        self.pruefungsleistung = pruefungsleistung
