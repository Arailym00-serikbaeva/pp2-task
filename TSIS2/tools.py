import pygame

def flood_fill(surface, x, y, new_color):
    # Тандалған пиксельдің қазіргі түсін анықтау
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return

    # Стек арқылы бояу (рекурсия емес, қатып қалмау үшін)
    pixels_to_fill = [(x, y)]
    while pixels_to_fill:
        curr_x, curr_y = pixels_to_fill.pop()
        
        # Егер түсі сәйкес келмесе немесе шекарадан шықса, өткізіп жіберу
        if not (0 <= curr_x < surface.get_width() and 0 <= curr_y < surface.get_height()):
            continue
        if surface.get_at((curr_x, curr_y)) != target_color:
            continue
        
        # Пиксельді бояу
        surface.set_at((curr_x, curr_y), new_color)
        
        # Көрші пиксельдерді стекке қосу
        pixels_to_fill.append((curr_x + 1, curr_y))
        pixels_to_fill.append((curr_x - 1, curr_y))
        pixels_to_fill.append((curr_x, curr_y + 1))
        pixels_to_fill.append((curr_x, curr_y - 1))