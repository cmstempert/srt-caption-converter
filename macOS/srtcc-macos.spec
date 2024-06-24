# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['gui_macos.py'],
    pathex=[],
    binaries=[],
    datas=[("file_handler_macos.py", "."), ("text_processor_macos.py", ".")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CaptionConverter-v0.1.2-M',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(exe,
    name="CaptionConverter.app",
    icon=None,
    bundle_identifier=None)
