from pathlib import Path

from tmsim.models import SimulationStatus
from tmsim.parser import load_machine
from tmsim.simulator import TuringMachine


EXAMPLES_DIR = Path("examples")


def test_recognizer_accepts_and_rejects():
    definition, _ = load_machine(EXAMPLES_DIR / "recognizer.yaml")
    machine = TuringMachine(definition)

    accepted = machine.simulate("aaabbb", max_steps=2000)
    assert accepted.status == SimulationStatus.ACCEPTED
    assert "XXX" in accepted.final_tape
    assert "YYY" in accepted.final_tape

    rejected = machine.simulate("aaabb", max_steps=2000)
    assert rejected.status == SimulationStatus.REJECTED


def test_alterer_flips_symbols():
    definition, _ = load_machine(EXAMPLES_DIR / "alterer.yaml")
    machine = TuringMachine(definition)

    result = machine.simulate("ababa", max_steps=100)
    assert result.status == SimulationStatus.ACCEPTED
    assert result.final_tape == "babab"
