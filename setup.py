from cx_Freeze import setup, Executable
from setuptools import setup, find_packages
# 옵션 설정
options = {
    "build_exe": {
        "packages": find_packages(),  # 내부 패키지 자동 탐색
        "includes": [
            "customtkinter",
            "tkinter",
            "PIL",
            "pickle",
            "pandas",
            "numpy",
            "datetime",
            "serial",
            "time",
            "os",
            "sys",
            "CTkMessagebox"
        ],
        "optimize": 2
    }
}

# 실행 파일 설정
executables = [
    Executable(
        script="main.py",
        base="Win32GUI",  # GUI 앱 설정 (콘솔 창 안 뜨게)
        target_name="MyApp.exe",
    )
]

# setup() 실행
setup(
    name="measurement_project",
    version="1.0",              # 버전 정보
    description="test_without_measuring",   # 설명
    author="SeongJin Wi",         # 제작자 이름
    author_email="wisj98@naver.com",  # 제작자 이메일
    options=options,                 # 빌드 옵션 (추가 설정 가능)
    executables=executables,             # 실행할 파일 (Executable 객체 리스트)
)
