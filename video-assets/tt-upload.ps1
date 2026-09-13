Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class WA {
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")] public static extern void mouse_event(int dwFlags, int dx, int dy, int cButtons, int dwExtraInfo);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
    public static void Click(int x, int y) {
        SetCursorPos(x, y);
        System.Threading.Thread.Sleep(150);
        mouse_event(0x0002, 0, 0, 0, 0);
        mouse_event(0x0004, 0, 0, 0, 0);
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
    Write-Host "Screenshot: $name"
}

function ForegroundTitle() {
    $h = [WA]::GetForegroundWindow()
    $sb = [System.Text.StringBuilder]::new(256)
    [WA]::GetWindowText($h, $sb, 256) | Out-Null
    return $sb.ToString()
}

$VIDEO = "C:\Users\Milli\OneDrive - Hillsborough County Public Schools\SET-Solar-Video3\video3-apartment-solar.mp4"

# Step 1: Bring Chrome to foreground
$chrome = Get-Process | Where-Object { $_.MainWindowTitle -like "*TikTok*" } | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
if (-not $chrome) {
    Write-Host "ERROR: Chrome with TikTok not found"
    exit 1
}
[WA]::ShowWindow($chrome.MainWindowHandle, 3) | Out-Null
[WA]::SetForegroundWindow($chrome.MainWindowHandle) | Out-Null
Start-Sleep -Seconds 2
Write-Host "Step 1: Chrome activated — $(ForegroundTitle)"

# Step 2: Dismiss restore dialog (X button top right)
[WA]::Click(1441, 84)
Start-Sleep -Seconds 1
Write-Host "Step 2: Dismissed restore dialog"

# Step 3: Click "Select video" button
[WA]::Click(725, 424)
Start-Sleep -Seconds 3
Write-Host "Step 3: Clicked Select video — $(ForegroundTitle)"
Screenshot "tt-step3"

# Step 4: Type file path in the file dialog
# The file dialog should now be open. Type the path into the filename field.
[System.Windows.Forms.SendKeys]::SendWait("^a")
Start-Sleep -Milliseconds 300
$escaped = $VIDEO -replace '[+^%~(){}]', '{$0}'
[System.Windows.Forms.SendKeys]::SendWait($escaped)
Start-Sleep -Seconds 1
Write-Host "Step 4: Typed file path"
Screenshot "tt-step4"

# Step 5: Press Enter to confirm file selection
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Start-Sleep -Seconds 8
Write-Host "Step 5: File selected, waiting for upload..."
Screenshot "tt-step5-uploading"

# Wait more for video processing
Start-Sleep -Seconds 10
Screenshot "tt-step5-processing"
Write-Host "Step 5b: Upload processing..."

Write-Host "DONE — Check screenshots for current state"
