#!/bin/sh

passed=9
failed=0
path=$(dirname $0)

echo "############# Begin C++ Tests #############"
$path/run_test.sh cpp cpp
((failed=$failed+$?))
echo ""

$path/run_test.sh cpp java result
((failed=$failed+$?))
echo ""

$path/run_test.sh cpp salobj result
((failed=$failed+$?))
echo ""

passed=$(($passed - $failed))
if [[ $failed -eq 0 ]] ; then
    echo "============= $passed C++ Tests PASSED ============="
    echo ""
else
    echo "############# C++ tests $passed PASSED and $failed FAILED. #############"
    echo ""
fi
exit $failed
