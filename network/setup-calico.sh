#!/bin/bash
PROGRAM=/usr/local/bin/calicoctl
cp ./calicoctl ${PROGRAM}
chmod +x $PROGRAM
$PROGRAM node run