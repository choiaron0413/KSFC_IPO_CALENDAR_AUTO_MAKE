# hook-streamlit.py
from PyInstaller.utils.hooks import copy_metadata, get_package_paths
import os

# 1. Streamlit 패키지 메타데이터 복사
datas = copy_metadata("streamlit")

# 2. Streamlit의 'static' 및 'web' 폴더를 찾아 실행 파일에 포함
pkg_base, pkg_dir = get_package_paths("streamlit")

for folder in ['static', 'web']:
    src_path = os.path.join(pkg_dir, folder)
    # destination (대상): 'streamlit/' 폴더 안에 포함
    datas += [(src_path, f'streamlit/{folder}')]

# Streamlit CLI가 내부적으로 사용하는 리소스 파일도 추가
datas += [(os.path.join(pkg_dir, 'py.typed'), 'streamlit')]