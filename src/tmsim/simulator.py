"""Motor de simulacion para la Maquina de Turing."""

from __future__ import annotations

from typing import List, Optional

from .models import MachineDefinition, SimulationResult, SimulationStatus, SimulationStep
from .tape import Tape


class TuringMachine:
    """Encapsula la logica de simulacion."""

    def __init__(self, definition: MachineDefinition) -> None:
        self.definition = definition

    def simulate(self, input_string: str, max_steps: Optional[int] = 1000) -> SimulationResult:
        """Ejecuta la MT sobre la cadena indicada."""

        tape = Tape(blank_symbol=self.definition.blank_symbol, initial_input=input_string)
        state = self.definition.initial_state
        steps: List[SimulationStep] = [
            SimulationStep(step=0, state=state, head_position=tape.head, tape_view=tape.instantaneous_description(state))
        ]
        transitions_taken = 0

        while True:
            if state in self.definition.accept_states:
                return SimulationResult(
                    input_string=input_string,
                    status=SimulationStatus.ACCEPTED,
                    reason="Estado de aceptacion alcanzado.",
                    steps=steps,
                    final_tape=tape.contents(),
                    transition_count=transitions_taken,
                )

            if max_steps is not None and transitions_taken >= max_steps:
                return SimulationResult(
                    input_string=input_string,
                    status=SimulationStatus.TIMEOUT,
                    reason=f"Se alcanzo el limite de {max_steps} transiciones.",
                    steps=steps,
                    final_tape=tape.contents(),
                    transition_count=transitions_taken,
                )

            current_symbol = tape.read()
            transition = self.definition.transitions.get((state, current_symbol))
            if transition is None:
                return SimulationResult(
                    input_string=input_string,
                    status=SimulationStatus.REJECTED,
                    reason=f"No existe transicion definida para ({state}, {current_symbol}).",
                    steps=steps,
                    final_tape=tape.contents(),
                    transition_count=transitions_taken,
                )

            tape.write(transition.write_symbol)
            tape.move(transition.move)
            state = transition.next_state
            transitions_taken += 1
            steps.append(
                SimulationStep(
                    step=transitions_taken,
                    state=state,
                    head_position=tape.head,
                    tape_view=tape.instantaneous_description(state),
                )
            )
