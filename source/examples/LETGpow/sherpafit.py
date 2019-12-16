# Sherpa code

load_pha('letgplaw_pha2.fits')
load_arf('legLEG_-1_garf.fits')
load_rmf('leg-1_rmf.fits')
set_source(xsphabs.a * xspowerlaw.xp)

group_counts(25)
fit()

# Do not display a window
# Delete this line for interactive use!
# set_preferences(['window.display', False])

plot_fit_delchi()
xscale('log')
savefig('m1_fit.png', bbox_inches='tight')
savefig('m1_fit.eps', bbox_inches='tight')
