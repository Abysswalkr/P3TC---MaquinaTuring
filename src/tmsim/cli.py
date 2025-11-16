"""Punto de entrada via linea de comandos."""

from __future__ import annotations

import argparse
import sys
from typing import Iterable, List, Optional

from .models import SimulationResult, SimulationStatus
from .parser import load_machine
from .simulator import TuringMachine


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simulador de Maquina de Turing basado en archivos YAML.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("config", help="Ruta al archivo YAML con la definicion de la MT.")
    parser.add_argument(
        "-i",
        "--input",
        dest="inputs",
        action="append",
        help="Cadena a simular. Puede repetirse para evaluar varias entradas.",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=5000,
        help="Limite de transiciones por cadena (0 = sin limite).",
    )
    return parser


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        definition, default_inputs = load_machine(args.config)
    except Exception as exc:  # pragma: no cover - se convierte en error de usuario
        print(f"Error al cargar la configuracion: {exc}", file=sys.stderr)
        return 2

    inputs = args.inputs or default_inputs
    if not inputs:
        print("No hay cadenas configuradas. Use --input para indicar al menos una.", file=sys.stderr)
        return 2

    max_steps = args.max_steps
    if max_steps is not None and max_steps <= 0:
        max_steps = None

    machine = TuringMachine(definition)
    for idx, entry in enumerate(inputs, start=1):
        result = machine.simulate(entry, max_steps=max_steps)
        _print_result(result)
        if idx < len(inputs):
            print()

    return 0


def _print_result(result: SimulationResult) -> None:
    print(f"== Cadena \"{result.input_string}\" ==")
    for step in result.steps:
        print(f"Paso {step.step:>4}: {step.tape_view}")
    status_message = {
        SimulationStatus.ACCEPTED: "ACEPTADA",
        SimulationStatus.REJECTED: "RECHAZADA",
        SimulationStatus.TIMEOUT: "SIN DECISION",
    }[result.status]
    print(f"Resultado: {status_message} ({result.reason})")
    print(f"Transiciones: {result.transition_count}")
    print(f"Cinta final: {result.final_tape}")


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
