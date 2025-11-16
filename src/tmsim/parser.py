"""Utilidades para cargar archivos YAML con la definicion de la MT."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

from .models import MachineDefinition, Transition, TransitionKey


def _normalize_symbol(value: Any, field_name: str) -> str:
    if isinstance(value, list):
        if len(value) != 1:
            raise ValueError(f"El campo '{field_name}' debe contener un unico simbolo.")
        value = value[0]
    if not isinstance(value, str) or not value:
        raise ValueError(f"El campo '{field_name}' debe ser una cadena no vacia.")
    return value


def _normalize_move(raw_move: Any) -> str:
    symbol = _normalize_symbol(raw_move, "move").upper()
    if symbol.startswith("L"):
        return "L"
    if symbol.startswith("R"):
        return "R"
    if symbol.startswith("S") or symbol.startswith("N"):
        return "S"
    raise ValueError(f"Movimiento invalido: {raw_move}")


def _extract_section(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    if "mt" in raw_data:
        return raw_data["mt"]
    if "machine" in raw_data:
        return raw_data["machine"]
    return raw_data


def load_machine(path: str | Path) -> Tuple[MachineDefinition, List[str]]:
    """
    Carga un archivo YAML y retorna la definicion y la lista de entradas.

    El archivo debe seguir la estructura descrita en las instrucciones del proyecto.
    """

    with Path(path).open("r", encoding="utf-8") as fh:
        raw_data = yaml.safe_load(fh) or {}

    section = _extract_section(raw_data)
    inputs = section.get("inputs") or raw_data.get("inputs") or []
    if not isinstance(inputs, list):
        raise ValueError("El campo 'inputs' debe ser una lista de cadenas.")
    inputs = [str(item) for item in inputs]

    states = _require_sequence(section, "states")
    input_alphabet = _require_sequence(section, "input_alphabet")
    tape_alphabet = _require_sequence(section, "tape_alphabet")
    blank_symbol = _normalize_symbol(section.get("blank_symbol", "B"), "blank_symbol")
    if blank_symbol not in tape_alphabet:
        tape_alphabet = list(tape_alphabet) + [blank_symbol]
    initial_state = _normalize_symbol(section.get("initial_state"), "initial_state")
    accept_states = _require_sequence(section, "accept_states")

    if initial_state not in states:
        raise ValueError("El estado inicial no pertenece al conjunto de estados.")
    for accept in accept_states:
        if accept not in states:
            raise ValueError(f"El estado de aceptacion '{accept}' no es valido.")

    transitions_map: Dict[TransitionKey, Transition] = {}
    for raw_transition in section.get("transitions", []):
        if not isinstance(raw_transition, dict):
            raise ValueError("Cada transicion debe ser un objeto con sus campos.")
        state = _normalize_symbol(raw_transition.get("state"), "state")
        read_symbol = _normalize_symbol(raw_transition.get("read"), "read")
        write_symbol = _normalize_symbol(raw_transition.get("write"), "write")
        move = _normalize_move(raw_transition.get("move"))
        next_state = _normalize_symbol(raw_transition.get("next"), "next")

        for symbol in (read_symbol, write_symbol):
            if symbol not in tape_alphabet:
                raise ValueError(f"El simbolo '{symbol}' no esta en el alfabeto de la cinta.")
        if state not in states or next_state not in states:
            raise ValueError("Las transiciones solo pueden usar estados declarados.")

        key = (state, read_symbol)
        if key in transitions_map:
            raise ValueError(f"Transicion duplicada para ({state}, {read_symbol}).")
        transitions_map[key] = Transition(state, read_symbol, write_symbol, move, next_state)

    definition = MachineDefinition(
        states=states,
        input_alphabet=input_alphabet,
        tape_alphabet=tape_alphabet,
        blank_symbol=blank_symbol,
        initial_state=initial_state,
        accept_states=accept_states,
        transitions=transitions_map,
    )
    return definition, inputs


def _require_sequence(section: Dict[str, Any], field_name: str) -> List[str]:
    raw_value = section.get(field_name)
    if not isinstance(raw_value, list) or not raw_value:
        raise ValueError(f"El campo '{field_name}' debe ser una lista no vacia.")
    return [str(item) for item in raw_value]
