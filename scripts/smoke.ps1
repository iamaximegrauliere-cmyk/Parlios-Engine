param(
  [string]$BaseUrl = "http://127.0.0.1:8080",
  [string]$ApiKey = $env:PARLIOS_API_KEY
)

function Assert-True($c,$m){ if(-not $c){ throw $m } }

$health = irm "$BaseUrl/health"
Assert-True ($health.ok -eq $true) "Health failed"

$ready = irm "$BaseUrl/ready"
Assert-True ($ready.ok -eq $true) "Ready failed"

$body = @{ goal = "Smoke test no-auth" } | ConvertTo-Json
$run1 = irm -Method Post -Uri "$BaseUrl/run" -ContentType 'application/json' -Body $body
Assert-True ($run1.ok -eq $true) "Run (no auth) failed"
Assert-True ($run1.output.Length -gt 0) "Run (no auth) empty output"

if ($ApiKey) {
  $Headers = @{ Authorization = "Bearer $ApiKey" }
  $body2 = @{ goal = "Smoke test bearer" } | ConvertTo-Json
  $run2 = irm -Method Post -Uri "$BaseUrl/run" -Headers $Headers -ContentType 'application/json' -Body $body2
  Assert-True ($run2.ok -eq $true) "Run (bearer) failed"
  Assert-True ($run2.output.Length -gt 0) "Run (bearer) empty output"
}
Write-Host "✅ Smoke OK"
