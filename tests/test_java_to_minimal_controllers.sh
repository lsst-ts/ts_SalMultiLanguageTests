#!/bin/sh

cd /home/saluser/repos/ts_sal/bin
passed=0
failed=0

echo "############# Begin Java Tests #############"
echo "******** Test Java to Java ********"
echo "Starting Java Commander"
./minimal_java_commander.sh 1 23 > java_commander.log 2>&1 &
sleep 5

echo "Starting Java Controller"
./minimal_java_controller.sh 1 23 > java_controller.log 2>&1
JAVA_CONTROLLER=$( cat java_controller.log 2>&1 )
JAVA_COMMANDER=$( cat java_commander.log )

echo "======== Java to Java Test Results ========"
for item in 10 52 0
do
    if [[ "$JAVA_CONTROLLER" == *"SALController: writing logLevel=$item"* ]]; then
        ((passed=$passed+1))
        echo "Test logLevel=$item PASS" |GREP_COLOR='01;36' grep -E --color 'PASS|$'
    else
        ((failed=$failed+1))
        echo "Test logLevel=$item FAIL" |grep -E --color 'FAIL|$'
        echo $JAVA_CONTROLLER
        echo $JAVA_COMMANDER
    fi
done
echo "******** Test complete ********"
echo ""
echo ""


echo "******** Test Java to C++ ********"
echo "Starting Java Commander"
./minimal_java_commander.sh 1 47 > java_commander.log 2>&1 &
sleep 5

echo "Starting C++ Controller"
./minimal_cpp_controller.sh 1 47 > cpp_controller.log 2>&1
CPP_CONTROLLER=$( cat cpp_controller.log 2>&1 )
JAVA_COMMANDER=$( cat java_commander.log )

echo "======== C++ to Java test results ========"
for item in 10 52 0
do
    if [[ "$CPP_CONTROLLER" == *"SALController: writing logLevel=$item"* ]]; then
        ((passed=$passed+1))
        echo "Test logLevel=$item PASS" |GREP_COLOR='01;36' grep -E --color 'PASS|$'
    else
        ((failed=$failed+1))
        echo "Test logLevel=$item FAIL" |grep -E --color 'FAIL|$'
        echo $CPP_CONTROLLER
        echo $JAVA_COMMANDER
    fi
done
echo "******** Test complete ********"
echo ""
echo ""


echo "******** Test Java to SalObj ********"
echo "Starting Java Commander"
./minimal_cpp_commander.sh 1 79 > cpp_commander.log 2>&1 &
sleep 5

echo "Starting SalObj Controller"
python /home/saluser/repos/ts_SalMultiLanguageTests/tests/controllers/minimal_salobj_controller.py 1 79 > salobj_controller.log 2>&1
SalObj_CONTROLLER=$( cat salobj_controller.log 2>&1 )
JAVA_COMMANDER=$( cat java_commander.log )

echo "======== Java to SalObj test results ========"
for item in 10 52 0
do
    if [[ "$SalObj_CONTROLLER" == *"SalobjController: writing logLevel=$item"* ]]; then
        ((passed=$passed+1))
        echo "Test logLevel=$item PASS" |GREP_COLOR='01;36' grep -E --color 'PASS|$'
    else
        ((failed=$failed+1))
        echo "Test logLevel=$item FAIL" |grep -E --color 'FAIL|$'
        echo $SalObj_CONTROLLER
        echo $JAVA_COMMANDER
    fi
done
echo "******** Test complete ********"
if [[ $test_status -ne 0 ]] ; then
    echo "$passed tests PASSED.  $test_status tests FAILED."
    echo ""
    exit $test_status
else
    echo "============= $passed Java Tests PASSED ============="
    echo ""
fi
