% Load the pha's and responses:

()=load_data("hetg_plaw_pha2.fits",[3,4]);

()=load_arf("hetg_plawMEG_-1_garf.fits");
()=load_arf("hetg_plawMEG_1_garf.fits");
assign_arf(1,1);
assign_arf(2,2);

()=load_rmf("hetg_plawmeg-1_rmf.fits");
()=load_rmf("hetg_plawmeg1_rmf.fits");
assign_rmf(1,1);
assign_rmf(2,2);

% Group and notice the data:
group_data(all_data, 8);
% 0.6 to 7.5 keV:
xnotice(all_data, Const_hc/7.5, Const_hc/0.6);

% List the data
list_data;

% open plot
plot_open("hetgmeg1.ps/CPS");

% Use keV for the X axis in plots:
plot_unit("keV");

% Use log x axis, linear y axis starting at 0.
xlog; xrange(0.5,10.0);
ylin; yrange(0.,);

% Can look at the data
title("MARX simulation of HETG observation");
plot_data_counts(1);
% show all of these in grey
oplot_data_counts(1,14);
oplot_data_counts(2,14);

% Ignore the line regions for the continuum fitting we'll do
%   Fe region
ignore(all_data, 0.95*Const_hc/6.4, 1.05*Const_hc/6.4);
%   Ne region
ignore(all_data, 0.97*Const_hc/0.8486, 1.03*Const_hc/0.8486);
%
% Replot the spectra again - use some colors:
oplot_data_counts(1,2);   %  MEG -1  red
oplot_data_counts(2,8);   %  MEG -1  orange

% Define the fitting function:
fit_fun("phabs(1)*powerlaw(1)");

% Set initial values and limits for the parameters;
% keep them all "thawed" with 0 as third argument.
set_par (1, 1.00,  0,  0.1,   10.0);
set_par (2, 0.01, 0,  1.e-4, 1.0);
set_par (3, 1.00,  0,  0.5,   2.5);

% Use Gehrels to help with low-counts bins
set_fit_statistic ("chisqr;sigma=gehrels");

set_fit_method ("lmdif;default");
()=fit_counts;
list_par;

% overplot one of the model fits
oplot_model_counts(1, 4);

plot_close();
