#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepare M9A assets, OCR models, and configuration for Android packaging.
Ensures zero pollution of system /tmp (all caches/temps in project root).
"""

import os
import shutil
import sys
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TMP_DIR = PROJECT_ROOT / ".tmp"
M9A_ROOT = PROJECT_ROOT / "upstream" / "m9a"
OCR_TARGET_DIR = M9A_ROOT / "resource" / "base" / "model" / "ocr"

# Ensure temp directory stays strictly inside project
TMP_DIR.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"] = str(TMP_DIR)
os.environ["TEMP"] = str(TMP_DIR)
os.environ["TMP"] = str(TMP_DIR)

OCR_BASE_URL = "https://raw.githubusercontent.com/MaaXYZ/MaaCommonAssets/main/OCR/ppocr_v6/small"
OCR_FILES = ["det.onnx", "rec.onnx", "keys.txt"]


def log(msg: str):
    print(f"[M9A-Prep] {msg}", flush=True)


def ensure_m9a_submodule():
    if not (M9A_ROOT / "interface.json").is_file():
        log("M9A submodule not detected, initializing...")
        import subprocess
        subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive", "upstream/m9a"],
            cwd=PROJECT_ROOT,
            check=True,
        )
    log(f"M9A found at {M9A_ROOT}")


def ensure_ocr_models():
    OCR_TARGET_DIR.mkdir(parents=True, exist_ok=True)
    all_exist = all((OCR_TARGET_DIR / f).is_file() for f in OCR_FILES)
    if all_exist:
        log("OCR models already present.")
        return

    # Try local submodule first
    local_ocr = M9A_ROOT / "MaaCommonAssets" / "OCR" / "ppocr_v6" / "small"
    if local_ocr.exists() and all((local_ocr / f).is_file() for f in OCR_FILES):
        log(f"Copying OCR models from local submodule: {local_ocr}")
        for f in OCR_FILES:
            shutil.copy2(local_ocr / f, OCR_TARGET_DIR / f)
        log("OCR models copied successfully.")
        return

    # Download from MaaCommonAssets raw
    log("Downloading OCR models from MaaCommonAssets...")
    for f in OCR_FILES:
        dest = OCR_TARGET_DIR / f
        if dest.is_file() and dest.stat().st_size > 0:
            log(f"  {f} already downloaded.")
            continue
        url = f"{OCR_BASE_URL}/{f}"
        log(f"  Downloading {f} from {url}...")
        req = urllib.request.Request(url, headers={"User-Agent": "M9A-Android-Prep"})
        with urllib.request.urlopen(req, timeout=120) as resp, open(dest, "wb") as out:
            shutil.copyfileobj(resp, out)
        log(f"  Saved {f} ({dest.stat().st_size / (1024 * 1024):.2f} MB)")
    log("All OCR models prepared.")


def ensure_icon():
    dest_png = PROJECT_ROOT / "logo.png"
    if dest_png.is_file():
        log("App icon logo.png already exists.")
        return

    src_ico = M9A_ROOT / "logo.ico"
    if src_ico.is_file():
        log("Converting logo.ico to logo.png...")
        try:
            from PIL import Image
            img = Image.open(src_ico)
            img.save(dest_png, format="PNG")
            log(f"Converted logo.png saved at {dest_png}")
            return
        except Exception as e:
            log(f"Failed to convert via PIL: {e}")

    log("Warning: logo.png not found, default app icon will be used.")


def ensure_local_properties():
    props_file = PROJECT_ROOT / "local.properties"
    content = [
        "# Auto-generated configuration for M9A Android packaging",
        "pi.profile=pi-profile.yaml",
        "build.debugAbi=arm64-v8a",
        "build.releaseAbi=arm64-v8a",
        "",
    ]
    if not props_file.is_file():
        props_file.write_text("\n".join(content), encoding="utf-8")
        log(f"Created local.properties pointing to pi-profile.yaml")
    else:
        existing = props_file.read_text(encoding="utf-8")
        if "pi.profile=" not in existing:
            props_file.write_text(existing.rstrip() + "\npi.profile=pi-profile.yaml\n", encoding="utf-8")
            log("Added pi.profile to local.properties")


def fix_m9a_startup_packages():
    """
    Remove hardcoded invalid activity suffixes from M9A pipeline files.
    'com.shenlan.m.reverse1999/com.ssgame.mobile.gamesdk.frame.AppStartUpActivity' -> 'com.shenlan.m.reverse1999'
    """
    if not M9A_ROOT.exists():
        return
    bad_spec = "/com.ssgame.mobile.gamesdk.frame.AppStartUpActivity"
    for json_file in M9A_ROOT.rglob("*.json"):
        try:
            text = json_file.read_text(encoding="utf-8")
            if bad_spec in text:
                new_text = text.replace(bad_spec, "")
                json_file.write_text(new_text, encoding="utf-8")
                log(f"Fixed launch package in {json_file.relative_to(PROJECT_ROOT)}")
        except Exception as e:
            log(f"Warning: could not process {json_file}: {e}")


def customize_m9a_metadata():
    """
    定制 M9A 元数据：
    1. CONTACT 仅保留邮箱 qiisme1021@icloud.com
    2. interface.json 仓库地址换为本项目 qi-1021/M9A-Meow，描述设置为“这是对于M9A手机端的一种实现”
    """
    if not M9A_ROOT.exists():
        return
    
    # 1. CONTACT 文件定制
    contact_file = M9A_ROOT / "CONTACT"
    contact_content = "| 联系方式 | 地址 |\n| :---: | :---: |\n| 邮箱 | [qiisme1021@icloud.com](mailto:qiisme1021@icloud.com) |\n"
    try:
        contact_file.write_text(contact_content, encoding="utf-8")
        log(f"Customized {contact_file.relative_to(PROJECT_ROOT)}")
    except Exception as e:
        log(f"Warning: could not write CONTACT: {e}")

    # 2. interface.json 元数据定制
    interface_file = M9A_ROOT / "interface.json"
    if interface_file.is_file():
        try:
            import json
            data = json.loads(interface_file.read_text(encoding="utf-8"))
            data["github"] = "https://github.com/qi-1021/M9A-Meow"
            data["description"] = "这是对于M9A手机端的一种实现，基于 MaaFramework 与 M9A 开源项目。"
            interface_file.write_text(json.dumps(data, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
            log(f"Customized metadata in {interface_file.relative_to(PROJECT_ROOT)}")
        except Exception as e:
            log(f"Warning: could not customize interface.json: {e}")


def main():
    log("Starting M9A Android preparation...")
    ensure_m9a_submodule()
    ensure_ocr_models()
    ensure_icon()
    ensure_local_properties()
    fix_m9a_startup_packages()
    customize_m9a_metadata()
    log("Preparation complete!")


if __name__ == "__main__":
    main()

