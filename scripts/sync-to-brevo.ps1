param(
    [Parameter(Mandatory=$true)][string]$Email,
    [string]$Name = ""
)

$envFile = "$HOME\.kiyomimax\.env"
$apiKey = (Get-Content $envFile | Where-Object { $_ -match "^BREVO_API_KEY=" }) -replace "^BREVO_API_KEY=", ""

if (-not $apiKey) { Write-Error "BREVO_API_KEY not found in $envFile"; exit 1 }

$today = (Get-Date).ToString("yyyy-MM-dd")

$body = @{
    email = $Email
    listIds = @(5)
    updateEnabled = $true
    attributes = @{
        SOLAR_SEQUENCE_STEP = 0
        SOLAR_SUBSCRIBE_DATE = $today
    }
}
if ($Name) { $body.attributes.FIRSTNAME = $Name }

$resp = Invoke-RestMethod -Uri "https://api.brevo.com/v3/contacts" -Method Post `
    -Headers @{ "api-key" = $apiKey; "Accept" = "application/json" } `
    -ContentType "application/json" -Body ($body | ConvertTo-Json -Depth 3)

Write-Host "Added $Email to Brevo list 5 (S.E.T. Solar Welcome Sequence) with subscribe date $today"
