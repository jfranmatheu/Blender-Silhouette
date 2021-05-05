from bgl import *
from . id_finder import IDFinder
from . draw.silueta import Draw_Live_Silueta
from . draw.gpu_fun import SetDepth, RstDepth


def live_draw_callback_px(draw_ctx, data, *args, **kwargs):
    settings, style = data
    if settings.live_texid != -1:
        if not style.show_in_front:
            #glEnable(GL_DEPTH_TEST)
            SetDepth()
        Draw_Live_Silueta (
            settings.live_texid,
            *settings.get_live_pos_size(draw_ctx),
            style
            #style.color, style.bg_color
        )
        if not style.show_in_front:
            #glDisable(GL_DEPTH_TEST)
            RstDepth()
        return
    

    '''
    if not IDFinder.matched():
        print("...checking")
        IDFinder.draw_next(draw_ctx.context, draw_ctx.area, *settings.get_live_pos_size(draw_ctx))
        return
    else:
        settings.live_texid = IDFinder.id_data['id']
    '''

    '''
    if not style.in_front:
        glEnable(GL_DEPTH_TEST)

    Draw_Texture (
        k,# if k != -1 else getattr(d[0],d[1]),
        x,
        y,
        w,
        h,
        style.color,
        style.bg_color
    )

    if not style.in_front:
        glDisable(GL_DEPTH_TEST)
    '''
