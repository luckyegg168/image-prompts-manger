"""
PromptMaster Pro — 內建預設詞庫 + LoRA 資料
"""

DEFAULT_CATEGORIES = [
    {
        "id": "style",
        "name": "🎨 風格 Style",
        "icon": "🎨",
        "tags": [
            "Masterpiece", "Best Quality", "Official Art", "Resin Figure",
            "Shoujo Manga", "Ghibli Style", "Dark Fantasy", "Cyberpunk",
            "Watercolor", "Oil Painting", "Flat Design", "Pixel Art",
            "Photorealistic", "Anime Style", "Comic Book", "Ukiyo-e",
            "Art Nouveau", "Vaporwave", "Steampunk", "Gothic Art"
        ]
    },
    {
        "id": "character",
        "name": "👤 人物 Character",
        "icon": "👤",
        "tags": [
            "1girl", "1boy", "Multiple Girls", "Couple",
            "Gothic Witch", "Elven Ears", "Angel Wings", "Demon Horns",
            "Maid", "Knight", "Idol", "Schoolgirl", "Warrior",
            "Princess", "Ninja", "Scientist", "Robot Girl", "Vampire"
        ]
    },
    {
        "id": "outfit",
        "name": "👗 服飾 Outfit",
        "icon": "👗",
        "tags": [
            "White Dress", "Gothic Lolita", "School Uniform", "Armor",
            "Kimono", "Cheongsam", "Casual Wear", "Fantasy Robe",
            "Maid Outfit", "Latex Suit", "Wedding Dress", "Swimsuit",
            "Military Uniform", "Hoodie", "Suit and Tie", "Crop Top",
            "Hanfu", "Sailor Uniform", "Cloak", "Lingerie"
        ]
    },
    {
        "id": "scene",
        "name": "🏞️ 場景 Scene",
        "icon": "🏞️",
        "tags": [
            "Sacred Banyan Tree", "Moonlit Cemetery", "Rainforest",
            "Sumeru Aesthetic", "Cyberpunk City", "Cherry Blossom",
            "Castle Interior", "Underwater", "Mountain Peak", "Library",
            "Space Station", "Japanese Garden", "Neon Alley",
            "Ancient Ruins", "Rooftop Sunset", "Snow Village",
            "Enchanted Forest", "Floating Islands", "Cathedral", "Beach"
        ]
    },
    {
        "id": "material",
        "name": "🪨 材質 Material",
        "icon": "🪨",
        "tags": [
            "Glossy Latex", "Transparent Resin", "Screentone",
            "Linen Texture", "Crystal Clear", "Metallic", "Velvet",
            "Porcelain", "Leather", "Silk", "Glass", "Wood Grain",
            "Marble", "Lace", "Fur", "Holographic"
        ]
    },
    {
        "id": "lighting",
        "name": "💡 燈光 Lighting",
        "icon": "💡",
        "tags": [
            "Komorebi", "Cinematic Lighting", "Subsurface Scattering",
            "Tyndall Effect", "God Rays", "Neon Glow", "Golden Hour",
            "Moonlight", "Studio Lighting", "Rim Light",
            "Volumetric Lighting", "Dramatic Shadow", "Soft Light",
            "Backlight", "Candlelight", "Bioluminescence"
        ]
    },
    {
        "id": "composition",
        "name": "📐 構圖 Composition",
        "icon": "📐",
        "tags": [
            "Close-up", "Full Body", "Upper Body", "Low Angle",
            "High Angle", "Dutch Angle", "Panoramic View",
            "Split Screen", "1/7 Scale", "Twin Composition",
            "Portrait", "Profile View", "From Behind",
            "Bird's Eye View", "Dynamic Angle", "Symmetry"
        ]
    },
    {
        "id": "quality",
        "name": "⭐ 品質 Quality",
        "icon": "⭐",
        "tags": [
            "8K UHD", "Highly Detailed", "Sharp Focus",
            "Intricate Details", "Beautiful Lighting",
            "Ultra Realistic", "Hyper Detailed",
            "Professional", "Vivid Colors", "HDR",
            "Ray Tracing", "Depth of Field"
        ]
    }
]

# 預設 LoRA 詞庫 —— 多組分類
DEFAULT_LORAS = [
    # === 動漫風格 ===
    {"name": "animeIllustDiffusion", "trigger": "anime illustration", "weight": 0.7,
     "base": "SD 1.5", "category": "動漫風格", "desc": "日系動漫插畫風"},
    {"name": "mapleSyrupStyle", "trigger": "maple syrup style", "weight": 0.8,
     "base": "SD 1.5", "category": "動漫風格", "desc": "楓糖甜美少女風"},
    {"name": "pastelMixStylized", "trigger": "pastel style", "weight": 0.7,
     "base": "SD 1.5", "category": "動漫風格", "desc": "粉彩夢幻風格"},
    {"name": "flatColor", "trigger": "flat color, cel shading", "weight": 0.6,
     "base": "SDXL", "category": "動漫風格", "desc": "平塗賽璐珞風"},
    {"name": "mangaLineArt", "trigger": "manga line art, monochrome", "weight": 0.7,
     "base": "SD 1.5", "category": "動漫風格", "desc": "漫畫線稿風"},
    {"name": "animagineXL", "trigger": "anime, masterpiece, best quality", "weight": 0.8,
     "base": "SDXL", "category": "動漫風格", "desc": "Animagine XL 精緻動漫"},
    {"name": "ponyDiffusion", "trigger": "score_9, score_8_up", "weight": 0.7,
     "base": "Pony", "category": "動漫風格", "desc": "Pony Diffusion 動漫底模"},

    # === 寫實風格 ===
    {"name": "realisticVision", "trigger": "RAW photo, 8k uhd, dslr", "weight": 0.8,
     "base": "SD 1.5", "category": "寫實風格", "desc": "真人寫實攝影"},
    {"name": "filmGrain", "trigger": "film grain, cinematic, 35mm", "weight": 0.5,
     "base": "SDXL", "category": "寫實風格", "desc": "電影膠片質感"},
    {"name": "bokehEffect", "trigger": "bokeh, depth of field, 85mm lens", "weight": 0.6,
     "base": "SDXL", "category": "寫實風格", "desc": "景深虛化效果"},
    {"name": "studioPortrait", "trigger": "studio lighting, portrait, softbox", "weight": 0.7,
     "base": "SD 1.5", "category": "寫實風格", "desc": "棚拍人像風"},
    {"name": "juggernautXL", "trigger": "photorealistic, hyperrealistic", "weight": 0.7,
     "base": "SDXL", "category": "寫實風格", "desc": "JuggernautXL 超寫實"},
    {"name": "realVisXL", "trigger": "realistic, detailed skin texture", "weight": 0.7,
     "base": "SDXL", "category": "寫實風格", "desc": "RealVisXL 真實肌理"},

    # === 特殊風格 ===
    {"name": "ghibliStyle", "trigger": "ghibli style, watercolor", "weight": 0.7,
     "base": "SDXL", "category": "特殊風格", "desc": "吉卜力水彩風"},
    {"name": "layearResin", "trigger": "layear style, resin figure", "weight": 0.8,
     "base": "SD 1.5", "category": "特殊風格", "desc": "樹脂手辦質感"},
    {"name": "pixelArt16bit", "trigger": "pixel art, 16-bit, retro", "weight": 0.9,
     "base": "SD 1.5", "category": "特殊風格", "desc": "像素藝術風"},
    {"name": "oilPaintingImpasto", "trigger": "oil painting, impasto, thick paint", "weight": 0.7,
     "base": "SDXL", "category": "特殊風格", "desc": "油畫厚塗風"},
    {"name": "cyberpunkEdge", "trigger": "cyberpunk, neon lights, chrome", "weight": 0.6,
     "base": "SDXL", "category": "特殊風格", "desc": "賽博龐克霓虹"},
    {"name": "inkWashSumie", "trigger": "ink wash painting, sumi-e, monochrome", "weight": 0.7,
     "base": "SDXL", "category": "特殊風格", "desc": "水墨畫風"},
    {"name": "artDecoGeometric", "trigger": "art deco, geometric patterns, gold", "weight": 0.6,
     "base": "SDXL", "category": "特殊風格", "desc": "裝飾藝術風"},
    {"name": "ukiyoeStyle", "trigger": "ukiyo-e, woodblock print", "weight": 0.7,
     "base": "SDXL", "category": "特殊風格", "desc": "浮世繪木版畫"},
    {"name": "claymation", "trigger": "claymation, stop motion, clay figure", "weight": 0.8,
     "base": "SDXL", "category": "特殊風格", "desc": "黏土動畫風"},
    {"name": "stainedGlass", "trigger": "stained glass, cathedral window", "weight": 0.7,
     "base": "SDXL", "category": "特殊風格", "desc": "彩繪玻璃風"},

    # === 角色 / IP ===
    {"name": "nahidaGenshin", "trigger": "nahida (genshin impact)", "weight": 0.8,
     "base": "SD 1.5", "category": "角色 IP", "desc": "原神・納西妲"},
    {"name": "hutaoGenshin", "trigger": "hu tao (genshin impact)", "weight": 0.8,
     "base": "SD 1.5", "category": "角色 IP", "desc": "原神・胡桃"},
    {"name": "raidenShogun", "trigger": "raiden shogun (genshin impact)", "weight": 0.8,
     "base": "SD 1.5", "category": "角色 IP", "desc": "原神・雷電將軍"},
    {"name": "hatsuneMiku", "trigger": "hatsune miku, vocaloid", "weight": 0.7,
     "base": "SD 1.5", "category": "角色 IP", "desc": "初音未來"},
    {"name": "saberFate", "trigger": "saber (fate)", "weight": 0.8,
     "base": "SD 1.5", "category": "角色 IP", "desc": "Fate・Saber"},
    {"name": "rem_rezero", "trigger": "rem (re:zero)", "weight": 0.8,
     "base": "SD 1.5", "category": "角色 IP", "desc": "Re:Zero・雷姆"},

    # === FLUX 專用 ===
    {"name": "fluxAnime", "trigger": "anime style, vibrant colors", "weight": 0.8,
     "base": "FLUX.1", "category": "FLUX 專用", "desc": "FLUX 動漫風"},
    {"name": "fluxRealism", "trigger": "photorealistic, raw photo", "weight": 0.7,
     "base": "FLUX.1", "category": "FLUX 專用", "desc": "FLUX 寫實風"},
    {"name": "fluxGhibli", "trigger": "ghibli watercolor, soft pastel", "weight": 0.7,
     "base": "FLUX.1", "category": "FLUX 專用", "desc": "FLUX 吉卜力風"},
    {"name": "fluxCinematic", "trigger": "cinematic, anamorphic, film still", "weight": 0.7,
     "base": "FLUX.1", "category": "FLUX 專用", "desc": "FLUX 電影風"},
]

# 預設負面提示詞
DEFAULT_NEGATIVE_PROMPTS = [
    "lowres", "bad anatomy", "bad hands", "text", "error",
    "missing fingers", "extra digit", "fewer digits", "cropped",
    "worst quality", "low quality", "normal quality",
    "jpeg artifacts", "signature", "watermark", "username",
    "blurry", "artist name", "deformed", "messy hair",
    "extra limbs", "mutated hands", "poorly drawn hands",
    "poorly drawn face", "mutation", "ugly", "duplicate",
    "morbid", "out of frame", "extra fingers"
]

# 內建預設組
DEFAULT_PRESETS = [
    {
        "name": "🌿 原神・納西妲手辦風",
        "tags": [
            {"text": "Masterpiece", "weight": 1.2, "category": "style"},
            {"text": "Best Quality", "weight": 1.2, "category": "style"},
            {"text": "Resin Figure", "weight": 1.0, "category": "style"},
            {"text": "1girl", "weight": 1.0, "category": "character"},
            {"text": "White Dress", "weight": 1.0, "category": "outfit"},
            {"text": "Sacred Banyan Tree", "weight": 1.0, "category": "scene"},
            {"text": "Subsurface Scattering", "weight": 1.0, "category": "lighting"},
            {"text": "Transparent Resin", "weight": 1.0, "category": "material"},
            {"text": "1/7 Scale", "weight": 1.0, "category": "composition"},
        ],
        "loras": [{"name": "layearResin", "weight": 0.8}, {"name": "nahidaGenshin", "weight": 0.8}],
        "description": "適用於 Nahida 風格的高品質樹脂手辦出圖"
    },
    {
        "name": "🦇 少女漫畫・哥德風",
        "tags": [
            {"text": "Shoujo Manga", "weight": 1.0, "category": "style"},
            {"text": "Best Quality", "weight": 1.2, "category": "style"},
            {"text": "Gothic Witch", "weight": 1.0, "category": "character"},
            {"text": "Gothic Lolita", "weight": 1.0, "category": "outfit"},
            {"text": "Moonlit Cemetery", "weight": 1.0, "category": "scene"},
            {"text": "Screentone", "weight": 1.0, "category": "material"},
            {"text": "Rim Light", "weight": 1.0, "category": "lighting"},
            {"text": "Close-up", "weight": 1.0, "category": "composition"},
        ],
        "loras": [{"name": "mangaLineArt", "weight": 0.6}],
        "description": "漫畫線稿風格的哥德少女"
    },
    {
        "name": "🍃 吉卜力・自然風",
        "tags": [
            {"text": "Ghibli Style", "weight": 1.0, "category": "style"},
            {"text": "Official Art", "weight": 1.0, "category": "style"},
            {"text": "1girl", "weight": 1.0, "category": "character"},
            {"text": "Casual Wear", "weight": 1.0, "category": "outfit"},
            {"text": "Cherry Blossom", "weight": 1.0, "category": "scene"},
            {"text": "Komorebi", "weight": 1.0, "category": "lighting"},
            {"text": "Watercolor", "weight": 1.0, "category": "style"},
            {"text": "Full Body", "weight": 1.0, "category": "composition"},
        ],
        "loras": [{"name": "ghibliStyle", "weight": 0.7}],
        "description": "宮崎駿水彩自然風"
    },
    {
        "name": "🌆 賽博龐克・霓虹",
        "tags": [
            {"text": "Cyberpunk", "weight": 1.0, "category": "style"},
            {"text": "Photorealistic", "weight": 1.0, "category": "style"},
            {"text": "1girl", "weight": 1.0, "category": "character"},
            {"text": "Latex Suit", "weight": 1.0, "category": "outfit"},
            {"text": "Cyberpunk City", "weight": 1.0, "category": "scene"},
            {"text": "Neon Glow", "weight": 1.0, "category": "lighting"},
            {"text": "Metallic", "weight": 1.0, "category": "material"},
            {"text": "Dutch Angle", "weight": 1.0, "category": "composition"},
        ],
        "loras": [{"name": "cyberpunkEdge", "weight": 0.6}],
        "description": "霓虹都市賽博龐克風"
    },
    {
        "name": "⚔️ 奇幻戰士・史詩",
        "tags": [
            {"text": "Dark Fantasy", "weight": 1.0, "category": "style"},
            {"text": "Best Quality", "weight": 1.2, "category": "style"},
            {"text": "Warrior", "weight": 1.0, "category": "character"},
            {"text": "Armor", "weight": 1.0, "category": "outfit"},
            {"text": "Castle Interior", "weight": 1.0, "category": "scene"},
            {"text": "Cinematic Lighting", "weight": 1.0, "category": "lighting"},
            {"text": "Metallic", "weight": 1.0, "category": "material"},
            {"text": "Low Angle", "weight": 1.0, "category": "composition"},
        ],
        "loras": [],
        "description": "史詩級暗黑奇幻戰士"
    },
]
