from .pipeline.steps import Pipeline

if False:
    mode = input(
        "\nN = Neue Site-Liste erzeugen\n"
        "M = Markierte Sites auswerten\n\n"
        "Auswahl: "
    ).strip().upper()
else:
    mode = "M"

Pipeline().run(mode)