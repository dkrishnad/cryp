@echo off
echo Fixing duplicate callback outputs by adding allow_duplicate=True...

cd "c:\Users\Hari\Desktop\Crypto bot"

REM Fix the main auto trading stats callback
powershell -Command "(Get-Content 'dashboard\callbacks.py') -replace '    prevent_initial_call=False\)', '    prevent_initial_call=False,\n    allow_duplicate=True\)' | Set-Content 'dashboard\callbacks.py'"

REM Fix virtual balance callbacks
powershell -Command "(Get-Content 'dashboard\callbacks.py') -replace '    \[Input\(''live-price-interval'', ''n_intervals''\)\]\)', '    [Input(''live-price-interval'', ''n_intervals'')],\n    allow_duplicate=True\)' | Set-Content 'dashboard\callbacks.py'"

echo Done! Duplicate callback outputs should now be fixed.
pause
