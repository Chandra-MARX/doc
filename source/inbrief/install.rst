.. _installing:

*******************************
Downloading and Installing Marx
*******************************

|marx| is distributed in the form of a compressed tar file and must be
compiled before it can be used.  This process is fairly painless and
is something that even those who have never compiled a C program
before can do.  It is written in ANSI-C (with a few POSIX extensions)
and is intended to be portable across most 64 bit Unix
operating systems, as well as MacOSX and CYGWIN.


The short-cut
-------------

.. note::

    This is the easiest installation method and is recommended for most users.

`CIAO`_ is now distributed as conda packages. |marx| is provided as one
of those pre-complied binary packages. If you follow the
`default instruction for the CIAO installation
<https://cxc.cfa.harvard.edu/ciao/threads/ciao_install_conda/>`_
marx is included in that install.


The normal way
--------------
First download |marx| from https://github.com/Chandra-MARX/marx/releases
and copy it to a directory that has at least a
couple of hundred megabytes of free disk space.  Note that this
directory and its contents will no longer be needed after |marx| has
been installed.

Next uncompress and untar the file::


    tar -xzf marx-6.0.1.tar.gz

(Some webbrowsers will automatically unzip a file when downloaded).  At this point the tar file is
no longer needed so it may be removed::

    rm marx-6.0.1.tar.gz

Now change to the newly created directory to start the build process::

    cd marx-6.0.1

The next step is to run the ``configure`` script, which will probe your
system to see what tools are available for compiling |marx|.  Before
doing so, we recommended that you read the ``INSTALL`` file.

Note that the configure script will take the ``CC``, ``CFLAGS``, ``LDFLAGS``, and
``ARCH``, variables from your environment, if they are defined. If not, it
will first look for gcc. So, if you have gcc installed, and you want to
use a compiler other than gcc, such as acc perhaps, you can instruct the
configure script to use the other compiler using:

::

    unix% setenv CC acc
    unix% setenv CFLAGS -g
    unix% ./configure


At this point you need to think about where you want |marx| to be
installed, and if you want the optional :marxtool:`marxrsp` program to also be
created (:marxtool:`marxrsp` was written for calibration purposes - it is
not needed by most users).  If you want :marxtool:`marxrsp` to be installed, then
you will also need to have `cfitsio`_ compiled and installed as detailed
in the ``INSTALL`` file.  For simplicity, here it is assumed that :marxtool:`marxrsp`
will not be installed.

Assume that you want |marx| installed in its own tree under
``/opt/marx/marx-version/``.  This value is known as the
*installation-prefix*.  It is important to understand that with
this choice the resulting |marx| executable will be placed in
``/opt/marx/marx-version/bin/``.

Now run the ``configure`` script
specifying this value as the ``--prefix`` argument:

.. parsed-literal::

    ./configure --prefix=/opt/marx/|version|

If all has gone well, the last bit of output from the above command
should resemble:

.. parsed-literal::

    You are compiling MARX with the following compiler configuration:
       CC = gcc
          .
          .
       MARX parameter files will be installed in /opt/marx/|version|/share/marx/pfiles/.
            
       To continue the build process, run 'make'.

If not, then you may not have the necessary tools installed to compile
|marx|, or you have an unsupported system.  If you are unable to
resolve the problem on your own, then contact |marx-email|.

Assuming all has gone well, execute the ``make`` command::

    make

(If this step fails and you are unable to resolve the problem, then contact |marx-email|.)

The final step in the installation process is to actually install the
compiled executables.  If you do not have write permission to the
installation-prefix directory (``/opt/marx/marx-version`` in this case),
then you will need to obtain the appropriate privileges to complete
the next step.  For example, this may require temporarily becoming the
``root`` user.  Now run::

    make install

to complete the installation. 

The install step will create the following directories:

``/opt/marx/marx-version/bin/``
    Directory where |marx|, :marxtool:`marx2fits`, and other |marx| -related executables are placed.

``/opt/marx/marx-version/share/marx/data/``
    Directory under which the |marx| calibration data files are located.

``/opt/marx/marx-version/share/marx/pfiles/``
    The parameter files used by |marx| are located here.

``/opt/marx/marx-version/share/doc/marx/``
    Directory containing |marx| -related documentation.

``/opt/marx/marx-version/lib/``
    Static versions of libraries distributed with and used by |marx| are put here.

``/opt/marx/marx-version/include/``
    The C header files of the |marx| libraries are put here.

``/opt/marx/marx-version/lib/marx/``
    Contains miscellaneous |marx| -related tools.

As indicated above, the |marx| executable will be copied to ``/opt/marx/marx-version/bin/``.
In addition, the |marx| installation contains some other tools described in
:ref:`tools`.
Binary executables for those tools are located in the same directory as |marx|
itself. Tools that are written as scripts in Python, ISIS or bash can be found
in ``/opt/marx/marx-version/lib/marx/``.
Both directories should be added to the user's ``PATH`` environment variable.
For e.g. a tcsh shell user add the following line to your ``~/.cshrc`` file::

  set path = ( /opt/marx/marx-version/bin /opt/marx/marx-version/lib/marx $path )

As the above indicates, the |marx| data files will be copied to the
``/opt/marx/marx-version/share/marx/data/`` directory.  |marx| will
automatically search this directory for calibration files.  Also note
that the parameter files will be placed under
``/opt/marx/marx-version/share/marx/pfiles/``.  As a helpful reminder, this
location is reported when |marx| is invoked as ``marx --help``.

The parameter files are **NOT** automatically loaded by |marx| unless the ``UPARM`` or ``PFILES`` environment variables are set appropriately.  For this
reason, it is recommended that the user copy these files to the
directory where the simulation will be performed.

Apple's ARM architecture (M1/M2 chips)
--------------------------------------
Depending on your setup, it might be necessary to explicitly point to the XCode
SDK, when using ``clang`` (or its alias ``gcc``) installed through Apple's Xcode::

  %> setenv CFLAGS "-g -I/Library/Developer/CommandLineTools/SDKs/MacOSX11.0.sdk/usr/include"

before calling the usual::

    %> ./configure
    %> make
    %> make install


Special cases
-------------
For most users, the steps described above are all that is needed. In this section we provide instruction for a few
special cases that are a little more involved.

Building marxrsp
~~~~~~~~~~~~~~~~

The above procedure will compile the majority of the programs in the
|marx| suite. The exceptions are the :marxtool:`marxrsp` and :marxtool:`rspdump` tools which
allows users to work with user provided FITS response matrix file (RMF).
In order to compile :marxtool:`marxrsp` and :marxtool:`rspdump`, you will need to obtain and
install the CFITSIO library if you do not already have it installed on
your system. The library can be obtained from the HEASARC web page as cfitsio_.

Instructions for installing the library are included with the CFITSIO
source code and will not be discussed here.

After installing the CFITSIO library, you must edit the Makefile in the
``marxrsp`` directory to point to the library. If you have the HEASARC 
FTOOLS or LHEASOFT packages installed on your system, you can use the
CFITSIO library distributed as part of that package. The following
excerpt from the Makefile indicates the two paths which must be defined
in order to build the :marxtool:`marxrsp` tool. The ``CFITSIO_LIB`` and ``CFITSIO_INC``
variables point to the location of the compiled CFITSIO library and
include files, respectively, and should be modified appropriately for
your particular system. The sample Makefile reproduced here shows an
example of building marxrsp using the CFITSIO library installed as part
of the LHEASOFT package on a machine running Linux.

.. code-block:: bash

    #---*- sh -*----------------------------------------------------------------
    # ANSI C compiler.  The default is to use your CC environment variable
    #---------------------------------------------------------------------------
    #CC = gcc         # Uncomment this line if you want gcc!!!
    #CFLAGS = -g

    #---------------------------------------------------------------------------
    # Where is your CFITSIO library and include file?  CFITSIO is part of IRAF.
    #---------------------------------------------------------------------------
    # At MIT, we use:
    #
    #CFITSIO_LIB = /nfs/wiwaxia/d4/ASC/lib/$(ARCH)
    #CFITSIO_INC = /nfs/wiwaxia/d4/ASC/include
    #
    # Perhaps one of these combinations will work for you:
    #
    #CFITSIO_LIB = /usr/local/include
    #CFITSIO_INC = /usr/local/lib
    #
    #CFITSIO_INC = /usr/local/src/ftools/SunOS_5.5_sparc/include
    #CFITSIO_LIB = /usr/local/src/ftools/SunOS_5.5_sparc/lib
    #
    CFITSIO_INC = /usr/local/src/lheasoft/Linux_2.2_i586/include
    CFITSIO_LIB = /usr/local/src/lheasoft/Linux_2.2_i586/lib

    #---------------------------------------------------------------------------
    # New versions of CFITSIO require additional networking libraries on some
    # systems.  The most well known system with this requirement is solaris.
    #---------------------------------------------------------------------------
    #NETLIBS = -lsocket -lnsl  # <<<---- Solaris
    NETLIBS =                # <<<---- Linux

    #---------------------------------------------------------------------------
    # There should be no need to modify anything else below this point
    #---------------------------------------------------------------------------

With the appropriate modifications to the marxrsp Makefile completed,
the tool can now be built. Assuming you are in the main |marx| source
directory, the commands:

::

    unix% cd ./marxrsp
    unix% make install

will build the marxrsp and rspdump executables and move them to the
``bin`` directory with the other tools in the suite. Note, you do not need
:marxtool:`marxrsp` to run |marx|  simulations.


Building |marx| on Multiple Architectures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The |marx| suite can be compiled to support multiple architectures
using the same source tree. To create |marx| on multiple
architectures (e.g. if your network has 32 and 64 bit machines), simply define an environment variable called ``ARCH`` and
set it to an architecture-dependent value. For example, to build
a version of for the NeXT platform, one could type:

::

    unix% setenv ARCH next
    unix% ./configure
    unix% make

This sequence will build NeXT executables and place them in the
“./bin/next” subdirectory. To then compile a Linux version as well, use:

::

    unix% setenv ARCH linux
    unix% ./configure
    unix% make

These binaries will be placed in ``./bin/linux``. This process can be
repeated as needed.



.. _knownbugs:

Known Bugs and Limitations
--------------------------

Currently there are no known bugs for installation issues. |marx| is tested on
MacOSX (clang and gcc compiler) and 64 bit linux (gcc compiler). We expect it
to work on other POSIX compliant platforms, too, but have not tested this.
