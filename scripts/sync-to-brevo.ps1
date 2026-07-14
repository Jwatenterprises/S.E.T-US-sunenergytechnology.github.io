param(
    [Parameter(Mandatory=$true)][string]$Email,
    [string]$Name = ""
)

$envFile = "$HOME\.kiyomimax\.env"
$apiKey = (Get-Content $envFile | Where-Object { $_ -match "^BREVO_API_KEY=" }) -replace "^BREVO_API_KEY=", ""

if (-not $apiKey) { Write-Error "BREVO_API_KEY not found in $envFile"; exit 1 }

$body = @{
    email = $Email
    listIds = @(4)
    updateEnabled = $true
}
if ($Name) { $body.attributes = @{ FIRSTNAME = $Name } }

$resp = Invoke-RestMethod -Uri "https://api.brevo.com/v3/contacts" -Method Post `
    -Headers @{ "api-key" = $apiKey; "Accept" = "application/json" } `
    -ContentType "application/json" -Body ($body | ConvertTo-Json -Depth 3)

Write-Host "Added $Email to Brevo list 4 (S.E.T. Solar US Nurture)"
