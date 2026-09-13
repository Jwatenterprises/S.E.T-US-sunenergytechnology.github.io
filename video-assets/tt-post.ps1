Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class W6 {
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")] public static extern void mouse_event(int dwFlags, int dx, int dy, int cButtons, int dwExtraInfo);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    public static void Click(int x, int y) {
        SetCursorPos(x, y);
        System.Threading.Thread.Sleep(200);
        mouse_event(0x0002, 0, 0, 0, 0);
        System.Threading.Thread.Sleep(50);
        mouse_event(0x0004, 0, 0, 0, 0);
    }
    public static void Scroll(int clicks) {
        mouse_event(0x0800, 0, 0, clicks * 120, 0);
    }
}
'@

function Screenshot($name) {
    $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bmp = [System.Drawing.Bitmap]::new($screen.Width, $screen.Height)
    $gfx = [System.Drawing.Graphics]::FromImage($bmp)
    $gfx.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
    $path = "$HOME\Documents\SunEnergyTechnology\video-assets\$name.png"
    $bmp.Save($path)
    $gfx.Dispose(); $bmp.Dispose()
}

$caption = @"
Living in an apartment? You can't put panels on the roof — but you CAN own a solar generator.

BLUETTI AC200L: 2,048Wh, fits under your desk, charges from a balcony panel or wall outlet.

No gas. No fumes. No landlord permission.

Under `$2,000 for apartment-proof backup power

Link in bio — find your perfect generator in 5 minutes

#solargenerator #apartmentliving #BLUETTI #AC200L #portablepower #blackout #emergencyprep #renterlife #solarpanel #offgrid #prepper #sustainability
"@

# Bring Chrome forward
$chrome = Get-Process | Where-Object { $_.MainWindowTitle -like "*TikTok*" } | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
[W6]::ShowWindow($chrome.MainWindowHandle, 3) | Out-Null
[W6]::SetForegroundWindow($chrome.MainWindowHandle) | Out-Null
Start-Sleep -Seconds 1

# Step 1: Click "Turn on" for content checks (red button at ~900, 517)
[W6]::Click(900, 517)
Start-Sleep -Seconds 2
Write-Host "Step 1: Content checks enabled"

# Step 2: Click "Got it" for editing features (at ~1007, 605)
[W6]::Click(1007, 605)
Start-Sleep -Seconds 2
Write-Host "Step 2: Editing notification dismissed"

# Dismiss Restore pages X
[W6]::Click(1441, 84)
Start-Sleep -Seconds 1

Screenshot "tt-post-step2"

# Step 3: Scroll to top to find caption field
[W6]::SetCursorPos(600, 400)
Start-Sleep -Milliseconds 300
# Scroll up
[W6]::Scroll(10)
Start-Sleep -Seconds 1
[W6]::Scroll(10)
Start-Sleep -Seconds 1
[W6]::Scroll(10)
Start-Sleep -Seconds 2

Screenshot "tt-post-step3-top"
Write-Host "Step 3: Scrolled to top"

# Step 4: Find and click the caption/description field
# The caption area is typically a contenteditable div near the top
# Let me click in the area where the caption usually is (below the title area)
# On TikTok creator upload, the caption is the first editable area
[W6]::Click(400, 300)
Start-Sleep -Seconds 1

# Try Ctrl+A to select any existing text, then type the caption
[System.Windows.Forms.SendKeys]::SendWait("^a")
Start-Sleep -Milliseconds 300

# Use clipboard to paste the caption
[System.Windows.Forms.Clipboard]::SetText($caption)
Start-Sleep -Milliseconds 300
[System.Windows.Forms.SendKeys]::SendWait("^v")
Start-Sleep -Seconds 2

Screenshot "tt-post-step4-caption"
Write-Host "Step 4: Caption pasted"

# Step 5: Scroll down to find and click Post button
[W6]::SetCursorPos(600, 400)
Start-Sleep -Milliseconds 300
[W6]::Scroll(-10)
Start-Sleep -Seconds 1
[W6]::Scroll(-10)
Start-Sleep -Seconds 2

Screenshot "tt-post-step5-postbtn"
Write-Host "Step 5: Looking for Post button"

Write-Host "DONE — check screenshots for state"
