Add-Type @"
using System;
using System.Text;
using System.Runtime.InteropServices;
public class ReviewWindowProbe {
 public delegate bool EnumProc(IntPtr h, IntPtr l);
 [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc f, IntPtr l);
 [DllImport("user32.dll")] public static extern bool EnumChildWindows(IntPtr h,EnumProc f,IntPtr l);
 [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h,out uint p);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h,StringBuilder b,int n);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] public static extern int GetClassName(IntPtr h,StringBuilder b,int n);
}
"@
$targetPid = 29452
$rows = [System.Collections.Generic.List[object]]::new()
$callback = [ReviewWindowProbe+EnumProc]{param($h,$l)
 $processId = [uint32]0
 [void][ReviewWindowProbe]::GetWindowThreadProcessId($h,[ref]$processId)
 if ($processId -eq $targetPid) {
   $caption = [System.Text.StringBuilder]::new(4096)
   $class = [System.Text.StringBuilder]::new(256)
   [void][ReviewWindowProbe]::GetWindowText($h,$caption,$caption.Capacity)
   [void][ReviewWindowProbe]::GetClassName($h,$class,$class.Capacity)
   $rows.Add([pscustomobject]@{Handle=$h.ToInt64();Class=$class.ToString();Caption=$caption.ToString()})
 }
 return $true
}
[void][ReviewWindowProbe]::EnumWindows($callback,[IntPtr]::Zero)
$parents = @($rows.ToArray())
foreach ($p in $parents) { [void][ReviewWindowProbe]::EnumChildWindows([IntPtr]$p.Handle,$callback,[IntPtr]::Zero) }
$rows | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath .\edu_output\review\mixed-review\word-window-probe.json -Encoding UTF8
$rows | ConvertTo-Json -Depth 5
