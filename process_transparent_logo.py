import os
import shutil
from PIL import Image

src_path = r"C:\Users\Sofyan-LEGION\.gemini\antigravity-ide\brain\a971a0be-2bde-4e9d-bd46-7a2d0be006fd\media__1785548997765.png"
out_dir = r"c:\Users\Sofyan-LEGION\.gemini\antigravity-ide\scratch\kampung-sipias\static\images"

os.makedirs(out_dir, exist_ok=True)

# 1. Open transparent PNG
img = Image.open(src_path).convert("RGBA")

# 2. Save main logo_sipias.png
dst_logo = os.path.join(out_dir, "logo_sipias.png")
img.save(dst_logo, "PNG")
print(f"Saved transparent logo to {dst_logo}")

# 3. Save 512x512
img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
img_512.save(os.path.join(out_dir, "favicon.png"), "PNG")

# 4. Save 192x192 (Google Favicon)
img_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
img_192.save(os.path.join(out_dir, "favicon-192x192.png"), "PNG")

# 5. Save 32x32
img_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
img_32.save(os.path.join(out_dir, "favicon-32x32.png"), "PNG")

# 6. Save Apple Touch Icon (180x180)
img_180 = img.resize((180, 180), Image.Resampling.LANCZOS)
img_180.save(os.path.join(out_dir, "apple-touch-icon.png"), "PNG")

# 7. Save ICO format
# Convert transparent PNG to RGBA ICO
img.save(os.path.join(out_dir, "favicon.ico"), format="ICO", sizes=[(16,16), (32,32), (48,48), (64,64)])

print("Successfully replaced all logo & favicon files with the crisp TRANSPARENT PNG logo!")
