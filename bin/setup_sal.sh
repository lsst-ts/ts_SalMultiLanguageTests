#!/bin/bash

source ./env_vars.env

cd $HOME/repos/ts_sal/test
rm -rf *

cp -r $HOME/repos/ts_xml/sal_interfaces/Test/Test*.xml $HOME/repos/ts_sal/test
cp -r $HOME/repos/ts_xml/sal_interfaces/SALSubsystems.xml $HOME/repos/ts_sal/test
cp -r $HOME/repos/ts_xml/sal_interfaces/SALGenerics.xml $HOME/repos/ts_sal/test
cp -r $HOME/repos/ts_xml/VERSION $HOME/repos/ts_sal/test
