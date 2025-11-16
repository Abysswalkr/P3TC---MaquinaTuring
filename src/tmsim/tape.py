"""Implementacion de la cinta y herramientas de visualizacion."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass
class Tape:
    """Representa una cinta infinita hacia ambos lados."""

    blank_symbol: str = "B"
    initial_input: str = ""
    cells: Dict[int, str] = field(default_factory=dict)
    head: int = 0

    def __post_init__(self) -> None:
        self.cells = {}
        for idx, symbol in enumerate(self.initial_input):
            self.cells[idx] = symbol
        self.head = 0

    def read(self) -> str:
        """Retorna el simbolo bajo el cabezal."""
        return self.cells.get(self.head, self.blank_symbol)

    def write(self, symbol: str) -> None:
        """Escribe un simbolo en la posicion actual."""
        if symbol == self.blank_symbol:
            self.cells.pop(self.head, None)
        else:
            self.cells[self.head] = symbol

    def move(self, direction: str) -> None:
        """Mueve el cabezal a la izquierda, derecha o lo deja en la misma posicion."""
        normalized = (direction or "S").upper()
        if normalized in {"R", "RIGHT"}:
            self.head += 1
        elif normalized in {"L", "LEFT"}:
            self.head -= 1
        elif normalized in {"S", "N", "STAY"}:
            return
        else:
            raise ValueError(f"Movimiento desconocido: {direction}")

    def bounds(self) -> Tuple[int, int]:
        """Retorna el rango relevante (min, max) visitado en la cinta."""
        positions = set(self.cells.keys())
        positions.add(self.head)
        positions.add(0)
        return min(positions), max(positions)

    def contents(self) -> str:
        """Devuelve la cinta completa (sin recortar) como cadena."""
        min_idx, max_idx = self.bounds()
        chars = [self.cells.get(i, self.blank_symbol) for i in range(min_idx, max_idx + 1)]
        tape = "".join(chars).strip(self.blank_symbol)
        return tape or self.blank_symbol

    def instantaneous_description(self, state: str) -> str:
        """Genera la descripcion instantanea alpha [q] beta."""
        min_idx, max_idx = self.bounds()
        if max_idx < min_idx:
            max_idx = min_idx
        left_chars = [self.cells.get(i, self.blank_symbol) for i in range(min_idx, self.head)]
        right_chars = [self.cells.get(i, self.blank_symbol) for i in range(self.head + 1, max_idx + 1)]
        left = "".join(left_chars).lstrip(self.blank_symbol)
        right = "".join(right_chars).rstrip(self.blank_symbol)
        head_symbol = self.read()
        return f"{left}[{state}]{head_symbol}{right}"
