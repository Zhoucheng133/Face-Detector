# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# 收集 mediapipe 的模型文件
mediapipe_datas = collect_data_files("mediapipe")

# 收集 opencv 数据
cv2_datas = collect_data_files("cv2")

# 收集 hidden imports
hiddenimports = (
    collect_submodules("mediapipe")
    + collect_submodules("cv2")
)

a = Analysis(
    ["app.py"],
    pathex=[str(Path(".").resolve())],
    binaries=[],
    datas=mediapipe_datas + cv2_datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "IPython",
        "notebook",
        "jupyter",
        "pytest",
        "tkinter",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="app",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
)
