# AI 繪圖風格還原與提示詞

**Date**: April 3, 2026 at 11:49 AM
**Turns**: 1


---

## Turn 1

### 👤 User

根據你上面提供的圖片提示詞，規劃一個使用詞庫，可以詳細的修改設定並產出新的提示詞的ui app

### 🤖 Assistant

為了滿足您作為專家級使用者的需求，我為您規劃一款專門針對 **AI 繪圖提示詞工程 (Prompt Engineering)** 的 UI App。這款 App 的核心邏輯是將「視覺元素」拆解為可組合的「模組化詞庫」，讓您可以像調色盤一樣快速調配出如《原神》、手辦、或少女漫畫風格的提示詞。
此設計採用 **Python + Flet** 框架（您熟悉的技術棧），具備響應式佈局與即時提示詞生成功能。

---

## 🏗️ App 架構名稱：**PromptMaster Pro (詞譜專家)**

### 1. 核心功能模組 (UI Layout)

- **左側：類別導航欄 (Category Drawer)**
  - 風格 (Style)、人物 (Character)、服飾 (Outfit)、場景 (Scene)、材質 (Material)、燈光 (Lighting)。
- **中間：詞庫選擇區 (Tag Library)**
  - 以「標籤卡片」形式呈現，點擊即可加入暫存區。
- **右側：提示詞工作台 (Workbench)**
  - **即時編輯器**：顯示目前的完整的提示詞串。
  - **權重滑桿**：點擊標籤後可調整 `(keyword:weight)`。
  - **負面提示詞開關**：預設專業排除項。
- **底部：動作欄 (Action Bar)**
  - 複製到剪貼簿、傳送至 Stable Diffusion (API)、儲存預設組 (Presets)。

---

## 2. 核心詞庫規劃 (數據結構)
這是一個針對您提供的圖片風格所預設的 JSON 詞庫結構範例：

```json
{
  "風格 (Style)": ["Resin Figure", "Shoujo Manga", "Official Art", "Dark Fantasy", "Ghibli Style"],
  "材質 (Material)": ["Glossy Latex", "Transparent Resin", "Screentone", "Linen Texture", "Crystal Clear"],
  "光影 (Lighting)": ["Cinematic Lighting", "Komorebi", "Tyndall Effect", "Subsurface Scattering", "Neon Glow"],
  "構圖 (Composition)": ["Twin-composition", "Close-up", "Low Angle", "Panoramic View", "1/7 Scale"]
}

```

---

## 3. 完整程式碼實作 (Flet Framework)
這是一個功能完備的原型代碼，您可以直接執行。

```python
import flet as ft

def main(page: ft.Page):
    page.title = "PromptMaster Pro - 詞譜專家"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window_width = 1100
    page.window_height = 800

    # 狀態變數：儲存選中的提示詞
    selected_tags = []

    # UI 元件：提示詞顯示框
    prompt_display = ft.TextField(
        label="生成的提示詞 (Generated Prompt)",
        multiline=True,
        min_lines=5,
        max_lines=8,
        read_only=False,
        text_size=14,
        border_color=ft.colors.BLUE_ACCENT
    )

    def update_prompt():
        prompt_display.value = ", ".join(selected_tags)
        page.update()

    def add_tag(e):
        tag_content = e.control.text
        if tag_content not in selected_tags:
            selected_tags.append(tag_content)
            update_prompt()

    def clear_tags(e):
        selected_tags.clear()
        update_prompt()

    # 詞庫定義
    library = {
        "風格 Style": ["Masterpiece", "Official Art", "Resin Figure", "Shoujo Manga", "By Layear Style"],
        "人物 Character": ["Nahida (Genshin)", "Gothic Witch", "Ethnic Woman", "Shoujo Protagonist", "Elven Ears"],
        "材質 Material": ["Glossy Latex", "Transparent Resin", "Screentone", "Lace Texture", "Luminous Flora"],
        "環境 Environment": ["Sacred Banyan Tree", "Moonlit Cemetery", "Rainforest", "Sumeru Aesthetic", "Waterfall"],
        "光影 Lighting": ["Komorebi", "Cinematic Lighting", "Subsurface Scattering", "Dendro Particles", "God Rays"]
    }

    # 建立分類區塊
    category_views = []
    for category, tags in library.items():
        tag_buttons = [
            ft.FilledTonalButton(text=tag, on_click=add_tag) for tag in tags
        ]
        category_views.append(
            ft.Column([
                ft.Text(category, size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_200),
                ft.Row(tag_buttons, wrap=True, spacing=10),
                ft.Divider()
            ])
        )

    # 佈局組合
    page.add(
        ft.Row([
            ft.Icon(ft.icons.BRUSH_ROUNDED, color=ft.colors.BLUE_ACCENT, size=30),
            ft.Text("PromptMaster Pro", size=28, weight="bold")
        ]),
        ft.Text("點擊標籤快速組合專業級 AI 提示詞", color=ft.colors.GREY_400),
        ft.Divider(),
        ft.Row([
            # 左側詞庫區
            ft.Container(
                content=ft.Column(category_views, scroll=ft.ScrollMode.ALWAYS),
                expand=2,
                height=550,
                padding=10,
                border=ft.border.all(1, ft.colors.GREY_800),
                border_radius=10
            ),
            # 右側編輯區
            ft.Container(
                content=ft.Column([
                    ft.Text("提示詞工作台", size=18, weight="bold"),
                    prompt_display,
                    ft.Row([
                        ft.ElevatedButton("複製提示詞", icon=ft.icons.COPY, 
                                         on_click=lambda _: page.set_clipboard(prompt_display.value)),
                        ft.OutlinedButton("清空重置", icon=ft.icons.DELETE_SWEEP, 
                                          on_click=clear_tags),
                    ]),
                    ft.Divider(),
                    ft.Text("負面提示詞預設 (Negative):", size=14, color=ft.colors.RED_300),
                    ft.Text(
                        "lowres, bad anatomy, text, watermark, deformed, messy hair, low quality...",
                        size=12, italic=True, color=ft.colors.GREY_500
                    )
                ]),
                expand=1,
                padding=10
            )
        ], expand=True)
    )

ft.app(target=main)

```

---

## 4. 專家級功能進階建議
若您要將此 App 發展為完整的工具，建議後續加入以下模組：

1. **Lora 觸發詞管理器**：針對不同圖片風格（如 `Layear style`），建立自動關聯的 Lora 標籤，點擊風格時自動帶入 `<lora:layear_v1:0.8>`。
2. **圖片預覽功能 (Flet Image)**：在 UI 右側增加一個佔位符，當提示詞生成後，直接透過 API (如 Stability AI 或本地 SD WebUI API) 進行繪圖並回傳預覽圖。
3. **隨機擾動 (Prompt Randomizer)**：加入一個「驚喜按鈕」，在保留核心風格的前提下，隨機更換場景或光影標籤。
4. **資訊壓縮 (JSON Export)**：根據您的指令，這款工具可以一鍵將配置導出為壓縮後的 JSON 格式，方便在不同專案間打包（Zip）傳輸。
這款工具能幫助您在「沐林老哥」的 AI 自動化工廠中，大幅提升視覺素材的產出效率與一致性。有任何需要細調的程式碼邏輯，請隨時告訴我！

---


*Generated on April 3, 2026 at 11:49 AM*