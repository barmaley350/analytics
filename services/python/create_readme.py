"""main."""

import re
from pathlib import Path

import nbformat
from nbconvert import MarkdownExporter


def create_empty_md(output_md: Path):
    output_md.write_text("", encoding="utf-8")


def append_md(file_path: Path, output_md: Path):
    with file_path.open("r", encoding="utf-8") as input_file:
        content = input_file.read()

    with output_md.open("a", encoding="utf-8") as output_file:
        output_file.write("\n\n" + content)


def append_jupyter_notebook(file_path: Path, output_md: Path) -> None:
    output_filename_template = f"files/jupyter/images/{file_path.stem}_{{unique_key}}_{{cell_index}}_{{index}}.png"
    markdown_exporter = MarkdownExporter(
        config={
            "ExtractOutputPreprocessor": {
                "enabled": True,
                "output_filename_template": output_filename_template,  # noqa: E501
            }
        }
    )

    with file_path.open("r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    (body, resources) = markdown_exporter.from_notebook_node(notebook)
    body_cleaned = re.sub(r"<style .*?>.*?</style>", "", body, flags=re.DOTALL)

    # Сохраняем все извлечённые изображения
    if "outputs" in resources:
        output_dir = output_md.parent
        output_dir.mkdir(exist_ok=True)
        for filename, data in resources["outputs"].items():
            (output_dir / filename).write_bytes(data)

    with output_md.open("a", encoding="utf-8") as f:
        f.write("\n\n" + body_cleaned)


if __name__ == "__main__":
    resources = [
        Path(__file__).parent.parent.parent / "md/README_DESCRIPTION.md",
        Path(__file__).parent.parent.parent / "md/README_CL.md",
        Path(__file__).parent.parent / "jupyter/notebooks/cars2_file.ipynb",
        Path(__file__).parent.parent.parent / "md/README_CC.md",
        Path(__file__).parent.parent.parent / "md/README_VISUAL.md",
        Path(__file__).parent.parent / "jupyter/notebooks/cars2_cc.ipynb",
    ]
    output_md = Path(__file__).parent.parent.parent / "README.md"
    # convert_and_merge(notebooks, output_md)
    create_empty_md(output_md)
    for file_path in resources:
        if file_path.suffix == ".md":
            append_md(file_path, output_md)
        if file_path.suffix == ".ipynb":
            append_jupyter_notebook(file_path, output_md)
