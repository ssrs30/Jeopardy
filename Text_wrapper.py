import pygame
import pygame.freetype
from pathlib import Path

def draw_wrapped_text(surface, text, font, color, rect, centered = False):
    # Convert rect to a pygame.Rect if it isn't one
    target_rect = pygame.Rect(rect)
    words = text.split(' ')
    lines = []
    
    current_line = ""
    for word in words:
        # Check how wide the line would be if we added this word
        test_line = current_line + word + " "
        line_rect = font.get_rect(test_line)
        
        if line_rect.width <= target_rect.width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    
    lines.append(current_line) # Add the last line

    # Draw each line, moving down by the font's height each time
    y_offset = target_rect.y
    line_height = font.get_sized_height()
    
    for line in lines:
        if y_offset + line_height > target_rect.bottom:
            break  # Stop if we run out of vertical space
        if centered:
            text_img, text_rect = font.render(line, color)
            text_rect.center = (target_rect.x, y_offset)
            surface.blit(text_img, text_rect)
        else:
            font.render_to(surface, (target_rect.x, y_offset), line, color)
        y_offset += line_height