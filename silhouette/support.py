# Bloque para apoyar el desarrollo.
# La build de GitHub lo lleva activado; la de la tienda (SuperHive) se genera con SHOW_SUPPORT = False.
# No tocar a mano: lo cambia build.py.
SHOW_SUPPORT = True

SUPERHIVE_URL = "https://superhivemarket.com/products/silhouette"


def draw_support(layout):
    if not SHOW_SUPPORT:
        return
    box = layout.box()
    col = box.column(align=True)
    col.label(text="Enjoying Silhouette?", icon='FUND')
    col.label(text="Made by an indie developer.")
    col.label(text="Support it on SuperHive!")
    row = box.row()
    row.scale_y = 1.3
    row.operator('wm.url_open', text="Support on SuperHive", icon='URL').url = SUPERHIVE_URL
