#!/bin/bash

set -e


function get_xfoil() {

    wget https://web.mit.edu/drela/Public/web/xfoil/xfoil6.97.tar.gz -O /tmp/xfoil6.97.tar.gz
    tar -xzvf /tmp/xfoil6.97.tar.gz -C /

}


function patch_xfoil() {

    mv /xfoil.patch /Xfoil
    cd /Xfoil
    git apply xfoil.patch

}


function make_xfoil() {

    cd /Xfoil/orrs/bin
    make -f Makefile_DP osgen
    make -f Makefile_DP osmap.o

    cd /Xfoil/orrs
    bin/osgen osmaps_ns.lst

    cd /Xfoil/plotlib
    make libPlt.a

    cd /Xfoil/bin
    make xfoil
    make pplot
    make pxplot

}


function main() {

    get_xfoil
    patch_xfoil
    make_xfoil

    ln -s /Xfoil/bin/xfoil /usr/bin/xfoil

}

main

