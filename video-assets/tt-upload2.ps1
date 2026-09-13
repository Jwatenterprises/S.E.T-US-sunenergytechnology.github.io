Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
using System.Text;
public class W2 {
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")] public static extern void mouse_event(int dwFlags, int dx, int dy, int cButtons, int dwExtraInfo);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
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

# Bring Chrome to foreground
$chrome = Get-Process | Where-Object { $_.MainWindowTitle -like "*TikTok*" } | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
[W2]::ShowWindow($chrome.MainWindowHandle, 3) | Out-Null
[W2]::SetForegroundWindow($chrome.MainWindowHandle) | Out-Null
Start-Sleep -Seconds 2

# Press Escape to close any open dialog
[System.Windows.Forms.SendKeys]::SendWait("{ESC}")
Start-Sleep -Seconds 2

Screenshot "tt2-step0"
Write-Host "Step 0: Chrome active, dialog closed"

# Click Select video button (centered on the red button)
[W2]::Click(725, 424)
Start-Sleep -Seconds 3

Screenshot "tt2-step1-dialog"
Write-Host "Step 1: File dialog should be open"

# Now use Alt+D to focus the address bar in the file dialog
[System.Windows.Forms.SendKeys]::SendWait("%d")
Start-Sleep -Milliseconds 500

# Type the Desktop path
[System.Windows.Forms.SendKeys]::SendWait("Desktop{ENTER}")
Start-Sleep -Seconds 2

Screenshot "tt2-step2-desktop"
Write-Host "Step 2: Navigated to Desktop"

# Now the file should be visible. Click in the File name field and type just the filename
# File name field — let's use Alt+N shortcut to focus it
[System.Windows.Forms.SendKeys]::SendWait("%n")
Start-Sleep -Milliseconds 500

# Type just the filename
[System.Windows.Forms.SendKeys]::SendWait("video3.mp4")
Start-Sleep -Seconds 1

Screenshot "tt2-step3-filename"
Write-Host "Step 3: Filename typed"

# Press Enter or click Open
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Start-Sleep -Seconds 8

Screenshot "tt2-step4-uploaded"
Write-Host "Step 4: File selected, uploading..."

# Wait for processing
Start-Sleep -Seconds 15
Screenshot "tt2-step5-ready"
Write-Host "Step 5: Upload should be complete"

Write-Host "DONE"
