#!/bin/sh

passed=9
failed=0
path=$(dirname $0)

echo "############# Begin Java Tests #############"
$path/run_test.sh java cpp
((failed=$failed+$?))
echo ""

$path/run_test.sh java java
((failed=$failed+$?))
echo ""

$path/run_test.sh java salobj
((failed=$failed+$?))
echo ""

passed=$(($passed - $failed))
if [[ $failed -eq 0 ]] ; then
    echo "============= $passed Java Tests PASSED ============="
    echo ""
else
    echo "############# Java tests $passed PASSED and $failed FAILED. #############"
    echo ""
fi
exit $failed
