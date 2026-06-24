from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Pruefungsleistung:
    """Repräsentiert eine Prüfungsleistung"""
    note: float

    @property
    def bestanden(self) -> bool:  
        """
        Gibt zurück, ob die Prüfungsleistung bestanden wurde.
        Eine Prüfungsleistung gilt als bestanden, wenn die Note kleiner oder gleich 4.0
        """
        return self.note <= 4.0
    