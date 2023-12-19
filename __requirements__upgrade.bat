echo version 0.0.2

echo off
cls || clear

echo ====================================================
echo ====================================================
echo ====================================================
echo =============1[UPDATE PIP]==========================
pip install --upgrade pip || pip3 install --upgrade pip || python -m pip install --upgrade pip || python3 -m pip install --upgrade pip || echo [ERROR] PIP UPDATE
echo _
echo _
echo _
echo _
echo _
echo _
echo _

echo =====================================================
echo =====================================================
echo =====================================================
echo =============2[UPDATE PIP REQUIREMENTS]==============
pip install --upgrade -r requirements.txt || pip3 install --upgrade -r requirements.txt || python -m pip install --upgrade -r requirements.txt || python3 -m pip install --upgrade -r requirements.txt || echo [ERROR] REQUIREMENTS UPDATE
echo _
echo _
echo _
echo _
echo _
echo _
echo _

echo =====================================================
echo =====================================================
echo =====================================================
echo =============3[UPDATE PIP REQUIREMENTS__AST]=========
pip install --upgrade -r requirements__AST.txt || pip3 install --upgrade -r requirements__AST.txt || python -m pip install --upgrade -r requirements__AST.txt || python3 -m pip install --upgrade -r requirements__AST.txt || echo [ERROR] REQUIREMENTS__AST UPDATE
echo _
echo _
echo _
echo _
echo _
echo _
echo _

echo =====================================================
echo =====================================================
echo =====================================================
echo =============4[FINISH]===============================
pause
