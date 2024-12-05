import torch

class SeicaAspectRatioPH:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
    
        aspect_ratios = ["custom",                      
                        "Galaxy S21 - 2400x1080",
                        "Galaxy S22/23/24 - 2340x1080",
                        "Galaxy S21/22/23 Ultra - 3088x1440",
                        "Galaxy S24 Ultra - 3120x1440",
                        "G/2 S21 - 1200x540",
                        "G/2 S22/23/24 - 1170x740",
                        "G/2 S21/22/23 Ultra - 1544x720",
                        "G/2 S24 Ultra - 1560x720",
                        "iPhone X - 1125x2436",
                        "iPhone 12/13 - 1170x2532",
                        "iPhone 12/13 Pro - 1242x2688",
                        "iPhone 12/13 Pro Max - 1284x2778",
                        "iPhone 14/15/16 - 2556x1179",
                        "iPhone 14/15/16 Plus - 2278x1284",
                        "iPhone 14/15 Pro - 2796x1290",
                        "iPhone 16 Pro 2622x1206",
                        "iPhone 14/15/16 Pro Max 2868x1320"]
               
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 64, "max": 8192}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 8192}),
                "aspect_ratio": (aspect_ratios,),
                "swap_dimensions": (["Off", "On"],),
                "upscale_factor": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 100.0, "step":0.1}),
                "prescale_factor": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 100.0, "step":0.1}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
            }
        }
    RETURN_TYPES = ("INT", "INT", "FLOAT", "FLOAT", "INT", "LATENT")
    RETURN_NAMES = ("width", "height", "upscale_factor", "prescale_factor", "batch_size", "empty_latent")
    FUNCTION = "Aspect_Ratio"
    CATEGORY = "Seica/Aspect Ratio"

    def Aspect_Ratio(self, width, height, aspect_ratio, swap_dimensions, upscale_factor, prescale_factor, batch_size):
        
        # Galaxy
        if aspect_ratio == "Galaxy S21 - 2400x1080":
            width, height = 1080, 2400  
        elif aspect_ratio == "Galaxy S22/23/24 - 2340x1080":
            width, height = 1080, 2340
        elif aspect_ratio == "Galaxy S21/22/23 Ultra - 3088x1440":
            width, height = 1440, 3088
        elif aspect_ratio == "Galaxy S24 Ultra - 3120x1440":
            width, height = 1440, 3120
        elif aspect_ratio == "G/2 S21 - 1200x540":
            width, height = 540, 1200    
        elif aspect_ratio == "G/2 S22/23/24 - 1170x740":
            width, height = 740, 1170
        elif aspect_ratio == "G/2 S21/22/23 Ultra - 1544x720":            
            width, height = 720, 1544
        elif aspect_ratio == "G/2 S24 Ultra - 1560x720":
            width, height = 720, 1560
        
        # iPhone   
        if aspect_ratio == "iPhone X - 1125x2436":
            width, height = 1125, 2436
        elif aspect_ratio == "iPhone 12/13 - 1170x2532":
            width, height = 1170, 2532  # Fixed typo here
        elif aspect_ratio == "iPhone 12/13 Pro - 1242x2688":
            width, height = 1242, 2688
        elif aspect_ratio == "iPhone 12/13 Pro Max - 1284x2778":
            width, height = 1284, 2778
        elif aspect_ratio == "iPhone 14/15/16 - 2556x1179":
            width, height = 1179, 2556
        elif aspect_ratio == "iPhone 14/15/16 Plus - 2278x1284":
            width, height = 1284, 2278
        elif aspect_ratio == "iPhone 14/15 Pro - 2796x1290":
            width, height = 1290, 2796
        elif aspect_ratio == "iPhone 16 Pro 2622x1206":
            width, height = 1206, 2622
        elif aspect_ratio == "iPhone 14/15/16 Pro Max 2868x1320":
            width, height = 1320, 2868                
        
        if swap_dimensions == "On":
            width, height = height, width
        
        width = int(width*prescale_factor)
        height = int(height*prescale_factor)
        
        latent = torch.zeros([batch_size, 4, height // 8, width // 8])
           
        return(width, height, upscale_factor, prescale_factor, batch_size, {"samples":latent})

NODE_CLASS_MAPPINGS = {
    "SeicaAspectRatio": SeicaAspectRatioPH
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SeicaAspectRatio": "Seica Aspect Ratio"
}