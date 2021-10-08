if { $argc != 4 } {
  puts "you need 4 parameters"
  return
}



#
# STEP#0: get parameters.
#

set FPGAVersion   [lindex $argv 0]
set workDir       [lindex $argv 1]
set topModuleName [lindex $argv 2]
set threads       [lindex $argv 3]
set outputDir $workDir/output

puts $FPGAVersion
puts $workDir
puts $topModuleName
puts $threads
puts $outputDir



#
# STEP#1: set output directory and create project.
#

file mkdir $outputDir
create_project $topModuleName $outputDir -part $FPGAVersion -force



#
# STEP#2: setup design sources and constraints.
#

foreach f [glob -dir $workDir *] {
  if {[string match *.xci $f] == 1} {
    add_files -fileset sources_1 $f
    puts $f
  }
  if {[string match *.v $f] == 1} {
    add_files -fileset sources_1 $f
    puts $f
  }
  if {[string match *.xdc $f] == 1} {
    add_files -fileset sources_1 $f
    puts $f
  }
}

foreach f [glob -dir $workDir */*] {
  if {[string match *.xci $f] == 1} {
    add_files -fileset sources_1 $f
    puts $f
  }
  if {[string match *.v $f] == 1} {
    add_files -fileset sources_1 $f
    puts $f
  }
  if {[string match *.xdc $f] == 1} {
    add_files -fileset sources_1 $f
    puts $f
  }
}

foreach f [glob -dir $workDir */*/*] {
  if {[string match *.xci $f] == 1} {
    add_files -fileset sources_1 $f
    puts $f
  }
  if {[string match *.v $f] == 1} {
    add_files -fileset sources_1 $f
    puts $f
  }
  if {[string match *.xdc $f] == 1} {
    add_files -fileset sources_1 $f
    puts $f
  }
}



#
# STEP#3: set project sources.
# the project will default to create fileset: source_1, sim_1, constrs_1.
#

set_property top $topModuleName [current_fileset]
update_compile_order -fileset sources_1
update_compile_order -fileset constrs_1


#
# STEP#4: run synthesis and the default utilization report.
# the project will default to create synth_1 task to compile.
#

launch_runs synth_1 -dir $outputDir -jobs $threads
wait_on_run synth_1



#
# STEP$5: run logic optimization, placement, physical logic optimization, route and
# bitstream generation. Generates design checkpoints, utilization and timing
# reports, plus custom reports.
#

launch_runs impl_1 -dir $outputDir -jobs $threads -to_step write_bitstream -force $workDir/$topModuleName.bit
wait_on_run impl_1

puts "Implementation done!"

