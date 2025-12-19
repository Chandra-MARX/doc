import configparser
import os
from warnings import warn
import gzip
import shutil
import sys

from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy.coordinates.name_resolve import NameResolveError
from astropy.table import Table, hstack
import numpy as np

from coords.chandra import sky_to_chandra
import ciao_contrib.runtool as rt

_cfg_name = 'marx_examples.cfg'
cfgpath = [os.path.join(os.path.dirname(sys.modules[__name__].__file__), '..', _cfg_name),
           os.path.join(os.path.dirname(sys.modules[__name__].__file__),  _cfg_name)]
'Path list to search for configuration files.'

def setup_marx() -> None:
    if not shutil.which('marx'):
        conf = configparser.ConfigParser()
        cfgfile = conf.read(cfgpath)
        if not cfgfile:
            raise Exception(f"No config file with path specifications found. File must be called {_cfg_name} and be located in one of the following directories: {cfgpath}")
        path = conf.get("marx", "path")
        os.environ['PATH'] = os.path.join(path, 'bin') + ':' + os.environ['PATH']
        if not shutil.which('marx'):
            raise Exception(f"marx not found in path {os.environ['PATH']}")
    marxpardir = os.path.dirname(shutil.which('marx')) + '/../share/marx/pfiles:'
    if marxpardir not in os.environ.get('PFILES', ''):
        os.environ['PFILES'] = marxpardir + os.environ.get('PFILES', '')

def setup_saotrace() -> None:
    """The notebooks are written assuming that SAOTrace is run
    in a container. If, instead, it is installed on the local system
    one needs to set up the environment before stating the notebook
    and leave the configuration parameters empty.
    """
    if not shutil.which('trace-nest'):
        conf = configparser.ConfigParser()
        cfgfile = conf.read(cfgpath)
        if not cfgfile:
            raise Exception(f"No config file with path specifications found. File must be called {_cfg_name} and be located in one of the following directories: {cfgpath}")

        path = conf.get("saotrace", "path")
        if path:
            os.environ['PATH'] = path + ':' + os.environ['PATH']

        return conf.get("saotrace", "trace-nest") + " "
    return "trace-nest "



def detectorfromkeyword(keyword: str) -> str:
    '''Determine detector type from fits header keyword

    For ACIS, this uses a heuristic to decide which chips are on,
    since Chandra allows arbitrary combinations,
    but MARX only know ACIS-I or ACIS-S.

    Parameters
    ----------
    keyword : string
        Chandra fits file header keyword like 'ACIS-012356'.

    Returns
    -------
    detector : string
        one of 'ACIS-I', 'ACIS-S', 'HRC-I', 'HRC-S', or ''
    '''
    # DetectorType
    if keyword.startswith('HRC'):
        return keyword
    
    if keyword.startswith('ACIS'):
        # Use a heuristic to decide which chips are on, since Chandra
        # allows arbitrary combinations, but MARX only knows ACIS-I or ACIS-S
        acisi = len(set(keyword).intersection(set('0123')))
        aciss = len(set(keyword).intersection(set('456789')))
        if acisi > aciss:
            return 'ACIS-I'
        else:
            return 'ACIS-S'
    
    return ''


def target_coos_from_asol(asolfile: str) -> tuple[float, float]:
    '''Get coordinates for the target named in asol file.

    If the target name cannot be resolved, return the nominal aimpoint,
    assuming a on-axis pointing.

    Parameters
    ----------
    asolfile : str
        Path and name of an asol file

    Returns
    -------
    ra, dec : float
        RA and Dec in degrees
    '''
    asol = fits.getheader(asolfile, 1)
    try:
        objname = asol['OBJECT'].split('/')[0]
        skyco = SkyCoord.from_name(objname)
        return skyco.ra.value, skyco.dec.value
    except NameResolveError:
        warn('Target name {0} not resolved by SIMBAD. Assuming on-axis target.'.format(objname))
        return asol['RA_NOM'], asol['DEC_NOM']


def marxpars_from_asol(asolfile: str, evt2file: str) -> dict:
    '''Set MARX parameters from asol and evt file.

    This function parses the header of a fits file and uses the
    information in the header to set as many marx parameters as possible.

    Parameters
    ----------
    asolfile : str
        Path and name of an asol file

    evt2file : str
        Path and name of an evt2 file

    Returns
    -------
    marx_pars : dict
        Dictionary with marx parameters as far as they can be extracted from
        the data in the asol file.
    '''
    asol = fits.getheader(asolfile, 1)
    evt = fits.getheader(evt2file, 1)

    '''Unzip fits file.

    MARX cannot read zipped fits files, so we need to unzip the .fits.gz asol
    files that we downloaded from the archive. On the other hand, CIAO
    tools work on both zipped or unzipped files, so there is no need to
    unzip all of them, just the files that MARX reads as input.
    '''
    if not os.path.exists(asolfile.removesuffix('.gz')):
        with gzip.open(asolfile, 'rb') as f_in:
            with open(asolfile.removesuffix('.gz'), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    marx_pars = {}
    marx_pars['RA_Nom'] = asol['RA_NOM']
    marx_pars['Dec_Nom'] = asol['DEC_NOM']
    marx_pars['Roll_Nom'] = asol['ROLL_NOM']
    marx_pars['GratingType'] = asol['GRATING']
    marx_pars['ExposureTime'] = asol['TSTOP'] - asol['TSTART']
    marx_pars['DitherModel'] = 'FILE'
    marx_pars['DitherFile'] = asolfile.removesuffix('.gz')
    marx_pars['TStart'] = asol['TSTART']

    # ACIS Exposure time (might vary for sub-array read-out)
    if evt['INSTRUME'][0:4] == 'ACIS':
        marx_pars['ACIS_Exposure_Time'] = evt['EXPTIME']
    # Target coordiantes
    # ra, dec = target_coos_from_asol(asolfile)
    marx_pars['SourceRA'] = evt['RA_TARG']
    marx_pars['SourceDEC'] = evt['DEC_TARG']

    # DetectorType
    det = detectorfromkeyword(evt['DETNAM'])
    if det != '':
        marx_pars['DetectorType'] = det
        # Find offsets from nominal pointing
        aimpts = Table.read(os.path.join(os.environ['CALDB'], 'data', 'chandra', 'default', 'aimpts', 'telD1999-07-23aimptsN0002.fits'))
        det2aimpts = {'ACIS-I': 'AI2', 'ACIS-S': 'AS1', 'HRC-I': 'HI1', 'HRC-S': 'HS1'}
        aimp = np.array([n.strip() for n in aimpts['AIMPOINT_NAME']])
        ind = aimp == det2aimpts[det]
        marx_pars['DetOffsetX'] = evt['SIM_X'] - aimpts[ind]['AIMPOINT'][0][0]
        # No Y offset possible
        marx_pars['DetOffsetZ'] = evt['SIM_Z'] - aimpts[ind]['AIMPOINT'][0][2]
    else:
        warn('detector {0} not understood. No DetectorType or aimpoint offset set.'.format(asol['DETNAM']))
    return marx_pars


def write_spectrum_from_fluxcorrection(asolfile : str,
                                       evt2file: str,
                                       x: float, y: float, region: str,
                                       psffrac: float=1) -> None:
    '''Estimate a source spectrum through flux correction.

    This technique extracts the source spectrum from an evt2 file
    and divides it by the arf. Strictly speaking, the result will
    be wrong (the model spectrum should be folded with ARF and RMF),
    but it is often good enough to get a simulation input that has
    roughly the same spectral shape.

    This function will write two files:
    - input_spec_marx.tbl : for use with marx
    - input_spec_saotrace.rdb : for use with saotrace

    Parameters
    ----------
    asolfile : string
        Path and name of an asol file
    evt2file : string
        Path and name of an evt2 file
    x : float
        Source X coordinate in sky pixels
    y : float
        Source Y coordinate in sky pixels
    region : str
        Region specification in CIAO format
    psffrac : float, optional
        Fraction of the PSF enclosed by the extraction region (default is 1)
    '''

    evt = fits.getheader(evt2file, 1)
    det = detectorfromkeyword(evt['DETNAM'])
    if det[:4] != 'ACIS':
        raise ValueError('This works only for ACIS. Detector found: {0}'.format(det))
    ccd_id = sky_to_chandra(evt, x, y)['chip_id'][0]

    rt.asphist(infile=asolfile, outfile='obs.asp', evtfile=evt2file, clobber=True)
    # It would be more accuarte to use mkwarf.
    # However, that's slower and for our purposes an approximate solution is good enough.
    rt.mkarf(detsubsys=f'ACIS-{ccd_id}', grating=evt['GRATING'],
            outfile='obs.arf', obsfile=evt2file,
            asphistfile='obs.asp', sourcepixelx=x, sourcepixely=y, engrid="0.3:8.0:0.1",
            maskfile='NONE', pbkfile='NONE', dafile='NONE', clobber=True)

    # We have to use the same energy binning in energy space here that we used for the arf!
    # So, first convert the PI to energy (to a precision that's good enough).
    rt.dmtcalc(f"{evt2file}[EVENTS][sky={region}]", "evt2_with_energy.fits", expr="energy=(float)pi*0.0149", clobber=True)
    rt.dmextract(infile="evt2_with_energy.fits[bin energy=.3:7.999:0.1]", outfile="obs.spec", clobber=True, opt="generic")

    # Write input tables for MARX and SAOTrace in the required formats
    # This is way easier in Python with Astropy than using CIAO and shell tools to manipulate
    # the formatting of the files.
    binned_spec = Table.read("obs.spec", format='fits', hdu=1)
    arf = Table.read("obs.arf", format='fits', hdu=1)
    del binned_spec.meta['comments']
    tab = hstack([binned_spec, arf], metadata_conflicts='silent')
    tab['flux'] = tab['COUNT_RATE'] / (tab['SPECRESP'] * psffrac)
    tab['fluxdens'] = tab['flux'] / 0.1  # divide by bin width to get flux density
    tab['ENERG_HI', 'fluxdens'].write("input_spec_marx.tbl", format='ascii.commented_header', overwrite=True)
    tab['ENERG_LO', 'ENERG_HI', 'flux'].write("input_spec_saotrace.rdb", format='ascii.rdb', overwrite=True)
