import pygame
import math
import datetime
from tools import flood_fill

pygame.init()

# Window size
WIDTH, HEIGHT = 1100, 820
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Studio - Professional")

# 12 Colors
PALETTE = [
    (0,0,0), (128,128,128), (255,255,255), (255,0,0), 
    (0,255,0), (0,0,255), (255,255,0), (255,0,255), 
    (0,255,255), (255,165,0), (165,42,42), (0,128,0)
]

# Canvas Area
canvas_rect = pygame.Rect(250, 20, 830, 770)
canvas = pygame.Surface((canvas_rect.width, canvas_rect.height))
canvas.fill((255, 255, 255))

# History stacks
undo_stack = [canvas.copy()]
redo_stack = []

def push_undo():
    undo_stack.append(canvas.copy())
    if len(undo_stack) > 20: undo_stack.pop(0)
    redo_stack.clear()

# State variables
tool = "pencil"
active_color = (0, 0, 0)
brush_size = 25
drawing = False
start_pos = None
text_input, text_active, text_pos = "", False, (0,0)

# Fonts
font_ui = pygame.font.SysFont("Segoe UI", 13)
font_bold = pygame.font.SysFont("Segoe UI", 15, bold=True)

def draw_sidebar():
    # Sidebar BG
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 240, HEIGHT))
    pygame.draw.line(screen, (230, 230, 230), (240, 0), (240, HEIGHT), 1)

    # 1. HISTORY (Top)
    y = 20
    screen.blit(font_bold.render("HISTORY", True, (37, 99, 235)), (20, y))
    u_btn = pygame.Rect(20, y+25, 95, 32)
    r_btn = pygame.Rect(125, y+25, 95, 32)
    for b, txt in [(u_btn, "Undo"), (r_btn, "Redo")]:
        pygame.draw.rect(screen, (245, 245, 245), b, border_radius=8)
        screen.blit(font_ui.render(txt, True, (50,50,50)), (b.x+30, b.y+7))

    # 2. TOOLS (2x3 Grid)
    y = 100
    screen.blit(font_bold.render("TOOLS", True, (37, 99, 235)), (20, y))
    tools_list = [("Pencil", "pencil"), ("Rectangle", "rect"), ("Circle", "circle"), 
                  ("Fill", "fill"), ("Text", "text"), ("Eraser", "eraser")]
    for i, (name, tid) in enumerate(tools_list):
        r, c = i // 2, i % 2
        rect = pygame.Rect(20 + c*105, y + 25 + r*38, 95, 32)
        is_act = tool == tid
        pygame.draw.rect(screen, (37, 99, 235) if is_act else (250, 250, 250), rect, border_radius=8)
        screen.blit(font_ui.render(name, True, (255,255,255) if is_act else (80,80,80)), (rect.x+15, rect.y+7))

    # 3. SIZE
    y = 250
    screen.blit(font_bold.render(f"SIZE: {brush_size}", True, (37, 99, 235)), (20, y))
    for i, s in enumerate([10, 25, 45, 75]):
        rect = pygame.Rect(20 + i*52, y + 25, 45, 38)
        is_sel = brush_size == s
        pygame.draw.rect(screen, (37, 99, 235) if is_sel else (240, 240, 240), rect, border_radius=8)
        pygame.draw.circle(screen, (255,255,255) if is_sel else (0,0,0), rect.center, 2 + i*3)

    # 4. COLORS (3x4 Grid)
    y = 350
    screen.blit(font_bold.render("COLORS", True, (37, 99, 235)), (20, y))
    for i, col in enumerate(PALETTE):
        r, c = i // 3, i % 3
        rect = pygame.Rect(20 + c*70, y + 30 + r*48, 62, 40)
        pygame.draw.rect(screen, col, rect, border_radius=8)
        pygame.draw.rect(screen, (220,220,220), rect, 1, border_radius=8)
        if active_color == col:
            pygame.draw.rect(screen, (37, 99, 235), rect.inflate(8, 8), 2, border_radius=10)

    # 5. BOTTOM ACTIONS (Save, Clear, Exit)
    y_btm = 610
    save_btn = pygame.Rect(20, y_btm, 200, 42)
    clear_btn = pygame.Rect(20, y_btm + 50, 200, 42)
    exit_btn = pygame.Rect(20, y_btm + 100, 200, 42)
    
    # Save
    pygame.draw.rect(screen, (230, 245, 230), save_btn, border_radius=10)
    screen.blit(font_bold.render("SAVE IMAGE", True, (34, 139, 34)), (75, y_btm+12))
    # Clear
    pygame.draw.rect(screen, (255, 240, 240), clear_btn, border_radius=10)
    screen.blit(font_bold.render("CLEAR CANVAS", True, (200, 50, 50)), (65, y_btm+62))
    # Exit
    pygame.draw.rect(screen, (230, 50, 50), exit_btn, border_radius=10)
    screen.blit(font_bold.render("EXIT APP", True, (255, 255, 255)), (85, y_btm+112))

running = True
while running:
    screen.fill((245, 247, 250))
    screen.blit(canvas, canvas_rect)
    draw_sidebar()
    
    m_pos = pygame.mouse.get_pos()
    m_rel = (m_pos[0] - canvas_rect.x, m_pos[1] - canvas_rect.y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if canvas_rect.collidepoint(m_pos):
                if tool == "fill":
                    flood_fill(canvas, *m_rel, active_color); push_undo()
                elif tool == "text":
                    text_active, text_pos, text_input = True, m_rel, ""
                else:
                    drawing, start_pos = True, m_rel
            else:
                # 1. History
                if pygame.Rect(20, 45, 95, 32).collidepoint(m_pos) and len(undo_stack) > 1:
                    redo_stack.append(undo_stack.pop()); canvas.blit(undo_stack[-1], (0, 0))
                if pygame.Rect(125, 45, 95, 32).collidepoint(m_pos) and redo_stack:
                    undo_stack.append(redo_stack.pop()); canvas.blit(undo_stack[-1], (0, 0))
                
                # 2. Tools
                for i in range(6):
                    r, c = i // 2, i % 2
                    if pygame.Rect(20 + c*105, 125 + r*38, 95, 32).collidepoint(m_pos):
                        tool = ["pencil", "rect", "circle", "fill", "text", "eraser"][i]
                
                # 3. Size
                for i, s in enumerate([10, 25, 45, 75]):
                    if pygame.Rect(20 + i*52, 275, 45, 38).collidepoint(m_pos): brush_size = s
                
                # 4. Colors
                for i, col in enumerate(PALETTE):
                    r, c = i // 3, i % 3
                    if pygame.Rect(20 + c*70, 380 + r*48, 62, 40).collidepoint(m_pos):
                        active_color = col
                        if tool == "eraser": tool = "pencil"
                
                # 5. Save Button
                if pygame.Rect(20, 610, 200, 42).collidepoint(m_pos):
                    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    pygame.image.save(canvas, f"drawing_{now}.png")
                    print(f"Saved as drawing_{now}.png")
                
                # 6. Clear & Exit
                if pygame.Rect(20, 660, 200, 42).collidepoint(m_pos):
                    canvas.fill((255,255,255)); push_undo()
                if pygame.Rect(20, 710, 200, 42).collidepoint(m_pos): running = False

        if event.type == pygame.MOUSEMOTION and drawing:
            if tool in ["pencil", "eraser"]:
                pygame.draw.line(canvas, (255,255,255) if tool=="eraser" else active_color, start_pos, m_rel, brush_size // 3)
                start_pos = m_rel

        if event.type == pygame.MOUSEBUTTONUP and drawing:
            if tool == "rect":
                r = pygame.Rect(start_pos, (m_rel[0]-start_pos[0], m_rel[1]-start_pos[1]))
                r.normalize(); pygame.draw.rect(canvas, active_color, r, brush_size // 10 + 1)
            elif tool == "circle":
                rad = int(math.hypot(m_rel[0]-start_pos[0], m_rel[1]-start_pos[1]))
                pygame.draw.circle(canvas, active_color, start_pos, rad, brush_size // 10 + 1)
            push_undo(); drawing = False

        if event.type == pygame.KEYDOWN and text_active:
            if event.key == pygame.K_RETURN:
                canvas.blit(pygame.font.SysFont("Segoe UI", brush_size).render(text_input, True, active_color), text_pos)
                push_undo(); text_active = False
            elif event.key == pygame.K_BACKSPACE: text_input = text_input[:-1]
            else: text_input += event.unicode

    if text_active:
        t_surf = pygame.font.SysFont("Segoe UI", brush_size).render(text_input + "|", True, active_color)
        screen.blit(t_surf, (text_pos[0] + canvas_rect.x, text_pos[1] + canvas_rect.y))

    pygame.display.flip()
pygame.quit()
