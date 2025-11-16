from pathlib import Path

from tmsim.parser import load_machine


EXAMPLES_DIR = Path("examples")


def test_load_machine_from_yaml():
    definition, inputs = load_machine(EXAMPLES_DIR / "recognizer.yaml")

    assert definition.initial_state == "q0"
    assert definition.blank_symbol == "B"
    assert "q_accept" in definition.accept_states
    assert ("q0", "a") in definition.transitions
    assert len(inputs) == 4

