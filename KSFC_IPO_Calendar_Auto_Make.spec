# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['KSFC_중복청약_IPO_캘린더.py'],
    pathex=[],
    binaries=[],
    datas=[('welcome_app.py', '.'), ('ipo_search.py', '.'), ('calendarUtils.py', '.')],
    hiddenimports=['streamlit.runtime.scriptrunner.magic_funcs', 'streamlit.web.cli', 'streamlit.web.bootstrap'],
    hookspath=['./hooks'],
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
    name='KSFC_IPO_Calendar_Auto_Make',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
