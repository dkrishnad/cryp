# FILES TO MOVE TO BIN - NO FUNCTIONALITY LOSS

BACKEND FILES TO MOVE:

- working_main.py (minimal 192-line version, superseded by comprehensive main.py)
- main_backup.py (duplicate of main_original.py)
- main_original.py (backup version)
- minimal_main.py (testing version)
- minimal_server.py (testing version)
- endpointsrealtest.py (135KB testing file)
- gradual_main.py (gradual loading test)
- auto_trader.py (superseded by advanced_auto_trading.py)
- auto_trader_backend.py (superseded)
- launch_bot.py (superseded by main.py)
- quick_backend_test.py
- quick_test.py
- test_main.py
- test_server.py
- test_startup.py
- test_step_imports.py
- fix_unicode.py (one-time fix)

DASHBOARD FILES TO MOVE:

- callbacks_clean.py (incomplete 35-callback version vs full 113-callback version)
- callbacks_backup.py
- callbacks_backup_before_duplicate_fix.py
- callbacks_backup_before_final_clean.py
- callbacks_fixed.py
- callbacks_minimal.py
- callbacks_simple.py
- callbacks_truly_clean.py
- refactoredcallback.py
- refactored*callbacks*\*.py (all versions)
- app_clean.py
- app_fixed.py
- layout_backup.py
- layout_fixed.py
- dashboard_utils.py (superseded by utils.py)
- All test\_\*.py files
- All debug\_\*.py files
- All simple\_\*.py files
- All minimal\_\*.py files
- All start\_\*.py files (except core startup)
- All fix\_\*.py files (one-time fixes)
- All diagnose\_\*.py files
- comprehensive\_\*.py files
- check_missing_endpoints.py
- final_fix_callbacks.py
- find_duplicates.py
- fix_duplicate_callbacks_final.py
- fix_line_5381.py
- fix_syntax_errors.py

MOST ADVANCED FILES (KEEP):
Backend: main.py (4,113 lines, 138 endpoints)
Dashboard: callbacks.py (5,209 lines, 113 callbacks)
Layout: layout.py (comprehensive)
Core: All production modules in backendtest/ and dashboardtest/

REASONING:

- main.py has 138 endpoints vs working_main.py's 10 endpoints
- callbacks.py has 113 callbacks vs callbacks_clean.py's 35 callbacks
- All backup/test/debug files are superseded by production versions
- No functionality will be lost - only removing duplicates and development artifacts
