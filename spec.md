# PromptMaster Pro — AI 繪圖提示詞管理器 規格書

> **版本**: v1.2  
> **技術棧**: Python 3.10+ / NiceGUI (Quasar + Tailwind)  
> **目標平台**: 本機瀏覽器 (localhost:8080)  
> **語系**: 繁體中文 zh-TW (預設) / English / 日本語  
> **更新日期**: 2026-04-03

---

## 1. 產品願景

打造一款**模組化 AI 繪圖提示詞工作站**，將視覺元素拆解為可組合的標籤詞庫，讓使用者像調色盤一樣快速調配出各種風格的提示詞。支援權重調整、負面提示詞管理、LoRA 觸發詞、預設組存取、多語系介面等專業功能。

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
| 💡 類別建議 | 每類別 10 條不重複建議提示詞，一鍵套用 |
| 🌐 多語系 | zh-TW / en-US / ja-JP 即時切換 |
| 📐 4K 16:9 輸出 | 預設解析度 1920×1080，16:9 比例 |

---

## 2. 技術架構

### 2.1 技術選型
- **框架**: NiceGUI 3.9+ (Python → Quasar/Vue 前端)
- **佈局**: Quasar 元件 + Tailwind CSS 輔助
- **持久化**: JSON 文件 (data/ 目錄)
- **狀態管理**: Python 類 + NiceGUI refreshable
- **國際化**: 自製 I18n 類 (`app/i18n.py`)

### 2.2 檔案結構
```
image-prompts-manager/
├── main.py                 # 應用入口 (全功能整合)
├── data/
│   ├── tags.json           # 使用者自訂詞庫 (執行時生成)
│   ├── loras.json          # LoRA 詞庫 (執行時生成)
│   ├── presets.json        # 預設組 (執行時生成)
│   ├── settings.json       # 設定 (含語系 locale)
│   └── generated/          # 生成圖片暫存
├── app/
│   ├── __init__.py
│   ├── state.py            # 應用狀態管理 + 語系捷徑
│   ├── default_data.py     # 內建詞庫 / LoRA / 建議 / 預設
│   └── i18n.py             # 多語系翻譯 (zh-TW/en-US/ja-JP)
├── AI.md
├── spec.md
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 3. 多語系規格

### 3.1 支援語系
| 語系代碼 | 語言 | 介面顯示 |
|---------|------|---------|
| zh-TW | 繁體中文 | 繁中 |
| en-US | English | EN |
| ja-JP | 日本語 | JA |

### 3.2 語系切換
- Header 右側語系按鈕群組 (繁中 / EN / JA)
- 語系設定持久化至 `data/settings.json` 的 `locale` 欄位
- 切換即時刷新所有 UI 組件文字

### 3.3 翻譯範圍
- 所有按鈕標籤、工作台標題、通知訊息
- 對話框標題與欄位、tooltip 文字
- 類別建議面板標題

---

## 4. 預設輸出規格

### 4.1 預設解析度
| 設定 | 數值 |
|------|------|
| 寬度 | 1920 px |
| 高度 | 1080 px |
| 比例 | 16:9 (4K 縮放比) |
| Steps | 28 |
| CFG Scale | 7.0 |
| Sampler | Euler a |
| Seed | -1 (隨機) |

### 4.2 快速尺寸快捷鍵
| 標籤 | 解析度 | 比例 |
|------|--------|------|
| 4K 16:9 | 1920×1080 | 16:9 ⭐ 預設 |
| HD 16:9 | 1280×720 | 16:9 |
| 1:1 HD | 1024×1024 | 1:1 |
| 4:3 | 1024×768 | 4:3 |
| 3:4 | 768×1024 | 3:4 |
| 1:1 | 512×512 | 1:1 |
| 2:3 | 512×768 | 2:3 |
| 3:2 | 768×512 | 3:2 |

---

## 5. 類別建議提示詞

每個類別包含 10 條不重複的建議提示詞組合，透過「💡 各類別建議提示詞」面板顯示於標籤詞庫下方。

| 類別 ID | 類別名稱 | 建議數量 |
|---------|---------|---------|
| style | 🎨 風格 | 10 |
| character | 👤 人物 | 10 |
| outfit | 👗 服飾 | 10 |
| scene | 🏞️ 場景 | 10 |
| material | 🪨 材質 | 10 |
| lighting | 💡 燈光 | 10 |
| composition | 📐 構圖 | 10 |
| quality | ⭐ 品質 | 10 |

**套用邏輯**: 點擊建議卡片，將逗號分隔的 tags 逐一加入工作台，已存在的自動跳過 (不重複)。

---

## 6. Bug 修正記錄

### v1.2 (2026-04-03)
| Bug | 原因 | 修正 |
|-----|------|------|
| `TypeError: object NoneType can't be used in 'await' expression` | `ui.clipboard.write()` 回傳 `None`，不是 coroutine，不可 `await` | 移除 `await`，改為直接呼叫 `ui.clipboard.write(text)` |

---

## 7. 預設 LoRA 詞庫 (多組)

### 7.1 動漫風格 LoRA (7 條)
| LoRA 名稱 | 觸發詞 | 預設權重 | 底模 |
|-----------|--------|---------|------|
| animeIllustDiffusion | `anime illustration` | 0.7 | SD 1.5 |
| mapleSyrupStyle | `maple syrup style` | 0.8 | SD 1.5 |
| pastelMixStylized | `pastel style` | 0.7 | SD 1.5 |
| flatColor | `flat color, cel shading` | 0.6 | SDXL |
| mangaLineArt | `manga line art, monochrome` | 0.7 | SD 1.5 |
| animagineXL | `anime, masterpiece, best quality` | 0.8 | SDXL |
| ponyDiffusion | `score_9, score_8_up` | 0.7 | Pony |

### 7.2 寫實風格 LoRA (6 條)
| LoRA 名稱 | 觸發詞 | 預設權重 | 底模 |
|-----------|--------|---------|------|
| realisticVision | `RAW photo, 8k uhd, dslr` | 0.8 | SD 1.5 |
| filmGrain | `film grain, cinematic, 35mm` | 0.5 | SDXL |
| bokehEffect | `bokeh, depth of field, 85mm lens` | 0.6 | SDXL |
| studioPortrait | `studio lighting, portrait, softbox` | 0.7 | SD 1.5 |
| juggernautXL | `photorealistic, hyperrealistic` | 0.7 | SDXL |
| realVisXL | `realistic, detailed skin texture` | 0.7 | SDXL |

### 7.3 特殊風格 LoRA (10 條)
| LoRA 名稱 | 觸發詞 | 預設權重 | 底模 |
|-----------|--------|---------|------|
| ghibliStyle | `ghibli style, watercolor` | 0.7 | SDXL |
| layearResin | `layear style, resin figure` | 0.8 | SD 1.5 |
| pixelArt16bit | `pixel art, 16-bit, retro` | 0.9 | SD 1.5 |
| oilPaintingImpasto | `oil painting, impasto, thick paint` | 0.7 | SDXL |
| cyberpunkEdge | `cyberpunk, neon lights, chrome` | 0.6 | SDXL |
| inkWashSumie | `ink wash painting, sumi-e, monochrome` | 0.7 | SDXL |
| artDecoGeometric | `art deco, geometric patterns, gold` | 0.6 | SDXL |
| ukiyoeStyle | `ukiyo-e, woodblock print` | 0.7 | SDXL |
| claymation | `claymation, stop motion, clay figure` | 0.8 | SDXL |
| stainedGlass | `stained glass, cathedral window` | 0.7 | SDXL |

### 7.4 角色 / IP LoRA (6 條)
| LoRA 名稱 | 觸發詞 | 說明 |
|-----------|--------|------|
| nahidaGenshin | `nahida (genshin impact)` | 原神・納西妲 |
| hutaoGenshin | `hu tao (genshin impact)` | 原神・胡桃 |
| raidenShogun | `raiden shogun (genshin impact)` | 原神・雷電將軍 |
| hatsuneMiku | `hatsune miku, vocaloid` | 初音未來 |
| saberFate | `saber (fate)` | Fate・Saber |
| rem_rezero | `rem (re:zero)` | Re:Zero・雷姆 |

### 7.5 FLUX 專用 LoRA (4 條)
| LoRA 名稱 | 觸發詞 | 底模 |
|-----------|--------|------|
| fluxAnime | `anime style, vibrant colors` | FLUX.1 |
| fluxRealism | `photorealistic, raw photo` | FLUX.1 |
| fluxGhibli | `ghibli watercolor, soft pastel` | FLUX.1 |
| fluxCinematic | `cinematic, anamorphic, film still` | FLUX.1 |

---

## 8. 功能規格

### 8.1 三欄佈局
- **左側 (220px)**: 類別導航 (ui.left_drawer) + LoRA 分組
- **中間 (flex-1)**: 標籤詞庫 (ui.chip) + 💡 建議面板
- **右側 (420px)**: 工作台 (提示詞輸出 / 預設 / 匯出)

### 8.2 核心功能
- ✅ 標籤點擊添加/移除
- ✅ 權重滑桿 (0.1 ~ 2.0)
- ✅ 負面提示詞管理 (預設 + 自訂)
- ✅ LoRA 管理與權重調整
- ✅ 預設組儲存/載入
- ✅ 隨機擾動器 (鎖定保護)
- ✅ 匯出/匯入 JSON
- ✅ 深色模式
- ✅ 剪貼板複製 (Bug Fix v1.2)
- ✅ 類別建議提示詞一鍵套用 (NEW v1.2)
- ✅ 多語系 zh-TW/en-US/ja-JP (NEW v1.2)
- ✅ 預設 4K 16:9 輸出 (NEW v1.2)

---

## 9. 驗收標準

1. `python main.py` 即可啟動，開啟 http://localhost:8080
2. 剪貼板複製功能正常 (不再出現 `TypeError: NoneType await`)
3. 語系切換按鈕 (繁中/EN/JA) 即時更新全部 UI 文字
4. 各類別顯示 10 條不重複建議提示詞，套用後跳過重複
5. 預設 API 設定為 1920×1080 (4K 16:9)
6. 預設詞庫涵蓋 8 類別、140+ 標籤
7. 預設 LoRA 涵蓋 33+ 條目 (動漫/寫實/特殊/角色/FLUX)
8. 資料以 JSON 持久化，語系設定存入 settings.json

---

*Generated: 2026-04-03*  
*Version: v1.2 — Bug Fix + i18n + Suggestions + 4K 16:9*
