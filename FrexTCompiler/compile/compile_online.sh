#/bin/bash
$3 -mode batch -source $4 -tclargs $5 $6 $7 $8 > $6/$7.log

if [ -f $6/output/impl_1/$7.bit ]; then
  cp $6/output/impl_1/$7.bit $6/$7.bit
fi

if [ -f $6/output/impl_1/$7.bit ]; then
  cp $6/output/impl_1/$7.bit $6/$7.bit
fi
