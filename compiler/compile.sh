#/bin/bash
rm -rf $2
/bin/unzip $1 -d $2

$3 -mode batch -source $4 -tclargs $5 $6 $7 $8 > $6/$7.log

if [ -f $6/output/impl_1/$7.bit ]; then
  cp $6/output/impl_1/$7.bit $6/$7.bit
fi
