"""
PromptMaster Pro — 應用狀態管理
"""
import json
import os
import random
from pathlib import Path
from typing import Optional

from app.default_data import (
    DEFAULT_CATEGORIES,
    DEFAULT_LORAS,
    DEFAULT_NEGATIVE_PROMPTS,
    DEFAULT_PRESETS,
)

DATA_DIR = Path(__file__).parent.parent / "data"


class AppState:
    """全域狀態容器"""

    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)

        # 詞庫
        self.categories: list[dict] = self._load_categories()
        self.loras: list[dict] = self._load_loras()

        # 工作台
        self.selected_tags: list[dict] = []  # [{text, weight, category, locked}]
        self.selected_loras: list[dict] = []  # [{name, trigger, weight}]
        self.negative_prompts: list[str] = list(DEFAULT_NEGATIVE_PROMPTS)
        self.negative_enabled: bool = True

        # 預設組
        self.presets: list[dict] = self._load_presets()

        # 搜尋
        self.search_query: str = ""
        self.active_category: str = self.categories[0]["id"] if self.categories else ""

        # UI
        self.dark_mode: bool = True

    # ---------- 資料載入 ----------

    def _load_categories(self) -> list[dict]:
        path = DATA_DIR / "tags.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return [dict(c) for c in DEFAULT_CATEGORIES]

    def _load_loras(self) -> list[dict]:
        path = DATA_DIR / "loras.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return [dict(l) for l in DEFAULT_LORAS]

    def _load_presets(self) -> list[dict]:
        path = DATA_DIR / "presets.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return [dict(p) for p in DEFAULT_PRESETS]

    # ---------- 持久化 ----------

    def save_categories(self):
        (DATA_DIR / "tags.json").write_text(
            json.dumps(self.categories, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def save_loras(self):
        (DATA_DIR / "loras.json").write_text(
            json.dumps(self.loras, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def save_presets(self):
        (DATA_DIR / "presets.json").write_text(
            json.dumps(self.presets, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    # ---------- 標籤操作 ----------

    def add_tag(self, text: str, category: str, weight: float = 1.0):
        """添加標籤到工作台"""
        if any(t["text"] == text for t in self.selected_tags):
            return False
        self.selected_tags.append({
            "text": text,
            "weight": weight,
            "category": category,
            "locked": False,
        })
        return True

    def remove_tag(self, text: str):
        """從工作台移除標籤"""
        self.selected_tags = [t for t in self.selected_tags if t["text"] != text]

    def toggle_tag(self, text: str, category: str):
        """切換標籤選中狀態"""
        if any(t["text"] == text for t in self.selected_tags):
            self.remove_tag(text)
            return False
        else:
            self.add_tag(text, category)
            return True

    def is_tag_selected(self, text: str) -> bool:
        return any(t["text"] == text for t in self.selected_tags)

    def set_tag_weight(self, text: str, weight: float):
        for t in self.selected_tags:
            if t["text"] == text:
                t["weight"] = round(weight, 1)
                break

    def toggle_tag_lock(self, text: str):
        for t in self.selected_tags:
            if t["text"] == text:
                t["locked"] = not t["locked"]
                break

    def clear_all_tags(self):
        self.selected_tags.clear()
        self.selected_loras.clear()

    # ---------- LoRA 操作 ----------

    def add_lora(self, lora: dict):
        if any(l["name"] == lora["name"] for l in self.selected_loras):
            return False
        self.selected_loras.append({
            "name": lora["name"],
            "trigger": lora["trigger"],
            "weight": lora.get("weight", 0.7),
        })
        return True

    def remove_lora(self, name: str):
        self.selected_loras = [l for l in self.selected_loras if l["name"] != name]

    def toggle_lora(self, lora: dict):
        if any(l["name"] == lora["name"] for l in self.selected_loras):
            self.remove_lora(lora["name"])
            return False
        else:
            self.add_lora(lora)
            return True

    def is_lora_selected(self, name: str) -> bool:
        return any(l["name"] == name for l in self.selected_loras)

    def set_lora_weight(self, name: str, weight: float):
        for l in self.selected_loras:
            if l["name"] == name:
                l["weight"] = round(weight, 1)
                break

    # ---------- 提示詞生成 ----------

    def generate_positive_prompt(self) -> str:
        parts = []
        for tag in self.selected_tags:
            w = tag["weight"]
            if abs(w - 1.0) < 0.05:
                parts.append(tag["text"])
            else:
                parts.append(f"({tag['text']}:{w:.1f})")
        for lora in self.selected_loras:
            parts.append(f"<lora:{lora['name']}:{lora['weight']:.1f}>")
        return ", ".join(parts)

    def generate_negative_prompt(self) -> str:
        if not self.negative_enabled:
            return ""
        return ", ".join(self.negative_prompts)

    # ---------- 預設組操作 ----------

    def save_as_preset(self, name: str, description: str = ""):
        preset = {
            "name": name,
            "description": description,
            "tags": [dict(t) for t in self.selected_tags],
            "loras": [dict(l) for l in self.selected_loras],
        }
        # 如果已存在同名，覆蓋
        self.presets = [p for p in self.presets if p["name"] != name]
        self.presets.append(preset)
        self.save_presets()

    def load_preset(self, name: str):
        for p in self.presets:
            if p["name"] == name:
                self.selected_tags = [dict(t) for t in p.get("tags", [])]
                # 確保每個 tag 都有 locked 欄位
                for t in self.selected_tags:
                    t.setdefault("locked", False)
                self.selected_loras = [dict(l) for l in p.get("loras", [])]
                # 補充 trigger 資訊
                for sl in self.selected_loras:
                    if "trigger" not in sl:
                        for lora in self.loras:
                            if lora["name"] == sl["name"]:
                                sl["trigger"] = lora["trigger"]
                                break
                return True
        return False

    def delete_preset(self, name: str):
        self.presets = [p for p in self.presets if p["name"] != name]
        self.save_presets()

    # ---------- 隨機擾動 ----------

    def randomize(self):
        """隨機替換未鎖定的標籤"""
        for i, tag in enumerate(self.selected_tags):
            if tag.get("locked"):
                continue
            cat_id = tag.get("category", "")
            cat = next((c for c in self.categories if c["id"] == cat_id), None)
            if cat and cat["tags"]:
                new_tag = random.choice(cat["tags"])
                self.selected_tags[i]["text"] = new_tag

    # ---------- 匯出 / 匯入 ----------

    def export_all(self) -> dict:
        return {
            "categories": self.categories,
            "loras": self.loras,
            "presets": self.presets,
        }

    def import_data(self, data: dict, merge: bool = True):
        if "categories" in data:
            if merge:
                existing_ids = {c["id"] for c in self.categories}
                for c in data["categories"]:
                    if c["id"] not in existing_ids:
                        self.categories.append(c)
            else:
                self.categories = data["categories"]
            self.save_categories()

        if "loras" in data:
            if merge:
                existing_names = {l["name"] for l in self.loras}
                for l in data["loras"]:
                    if l["name"] not in existing_names:
                        self.loras.append(l)
            else:
                self.loras = data["loras"]
            self.save_loras()

        if "presets" in data:
            if merge:
                existing_names = {p["name"] for p in self.presets}
                for p in data["presets"]:
                    if p["name"] not in existing_names:
                        self.presets.append(p)
            else:
                self.presets = data["presets"]
            self.save_presets()
