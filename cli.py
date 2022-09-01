import typer
from typing import Optional
from saenghwalgilogbu.main import main


app = typer.Typer()


@app.command()
def run(
    name: str, data_sheet_path: str, exception_map_path: Optional[str] = None
):
    return main(name, data_sheet_path, exception_map_path=exception_map_path)


if __name__ == "__main__":
    app()
