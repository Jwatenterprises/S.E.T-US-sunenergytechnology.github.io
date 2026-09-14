# S.E.T. Solar — Price Drop Alert Sender
# Usage: .\send-price-drop-alert.ps1 -ProductName "EcoFlow DELTA 2 Max" -OldPrice "$2,399" -NewPrice "$1,799" -Savings "$600 (25% off)" -ProductUrl "https://www.awin1.com/cread.php?awinmid=..."
# Sends to Brevo List 7 (Deal Alerts) using Template 43

param(
    [Parameter(Mandatory=$true)][string]$ProductName,
    [Parameter(Mandatory=$true)][string]$OldPrice,
    [Parameter(Mandatory=$true)][string]$NewPrice,
    [Parameter(Mandatory=$true)][string]$Savings,
    [Parameter(Mandatory=$true)][string]$ProductUrl,
    [string]$ExtraNote = "",
    [string]$SubjectOverride = ""
)

# Load API key from environment or .env file
$apiKey = $env:BREVO_API_KEY
if (-not $apiKey) {
    $envFile = Join-Path $PSScriptRoot "..\..\..\.kiyomimax\.env"
    if (Test-Path $envFile) {
        Get-Content $envFile | ForEach-Object {
            if ($_ -match "^BREVO_API_KEY=(.+)$") { $apiKey = $Matches[1].Trim('"').Trim("'") }
        }
    }
}
if (-not $apiKey) {
    Write-Host "ERROR: Set BREVO_API_KEY environment variable or add it to ~/.kiyomimax/.env" -ForegroundColor Red
    exit 1
}
$listId = 7   # S.E.T. Solar Deal Alerts
$templateId = 43

$subject = if ($SubjectOverride) { $SubjectOverride } else { "Price Drop: $ProductName just dropped to $NewPrice" }

$body = @{
    sender = @{ name = "S.E.T. Solar"; email = "biz@sunenergytechnology.net" }
    name = "Price Drop - $ProductName - $(Get-Date -Format 'yyyy-MM-dd')"
    subject = $subject
    templateId = $templateId
    recipients = @{ listIds = @($listId) }
    params = @{
        PRODUCT_NAME = $ProductName
        OLD_PRICE = $OldPrice
        NEW_PRICE = $NewPrice
        SAVINGS = $Savings
        PRODUCT_URL = $ProductUrl
        EXTRA_NOTE = $ExtraNote
    }
} | ConvertTo-Json -Depth 4

$headers = @{
    "api-key" = $apiKey
    "Content-Type" = "application/json"
}

Write-Host "`n=== S.E.T. Solar Price Drop Alert ===" -ForegroundColor Yellow
Write-Host "Product: $ProductName"
Write-Host "Price:   $OldPrice -> $NewPrice ($Savings)"
Write-Host "Link:    $ProductUrl"
Write-Host "List:    Deal Alerts (ID $listId)"
Write-Host ""

# Create campaign
$response = Invoke-RestMethod -Uri "https://api.brevo.com/v3/emailCampaigns" -Method Post -Headers $headers -Body $body
$campaignId = $response.id
Write-Host "Campaign created: #$campaignId" -ForegroundColor Green

# Send immediately
$sendResponse = Invoke-RestMethod -Uri "https://api.brevo.com/v3/emailCampaigns/$campaignId/sendNow" -Method Post -Headers $headers
Write-Host "SENT! Campaign #$campaignId delivered to Deal Alerts list." -ForegroundColor Green
Write-Host ""
