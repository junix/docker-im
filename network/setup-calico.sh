#!/bin/bash
PROGRAM=/usr/local/bin/calicoctl
wget -O $PROGRAM http://www.projectcalico.org/builds/calicoctl
chmod +x $PROGRAM
$PROGRAM node run