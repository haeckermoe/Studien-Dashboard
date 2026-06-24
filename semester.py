from __future__ import annotations
from dataclasses import dataclass, field
from modul import Modul

@dataclass
class Semester():
    """Repräsentiert die Semester mit allen Modulen und Semesterzielen"""
    nummer: int
    ziel_ects: int
    module: list[Modul] = field(default_factory = list)

    def modul_hinzufuegen(self, modul: Modul) -> None:
        """Fügt ein Modul hinzu"""
        if modul.pruefungsleistung is None or modul.pruefungsleistung.bestanden:
            self.module.append(modul)
                    

    def erreichte_ects(self) -> int:
        """Berechnet Semester ECTS aus den Modulen"""
        return sum(m.ects for m in self.module)