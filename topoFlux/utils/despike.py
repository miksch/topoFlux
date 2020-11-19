import numpy as np
import pandas as pd

"""
Limits from utespac/v&m 97

% --- DATA CONDITIONING OPTIONS See: Vickers and Mahrt 97 and envsupport.licor.com/help/EddyPro3/Content/Topics/Despiking_Raw_Stat_Screening.htm
% 1. spike removal and spike test
info.spikeTest.maxRuns = 20;  % max number of time to run through despike algorithm
info.spikeTest.windowSizeFraction = 1;  % fraction that is multiplied by info.avgPer to get width of averaging window.  Must be <= 1
info.spikeTest.maxConsecutiveOutliers = 10;  % maximum number of consecutive spikes that will be removed.  Longer segments are considered physical
info.spikeTest.maxPercent = 2; % max acceptable percentage of spikes per averaging period
% number of std's to define a spike
info.spikeTest.spikeDef.u = 3.5;
info.spikeTest.spikeDef.v = 3.5;
info.spikeTest.spikeDef.w = 5;
info.spikeTest.spikeDef.Tson = 3.5;
info.spikeTest.spikeDef.fw = 3.5;
info.spikeTest.spikeDef.irgaCO2 = 3.5;
info.spikeTest.spikeDef.irgaH2O = 3.5;
info.spikeTest.spikeDef.KH2O = 3.5;
info.spikeTest.spikeDef.cup = 3.5;
info.spikeTest.spikeDef.birdSpd = 3.5;
info.spikeTest.spikeDef.otherInstrument = 5;

% 2. absolute limits.  Hard flag if single instance occurs over averaging period
info.absoluteLimitsTest.u = [-50, 50]; % m/s
info.absoluteLimitsTest.v = [-50, 50];
info.absoluteLimitsTest.w = [-10, 10];
info.absoluteLimitsTest.Tson = [-20, 80];  % deg C
info.absoluteLimitsTest.fw = [-20, 80];
info.absoluteLimitsTest.irgaCO2 = [0, 1500]; % mg/m^3
info.absoluteLimitsTest.irgaH2O = [0, 50];  % g/m^3
info.absoluteLimitsTest.KH2O = [0, 50];
info.absoluteLimitsTest.cup = [0 50];
info.absoluteLimitsTest.birdSpd = [0 50];

% 3. wind direction
% enter +/- envelope around around tower orientation to define 'bad wind direction'
info.windDirectionTest.envelopeSize = 20;

% 4. excessive NaN test
info.nanTest.maxPercent = 52;

% 5. diagnostic tests
info.diagnosticTest.H2OminSignal = 0.7;
info.diagnosticTest.CO2minSignal = 0.7;
%info.diagnosticTest.meanGasDiagnosticLimit = 0.1; %This seems arbitraty
info.diagnosticTest.meanGasDiagnosticLimit = 10;
info.diagnosticTest.meanSonicDiagnosticLimit = 256; %This seems arbitrary
info.diagnosticTest.meanLiGasDiagnosticLimit = 220;  % Full strength is 255, less indicates problems.  See manual. 
"""