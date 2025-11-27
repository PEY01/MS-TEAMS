from PIL import Image, ImageDraw, ImageFont
print("---Badge Generator App---")
name = input("Enter the Name: ")
award = input("Enter an Award: ")

badge = Image.new("RGB", (500, 300), "white")
draw = ImageDraw.Draw(badge)
draw.text((150, 120), f"{name}", fill="black")
draw.text((150, 160), f"{award}", fill="black")

border_color = "#333333"

filename = f"badges/{name}_{award}.png"
badge.save(filename)

print("\nBadge Created!")
print(f"Saved as {filename}")