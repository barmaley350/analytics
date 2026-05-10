"""main."""

import re
from pathlib import Path

import nbformat
from nbconvert import MarkdownExporter


def convert_and_merge(notebook_paths: list[Path], output_md: Path) -> None:
    """Convert notebooks to markdown and merge them."""
    markdown_exporter = MarkdownExporter(
        config={
            "ExtractOutputPreprocessor": {
                "enabled": True,
                "output_filename_template": "files/jupyter/images/{unique_key}_{cell_index}_{index}.png",  # noqa: E501
            }
        }
    )
    full_content = []

    for nb_path in notebook_paths:
        with nb_path.open("r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        (body, resources) = markdown_exporter.from_notebook_node(notebook)
        body_cleaned = re.sub(r"<style scoped>.*?</style>", "", body, flags=re.DOTALL)
        full_content.append(body_cleaned)

        # Сохраняем все извлечённые изображения
        if "outputs" in resources:
            output_dir = output_md.parent.parent
            output_dir.mkdir(exist_ok=True)
            for filename, data in resources["outputs"].items():
                (output_dir / filename).write_bytes(data)

    with output_md.open("w", encoding="utf-8") as f:
        f.write("\n".join(full_content))


if __name__ == "__main__":
    notebooks = [
        Path(__file__).parent.parent / "jupyter/notebooks/header.ipynb",
        Path(__file__).parent.parent / "jupyter/notebooks/examples.ipynb",
    ]
    output_md = Path(__file__).parent.parent.parent / "md/SQLBOOK.md"
    convert_and_merge(notebooks, output_md)
