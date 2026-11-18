<p align="center">
  <img src="docs/images/banner.svg" alt="Silhouette" width="100%">
</p>

<p align="center">
  <a href="https://github.com/jfranmatheu/Blender-Silhouette/releases/latest"><img src="https://img.shields.io/github/v/release/jfranmatheu/Blender-Silhouette?style=for-the-badge&color=ff7a18&label=release" alt="Release"></a>
  <img src="https://img.shields.io/badge/Blender-5.3%2B-ea7600?style=for-the-badge&logo=blender&logoColor=white" alt="Blender 5.3+">
  <img src="https://img.shields.io/badge/GPU-Vulkan%20%7C%20OpenGL%20%7C%20Metal-38506b?style=for-the-badge" alt="GPU backends">
  <a href="LICENSE.md"><img src="https://img.shields.io/badge/licencia-GPLv3-4f622f?style=for-the-badge" alt="GPLv3"></a>
</p>

<p align="center">
  <b>Silhouette</b> dibuja encima del viewport una vista plana y sin detalles de tu malla,<br>
  para que veas de un vistazo si la forma se lee bien desde delante, de lado o desde arriba.
</p>

<p align="center">
  <a href="#-instalación"><b>Instalación</b></a> ·
  <a href="#-qué-hace"><b>Qué hace</b></a> ·
  <a href="https://jfranmatheu.github.io/Blender-Silhouette/"><b>🌐 Web</b></a> ·
  <a href="DOCS.md"><b>Documentación</b></a> ·
  <a href="https://github.com/jfranmatheu/Blender-Silhouette/releases"><b>Descargas</b></a>
</p>

<br>

<p align="center">
  <img src="docs/images/overview.png" alt="Silhouette en el viewport de Blender 5.3" width="92%">
</p>

---

## ✨ Qué hace

<table>
  <tr>
    <td width="33%" align="center">
      <img src="docs/images/preset_front.png" width="100%"><br>
      <b>Vistas predefinidas</b><br>
      <sub>Frontal, trasera, laterales, superior e inferior. Cambia entre ellas con los tres botones de colores.</sub>
    </td>
    <td width="33%" align="center">
      <img src="docs/images/preset_right.png" width="100%"><br>
      <b>Estilo a tu gusto</b><br>
      <sub>Color, fondo transparente u opaco, opacidad y el nombre de la vista en una esquina.</sub>
    </td>
    <td width="33%" align="center">
      <img src="docs/images/panel.png" width="100%"><br>
      <b>Todo en un panel</b><br>
      <sub>El botón del fantasma en la cabecera del viewport lo enciende y la flechita abre los ajustes.</sub>
    </td>
  </tr>
</table>

<p align="center">
  <img src="docs/images/navigation.png" alt="Modo Navigation" width="80%"><br>
  <sub><b>Modo Navigation</b>: la silueta de lo que estás viendo, con el mismo encuadre que el viewport, siguiéndote mientras navegas o esculpes.</sub>
</p>

| | |
|---|---|
| 🎯 **Objetivos** | Objeto activo, objetos seleccionados, un objeto fijo o una colección entera. |
| 🎥 **Modos de vista** | *Preset* (vistas ortográficas), *Camera* (la cámara de la escena u otra que elijas) y *Navigation* (tu vista del viewport tal cual). |
| 🗿 **Sculpt** | Toca la silueta para refrescarla o activa el auto-refresco cada pocos segundos. |
| ⚡ **Ligero** | Solo se vuelve a renderizar cuando cambia algo (posición, escala, rotación, malla...). |

## 📦 Instalación

> [!IMPORTANT]
> Esta versión necesita **Blender 5.3 o superior**. Para Blender 2.93 usa la [release 2.1](https://github.com/jfranmatheu/Blender-Silhouette/releases).

1. Descarga `silhouette_v2.2.0_blender-5.3.zip` desde la [última release](https://github.com/jfranmatheu/Blender-Silhouette/releases/latest).
2. En Blender: **Edit ▸ Preferences ▸ Get Extensions ▸ ⌄ ▸ Install from Disk...** y elige el zip (o arrástralo directamente a la ventana de Blender).
3. Pulsa el icono 👻 en la cabecera del viewport 3D. Listo.

## 📚 Documentación

Toda la explicación con capturas está en **[DOCS.md](DOCS.md)**: cada opción del panel, los modos de vista y los trucos para sculpt.

## 🛠️ Novedades de la 2.2

- Portado a **Blender 5.3**: fuera `bgl`, todo el dibujado va con el módulo `gpu`, así que funciona en Vulkan, OpenGL y Metal.
- Shaders reescritos con `GPUShaderCreateInfo`.
- El modo **Navigation** usa ahora la proyección real del viewport: se ve el modelo entero y con el mismo encuadre, sin recortes, y ya no hace falta tener una cámara en la escena.
- Fuera la vista en vivo (beta): hacía lo mismo que Navigation, y el panel queda mucho más limpio.
- La silueta se dibuja **por encima de la geometría** por defecto.
- Empaquetado como **extensión** (`blender_manifest.toml`).

## 📄 Licencia

Silhouette es software libre bajo la **[GNU GPL v3](LICENSE.md)**.

<p align="center"><sub>Hecho con cariño por <a href="https://github.com/jfranmatheu">@jfranmatheu</a></sub></p>
