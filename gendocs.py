import inspect
from pathlib import Path
import subprocess
from textwrap import dedent
import typing


def public_property(obj):
    return isinstance(obj, property) and not obj.__name__.startswith("_")


def public_method(obj):
    if not (inspect.isfunction(obj) or inspect.ismethod(obj)):
        return False
    if obj.__name__.startswith("_") and obj.__name__ != "__init__":
        return False
    return True


def codeblock(code):
    return f"```python\n{code}\n```"


def heading(name, level=1):
    return f"{'#' * level} {name}"


def gh_permalink(file, obj):
    file = Path(file).relative_to(Path(".").absolute())
    lines, start = inspect.getsourcelines(obj)
    end = start + len(lines) - 1
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    url = f"https://github.com/doceme/py-spidev/blob/{commit}/{file}#L{start}-L{end}"
    return f"[Full source]({url})"


def details(content, summary="Signature"):
    return f"""<details><summary>{summary}</summary>\n\n{content}\n\n</details>\n"""


def document_class(cls):
    yield heading(cls.__name__, 2)

    if doc := inspect.getdoc(cls):
        yield doc

    file = inspect.getsourcefile(cls)

    yield heading("Properties", 3)
    for name, m in inspect.getmembers(cls, public_property):
        ptype = m.fget.__annotations__["return"]
        item = f"- `{name}` (`{ptype}`)"
        if doc := inspect.getdoc(m):
            item += f': {doc.replace("\n", " ")}'
        yield item

    yield ""

    yield heading("Methods", 3)
    for name, m in inspect.getmembers(cls, public_method):
        signature = inspect.signature(m)

        # method parameters with 'self' removed
        params = dict(signature.parameters)
        del params["self"]

        # simple signature
        yield heading(f"`{name}({', '.join(params)})`", 4)

        # full (type-hints included) signature
        clean_signature = signature.format(max_width=80).replace("'", "")
        text = f"def {name}{clean_signature}"
        yield details(codeblock(text) + "\n" + gh_permalink(file, m))

        if doc := inspect.getdoc(m):
            yield doc


if __name__ == "__main__":
    import spidev

    if doc := inspect.getdoc(spidev):
        print(doc, end="\n\n")

    for line in document_class(spidev.SpiDev):
        print(line, end="\n\n")

    # with open("spi-numbering.md") as f:
    #     print(f.read())
