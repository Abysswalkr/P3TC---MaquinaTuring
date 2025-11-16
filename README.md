# Simulador de Maquinas de Turing

Proyecto final del curso de Teoria de la Computacion (Proyecto 3). El repositorio contiene un simulador general para maquinas de Turing de una cinta descritas mediante archivos YAML, ademas de configuraciones de ejemplo para una MT reconocedora y una MT alteradora.

## Objetivos cubiertos

- Parsing completo de la configuracion formal (estados, alfabetos, transiciones, entradas).
- Simulacion paso a paso con descripciones instantaneas (IDs) en cada transicion.
- Reporte del resultado (aceptada, rechazada o sin decision por limite de pasos) junto con la cinta final.
- Proyecto listo para demostrar dos escenarios solicitados en el PDF:
  - MT reconocedora del lenguaje {a^n b^n | n >= 1} con ejemplos aceptados y no aceptados (longitud >= 5).
  - MT alteradora que invierte los simbolos `a`/`b` sobre la cinta (4 cadenas de longitud >= 5).
- Suite de pruebas automatizadas (`pytest`) para validar el parser y el motor de simulacion.

## Requisitos

- Python 3.10 o superior.
- `pip` para instalar dependencias.

## Instalacion

```bash
pip install -e .[dev]
```

El modo editable expone el comando `tmsim` y permite ejecutar `pytest` sin configuraciones extra.

## Estructura del archivo YAML

```yaml
mt:
  states: [q0, q1, q_accept]
  input_alphabet: [a, b]
  tape_alphabet: [a, b, B, X, Y]
  blank_symbol: B
  initial_state: q0
  accept_states: [q_accept]
  transitions:
    - state: q0
      read: a
      write: X
      move: R        # L, R o S
      next: q1
  inputs:
    - cadena1
    - cadena2
```

Notas:

- `move` admite `L`, `R`, `S` o las palabras `LEFT`, `RIGHT`, `STAY`.
- El alfabeto de la cinta debe contener todos los simbolos que aparecen en `input_alphabet` y el simbolo en `blank_symbol`.
- Si se omite `inputs`, se pueden pasar cadenas via linea de comandos con `--input`.

## Uso

Simular todas las cadenas configuradas en el YAML:

```bash
python -m tmsim examples/recognizer.yaml
```

Simular un subconjunto definido al vuelo y sin limite de pasos:

```bash
tmsim examples/recognizer.yaml --input aaabbb --input aababb --max-steps 0
```

El simulador imprime:

1. IDs numeradas (`Paso N: ...`) donde se inserta el estado entre corchetes en la posicion del cabezal.
2. Estado final de la cadena (ACEPTADA, RECHAZADA o SIN DECISION) y la razon correspondiente.
3. Numero de transiciones realizadas y contenido final de la cinta (sin blancos extremos).

## Ejemplos incluidos

- `examples/recognizer.yaml`: reconoce {a^n b^n | n >= 1}. Las primeras dos cadenas se aceptan y las dos ultimas se rechazan, cumpliendo el requisito de longitudes >= 5.
- `examples/alterer.yaml`: reemplaza cada `a` por `b` y viceversa hasta llegar al blank, mostrando cuatro cadenas de longitud >= 5.

Con estas configuraciones se cubren las evidencias solicitadas en el PDF (MT reconocedora y MT alteradora). Para el video final basta con ejecutar ambos archivos, mostrar las salidas y, en la ultima parte, explicar brevemente la arquitectura (ver mas abajo).

## Arquitectura del codigo

- `src/tmsim/parser.py`: lectura y validacion del YAML; convierte la lista de transiciones en un diccionario `(estado, simbolo)` -> transicion.
- `src/tmsim/tape.py`: implementa la cinta infinita, operaciones de lectura/escritura, desplazamientos y la construccion de IDs.
- `src/tmsim/simulator.py`: motor determinista que ejecuta las transiciones, controla el limite de pasos y genera `SimulationResult`.
- `src/tmsim/cli.py`: CLI con `argparse` (`python -m tmsim` o el entrypoint `tmsim`).
- `examples/`: configuraciones listas para el video.
- `tests/`: validan carga de YAML y casos clave de simulacion (reconocedora y alteradora).

## Pruebas automatizadas

```bash
pytest
```

La configuracion de `pyproject.toml` agrega `src` al `PYTHONPATH`, por lo que no se requiere ningun paso adicional antes de ejecutar las pruebas.

## Flujo sugerido para la prueba del código

1. Ejecutar `python -m tmsim examples/recognizer.yaml` y mostrar:
   - Dos cadenas aceptadas (>= 5 simbolos).
   - Dos cadenas rechazadas (>= 5 simbolos) explicando por que se detienen.
2. Ejecutar `python -m tmsim examples/alterer.yaml` demostrando las cuatro cadenas (>= 5 simbolos) y observando la cinta final transformada.
3. (Opcional) Ejecutar `pytest` para realizar las pruebas y verificar que el código es correcto.

-----

### Vídeo de ejecución

Se puede ver la ejecución del vídeo en YouTube a travez del siguiente link: https://youtu.be/OloltZyQjOA