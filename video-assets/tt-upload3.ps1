Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class W5 {
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

# Step 0: Dismiss the Chrome Gemini overlay by clicking elsewhere first
$chrome = Get-Process | Where-Object { $_.MainWindowTitle -like "*TikTok*" } | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
[W5]::ShowWindow($chrome.MainWindowHandle, 3) | Out-Null
[W5]::SetForegroundWindow($chrome.MainWindowHandle) | Out-Null
Start-Sleep -Seconds 1

# Close Gemini popup by pressing Escape
[System.Windows.Forms.SendKeys]::SendWait("{ESC}")
Start-Sleep -Seconds 1

# Dismiss the Restore pages bar
[W5]::Click(1441, 84)
Start-Sleep -Seconds 1

# Step 1: Click Select video
[W5]::Click(725, 424)
Start-Sleep -Seconds 3
Write-Host "Step 1: Clicked Select video"
Screenshot "tt5-dialog-open"

# Step 2: Navigate to the exports folder using the address bar
# Alt+D focuses the address bar in file dialog
[System.Windows.Forms.SendKeys]::SendWait("%d")
Start-Sleep -Milliseconds 500

# Type the folder path (no file)
$folderPath = "C:\Users\Milli\Documents\SunEnergyTechnology\video-assets\exports"
[System.Windows.Forms.Clipboard]::SetText($folderPath)
Start-Sleep -Milliseconds 200
[System.Windows.Forms.SendKeys]::SendWait("^a")
Start-Sleep -Milliseconds 100
[System.Windows.Forms.SendKeys]::SendWait("^v")
Start-Sleep -Milliseconds 500
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Start-Sleep -Seconds 3
Write-Host "Step 2: Navigated to exports folder"
Screenshot "tt5-in-folder"

# Step 3: The video file should now be visible. Click on it.
# In a file dialog listing, the first/only mp4 should be video3-apartment-solar.mp4
# Use Alt+N to focus filename, type the name
[System.Windows.Forms.SendKeys]::SendWait("%n")
Start-Sleep -Milliseconds 300
[System.Windows.Forms.SendKeys]::SendWait("^a")
Start-Sleep -Milliseconds 100
# Type just the filename (no path needed since we navigated to the folder)
[System.Windows.Forms.Clipboard]::SetText("video3-apartment-solar.mp4")
Start-Sleep -Milliseconds 200
[System.Windows.Forms.SendKeys]::SendWait("^v")
Start-Sleep -Seconds 1
Write-Host "Step 3: Filename entered"
Screenshot "tt5-filename"

# Step 4: Click Open / Press Enter
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Start-Sleep -Seconds 10
Write-Host "Step 4: File submitted"
Screenshot "tt5-uploading"

# Wait for upload to process
Start-Sleep -Seconds 15
Screenshot "tt5-ready"
Write-Host "Step 5: Upload should be processing"

Write-Host "DONE"
