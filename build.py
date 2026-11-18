"""
Genera las dos builds de Silhouette:

  - GitHub: con el bloque de "apoya el desarrollo" en preferencias y en el panel.
    -> dist/silhouette_v<version>_blender-<min>.zip

  - Tienda (SuperHive): igual pero sin ese bloque.
    -> releases/store/silhouette_v<version>_blender-<min>_store.zip

Uso:
    python build.py                 # las dos
    python build.py github|store    # solo una

Blender se busca en la variable de entorno BLENDER o en la ruta por defecto de Windows.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "silhouette"
BLENDER = os.environ.get("BLENDER", r"C:\Program Files\Blender Foundation\Blender 5.3\blender.exe")


def manifest():
    # Lectura simple (clave = "valor") para no depender de tomllib (Python 3.11+).
    text = (SRC / "blender_manifest.toml").read_text(encoding="utf-8")
    return dict(re.findall(r'^(\w+)\s*=\s*"([^"]*)"', text, flags=re.M))


def extension_build(source_dir: Path, output: Path):
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    result = subprocess.run(
        [BLENDER, "--factory-startup", "--command", "extension", "build",
         "--source-dir", str(source_dir), "--output-filepath", str(output)],
        capture_output=True, text=True)
    if result.returncode != 0 or not output.exists():
        print(result.stdout, result.stderr)
        sys.exit(f"ERROR: fallo al generar {output.name}")
    print(f"  -> {output.relative_to(ROOT)}")


def copy_source(dst: Path):
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def build_github(name):
    print("Build GitHub (con bloque de apoyo)")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "silhouette"
        copy_source(src)
        set_support(src, True)
        extension_build(src, ROOT / "dist" / f"{name}.zip")


def build_store(name):
    print("Build tienda (sin bloque de apoyo)")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "silhouette"
        copy_source(src)
        set_support(src, False)
        extension_build(src, ROOT / "releases" / "store" / f"{name}_store.zip")


def set_support(src: Path, enabled: bool):
    path = src / "support.py"
    text = path.read_text(encoding="utf-8")
    text, count = re.subn(r"^SHOW_SUPPORT = (True|False)$", f"SHOW_SUPPORT = {enabled}", text, flags=re.M)
    if count != 1:
        sys.exit("ERROR: no encuentro SHOW_SUPPORT en support.py")
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    m = manifest()
    min_ver = ".".join(m["blender_version_min"].split(".")[:2])
    name = f"silhouette_v{m['version']}_blender-{min_ver}"
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "github"):
        build_github(name)
    if which in ("all", "store"):
        build_store(name)
