#!/usr/bin/env python3

from argparse import ArgumentParser
import mdtraj as mdt
__version__ = "1.0.0"


def mesmy_cli():
    parser = ArgumentParser(
        description="Create a script for a multi-step Amber MD"
        " relaxation/equilibration workflow."
    )
    parser.add_argument("-i", "--inpcrd",
                        help="Input Amber CRD file.", required=True)
    parser.add_argument("-p", "--prmtop",
                        help="Input Amber PRMTOP file.", required=True)
    parser.add_argument("-temp", "--temperature",
                        help="Simulation temperature.", default="310.0", 
                        required=False)
    parser.add_argument("-exec", "--executable",
                        help="Simulation temperature.", default="sander.MPI", 
                        required=False)
    parser.add_argument("--version", action="version", version=__version__)

    args = parser.parse_args()

    t = mdt.load(args.inpcrd, top=args.prmtop)
    t_solute = t.atom_slice(
        t.topology.select('not water'))
    nres = t_solute.n_residues
    script = f"""#!/bin/bash


# An equilibration workflow.
# Designed for "standard" protein or protein/ligand systems
# in explicit solvent. Not optimised for membrane protein systems.
#
# Developed from scripts provided by the Hughes lab at the University
# of Montana.
#

# You may wish to modify some of the parameters below.
prmtop_file="{args.prmtop}"
inpcrd_file="{args.inpcrd}"
solute={nres} # number of residues in solute
T="{args.temperature}" # target temperature in K
PMEMD="{args.executable}" # name of your MD executable (e.g. may be "pmemd.MPI")

### DO NOT MODIFY BELOW THIS LINE UNLESS YOU KNOW WHAT YOU ARE DOING ###



# 1K step Steepest Descent Minimization with strong restraints on heavy atoms, no shake
cat > step1.in <<EOF
Min explicit solvent heavy atom rest no shake
&cntrl
  imin = 1, ntmin = 2, maxcyc = 1000,
  ntwx = 500, ioutfm = 1, ntpr = 50, ntwr = 500,
  ntc = 1, ntf = 1, ntb = 1, cut = 8.0,
  igb = 0, saltcon = 0.0,
  ntr = 1, restraintmask = ':1-$solute & !@H=', restraint_wt = 5.0,
&end
EOF

# NTV MD with strong restraints on heavy atoms, shake, dt=.001, 15 ps
cat > step2.in <<EOF
MD explicit solvent heavy atom rest shake dt 0.001
&cntrl
  imin = 0, nstlim = 1000, dt=0.001,
  ntx = 1, irest = 0, ig = -1,
  ntwx = 500, ioutfm = 1, ntpr = 50, ntwr = 500,
  iwrap = 1, nscm = 0,
  ntc = 2, ntf = 1, ntb = 1, cut = 8.0,
  ntt = 1, tautp = 0.5, temp0 = $T, tempi = $T,
  ntp = 0, taup = 0.5,
  igb = 0, saltcon = 0.0,
  ntr = 1, restraintmask = ':1-$solute & !@H=', restraint_wt = 5.0,
&end
EOF

# Steepest Descent Minimization with relaxed restraints on heavy atoms, no shake
cat > step3.in <<EOF
Min explicit solvent relaxed heavy atom rest no shake
&cntrl
  imin = 1, ntmin = 2, maxcyc = 1000,
  ntwx = 500, ioutfm = 1, ntpr = 50, ntwr = 500,
  ntc = 1, ntf = 1, ntb = 1, cut = 8.0,
  igb = 0, saltcon = 0.0,
  ntr = 1, restraintmask = ':1-$solute & !@H=', restraint_wt = 2.0,
&end
EOF

# Steepest Descent Minimization with minimal restraints on heavy atoms, no shake
cat > step4.in <<EOF
Min explicit solvent minimal heavy atom rest no shake
&cntrl
  imin = 1, ntmin = 2, maxcyc = 1000,
  ntwx = 500, ioutfm = 1, ntpr = 50, ntwr = 500,
  ntc = 1, ntf = 1, ntb = 1, cut = 8.0,
  igb = 0, saltcon = 0.0,
  ntr = 1, restraintmask = ':1-$solute & !@H=', restraint_wt = 0.1,
&end
EOF

# Steepest Descent Minimization with no restraints, no shake
cat > step5.in <<EOF
Min explicit solvent no heavy atom res no shake
&cntrl
  imin = 1, ntmin = 2, maxcyc = 1000,
  ntwx = 500, ioutfm = 1, ntpr = 50, ntwr = 500,
  ntc = 1, ntf = 1, ntb = 1, cut = 8.0,
  igb = 0, saltcon = 0.0,
  ntr = 0,
&end
EOF

# NTP MD with shake and low restraints on heavy atoms, 5 ps dt=.001
cat > step6.in <<EOF
MD explicit solvent heavy atom low rest shake dt 0.001
&cntrl
  imin = 0, nstlim = 1000, dt=0.001,
  ntx = 1, irest = 0, ig = -1,
  ntwx = 500, ioutfm = 1, ntpr = 50, ntwr = 500,
  iwrap = 1, nscm = 0,
  ntc = 2, ntf = 1, ntb = 2, cut = 8.0,
  ntt = 1, tautp = 1.0, temp0 = $T, tempi = $T,
  ntp = 1, taup = 1.0,
  igb = 0, saltcon = 0.0,
  ntr = 1, restraintmask = ':1-$solute & !@H=', restraint_wt = 1.0,
&end
EOF

# NTP MD with shake and minimal restraints on heavy atoms
cat > step7.in <<EOF
MD explicit solvent heavy atom minimal rest shake dt 0.001, 10 ps, dt=.001
&cntrl
  imin = 0, nstlim = 1000, dt=0.001,
  ntx = 5, irest = 1,
  ntwx = 500, ioutfm = 1, ntpr = 50, ntwr = 500,
  iwrap = 1, nscm = 0,
  ntc = 2, ntf = 1, ntb = 2, cut = 8.0,
  ntt = 1, tautp = 1.0, temp0 = $T, tempi = $T,
  ntp = 1, taup = 1.0,
  igb = 0, saltcon = 0.0,
  ntr = 1, restraintmask = ':1-$solute & !@H=', restraint_wt = 0.5,
&end
EOF

# NTP MD with shake and minimal restraints on backbone atoms, dt=0.001, 10 ps
cat > step8.in <<EOF
MD explicit solvent heavy atom minimal BB rest shake dt 0.001
&cntrl
  imin = 0, nstlim = 1000, dt=0.001,
  ntx = 5, irest = 1,
  ntwx = 500, ioutfm = 1, ntpr = 50, ntwr = 500,
  iwrap = 1, nscm = 0,
  ntc = 2, ntf = 1, ntb = 2, cut = 8.0,
  ntt = 1, tautp = 1.0, temp0 = $T, tempi = $T,
  ntp = 1, taup = 1.0,
  igb = 0, saltcon = 0.0,
  ntr = 1, restraintmask = ":1-$solute@H,N,CA,HA,C,O", restraint_wt = 0.5,
&end
EOF

# NTP MD with shake and no restraints, dt=0.002, 1 ns
cat > step9.in <<EOF
MD explicit solvent heavy atom no rest shake dt 0.002
&cntrl
  imin = 0, nstlim = 1000, dt=0.002,
  ntx = 5, irest = 1,
  ntwx = 100, ioutfm = 1, ntpr = 1000, ntwr = 1000,
  iwrap = 1, nscm = 1000,
  ntc = 2, ntf = 1, ntb = 2, cut = 8.0,
  ntt = 1, tautp = 1.0, temp0 = $T, tempi = $T,
  ntp = 1, taup = 1.0,
  igb = 0, saltcon = 0.0,
  ntr = 0,
&end
EOF

START="`date +%s.%N`"

# Minimization Phase
for RUN in step1 step2 step3 step4 step5 ; do
 echo "------------------------"
 echo "Minimization phase: $RUN"
 echo "------------------------"
 if [[ ! -f $RUN.rst7 ]]; then
     echo "File -- $RUN.rst7 -- does not exist. Running job..."
     $PMEMD -O -i $RUN.in -p $prmtop_file -c $inpcrd_file -ref $inpcrd_file -o $RUN.out -x $RUN.nc -r $RUN.rst7 -inf $RUN.mdinfo
 else
     echo "File -- $RUN.rst7 -- exists.  Checking the next step."
 fi
 echo ""
 inpcrd_file="$RUN.rst7"
done

# Equilibration phase - reference coords are last coords from minimize phase
REF=$inpcrd_file
for RUN in step6 step7 step8 step9 ; do

 echo "------------------------"
 echo "Equilibration phase: $RUN"
 echo "------------------------"
 if [[ ! -f $RUN.rst7 ]]; then
     echo "File -- $RUN.rst7 -- does not exist. Running job..."
     $PMEMD -O -i $RUN.in -p $prmtop_file -c $inpcrd_file -ref $REF -o $RUN.out -x $RUN.nc -r $RUN.rst7 -inf $RUN.mdinfo
 else
     echo "File -- $RUN.rst7 -- exists.  Checking the next step."
 fi
  echo ""
  inpcrd_file="$RUN.rst7"

done

sed -i 's/0.3000000E+02/0.0000000E+00/g' step9.rst7

STOP="`date +%s.%N`"
TIMING=`echo "scale=4; $STOP - $START;" | bc`
echo "$TIMING seconds."
echo ""

exit 0    
    """
    print(script)


if __name__ == "__main__":
    mesmy_cli()
