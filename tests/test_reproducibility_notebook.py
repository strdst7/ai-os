import json
from pathlib import Path

import nbformat

NOTEBOOK = Path(__file__).resolve().parents[1] / "notebooks" / "reproducibility_analysis.ipynb"


def load_notebook():
    assert NOTEBOOK.is_file(), "reproducibility notebook is missing"
    return nbformat.read(NOTEBOOK, as_version=4)


def test_notebook_is_valid_and_has_no_stored_errors():
    notebook = load_notebook()
    nbformat.validate(notebook)
    errors = [
        output
        for cell in notebook.cells
        for output in cell.get("outputs", [])
        if output.output_type == "error"
    ]
    assert errors == [], f"notebook has stored cell errors: {errors}"


def test_notebook_outputs_match_the_committed_dataset():
    # The notebook is executed at build time, so its stored output must agree
    # with data/sample_telemetry.json. This catches a stale notebook after the
    # dataset is regenerated.
    records = json.loads((NOTEBOOK.parents[1] / "data" / "sample_telemetry.json").read_text())
    streams = [
        output.text
        for cell in load_notebook().cells
        for output in cell.get("outputs", [])
        if output.output_type == "stream"
    ]
    combined = "\n".join(streams)
    assert f"loaded {len(records)} monitoring cycles" in combined
    assert f"schema: OK for all {len(records)} records" in combined


def test_notebook_has_embedded_figures():
    images = [
        output
        for cell in load_notebook().cells
        for output in cell.get("outputs", [])
        if "image/png" in output.get("data", {})
    ]
    assert len(images) >= 3, "expected the stability, decomposition, and timing figures"
