from __future__ import annotations
from dataclasses import dataclass, field
from semester import Semester

@dataclass
class Studium():
    """Repräsentiert das Studium mit allen Semestern und Zielen"""
    start_datum: str
    ziel_monate: int
    ziel_ects: int
    semester: list[Semester] = field(default_factory = list)

    def erreichte_ects(self) -> int:
        """Berechnet die Gesamt ECTS aus den Semester ECTS"""
        return sum(s.erreichte_ects() for s in self.semester)
        
    def semester_hinzufuegen(self, semester: Semester) -> None:
        """Fügt ein Semester hinzu"""
        self.semester.append(semester)

    