from bgl import *


def live_draw_callback_px(draw_ctx, rt, *args, **kwargs):
    x, y, w, h = rt.get_pos_size(draw_ctx.area)
    if rt.texid != -1:
        if not rt.in_front:
            glEnable(GL_DEPTH_TEST)
        Draw_Image_Simple (
            rt.texid,
            x, y, w, h,
            rt.color, rt.bg_color
        )
        if not rt.in_front:
            glDisable(GL_DEPTH_TEST)
        return
    
    if not IDFinder.matched():
        print("...checking")
        IDFinder.draw_next(draw_ctx.context, draw_ctx.area, x, y, w, h)
        return
    else:
        rt.texid = IDFinder.id_data['id']
    
    if not rt.in_front:
        glEnable(GL_DEPTH_TEST)
    if rt.experimental:
        #print("Drawing Experimental LiveView")
        k = args[0][0]
        if k == -1:
            d = args[0][1]
            Draw_Image_MoreSimple(getattr(d[0],d[1]), x, y, w, h)
        else:
            Draw_Image_Simple (
                k,# if k != -1 else getattr(d[0],d[1]),
                x,
                y,
                w,
                h,
                rt.color,
                rt.bg_color
            )
    else:
        #print("Drawing LiveView")
        if IDFinder.matched():
            live_draw_off (
                draw_ctx.context,
                x,
                y,
                w,
                h,
                rt.color,
                rt.bg_color
            )
        else:
            IDFinder.draw_next(draw_ctx.context, draw_ctx.area, x, y, w, h)
    if not rt.in_front:
        glDisable(GL_DEPTH_TEST)
