
set ROOT_DIR=%~dp0
cd /d %ROOT_DIR%

set PYTHON=
set PIP=pip
set PYENV_STATUS=2 

rem Python 環境によってセットアップを分岐
if not %PYENV_STATUS%==2 (goto skip_embbedable)

rem システム情報のbitに合わせて embeddable python をダウンロード
if exist %ROOT_DIR%python (goto skip_dl_python)
if %PROCESSOR_ARCHITECTURE%==AMD64 (
    curl -sSL https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-amd64.zip -o %ROOT_DIR%python.zip
) else (
    curl https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-win32.zip --output %ROOT_DIR%python.zip
)

rem embeddable python の zip を解凍
powershell -NoProfile -ExecutionPolicy Unrestricted Expand-Archive -Path %ROOT_DIR%python.zip -DestinationPath python -Force

del python.zip

:skip_dl_python
set PYTHON=%ROOT_DIR%python\python.exe
set PIP=%ROOT_DIR%python\Scripts\pip.exe
if exist %ROOT_DIR%python\python310._pth (%PYTHON% src\setup\activate_pip.py)

:skip_embbedable
if not defined PYTHON (set PYTHON=python)

if not %PYENV_STATUS%==1 (goto skip_venv)
%PYTHON% -m venv venv
call .\venv\scripts\activate.bat

:skip_venv

rem パッケージとモデルのダウンロード
%PYTHON% -m %PIP% --upgrade pip
%PYTHON% src\setup\install_package.py
%PYTHON% src\setup\dl_model.py

if %PYENV_STATUS%==1 (call .\venv\scripts\deactivate.bat)

