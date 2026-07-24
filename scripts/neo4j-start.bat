@echo off
REM ============================================================
REM 华严项目 — Neo4j 本地启动脚本
REM 使用: scripts\neo4j-start.bat [console|install|start|stop|status]
REM ============================================================

setlocal

set NEO4J_HOME=%USERPROFILE%\neo4j-community-5.26.4
set JAVA_HOME=C:\Program Files\Java\jdk-20

REM Verify Java
if not exist "%JAVA_HOME%\bin\java.exe" (
    echo [ERROR] Java not found at %JAVA_HOME%
    exit /b 1
)

REM Verify Neo4j
if not exist "%NEO4J_HOME%\bin\neo4j.bat" (
    echo [ERROR] Neo4j not found at %NEO4J_HOME%
    exit /b 1
)

set PATH=%JAVA_HOME%\bin;%PATH%

set ACTION=%1
if "%ACTION%"=="" set ACTION=console

echo.
echo === 华严 Neo4j 本地实例 ===
echo JAVA_HOME: %JAVA_HOME%
echo NEO4J_HOME: %NEO4J_HOME%
echo Action: %ACTION%
echo.

if "%ACTION%"=="console" (
    echo Starting Neo4j in console mode (Ctrl+C to stop)...
    "%NEO4J_HOME%\bin\neo4j.bat" console
) else if "%ACTION%"=="start" (
    echo Starting Neo4j service...
    "%NEO4J_HOME%\bin\neo4j.bat" start
) else if "%ACTION%"=="stop" (
    echo Stopping Neo4j...
    "%NEO4J_HOME%\bin\neo4j.bat" stop
) else if "%ACTION%"=="status" (
    "%NEO4J_HOME%\bin\neo4j.bat" status
) else if "%ACTION%"=="install" (
    echo Installing Neo4j as Windows service...
    "%NEO4J_HOME%\bin\neo4j.bat" install-service
) else if "%ACTION%"=="set-pass" (
    echo Setting initial password for huayan database...
    "%NEO4J_HOME%\bin\neo4j-admin.bat" dbms set-initial-password huayan2024
) else (
    echo Usage: neo4j-start.bat [console^|install^|start^|stop^|status^|set-pass]
    echo   console  - Run in foreground (recommended for dev)
    echo   install  - Install as Windows service
    echo   start    - Start the service
    echo   stop     - Stop the service
    echo   status   - Check if running
    echo   set-pass - Set initial password to huayan2024
)

endlocal
