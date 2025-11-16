"""Modelos y estructuras de datos para el simulador de Maquina de Turing."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Sequence, Tuple


TransitionKey = Tuple[str, str]


class SimulationStatus(str, Enum):
    """Posibles resultados de una simulacion."""

    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    TIMEOUT = "TIMEOUT"


@dataclass(frozen=True)
class Transition:
    """Representa una funcion de transicion delta(q, simbolo)."""

    state: str
    read_symbol: str
    write_symbol: str
    move: str
    next_state: str


@dataclass
class MachineDefinition:
    """Configuracion completa de una Maquina de Turing."""

    states: Sequence[str]
    input_alphabet: Sequence[str]
    tape_alphabet: Sequence[str]
    blank_symbol: str
    initial_state: str
    accept_states: Sequence[str]
    transitions: Dict[TransitionKey, Transition]


@dataclass
class SimulationStep:
    """Descripcion instantanea de la MT en un paso determinado."""

    step: int
    state: str
    head_position: int
    tape_view: str


@dataclass
class SimulationResult:
    """Resultado completo después de simular una cadena."""

    input_string: str
    status: SimulationStatus
    reason: str
    steps: List[SimulationStep]
    final_tape: str
    transition_count: int
