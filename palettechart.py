import matplotlib.pyplot as plt

# Define the seasonal color palettes with fallback RGB hex codes for custom color names
seasonal_palettes_hex = {
    "Spring": [
        ("Bright yellow", "#FFEA00"), ("Gold yellow", "#FFD700"), ("Pastel yellow", "#FFFF99"),
        ("Yellow gold", "#FADA5E"), ("Baby pink", "#FFC0CB"), ("Light pink", "#FFB6C1"),
        ("Salmon", "#FA8072"), ("Coral", "#FF7F50"), ("Light blue", "#ADD8E6"),
        ("Sky blue", "#87CEEB"), ("Light green", "#90EE90"), ("Mint", "#98FF98"),
        ("Peach", "#FFE5B4"), ("Amber", "#FFBF00"), ("Lemon", "#FFF44F")
    ],
    "Summer": [
        ("Cobalt blue", "#0047AB"), ("Indigo", "#4B0082"), ("Blue gray", "#6699CC"),
        ("Gray white", "#D3D3D3"), ("Ivory", "#FFFFF0"), ("Ecru", "#C2B280"),
        ("Stone", "#837060"), ("Dusty pink", "#DCAE96"), ("Rose", "#FF007F"),
        ("Mauve", "#E0B0FF"), ("Light purple", "#CBC3E3"), ("Lilac", "#C8A2C8"),
        ("Pastel purple", "#B39EB5"), ("Pastel blue", "#AEC6CF"), ("Pastel green", "#77DD77"),
        ("Pastel pink", "#FFD1DC"), ("Dusty rose", "#C08081"), ("Light red", "#FF6961")
    ],
    "Autumn": [
        ("Charcoal", "#36454F"), ("Mahogany", "#C04000"), ("Rust", "#B7410E"),
        ("Cream", "#FFFDD0"), ("Taupe", "#483C32"), ("Wheat", "#F5DEB3"),
        ("Mustard", "#FFDB58"), ("Khaki green", "#78866B"), ("Olive", "#808000"),
        ("Terracotta", "#E2725B"), ("Dark maroon", "#800000"), ("Dark red", "#8B0000"),
        ("Burnt orange", "#CC5500"), ("Copper", "#B87333"), ("Dark green", "#006400"),
        ("Sea green", "#2E8B57"), ("Dark gray", "#A9A9A9"), ("Gray silver", "#C0C0C0"),
        ("Amber", "#FFBF00"), ("Gold yellow", "#FFD700"), ("Ecru", "#C2B280")
    ],
    "Winter": [
        ("Bright blue", "#0096FF"), ("Dark blue", "#00008B"), ("Navy blue", "#000080"),
        ("Royal blue", "#4169E1"), ("White gray", "#F5F5F5"), ("Gray white", "#D3D3D3"),
        ("Bright pink", "#FF007F"), ("Neon pink", "#FF6EC7"), ("Hot pink", "#FF69B4"),
        ("Fuchsia", "#FF00FF"), ("Dark purple", "#301934"), ("Violet", "#8F00FF"),
        ("Bright red", "#FF0000"), ("Ruby red", "#9B111E"), ("Magenta", "#FF00FF"),
        ("Cyan", "#00FFFF"), ("Aquamarine", "#7FFFD4"), ("Emerald green", "#50C878"),
        ("Teal", "#008080"), ("Neon green", "#39FF14"), ("Plum", "#8E4585"), ("Maroon", "#800000")
    ]
}

# Plotting the palettes
fig, axes = plt.subplots(4, 1, figsize=(14, 10))
fig.subplots_adjust(hspace=0.8)

for ax, (season, colors) in zip(axes, seasonal_palettes_hex.items()):
    ax.set_title(f"{season} Palette", fontsize=14, weight='bold')
    for i, (color_name, hex_value) in enumerate(colors):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=hex_value))
        ax.text(i + 0.5, -0.1, color_name, ha='center', va='top', fontsize=8, rotation=90)
    ax.set_xlim(0, len(colors))
    ax.set_ylim(0, 1)
    ax.axis('off')

plt.tight_layout()
plt.show()
