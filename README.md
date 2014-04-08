Romstools
=========

This page contains a variety of tools for plotting and analysing output from the Regional Ocean Model
(ROMS - http://myroms.org/). Currently, the following tools are separated into distinct folders as separate
toolboxes that can be used indepdentely.

<ul>
<li>Volume flux calculations</li>
</ul>


<h3> General requirements</h3>
<ul>
<li>Python installation with numpy, basemap, and matplotlib</li>
<li>Python netCDF4 interface - http://code.google.com/p/netcdf4-python/</li>
<li>In some cases a Fortran compiler combined with F2PY (part of numpy) is required to create python modules</li>
<li>A full Python distribution such as <a href="https://store.continuum.io/cshop/anaconda/">Anaconda</a> or
<a href="https://www.enthought.com/">Enthought Python Distribution</a> is reccomended</li>
</ul>


<h3> Volume flux calculations </h3>

To calculate the fluxes you run the script <em>calculateFluxes.py</em> either as a standalone python program or executed
as a job-script. If you run the program on a super-computer (e.g. Hexagon) you may want to run the script as a job
and use the script <em>runJob.sh</em> to queue your job (Hexagon: qsub runJob.sh).

This toolbox is a mixture of Fortrand and Python tools where the core programs are taken from the excellent pyroms
toolbox also available on github: https://github.com/kshedstrom/pyroms. However, to avoid having to install the
entire toolbox to calculate the fluxes, this smaller toolbox was created.


<h3> Define transects and depth ranges </h3>
You can define a list of transects you want the volume transport calculated for in the function
<strong>defineTransects().</strong>.  The output from running is a comma separated value file containing the positive,
negative, and net transport through the transect. You can also caluclate the transport for the e.g. just the upper
500 meters of the water column by defining the minimum and maximum depths:

```Python
minDepth=0
maxDepth=500
```

<h3> Requirements </h3>
This toolbox still requires you to have a Fortran compiler to compile the Fortran programs and generate Python modules.
On Hexagon this is done by loading the gnu modules (for Fortran compiler compatible with Python and numpy). In the
terminal window type:

```bash
module swap PrgEnv-pgi PrgEnv-gnu
module unload notur
f2py --verbose  -c -m iso iso.f90
f2py --verbose  -c -m obs_interp obs_interp.f
```

This should provide you with two python modules (obs_interp.so and iso.so) which you can try to import to python with:

```bash
Python 2.7.2 (default, Mar 22 2012, 12:32:11)
[GCC 4.6.1 20110627 (Cray Inc.)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import iso
>>> print iso.__doc__
```

<h3> Contact </h3>

<ul>
<li>me (at) trondkristiansen.com</li>
</ul>




