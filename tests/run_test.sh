#!/bin/sh

### FUNCTIONS ##

function run_test() {
    echo "******** Test $upper_commander to $upper_controller ********"
    echo "Starting $upper_commander Commander"
    ${commander_exec} 1 23 > ${commander}_commander.log 2>&1 &
    sleep 5

    echo "Starting $upper_controller Controller"
    ${controller_exec} 1 23 > ${controller}_controller.log 2>&1
    COMMANDER=$(cat ${commander}_commander.log)
    CONTROLLER=$( cat ${controller}_controller.log 2>&1 )

    echo "======== $upper_commander to $upper_controller Test Results ========"
    for item in 10 52 0
    do
        if [[ "$CONTROLLER" == *"$controller_text: writing logLevel=$item"* ]]; then
            echo "Test logLevel=$item PASS" |GREP_COLOR='01;36' grep -E --color 'PASS|$'
        else
            ((failed=$failed+1))
            echo "Test logLevel=$item FAIL" |grep -E --color 'FAIL|$'
            echo -e "%%%%%%%%%% Commander log BEGIN: \n $COMMANDER \nEND %%%%%%%%%%"
            echo -e "%%%%%%%%%% Controller log BEGIN: \n $CONTROLLER \nEND %%%%%%%%%%"
        fi
    done
    echo "******** Test complete ********"
    echo ""
}


### Arguments ###

arg_status=0
commander=$(echo "cpp java" |grep -o $1)
controller=$(echo "cpp java salobj" |grep -o $2)
failed=0

case $commander in
    cpp)
      upper_commander="C++"
      commander_exec="/home/saluser/repos/ts_sal/bin/minimal_cpp_commander.sh"
      ;;
    java)
      upper_commander="Java"
      commander_exec="/home/saluser/repos/ts_sal/bin/minimal_java_commander.sh"
      ;;
    *)
      echo "Usage: Specified commander must each be one of [cpp java]."
      ((arg_status=$arg_status+1))
      ;;
esac

case $controller in

    "cpp")
      upper_controller="C++"
      controller_text="SALController"
      controller_exec="/home/saluser/repos/ts_sal/bin/minimal_cpp_controller.sh"
      ;;

    "java")
      upper_controller="Java"
      controller_text="SALController"
      controller_exec="/home/saluser/repos/ts_sal/bin/minimal_java_controller.sh"
      ;;

    "salobj")
      upper_controller="SalObj"
      controller_text="SalobjController"
      controller_exec="python /home/saluser/repos/ts_SalMultiLanguageTests/tests/controllers/minimal_salobj_controller.py"
      ;;

    *)
      echo "Usage: Specified controller must be one of [cpp, java, salobj]."
      ((arg_status=$arg_status+1))
      ;;
esac

if [[ $arg_status -ne 0 ]]; then
    exit $arg_status
else
    run_test
    exit $failed
fi
