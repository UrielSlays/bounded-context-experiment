$wd = '<repo>-build'
Set-Location $wd
cmd /c "codex exec -m gpt-5.6-sol -c service_tier=default -c model_reasoning_effort=xhigh < MBCX-01-BUILD-SEAT3-CODEX-EXEC-PROMPT-r2.txt > MBCX-01-BUILD-SEAT3-CODEX-EXEC-r2.log 2>&1"
Set-Content -Path (Join-Path $wd 'MBCX-01-BUILD-SEAT3-CODEX-EXEC-r2.complete.json') -Value ('{"exit":' + $LASTEXITCODE + ',"finished_utc":"' + (Get-Date).ToUniversalTime().ToString('o') + '"}')
