"""
PromptMaster Pro — AI 繪圖提示詞管理器
主入口：python main.py

修正記錄:
  - Fix: ui.clipboard.write() 不可 await，移除 await 修正 TypeError
  - Feat: 多語系支援 (zh-TW 預設 / en-US / ja-JP)
  - Feat: 各類別不重複建議提示詞面板 (💡 建議)
  - Feat: 預設輸出 4K 16:9 (1920×1080)
"""

import json
from nicegui import ui, app

from app.state import AppState
from app.i18n import SUPPORTED_LOCALES

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

.unified-prompt-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(6,182,212,0.08)) !important;
    border: 2px solid rgba(124,58,237,0.35) !important;
    border-radius: 14px !important;
}

.unified-prompt-text {
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 12px;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-all;
    padding: 12px;
    border-radius: 8px;
    background: rgba(0,0,0,0.25);
    border: 1px solid rgba(255,255,255,0.06);
    max-height: 200px;
    overflow-y: auto;
}

.gen-btn {
    background: linear-gradient(135deg, #7c3aed, #06b6d4) !important;
    color: white !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.gen-btn:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.4) !important;
}

.preview-img {
    border-radius: 12px;
    border: 1px solid rgba(124,58,237,0.3);
    max-width: 100%;
    max-height: 400px;
    object-fit: contain;
}

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 8px rgba(124,58,237,0.3); }
    50% { box-shadow: 0 0 20px rgba(124,58,237,0.6); }
}
.generating {
    animation: pulse-glow 1.5s ease-in-out infinite;
}

.sugg-chip {
    cursor: pointer;
    transition: all 0.15s ease;
    font-size: 11px;
}
.sugg-chip:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(6,182,212,0.2);
}

.lang-btn {
    font-size: 11px !important;
    min-width: 36px !important;
    padding: 2px 6px !important;
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

    # 從設定檔還原語系
    saved_locale = state.api_settings.get("locale", "zh-TW")
    if saved_locale != state.locale:
        state.set_locale(saved_locale)

    # ------ 頂部 Header ------
    with ui.header().classes("items-center px-6 no-wrap h-14").style(
        "background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); "
        "border-bottom: 1px solid rgba(124,58,237,0.3);"
    ):
        ui.icon("brush", size="28px", color="#7c3aed")
        ui.label(state.t("app_title")).classes("text-lg font-bold ml-2").style(
            "background: linear-gradient(135deg, #a855f7, #06b6d4); "
            "-webkit-background-clip: text; -webkit-text-fill-color: transparent;"
        )
        ui.label(state.t("app_subtitle")).classes("text-xs ml-2 opacity-60")
        ui.space()
        ui.label("").bind_text_from(
            state, "selected_tags",
            lambda tags: state.t("selected_tags_count", n=len(tags))
        ).classes("text-xs opacity-50 mr-4")

        # 語系切換
        build_lang_switcher()

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
#  語系切換器
# ============================================================
@ui.refreshable
def build_lang_switcher():
    locale_labels = {"zh-TW": "繁中", "en-US": "EN", "ja-JP": "JA"}
    with ui.button_group().props("flat"):
        for loc in SUPPORTED_LOCALES:
            is_active = loc == state.locale
            btn = ui.button(
                locale_labels.get(loc, loc),
                on_click=lambda l=loc: switch_locale(l),
            ).props(
                f"{'color=purple-5' if is_active else 'color=grey-6'} no-caps dense size=xs"
            ).classes("lang-btn")
            if is_active:
                btn.style("font-weight: 700;")


def switch_locale(locale: str):
    state.set_locale(locale)
    # 全面刷新
    build_lang_switcher.refresh()
    build_category_nav.refresh()
    build_tag_library.refresh()
    build_workbench.refresh()


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
        placeholder=state.t("search_placeholder"),
        on_change=lambda e: on_search(e.value),
    ).classes("mx-3 mt-3").props("dense outlined dark")

    ui.separator().classes("my-2")

    # 類別按鈕
    ui.label(state.t("nav_categories")).classes(
        "text-xs font-bold uppercase tracking-wider ml-4 opacity-50"
    )

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
    ui.label(state.t("nav_lora")).classes(
        "text-xs font-bold uppercase tracking-wider ml-4 opacity-50"
    )

    # 依分類分組顯示 LoRA
    lora_categories: dict[str, list] = {}
    for lora in state.loras:
        cat = lora.get("category", "其他")
        lora_categories.setdefault(cat, []).append(lora)

    for lcat, loras in lora_categories.items():
        with ui.expansion(lcat).classes("w-full").props("dense"):
            for lora in loras:
                is_sel = state.is_lora_selected(lora["name"])
                with ui.row().classes(
                    "items-center w-full px-2 py-1 cursor-pointer rounded hover:bg-white/5"
                ).on("click", lambda l=lora: on_lora_click(l)):
                    ui.icon(
                        "check_circle" if is_sel else "radio_button_unchecked",
                        size="16px",
                        color="#06b6d4" if is_sel else "grey-6",
                    )
                    with ui.column().classes("gap-0 ml-2"):
                        ui.label(lora["name"]).classes("text-xs font-medium")
                        ui.label(
                            f'{lora["base"]} · w={lora.get("weight", 0.7)}'
                        ).classes("text-xs opacity-40")


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
#  中間：標籤詞庫 + 建議提示詞
# ============================================================
@ui.refreshable
def build_tag_library():
    cat = next((c for c in state.categories if c["id"] == state.active_category), None)
    if not cat:
        ui.label(state.t("select_category")).classes("text-lg opacity-50")
        return

    # 標題列
    with ui.row().classes("items-center gap-2 mb-2"):
        ui.label(cat["name"]).classes("text-xl font-bold")
        ui.badge(state.t("tag_count_badge", n=len(cat["tags"]))).props("color=purple-8")

    # 過濾
    tags = cat["tags"]
    if state.search_query:
        tags = [t for t in tags if state.search_query in t.lower()]

    if not tags:
        ui.label(state.t("tag_not_found")).classes("opacity-50 text-sm italic")
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

    # ==== 💡 各類別建議提示詞 ====
    suggestions = state.category_suggestions.get(cat["id"], [])
    if suggestions:
        ui.separator().classes("my-3")
        with ui.row().classes("items-center gap-2 mb-2"):
            ui.label(state.t("sugg_title")).classes("font-bold text-sm").style(
                "background: linear-gradient(135deg, #06b6d4, #22d3ee); "
                "-webkit-background-clip: text; -webkit-text-fill-color: transparent;"
            )
            ui.badge(f"{len(suggestions)}").props("color=cyan-8")

        with ui.column().classes("gap-2 w-full"):
            for sugg in suggestions:
                with ui.card().classes("w-full sugg-chip").style(
                    "background: rgba(6,182,212,0.06); "
                    "border: 1px solid rgba(6,182,212,0.2); "
                    "border-radius: 10px; padding: 8px 12px; cursor: pointer;"
                ).on("click", lambda s=sugg, c=cat["id"]: apply_suggestion(s, c)):
                    with ui.row().classes("items-center gap-2 w-full"):
                        ui.icon("add_circle_outline", size="16px", color="#06b6d4")
                        ui.label(sugg).classes("text-xs flex-1").style(
                            "font-family: 'JetBrains Mono', monospace; opacity: 0.9;"
                        )


def apply_suggestion(sugg: str, cat_id: str):
    """將建議提示詞的每個 tag 加入，跳過重複"""
    tags = [t.strip() for t in sugg.split(",") if t.strip()]
    added = 0
    for tag in tags:
        if state.add_tag(tag, cat_id):
            added += 1
    build_tag_library.refresh()
    build_workbench.refresh()
    if added:
        ui.notify(
            f"✅ 已加入 {added} 個標籤",
            type="positive",
            position="bottom-right",
        )
    else:
        ui.notify("標籤已全部存在", type="info", position="bottom-right")


def on_tag_click(text: str, category: str):
    state.toggle_tag(text, category)
    build_tag_library.refresh()
    build_workbench.refresh()


# ============================================================
#  右側：工作台
# ============================================================
@ui.refreshable
def build_workbench():
    T = state.t  # 語系捷徑

    # ==== 統一提示詞輸出 (最醒目) ====
    has_content = bool(state.selected_tags or state.selected_loras)

    with ui.card().classes("w-full unified-prompt-card"):
        with ui.row().classes("items-center justify-between w-full"):
            ui.label(T("wb_unified_output")).classes("font-bold text-base").style(
                "background: linear-gradient(135deg, #a855f7, #06b6d4); "
                "-webkit-background-clip: text; -webkit-text-fill-color: transparent;"
            )
            with ui.row().classes("gap-1"):
                ui.button(
                    icon="content_copy",
                    on_click=lambda: copy_prompt("full"),
                ).props("flat round size=sm color=purple-4").tooltip(T("wb_tooltip_copy"))
                ui.button(
                    icon="settings",
                    on_click=show_api_settings_dialog,
                ).props("flat round size=sm color=grey-5").tooltip(T("wb_tooltip_settings"))

        if has_content:
            full_prompt = state.generate_full_prompt()
            ui.html(f'<div class="unified-prompt-text">{full_prompt}</div>')

            # 生成參數摘要
            s = state.api_settings
            with ui.row().classes("gap-3 flex-wrap mt-1"):
                ui.badge(f'{s.get("width", 1920)}×{s.get("height", 1080)}').props(
                    "color=purple-9 outline"
                )
                ui.badge(f'Steps: {s.get("steps", 28)}').props("color=cyan-8 outline")
                ui.badge(f'CFG: {s.get("cfg_scale", 7.0)}').props("color=teal-8 outline")
                ui.badge(f'{s.get("sampler", "Euler a")}').props("color=indigo-8 outline")

            # 動作按鈕列
            with ui.row().classes("w-full gap-2 mt-2"):
                ui.button(
                    T("btn_copy_positive"),
                    on_click=lambda: copy_prompt("positive"),
                ).props("outline no-caps size=sm color=purple-5").classes("action-btn")
                ui.button(
                    T("btn_copy_negative"),
                    on_click=lambda: copy_prompt("negative"),
                ).props("outline no-caps size=sm color=red-5").classes("action-btn")
                ui.button(
                    T("btn_copy_full"),
                    on_click=lambda: copy_prompt("full"),
                ).props("no-caps size=sm color=purple-8").classes("action-btn")
                ui.button(
                    T("btn_generate"),
                    on_click=generate_image,
                ).props("no-caps size=sm").classes("gen-btn action-btn")
        else:
            ui.label(T("wb_placeholder")).classes(
                "opacity-40 text-sm italic py-4 text-center w-full"
            )

    # ==== 圖片預覽 ====
    if state.last_generated_image:
        with ui.card().classes("w-full").style(
            "background: rgba(26,26,46,0.5); "
            "border: 1px solid rgba(124,58,237,0.2); border-radius: 12px;"
        ):
            with ui.row().classes("items-center justify-between w-full"):
                ui.label(T("wb_gen_result")).classes("font-bold text-sm")
                ui.button(
                    icon="close",
                    on_click=clear_preview,
                ).props("flat round size=sm color=grey-5")
            ui.image(
                f"data:image/png;base64,{state.last_generated_image}"
            ).classes("preview-img w-full")

    # ---- 正面提示詞明細 ----
    if has_content:
        with ui.card().classes("w-full workbench-card").style(
            "background: rgba(124,58,237,0.08); "
            "border: 1px solid rgba(124,58,237,0.2); border-radius: 12px;"
        ):
            with ui.row().classes("items-center justify-between w-full"):
                ui.label(T("wb_positive")).classes("font-bold text-sm")
                ui.button(
                    icon="casino",
                    on_click=randomize_prompt,
                ).props("flat round size=sm").tooltip(T("wb_tooltip_randomize"))

            prompt_text = state.generate_positive_prompt()
            ui.textarea(value=prompt_text).classes("w-full prompt-output").props(
                "readonly outlined rows=3 dark"
            ).style("font-size: 12px;")

    # ---- 已選標籤列表 (含權重) ----
    if state.selected_tags:
        with ui.card().classes("w-full").style(
            "background: rgba(26,26,46,0.6); "
            "border: 1px solid rgba(255,255,255,0.08); border-radius: 12px;"
        ):
            with ui.row().classes("items-center justify-between w-full"):
                ui.label(T("wb_selected_tags")).classes("font-bold text-sm")
                ui.button(
                    T("wb_clear"),
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
                        T("btn_locked") if tag.get("locked") else T("btn_lock_hint")
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
            "background: rgba(6,182,212,0.08); "
            "border: 1px solid rgba(6,182,212,0.2); border-radius: 12px;"
        ):
            ui.label(T("wb_selected_lora")).classes("font-bold text-sm")
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
        "background: rgba(239,68,68,0.06); "
        "border: 1px solid rgba(239,68,68,0.15); border-radius: 12px;"
    ):
        with ui.row().classes("items-center justify-between w-full"):
            ui.label(T("wb_negative")).classes("font-bold text-sm")
            with ui.row().classes("gap-1"):
                ui.switch(
                    value=state.negative_enabled,
                    on_change=lambda e: toggle_negative(e.value),
                ).props("dense color=red-4")
                ui.button(
                    icon="content_copy",
                    on_click=lambda: copy_prompt("negative"),
                ).props("flat round size=sm").tooltip(T("wb_tooltip_copy_neg"))

        if state.negative_enabled:
            neg_text = state.generate_negative_prompt()
            ui.textarea(value=neg_text).classes("w-full prompt-output").props(
                "readonly outlined rows=3 dark"
            ).style("font-size: 11px; opacity: 0.8;")

    # ---- 動作列 ----
    ui.separator().classes("my-1")
    with ui.row().classes("w-full justify-center gap-2 flex-wrap"):
        ui.button(T("btn_save_preset"), on_click=show_save_dialog).props(
            "outline no-caps size=sm color=purple-5"
        ).classes("action-btn")
        ui.button(T("btn_load_preset"), on_click=show_load_dialog).props(
            "outline no-caps size=sm color=cyan-5"
        ).classes("action-btn")
        ui.button(T("btn_export"), on_click=export_data).props(
            "outline no-caps size=sm color=teal-5"
        ).classes("action-btn")
        ui.button(T("btn_import"), on_click=show_import_dialog).props(
            "outline no-caps size=sm color=amber-5"
        ).classes("action-btn")
        ui.button(T("btn_api"), on_click=show_api_settings_dialog).props(
            "outline no-caps size=sm color=grey-5"
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
    ui.notify(state.t("notify_cleared"), type="info", position="bottom-right")


def toggle_negative(value: bool):
    state.negative_enabled = value
    build_workbench.refresh()


def randomize_prompt():
    state.randomize()
    build_tag_library.refresh()
    build_workbench.refresh()
    ui.notify(state.t("notify_randomized"), type="positive", position="bottom-right")


def copy_prompt(kind: str):
    """
    複製提示詞到剪貼板。
    修正: ui.clipboard.write() 是同步方法，不可 await。
    """
    if kind == "positive":
        text = state.generate_positive_prompt()
        notify_key = "notify_copied_positive"
    elif kind == "negative":
        text = state.generate_negative_prompt()
        notify_key = "notify_copied_negative"
    elif kind == "full":
        text = state.generate_full_prompt()
        notify_key = "notify_copied_full"
    else:
        text = ""
        notify_key = "notify_no_content"

    if text:
        # FIX: ui.clipboard.write() returns None — do NOT await it
        ui.clipboard.write(text)
        ui.notify(state.t(notify_key), type="positive", position="bottom-right")
    else:
        ui.notify(state.t("notify_no_content"), type="warning", position="bottom-right")


# ============================================================
#  對話框
# ============================================================
def show_save_dialog():
    T = state.t
    with ui.dialog() as dlg, ui.card().style("min-width: 400px; border-radius: 16px;"):
        ui.label(T("dlg_save_preset_title")).classes("text-lg font-bold")
        name_input = ui.input(T("dlg_save_preset_name"), value="").classes("w-full")
        desc_input = ui.input(T("dlg_save_preset_desc")).classes("w-full")
        with ui.row().classes("w-full justify-end gap-2 mt-2"):
            ui.button(T("btn_cancel"), on_click=dlg.close).props("flat no-caps")
            ui.button(
                T("btn_save"),
                on_click=lambda: save_preset(dlg, name_input.value, desc_input.value),
            ).props("no-caps color=purple-8")
    dlg.open()


def save_preset(dlg, name: str, desc: str):
    if not name.strip():
        ui.notify(state.t("notify_preset_need_name"), type="warning")
        return
    state.save_as_preset(name.strip(), desc.strip())
    dlg.close()
    ui.notify(
        state.t("notify_preset_saved", name=name), type="positive", position="bottom-right"
    )


def show_load_dialog():
    T = state.t
    with ui.dialog() as dlg, ui.card().style(
        "min-width: 500px; max-height: 600px; border-radius: 16px;"
    ):
        ui.label(T("dlg_load_preset_title")).classes("text-lg font-bold mb-2")

        if not state.presets:
            ui.label(T("dlg_no_presets")).classes("opacity-50")
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
                            on_click=lambda e, p=preset["name"], d=dlg: delete_preset_action(
                                e, p, d
                            ),
                        ).props("flat round size=sm color=red-4")

        ui.button(T("btn_close"), on_click=dlg.close).props("flat no-caps").classes("mt-2")
    dlg.open()


def load_preset(name: str, dlg):
    state.load_preset(name)
    dlg.close()
    build_tag_library.refresh()
    build_workbench.refresh()
    build_category_nav.refresh()
    ui.notify(
        state.t("notify_preset_loaded", name=name), type="positive", position="bottom-right"
    )


def delete_preset_action(e, name: str, dlg):
    e.stop_propagation = True
    state.delete_preset(name)
    dlg.close()
    ui.notify(
        state.t("notify_preset_deleted", name=name), type="info", position="bottom-right"
    )
    show_load_dialog()


def export_data():
    data = state.export_all()
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    ui.download(json_str.encode("utf-8"), "promptmaster_export.json")
    ui.notify(state.t("notify_exported"), type="positive", position="bottom-right")


def show_import_dialog():
    T = state.t
    with ui.dialog() as dlg, ui.card().style("min-width: 400px; border-radius: 16px;"):
        ui.label(T("dlg_import_title")).classes("text-lg font-bold")
        ui.label(T("dlg_import_desc")).classes("text-xs opacity-50 mb-2")

        ui.upload(
            label=T("dlg_import_label"),
            on_upload=lambda e: handle_import(e, dlg),
            auto_upload=True,
        ).props("accept=.json").classes("w-full")

        ui.button(T("btn_cancel"), on_click=dlg.close).props("flat no-caps").classes("mt-2")
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
        ui.notify(state.t("notify_imported"), type="positive", position="bottom-right")
    except Exception as ex:
        ui.notify(
            state.t("notify_import_fail", e=ex), type="negative", position="bottom-right"
        )


# ============================================================
#  圖片生成
# ============================================================
async def generate_image():
    """Call SD WebUI API to generate image"""
    if not state.selected_tags:
        ui.notify(state.t("notify_select_tags_first"), type="warning", position="bottom-right")
        return

    ui.notify(
        state.t("notify_generating"),
        type="info",
        position="bottom-right",
        timeout=None,
        spinner=True,
        close_button=True,
    )

    try:
        result = await state.generate_image_api()
        build_workbench.refresh()
        if result:
            ui.notify(state.t("notify_gen_done"), type="positive", position="bottom-right")
        else:
            ui.notify(state.t("notify_gen_empty"), type="warning", position="bottom-right")
    except ConnectionError as e:
        ui.notify(
            f"{state.t('notify_gen_fail_conn')}\n{e}",
            type="negative",
            position="bottom-right",
            multi_line=True,
        )
    except Exception as e:
        ui.notify(
            state.t("notify_gen_fail", e=e), type="negative", position="bottom-right"
        )


def clear_preview():
    state.last_generated_image = None
    build_workbench.refresh()


# ============================================================
#  API 設定對話框
# ============================================================
def show_api_settings_dialog():
    T = state.t
    s = state.api_settings
    with ui.dialog() as dlg, ui.card().style("min-width: 500px; border-radius: 16px;"):
        ui.label(T("dlg_api_title")).classes("text-lg font-bold")
        ui.label(T("dlg_api_desc")).classes("text-xs opacity-50 mb-2")

        api_url = ui.input(T("dlg_api_url"), value=s.get("api_url", "http://127.0.0.1:7860")).classes("w-full")
        api_key = ui.input(T("dlg_api_key"), value=s.get("api_key", "")).classes("w-full").props("type=password")

        ui.separator().classes("my-2")
        ui.label(T("dlg_gen_params")).classes("font-bold text-sm")

        with ui.row().classes("w-full gap-4"):
            width_input = ui.number(
                T("dlg_width"), value=s.get("width", 1920), min=256, max=4096, step=64
            ).classes("flex-1")
            height_input = ui.number(
                T("dlg_height"), value=s.get("height", 1080), min=256, max=4096, step=64
            ).classes("flex-1")

        with ui.row().classes("w-full gap-4"):
            steps_input = ui.number(
                T("dlg_steps"), value=s.get("steps", 28), min=1, max=150, step=1
            ).classes("flex-1")
            cfg_input = ui.number(
                T("dlg_cfg"), value=s.get("cfg_scale", 7.0), min=1.0, max=30.0, step=0.5,
                format="%.1f"
            ).classes("flex-1")

        sampler_input = ui.select(
            [
                "Euler a", "Euler", "DPM++ 2M Karras", "DPM++ SDE Karras",
                "DPM++ 2M SDE Karras", "DDIM", "UniPC", "LMS",
                "DPM++ 2S a Karras", "DPM2 a Karras",
            ],
            value=s.get("sampler", "Euler a"),
            label=T("dlg_sampler"),
        ).classes("w-full")

        seed_input = ui.number(
            T("dlg_seed"), value=s.get("seed", -1), min=-1, step=1
        ).classes("w-full")

        # 常用尺寸快捷 (含 4K 16:9)
        ui.label(T("dlg_quick_size")).classes("text-xs opacity-50 mt-2")
        with ui.row().classes("gap-1 flex-wrap"):
            for w, h, label in [
                (1920, 1080, "4K 16:9"),
                (1280, 720, "HD 16:9"),
                (1024, 1024, "1:1 HD"),
                (1024, 768, "4:3"),
                (768, 1024, "3:4"),
                (512, 512, "1:1"),
                (512, 768, "2:3"),
                (768, 512, "3:2"),
            ]:
                ui.button(
                    f"{label} ({w}×{h})",
                    on_click=lambda wi=w, hi=h: (
                        width_input.set_value(wi), height_input.set_value(hi)
                    ),
                ).props("outline no-caps size=xs color=grey-6")

        with ui.row().classes("w-full justify-end gap-2 mt-3"):
            ui.button(T("btn_cancel"), on_click=dlg.close).props("flat no-caps")
            ui.button(
                T("btn_save_settings"),
                on_click=lambda: save_api_settings(
                    dlg, api_url.value, api_key.value,
                    int(width_input.value or 1920), int(height_input.value or 1080),
                    int(steps_input.value or 28), float(cfg_input.value or 7.0),
                    sampler_input.value,
                    int(seed_input.value if seed_input.value is not None else -1),
                ),
            ).props("no-caps color=purple-8")
    dlg.open()


def save_api_settings(dlg, api_url, api_key, width, height, steps, cfg, sampler, seed):
    state.api_settings.update({
        "api_url": api_url,
        "api_key": api_key,
        "width": width,
        "height": height,
        "steps": steps,
        "cfg_scale": cfg,
        "sampler": sampler,
        "seed": seed,
    })
    state.save_settings()
    dlg.close()
    build_workbench.refresh()
    ui.notify(state.t("notify_settings_saved"), type="positive", position="bottom-right")


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
