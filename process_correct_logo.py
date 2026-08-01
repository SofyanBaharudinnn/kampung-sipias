import os
import shutil
from PIL import Image

src_path = r"C:\Users\Sofyan-LEGION\.gemini\antigravity-ide\brain\a971a0be-2bde-4e9d-bd46-7a2d0be006fd\media__1785547670725.jpg"
out_dir = r"c:\Users\Sofyan-LEGION\.gemini\antigravity-ide\scratch\kampung-sipias\static\images"

os.makedirs(out_dir, exist_ok=True)

# Open the 1024x1024 JPG logo
img = Image.open(src_path).convert("RGBA")

# Save logo_sipias.png
dst_logo = os.path.join(out_dir, "logo_sipias.png")
img.save(dst_logo, "PNG")
print(f"Updated logo_sipias.png from {src_path}")

# Save 512x512 PNG
img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
img_512.save(os.path.join(out_dir, "favicon.png"), "PNG")

# Save 192x192 PNG (for Google Search specification)
img_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
img_192.save(os.path.join(out_dir, "favicon-192x192.png"), "PNG")

# Save 32x32 PNG
img_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
img_32.save(os.path.join(out_dir, "favicon-32x32.png"), "PNG")

# Save 180x180 apple touch icon
img_180 = img.resize((180, 180), Image.Resampling.LANCZOS)
img_180.save(os.path.join(out_dir, "apple-touch-icon.png"), "PNG")

# Save ICO
img.save(os.path.join(out_dir, "favicon.ico"), format="ICO", sizes=[(16,16), (32,32), (48,48), (64,64)])

print("Successfully replaced all logo and favicon files with the REAL Kampung Sipias badge logo!")
