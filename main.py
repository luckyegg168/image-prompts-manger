"""
PromptMaster Pro — AI 繪圖提示詞管理器
主入口：python main.py
"""

import json
from nicegui import ui, app

from app.state import AppState

state = AppState()

# ============================================================
#  自訂 CSS
# ============================================================
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+TC:wght@400;500;700&display=swap');

:root {
    --pm-primary: #7c3aed;
    --pm-accent: #06b6d4;
    --pm-glow: rgba(124, 58, 237, 0.15);
}

body {
    font-family: 'Inter', 'Noto Sans TC', system-ui, sans-serif !important;
}

.tag-chip {
    cursor: pointer;
    transition: all 0.15s ease-out;
    user-select: none;
}
.tag-chip:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
}
.tag-chip-selected {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    color: white !important;
}

.lora-chip {
    cursor: pointer;
    transition: all 0.15s ease-out;
}
.lora-chip:hover {
    transform: translateY(-1px);
}
.lora-chip-selected {
    background: linear-gradient(135deg, #06b6d4, #22d3ee) !important;
    color: white !important;
}

.category-btn {
    transition: all 0.15s ease;
    border-radius: 10px !important;
}
.category-btn-active {
    background: linear-gradient(135deg, #7c3aed22, #a855f722) !important;
    border-left: 3px solid #7c3aed !important;
}

.prompt-output {
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 13px;
    line-height: 1.6;
}

.workbench-card {
    backdrop-filter: blur(12px);
}

.action-btn {
    transition: all 0.15s ease;
}
.action-btn:hover {
    transform: translateY(-1px);
}

.weight-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 13px;
    transition: all 0.15s ease;
}

.preset-card {
    transition: all 0.2s ease;
    cursor: pointer;
}
.preset-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}
</style>
"""


# ============================================================
#  頁面入口
# ============================================================
@ui.page("/")
def index():
    ui.add_head_html(CUSTOM_CSS)
    ui.dark_mode(state.dark_mode)

    # ------ 頂部 Header ------
    with ui.header().classes("items-center px-6 no-wrap h-14").style(
        "background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); "
        "border-bottom: 1px solid rgba(124,58,237,0.3);"
    ):
        ui.icon("brush", size="28px", color="#7c3aed")
        ui.label("PromptMaster Pro").classes("text-lg font-bold ml-2").style(
            "background: linear-gradient(135deg, #a855f7, #06b6d4); "
            "-webkit-background-clip: text; -webkit-text-fill-color: transparent;"
        )
        ui.label("詞譜專家").classes("text-xs ml-2 opacity-60")
        ui.space()
        ui.label("").bind_text_from(
            state, "selected_tags", lambda tags: f"已選 {len(tags)} 標籤"
        ).classes("text-xs opacity-50 mr-4")

        # 深色模式切換
        dark_toggle = ui.button(
            icon="dark_mode" if state.dark_mode else "light_mode",
            on_click=lambda: toggle_dark(dark_toggle),
        ).props("flat round size=sm color=grey-5")

    # ------ 左側 Drawer：類別導航 + LoRA ------
    with ui.left_drawer(value=True).classes("p-0").style(
        "width: 220px; background: rgba(26,26,46,0.95); "
        "border-right: 1px solid rgba(124,58,237,0.2);"
    ).props("show-if-above bordered"):
        build_category_nav()

    # ------ 主內容：中間標籤 + 右側工作台 ------
    with ui.row().classes("w-full h-full gap-0"):
        # 中間：標籤選擇區
        with ui.column().classes("flex-1 p-4 gap-3 overflow-auto").style(
            "min-width: 400px; max-height: calc(100vh - 56px);"
        ):
            build_tag_library()

        # 右側：工作台
        with ui.column().classes("p-4 gap-3 overflow-auto").style(
            "width: 420px; max-height: calc(100vh - 56px); "
            "background: rgba(26,26,46,0.4); "
            "border-left: 1px solid rgba(124,58,237,0.15);"
        ):
            build_workbench()


# ============================================================
#  深色模式切換
# ============================================================
def toggle_dark(btn):
    state.dark_mode = not state.dark_mode
    ui.dark_mode(state.dark_mode)
    btn.props(f'icon={"dark_mode" if state.dark_mode else "light_mode"}')


# ============================================================
#  左側：類別導航
# ============================================================
@ui.refreshable
def build_category_nav():
    # 搜尋框
    ui.input(
        placeholder="🔍 搜尋標籤...",
        on_change=lambda e: on_search(e.value),
    ).classes("mx-3 mt-3").props("dense outlined dark")

    ui.separator().classes("my-2")

    # 類別按鈕
    ui.label("📂 類別").classes("text-xs font-bold uppercase tracking-wider ml-4 opacity-50")

    for cat in state.categories:
        is_active = cat["id"] == state.active_category
        btn_class = "category-btn category-btn-active" if is_active else "category-btn"
        ui.button(
            cat["name"],
            on_click=lambda c=cat["id"]: switch_category(c),
        ).classes(f"w-full justify-start text-left px-4 {btn_class}").props(
            "flat no-caps align=left"
        ).style("font-size: 13px;")

    ui.separator().classes("my-2")

    # LoRA 區域
    ui.label("🔌 LoRA").classes("text-xs font-bold uppercase tracking-wider ml-4 opacity-50")

    # 依分類分組顯示 LoRA
    lora_categories = {}
    for lora in state.loras:
        cat = lora.get("category", "其他")
        lora_categories.setdefault(cat, []).append(lora)

    for lcat, loras in lora_categories.items():
        with ui.expansion(lcat).classes("w-full").props("dense"):
            for lora in loras:
                is_sel = state.is_lora_selected(lora["name"])
                chip_class = "lora-chip lora-chip-selected" if is_sel else "lora-chip"
                with ui.row().classes("items-center w-full px-2 py-1 cursor-pointer rounded hover:bg-white/5").on(
                    "click", lambda l=lora: on_lora_click(l)
                ):
                    ui.icon(
                        "check_circle" if is_sel else "radio_button_unchecked",
                        size="16px",
                        color="#06b6d4" if is_sel else "grey-6",
                    )
                    with ui.column().classes("gap-0 ml-2"):
                        ui.label(lora["name"]).classes("text-xs font-medium")
                        ui.label(f'{lora["base"]} · w={lora.get("weight", 0.7)}').classes(
                            "text-xs opacity-40"
                        )


def switch_category(cat_id: str):
    state.active_category = cat_id
    build_category_nav.refresh()
    build_tag_library.refresh()


def on_search(query: str):
    state.search_query = query.strip().lower()
    build_tag_library.refresh()


def on_lora_click(lora: dict):
    state.toggle_lora(lora)
    build_category_nav.refresh()
    build_workbench.refresh()


# ============================================================
#  中間：標籤詞庫
# ============================================================
@ui.refreshable
def build_tag_library():
    cat = next((c for c in state.categories if c["id"] == state.active_category), None)
    if not cat:
        ui.label("請選擇類別").classes("text-lg opacity-50")
        return

    # 標題
    with ui.row().classes("items-center gap-2 mb-2"):
        ui.label(cat["name"]).classes("text-xl font-bold")
        ui.badge(f'{len(cat["tags"])} 標籤').props("color=purple-8")

    # 過濾
    tags = cat["tags"]
    if state.search_query:
        tags = [t for t in tags if state.search_query in t.lower()]

    if not tags:
        ui.label("找不到符合的標籤").classes("opacity-50 text-sm italic")
        return

    # 標籤卡片 Grid
    with ui.row().classes("flex-wrap gap-2"):
        for tag_text in tags:
            is_sel = state.is_tag_selected(tag_text)
            chip_class = "tag-chip tag-chip-selected" if is_sel else "tag-chip"

            chip = ui.chip(
                tag_text,
                icon="check" if is_sel else None,
                on_click=lambda t=tag_text, c=cat["id"]: on_tag_click(t, c),
                selectable=False,
                removable=False,
            ).classes(chip_class)

            if is_sel:
                chip.props("color=purple-8")
            else:
                chip.props("outline color=grey-6")


def on_tag_click(text: str, category: str):
    state.toggle_tag(text, category)
    build_tag_library.refresh()
    build_workbench.refresh()


# ============================================================
#  右側：工作台
# ============================================================
@ui.refreshable
def build_workbench():
    # ---- 正面提示詞 ----
    with ui.card().classes("w-full workbench-card").style(
        "background: rgba(124,58,237,0.08); border: 1px solid rgba(124,58,237,0.2); border-radius: 12px;"
    ):
        with ui.row().classes("items-center justify-between w-full"):
            ui.label("✨ 正面提示詞").classes("font-bold text-sm")
            with ui.row().classes("gap-1"):
                ui.button(
                    icon="content_copy",
                    on_click=lambda: copy_prompt("positive"),
                ).props("flat round size=sm").tooltip("複製正面提示詞")
                ui.button(
                    icon="casino",
                    on_click=randomize_prompt,
                ).props("flat round size=sm").tooltip("隨機擾動")

        prompt_text = state.generate_positive_prompt()
        ui.textarea(value=prompt_text).classes("w-full prompt-output").props(
            "readonly outlined rows=4 dark"
        ).style("font-size: 12px;")

    # ---- 已選標籤列表 (含權重) ----
    if state.selected_tags:
        with ui.card().classes("w-full").style(
            "background: rgba(26,26,46,0.6); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px;"
        ):
            with ui.row().classes("items-center justify-between w-full"):
                ui.label("🏷️ 已選標籤").classes("font-bold text-sm")
                ui.button(
                    "清空",
                    icon="delete_sweep",
                    on_click=clear_all,
                ).props("flat size=sm color=red-4 no-caps")

            for tag in state.selected_tags:
                with ui.row().classes("items-center w-full gap-2 py-1").style(
                    "border-bottom: 1px solid rgba(255,255,255,0.05);"
                ):
                    # 鎖定按鈕
                    lock_icon = "lock" if tag.get("locked") else "lock_open"
                    lock_color = "amber-5" if tag.get("locked") else "grey-6"
                    ui.button(
                        icon=lock_icon,
                        on_click=lambda t=tag["text"]: toggle_lock(t),
                    ).props(f"flat round dense size=xs color={lock_color}").tooltip(
                        "鎖定 (隨機時不替換)" if not tag.get("locked") else "已鎖定"
                    )

                    # 標籤名稱
                    ui.label(tag["text"]).classes("text-xs flex-1 font-medium")

                    # 權重調整
                    ui.number(
                        value=tag["weight"],
                        min=0.1,
                        max=2.0,
                        step=0.1,
                        format="%.1f",
                        on_change=lambda e, t=tag["text"]: on_weight_change(t, e.value),
                    ).classes("w-20").props("dense outlined dark")

                    # 移除按鈕
                    ui.button(
                        icon="close",
                        on_click=lambda t=tag["text"]: remove_tag(t),
                    ).props("flat round dense size=xs color=red-4")

    # ---- 已選 LoRA ----
    if state.selected_loras:
        with ui.card().classes("w-full").style(
            "background: rgba(6,182,212,0.08); border: 1px solid rgba(6,182,212,0.2); border-radius: 12px;"
        ):
            ui.label("🔌 已選 LoRA").classes("font-bold text-sm")
            for lora in state.selected_loras:
                with ui.row().classes("items-center w-full gap-2 py-1").style(
                    "border-bottom: 1px solid rgba(255,255,255,0.05);"
                ):
                    ui.icon("memory", size="16px", color="#06b6d4")
                    ui.label(lora["name"]).classes("text-xs flex-1 font-medium")
                    ui.number(
                        value=lora["weight"],
                        min=0.1,
                        max=1.0,
                        step=0.1,
                        format="%.1f",
                        on_change=lambda e, n=lora["name"]: on_lora_weight_change(n, e.value),
                    ).classes("w-20").props("dense outlined dark")
                    ui.button(
                        icon="close",
                        on_click=lambda n=lora["name"]: remove_lora(n),
                    ).props("flat round dense size=xs color=red-4")

    # ---- 負面提示詞 ----
    with ui.card().classes("w-full").style(
        "background: rgba(239,68,68,0.06); border: 1px solid rgba(239,68,68,0.15); border-radius: 12px;"
    ):
        with ui.row().classes("items-center justify-between w-full"):
            ui.label("🚫 負面提示詞").classes("font-bold text-sm")
            with ui.row().classes("gap-1"):
                ui.switch(
                    value=state.negative_enabled,
                    on_change=lambda e: toggle_negative(e.value),
                ).props("dense color=red-4")
                ui.button(
                    icon="content_copy",
                    on_click=lambda: copy_prompt("negative"),
                ).props("flat round size=sm").tooltip("複製負面提示詞")

        if state.negative_enabled:
            neg_text = state.generate_negative_prompt()
            ui.textarea(value=neg_text).classes("w-full prompt-output").props(
                "readonly outlined rows=3 dark"
            ).style("font-size: 11px; opacity: 0.8;")

    # ---- 動作列 ----
    ui.separator().classes("my-1")
    with ui.row().classes("w-full justify-center gap-2 flex-wrap"):
        ui.button("💾 儲存預設", on_click=show_save_dialog).props(
            "outline no-caps size=sm color=purple-5"
        ).classes("action-btn")
        ui.button("📂 載入預設", on_click=show_load_dialog).props(
            "outline no-caps size=sm color=cyan-5"
        ).classes("action-btn")
        ui.button("📤 匯出", on_click=export_data).props(
            "outline no-caps size=sm color=teal-5"
        ).classes("action-btn")
        ui.button("📥 匯入", on_click=show_import_dialog).props(
            "outline no-caps size=sm color=amber-5"
        ).classes("action-btn")


# ============================================================
#  工作台操作
# ============================================================
def on_weight_change(text: str, value):
    if value is not None:
        state.set_tag_weight(text, float(value))
        build_workbench.refresh()


def on_lora_weight_change(name: str, value):
    if value is not None:
        state.set_lora_weight(name, float(value))
        build_workbench.refresh()


def remove_tag(text: str):
    state.remove_tag(text)
    build_tag_library.refresh()
    build_workbench.refresh()


def remove_lora(name: str):
    state.remove_lora(name)
    build_category_nav.refresh()
    build_workbench.refresh()


def toggle_lock(text: str):
    state.toggle_tag_lock(text)
    build_workbench.refresh()


def clear_all():
    state.clear_all_tags()
    build_tag_library.refresh()
    build_workbench.refresh()
    build_category_nav.refresh()
    ui.notify("已清空所有標籤", type="info", position="bottom-right")


def toggle_negative(value: bool):
    state.negative_enabled = value
    build_workbench.refresh()


def randomize_prompt():
    state.randomize()
    build_tag_library.refresh()
    build_workbench.refresh()
    ui.notify("🎲 已隨機替換未鎖定標籤", type="positive", position="bottom-right")


async def copy_prompt(kind: str):
    if kind == "positive":
        text = state.generate_positive_prompt()
    else:
        text = state.generate_negative_prompt()

    if text:
        await ui.clipboard.write(text)
        ui.notify(
            f"✅ 已複製{'正面' if kind == 'positive' else '負面'}提示詞",
            type="positive",
            position="bottom-right",
        )
    else:
        ui.notify("沒有內容可複製", type="warning", position="bottom-right")


# ============================================================
#  對話框
# ============================================================
def show_save_dialog():
    with ui.dialog() as dlg, ui.card().style(
        "min-width: 400px; border-radius: 16px;"
    ):
        ui.label("💾 儲存預設組").classes("text-lg font-bold")
        name_input = ui.input("預設名稱", value="我的預設").classes("w-full")
        desc_input = ui.input("描述 (選填)").classes("w-full")
        with ui.row().classes("w-full justify-end gap-2 mt-2"):
            ui.button("取消", on_click=dlg.close).props("flat no-caps")
            ui.button(
                "儲存",
                on_click=lambda: save_preset(dlg, name_input.value, desc_input.value),
            ).props("no-caps color=purple-8")
    dlg.open()


def save_preset(dlg, name: str, desc: str):
    if not name.strip():
        ui.notify("請輸入名稱", type="warning")
        return
    state.save_as_preset(name.strip(), desc.strip())
    dlg.close()
    ui.notify(f"✅ 已儲存預設: {name}", type="positive", position="bottom-right")


def show_load_dialog():
    with ui.dialog() as dlg, ui.card().style(
        "min-width: 500px; max-height: 600px; border-radius: 16px;"
    ):
        ui.label("📂 載入預設組").classes("text-lg font-bold mb-2")

        if not state.presets:
            ui.label("尚無預設組").classes("opacity-50")
        else:
            for preset in state.presets:
                with ui.card().classes("w-full preset-card mb-2").style(
                    "border-radius: 10px;"
                ).on("click", lambda p=preset["name"], d=dlg: load_preset(p, d)):
                    with ui.row().classes("items-center justify-between w-full"):
                        with ui.column().classes("gap-0"):
                            ui.label(preset["name"]).classes("font-bold text-sm")
                            desc = preset.get("description", "")
                            if desc:
                                ui.label(desc).classes("text-xs opacity-50")
                        ui.button(
                            icon="delete",
                            on_click=lambda e, p=preset["name"], d=dlg: delete_preset_action(e, p, d),
                        ).props("flat round size=sm color=red-4")

        ui.button("關閉", on_click=dlg.close).props("flat no-caps").classes("mt-2")
    dlg.open()


def load_preset(name: str, dlg):
    state.load_preset(name)
    dlg.close()
    build_tag_library.refresh()
    build_workbench.refresh()
    build_category_nav.refresh()
    ui.notify(f"✅ 已載入: {name}", type="positive", position="bottom-right")


def delete_preset_action(e, name: str, dlg):
    e.stop_propagation = True
    state.delete_preset(name)
    dlg.close()
    ui.notify(f"🗑️ 已刪除: {name}", type="info", position="bottom-right")
    show_load_dialog()


def export_data():
    data = state.export_all()
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    ui.download(json_str.encode("utf-8"), "promptmaster_export.json")
    ui.notify("📤 已匯出資料", type="positive", position="bottom-right")


def show_import_dialog():
    with ui.dialog() as dlg, ui.card().style(
        "min-width: 400px; border-radius: 16px;"
    ):
        ui.label("📥 匯入資料").classes("text-lg font-bold")
        ui.label("請選擇 JSON 檔案匯入").classes("text-xs opacity-50 mb-2")

        upload = ui.upload(
            label="選擇 JSON 檔案",
            on_upload=lambda e: handle_import(e, dlg),
            auto_upload=True,
        ).props("accept=.json").classes("w-full")

        ui.button("取消", on_click=dlg.close).props("flat no-caps").classes("mt-2")
    dlg.open()


def handle_import(e, dlg):
    try:
        content = e.content.read().decode("utf-8")
        data = json.loads(content)
        state.import_data(data, merge=True)
        dlg.close()
        build_tag_library.refresh()
        build_category_nav.refresh()
        build_workbench.refresh()
        ui.notify("✅ 匯入成功", type="positive", position="bottom-right")
    except Exception as ex:
        ui.notify(f"匯入失敗: {ex}", type="negative", position="bottom-right")


# ============================================================
#  啟動
# ============================================================
ui.run(
    title="PromptMaster Pro — 詞譜專家",
    port=8080,
    dark=True,
    reload=False,
    favicon="🎨",
)
