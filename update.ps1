$Year = 2026
$Round = 1
$File = "assets\js\script.js"

$Date = (Get-Date).AddDays(-2).ToString("MM-dd")

@"
2026
1
$Date
$Round
2
6
"@ | python CLI.py

$Data = Get-Content "data\$year.json"

(Get-Content $File) `
    -replace '^\s\s2026:.*$', "  2026: $Data," |
    Set-Content $File

git add .
git commit -m "Stats updates $Date"
# git push