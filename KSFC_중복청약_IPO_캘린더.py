import streamlit.web.cli as stcli
import os
import sys

# 해당 스크립트는 Pyinstaller를 통해 파이썬 패키지를 모두 패키징해서 완전한 실행파일로 만들어주기 위해 작성되었습니다.
# PyInstaller가 압축 해제한 경로(sys._MEIPASS)를 참조하여 파일 경로를 얻는 함수
def resource_path(relative_path):
    """ 실행 파일 환경에서 리소스의 절대 경로를 얻습니다. """
    try:
        # PyInstaller에 의해 임시 폴더에 압축이 풀린 경우
        # _MEI 폴더 경로 + 포함된 파일의 상대 경로
        base_path = sys._MEIPASS 
    except Exception:
        # 일반 파이썬 환경에서 실행되는 경우
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    # 📌 이 부분이 실행 파일 내부에 포함시킨 파일 이름과 정확히 일치해야 합니다.
    APP_FILENAME = "welcome_app.py" 
    
    # sys.argv에 Streamlit 실행 명령을 설정합니다.
    sys.argv = [
        "streamlit",
        "run",
        # 📌 resource_path 함수를 통해 _MEI 폴더 내의 정확한 경로를 Streamlit에 전달합니다.
        resource_path(APP_FILENAME), 
        "--global.developmentMode=false",
    ]
    
    sys.exit(stcli.main())