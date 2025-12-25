import pygame
import numpy as np

# --- 1. PRE-CALCULATE LOOKUP TABLE (Runs once at import) ---
# We compute the thermal colors for all 256 possible intensity levels upfront.
# This prevents doing the same heavy math millions of times per second.
_snake_lut = np.zeros((256, 3), dtype=np.uint8)
indices = np.arange(256)

# Apply the same formulas as before, but on the small lookup table
_snake_lut[:, 0] = np.clip(indices * 1.5, 0, 255)       # Red Channel
_snake_lut[:, 1] = np.clip((indices - 100) * 3, 0, 255) # Green Channel
_snake_lut[:, 2] = np.clip(255 - indices, 0, 255)       # Blue Channel


def apply_snake_vision(surf):
    """ SERPENT : High Performance + Full Resolution """
    # 1. Get pixels as integers directly (W, H, 3)
    pix = pygame.surfarray.pixels3d(surf)
    
    # 2. Calculate Intensity using efficient Integer Math
    # We sum R+G+B and divide by 3. 
    # (Using uint16 for the sum prevents overflow before division)
    intensity = (pix[:,:,0].astype(np.uint16) + 
                 pix[:,:,1].astype(np.uint16) + 
                 pix[:,:,2].astype(np.uint16)) // 3
                 
    # 3. Apply the Lookup Table
    # NumPy replaces every intensity value with the pre-calculated color instantly.
    new_pix = _snake_lut[intensity]
    return pygame.surfarray.make_surface(new_pix)


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