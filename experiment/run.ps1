# Automation script
#
# Number of Repetitions: 5
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

write-host "Checking source path..." -noNewLine
if (test-path ../src/main.py) {
    write-host " main.py found!" -foregroundColor green 

    $pop = @(1, 2, 3, 4, 5)
    $nodes = @(10, 30, 60)
    $repetitions = 5
    $maxTime = 1000

    write-host "Running experiment... take a sit and relax :)"
    for ($id=1; $id -le $repetitions; $id++) {
        write-host "Running #$id... " -noNewLine
        foreach ($p in $pop) {
            foreach ($n in $nodes) {
                $log = & python ../src/main.py $id $n $p $maxTime

                # The log file has the following format:
                # Exp ID, Population, Nodes, Length, Iteration, Elapsed Time
                set-content -Encoding UTF8 $p-$n-$id.txt $log
            }
        }
        write-host "Ok!" -foregroundColor cyan
    }
    write-host "`nFinished!" -foregroundColor green

} else {
    write-host " main.py not found!" -foregroundColor red
}
