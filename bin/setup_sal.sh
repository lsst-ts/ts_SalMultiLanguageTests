#!/bin/bash

source ./env_vars.env

cd $HOME/repos/ts_sal/test
rm -rf *

cp -r $TS_XML_DIR/python/lsst/ts/xml/data/sal_interfaces/Test/Test*.xml $HOME/repos/ts_sal/test
cp -r $TS_XML_DIR/python/lsst/ts/xml/data/sal_interfaces/SALSubsystems.xml $HOME/repos/ts_sal/test
cp -r $TS_XML_DIR/python/lsst/ts/xml/data/sal_interfaces/SALGenerics.xml $HOME/repos/ts_sal/test
