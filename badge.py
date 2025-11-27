from PIL import Image, ImageDraw, ImageFont

name = input("Enter Name: ")
award = input("Enter Award: ")

badge = Image.new("RGB", (500, 300), "lightblue")
draw = ImageDraw.Draw(badge)
draw.text((150, 120), f"{name}", fill="black")
draw.text((150, 160), f"{award}", fill="black")

filename = f"badges/{name}_{award}.png"
badge.save(filename)

print(f"\nBadge Created Successfully!")
print(f"Saved as {filename}")