# Automation script
#
# Factors:
#     1) Colony Population: 1, 2, 3, 4, 5
#     2) Number of Nodes:   10, 30, 60
#
# Response Variable:
#     1) Best trail distance
#     2) Time elapsed in seconds
#
# Contributors:
#     Jeanderson Candido <http://jeandersonbc.github.io>

# Helper function to customize output
function getColor($p) {
    if ($p % 2 -eq 0) { return [System.ConsoleColor]::cyan }
    return [System.ConsoleColor]::darkcyan
}

write-host "Checking source path..." -noNewLine
if (test-path ../src/main.py) {
    write-host " main.py found!" -foregroundColor green 
    write-host "--------------------------------------"

    $pop = @(1, 2, 3, 4, 5)
    $nodes = @(10, 30, 60)
    $maxTime = 1000

    write-host ("Pop", "Nodes", "Len", "Time (secs)") -Separator "`t"
    foreach ($p in $pop) {
        foreach ($n in $nodes) {
            $output = & python ../src/main.py $n $p $maxTime

            $color = getColor($p)
            write-host ($p, $n, $output) -Separator "`t" -foregroundColor $color
        }
    }
    write-host "`nFinished!" -foregroundColor green

} else {
    write-host " main.py not found!" -foregroundColor red
}
