import os, random

def get_random_image_in_folder(folder_path: str) -> str:
    # 1. Get a list of all files in the folder that end with .png
        png_files = [
            file for file in os.listdir(folder_path) if file.lower().endswith(".png")
        ]
    
        # 2. Check if any PNG files were found
        if not png_files:
            raise FileNotFoundError(f"No PNG files found in {folder_path}")
    
        # 3. Choose a random file name
        chosen_file = random.choice(png_files)
    
        # 4. Join the folder path and file name to create the full path
        return os.path.join(folder_path, chosen_file)


def get_random_grass_image() -> str:
    return get_random_image_in_folder("assets/grass/")

def get_random_water_image() -> str:
    return get_random_image_in_folder("assets/water/")

def get_random_obstacle_image() -> str:
    return get_random_image_in_folder("assets/obstacles/")

def get_character_idle_image() -> str:
    return get_random_image_in_folder("assets/character/idle")

def get_character_walking_image() -> str:
    return get_random_image_in_folder("assets/character/walking")

def get_random_path_image() -> str:
    return get_random_image_in_folder("assets/path/")

def get_random_water_and_obstacle_image(chance_for_obstacle: float = 1) -> str:
    tile_type = 1 if random.random() < chance_for_obstacle else 0
    if tile_type:
        return get_random_obstacle_image()
    else:
        return get_random_water_image()

def get_pixels_font() -> str:
    return "assets/fonts/BoldPixels.ttf"

def get_apple_path_image() -> str:
    return "assets/objects/apple.png"

def get_key_path_image() -> str:
    return "assets/objects/key.png"

def get_chest_path_image(state: bool = False) -> str:
    if state  == False:
        return "assets/objects/chest_closed.png"
    else:
        return "assets/objects/chest_opened.png"