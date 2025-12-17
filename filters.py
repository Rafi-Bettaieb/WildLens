import pygame
import numpy as np

def apply_snake_vision(surf):
    """ SERPENT : Simulation Thermique (Heatmap) """
    pix = pygame.surfarray.pixels3d(surf).astype(float)
    intensity = np.mean(pix, axis=2)
    new_pix = np.zeros_like(pix)
    new_pix[:,:,0] = np.clip(intensity * 1.5, 0, 255)
    new_pix[:,:,1] = np.clip((intensity - 100) * 3, 0, 255)
    new_pix[:,:,2] = np.clip(255 - intensity, 0, 255)
    return pygame.surfarray.make_surface(new_pix.astype(np.uint8))

def apply_bee_vision(surf):
    """ ABEILLE : Vision UV simulée + Facettes """
    pix = pygame.surfarray.pixels3d(surf)
    pix[:,:,0] = 0
    pix[:,:,2] = np.clip(pix[:,:,2].astype(int)*2, 0, 255)
    del pix
    w, h = surf.get_size()
    return pygame.transform.scale(
        pygame.transform.scale(surf, (w//12, h//12)), 
        (w, h)
    )

def apply_bat_vision(surf):
    """ Vision chauve-souris : détection de contours verte """
    pix = pygame.surfarray.pixels3d(surf)
    gray = np.mean(pix, axis=2)
    edges = np.abs(gray - np.roll(gray, 1, axis=0)) + np.abs(gray - np.roll(gray, 1, axis=1))
    edges = edges > 25
    new_pix = np.zeros_like(pix)
    new_pix[edges, 1] = 255
    return pygame.surfarray.make_surface(new_pix)

# --- UPDATED FUNCTION ---
def apply_eagle_vision(surf, player_pos=None):
    """ AIGLE : Zoom 2x (Center on Player) + Contraste élevé """
    # 1. Apply High Contrast
    pix = pygame.surfarray.pixels3d(surf).astype(float)
    factor = 1.5 
    contrasted = (pix - 128) * factor + 128
    final_pix = np.clip(contrasted, 0, 255).astype(np.uint8)
    
    temp_surf = pygame.surfarray.make_surface(final_pix)
    
    # 2. Apply Zoom
    w, h = surf.get_size()
    zoom_w = w // 2
    zoom_h = h // 2
    
    if player_pos:
        # Calculate the top-left corner of the crop box so it centers on the player
        px, py = player_pos
        crop_x = px - (zoom_w // 2)
        crop_y = py - (zoom_h // 2)
        
        # IMPORTANT: Clamp the box to the screen edges!
        # This prevents crashing if the player is standing near the edge of the screen
        crop_x = max(0, min(crop_x, w - zoom_w))
        crop_y = max(0, min(crop_y, h - zoom_h))
        
        crop_rect = pygame.Rect(crop_x, crop_y, zoom_w, zoom_h)
    else:
        # Default to center if no player position is given
        crop_rect = pygame.Rect(w // 4, h // 4, zoom_w, zoom_h)
    
    zoom_area = temp_surf.subsurface(crop_rect)
    return pygame.transform.scale(zoom_area, (w, h))
# ------------------------

def apply_dog_vision(surf):
    """ CHIEN : Dichromate + Flou """
    pix = pygame.surfarray.pixels3d(surf)
    avg = (pix[:,:,0].astype(np.uint16) + pix[:,:,1].astype(np.uint16)) // 2
    pix[:,:,0] = avg
    pix[:,:,1] = avg
    del pix
    w, h = surf.get_size()
    return pygame.transform.smoothscale(
        pygame.transform.smoothscale(surf, (w//6, h//6)), 
        (w, h)
    )

def apply_deepsea_vision(surf):
    """ POISSON : Profondeur + Bruit """
    pix = pygame.surfarray.pixels3d(surf).astype(float)
    lum = np.clip((pix[:,:,1]*0.6 + pix[:,:,2]*0.4)*3.0 + 
                  np.random.randint(-30, 30, pix.shape[:2]), 0, 255).astype(np.uint8)
    new = np.zeros_like(pix, dtype=np.uint8)
    new[:,:,1] = lum
    new[:,:,2] = (lum*0.8).astype(np.uint8)
    return pygame.surfarray.make_surface(new)