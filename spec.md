# PromptMaster Pro — AI 繪圖提示詞管理器 規格書

> **版本**: v1.0  
> **技術棧**: Python 3.10+ / NiceGUI (Quasar + Tailwind)  
> **目標平台**: 本機瀏覽器 (localhost)  
> **語系**: 繁體中文 (zh-TW) 為主介面，提示詞內容為英文  

---

## 1. 產品願景

打造一款**模組化 AI 繪圖提示詞工作站**，將視覺元素拆解為可組合的標籤詞庫，讓使用者像調色盤一樣快速調配出各種風格的提示詞。支援權重調整、負面提示詞管理、LoRA 觸發詞、預設組存取等專業功能。

### 1.1 目標使用者
- AI 繪圖進階玩家（Stable Diffusion / ComfyUI / Midjourney / FLUX）
- 需要快速產出大量風格一致提示詞的內容創作者
- 需要管理個人詞庫並持續擴充的 Prompt 工程師

### 1.2 核心價值
| 價值主張 | 說明 |
|---------|------|
| 🎨 模組化組合 | 將提示詞依類別分群，以標籤卡片點擊組合 |
| ⚖️ 精確權重控制 | 每個標籤可獨立設定 `(keyword:weight)` |
| 💾 預設組管理 | 一鍵儲存 / 載入常用提示詞組合 |
| 🔌 LoRA 自動關聯 | 選擇風格時自動帶入對應 LoRA 觸發詞 |
| 🎲 智慧隨機 | 保留核心風格、隨機替換次要元素 |

---

## 2. 技術架構

### 2.1 技術選型
- **框架**: NiceGUI 3.9+ (Python → Quasar/Vue 前端)
- **佈局**: Quasar 元件 + Tailwind CSS 輔助
- **持久化**: JSON 文件 (data/ 目錄)
- **狀態管理**: Python 類 + NiceGUI refreshable

### 2.2 檔案結構
```
image-prompts-manager/
├── main.py                 # 應用入口
├── data/
│   ├── tags.json           # 使用者自訂詞庫 (執行時生成)
│   ├── presets.json        # 預設組 (執行時生成)
│   └── settings.json       # 設定 (執行時生成)
├── app/
│   ├── __init__.py
│   ├── state.py            # 應用狀態管理
│   ├── default_data.py     # 內建預設詞庫 + LoRA
│   ├── ui_header.py        # 頂部標題列
│   ├── ui_categories.py    # 左側類別導航
│   ├── ui_tags.py          # 中間標籤詞庫
│   ├── ui_workbench.py     # 右側工作台
│   └── ui_dialogs.py       # 對話框 (預設/匯出/設定)
├── AI.md
├── spec.md
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 3. 預設 LoRA 詞庫 (多組)

### 3.1 動漫風格 LoRA
| LoRA 名稱 | 觸發詞 | 預設權重 | 底模 | 說明 |
|-----------|--------|---------|------|------|
| animeIllustDiffusion | `anime illustration` | 0.7 | SD 1.5 | 日系動漫插畫風 |
| mapleSyrupStyle | `maple syrup style` | 0.8 | SD 1.5 | 楓糖甜美少女風 |
| pastelMixStylized | `pastel style` | 0.7 | SD 1.5 | 粉彩夢幻風格 |
| flatColor | `flat color` | 0.6 | SDXL | 平塗賽璐珞風 |
| mangaLineArt | `manga line art, monochrome` | 0.7 | SD 1.5 | 漫畫線稿風 |

### 3.2 寫實風格 LoRA
| LoRA 名稱 | 觸發詞 | 預設權重 | 底模 | 說明 |
|-----------|--------|---------|------|------|
| realisticVision | `RAW photo, 8k uhd, dslr` | 0.8 | SD 1.5 | 真人寫實攝影 |
| filmGrain | `film grain, cinematic` | 0.5 | SDXL | 電影膠片質感 |
| bokenEffect | `bokeh, depth of field, 85mm` | 0.6 | SDXL | 景深虛化效果 |
| studioPortrait | `studio lighting, portrait` | 0.7 | SD 1.5 | 棚拍人像風 |

### 3.3 特殊風格 LoRA
| LoRA 名稱 | 觸發詞 | 預設權重 | 底模 | 說明 |
|-----------|--------|---------|------|------|
| ghibliStyle | `ghibli style` | 0.7 | SDXL | 吉卜力水彩風 |
| layearResin | `layear style, resin figure` | 0.8 | SD 1.5 | 樹脂手辦質感 |
| pixelArt | `pixel art, 16-bit` | 0.9 | SD 1.5 | 像素藝術風 |
| oilPainting | `oil painting, impasto` | 0.7 | SDXL | 油畫厚塗風 |
| cyberpunkEdge | `cyberpunk, neon, chrome` | 0.6 | SDXL | 賽博龐克霓虹 |
| inkWash | `ink wash, sumi-e` | 0.7 | SDXL | 水墨畫風 |
| artDeco | `art deco, geometric` | 0.6 | SDXL | 裝飾藝術風 |

### 3.4 角色 / IP LoRA
| LoRA 名稱 | 觸發詞 | 預設權重 | 底模 | 說明 |
|-----------|--------|---------|------|------|
| nahidaGenshin | `nahida (genshin impact)` | 0.8 | SD 1.5 | 原神・納西妲 |
| hutaoGenshin | `hu tao (genshin impact)` | 0.8 | SD 1.5 | 原神・胡桃 |
| raidenShogun | `raiden shogun (genshin impact)` | 0.8 | SD 1.5 | 原神・雷電將軍 |
| hatsuneMiku | `hatsune miku, vocaloid` | 0.7 | SD 1.5 | 初音未來 |

### 3.5 FLUX 專用 LoRA
| LoRA 名稱 | 觸發詞 | 預設權重 | 底模 | 說明 |
|-----------|--------|---------|------|------|
| fluxAnime | `anime style` | 0.8 | FLUX.1 | FLUX 動漫風 |
| fluxRealism | `photorealistic, raw photo` | 0.7 | FLUX.1 | FLUX 寫實風 |
| fluxGhibli | `ghibli watercolor` | 0.7 | FLUX.1 | FLUX 吉卜力風 |

---

## 4. 功能規格 (同原 spec，改為 NiceGUI 實現)

### 4.1 三欄佈局
- **左側**: 類別導航 (ui.left_drawer)
- **中間**: 標籤詞庫 (ui.card + ui.chip)
- **右側**: 工作台 (ui.card + ui.textarea)

### 4.2 核心功能
- 標籤點擊添加/移除
- 權重滑桿 (0.1 ~ 2.0)
- 負面提示詞管理 (預設 + 自訂)
- LoRA 管理與權重調整
- 預設組儲存/載入
- 隨機擾動器
- 匯出/匯入 JSON
- 深色模式

---

## 5. 驗收標準

1. `python main.py` 即可啟動
2. 預設詞庫涵蓋 7+ 類別、70+ 標籤
3. 預設 LoRA 涵蓋 20+ 條目 (動漫/寫實/特殊/角色/FLUX)
4. 標籤點擊後即時反映在工作台
5. 提示詞可一鍵複製
6. 深色模式視覺一致
7. 資料以 JSON 持久化

---

*Generated: 2026-04-03*
*Based on: AI.md — PromptMaster Pro 初版概念*
