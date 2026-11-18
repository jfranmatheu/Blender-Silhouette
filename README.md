<p align="center">
  <img src="docs/images/banner.svg" alt="Silhouette" width="100%">
</p>

<p align="center">
  <a href="https://github.com/jfranmatheu/Blender-Silhouette/releases/latest"><img src="https://img.shields.io/github/v/release/jfranmatheu/Blender-Silhouette?style=for-the-badge&color=ff7a18&label=release" alt="Release"></a>
  <img src="https://img.shields.io/badge/Blender-5.3%2B-ea7600?style=for-the-badge&logo=blender&logoColor=white" alt="Blender 5.3+">
  <img src="https://img.shields.io/badge/GPU-Vulkan%20%7C%20OpenGL%20%7C%20Metal-38506b?style=for-the-badge" alt="GPU backends">
  <a href="LICENSE.md"><img src="https://img.shields.io/badge/license-GPLv3-4f622f?style=for-the-badge" alt="GPLv3"></a>
</p>

<p align="center">
  <b>Silhouette</b> draws a flat, detail-free view of your mesh on top of the viewport,<br>
  so you can tell at a glance whether the shape reads well from the front, the side or the top.
</p>

<p align="center">
  <a href="#-installation"><b>Installation</b></a> ·
  <a href="#-what-it-does"><b>What it does</b></a> ·
  <a href="https://jfranmatheu.github.io/Blender-Silhouette/"><b>🌐 Website</b></a> ·
  <a href="DOCS.md"><b>Documentation</b></a> ·
  <a href="https://github.com/jfranmatheu/Blender-Silhouette/releases"><b>Downloads</b></a>
</p>

<br>

<p align="center">
  <img src="docs/images/overview.png" alt="Silhouette in the Blender 5.3 viewport" width="92%">
</p>

---

## ✨ What it does

<table>
  <tr>
    <td width="33%" align="center">
      <img src="docs/images/preset_front.png" width="100%"><br>
      <b>Preset views</b><br>
      <sub>Front, back, left, right, top and bottom. Switch between them with the three colored buttons.</sub>
    </td>
    <td width="33%" align="center">
      <img src="docs/images/preset_right.png" width="100%"><br>
      <b>Your own style</b><br>
      <sub>Color, transparent or solid background, opacity and the view name in a corner.</sub>
    </td>
    <td width="33%" align="center">
      <img src="docs/images/panel.png" width="100%"><br>
      <b>All in one panel</b><br>
      <sub>The ghost button in the viewport header turns it on, and the little arrow opens the settings.</sub>
    </td>
  </tr>
</table>

<p align="center">
  <img src="docs/images/navigation.png" alt="Navigation mode" width="80%"><br>
  <sub><b>Navigation mode</b>: the silhouette of what you're looking at, framed exactly like the viewport, following you while you navigate or sculpt.</sub>
</p>

| | |
|---|---|
| 🎯 **Targets** | Active object, selected objects, a fixed object or a whole collection. |
| 🎥 **View modes** | *Preset* (orthographic views), *Camera* (the scene camera or any camera you pick) and *Navigation* (your viewport view, as is). |
| 🗿 **Sculpt** | Click the silhouette to refresh it, or turn on auto-refresh every few seconds. |
| ⚡ **Lightweight** | It only re-renders when something changes (location, scale, rotation, mesh...). |

## 📦 Installation

> [!IMPORTANT]
> This version requires **Blender 5.3 or newer**. For Blender 2.93 use the [2.1 release](https://github.com/jfranmatheu/Blender-Silhouette/releases/tag/v2.1).

1. Download `silhouette_v2.2.0_blender-5.3.zip` from the [latest release](https://github.com/jfranmatheu/Blender-Silhouette/releases/latest).
2. In Blender: **Edit ▸ Preferences ▸ Get Extensions ▸ ⌄ ▸ Install from Disk...** and pick the zip (or just drag it onto the Blender window).
3. Click the 👻 icon in the 3D viewport header. Done.

## 📚 Documentation

The full guide with screenshots lives in **[DOCS.md](DOCS.md)** and on the **[website](https://jfranmatheu.github.io/Blender-Silhouette/)**: every panel option, the view modes and some sculpting tips.

## 🛠️ What's new in 2.2

- Ported to **Blender 5.3**: `bgl` is gone and all drawing goes through the `gpu` module, so it works on Vulkan, OpenGL and Metal.
- Shaders rewritten with `GPUShaderCreateInfo`.
- **Navigation** mode now uses the real viewport projection: you see the whole model with the same framing, no cropping, and the scene no longer needs a camera.
- **Camera** mode uses the scene camera by default when you don't pick one.
- The old live view (beta) is gone: it did the same as Navigation, and the panel is much cleaner now.
- The silhouette is drawn **in front of the geometry** by default.
- Packaged as an **extension** (`blender_manifest.toml`).

## 📄 License

Silhouette is free software released under the **[GNU GPL v3](LICENSE.md)**.

<p align="center"><sub>Made with love by <a href="https://github.com/jfranmatheu">@jfranmatheu</a></sub></p>
