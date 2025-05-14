% original script for Matlab version R2017 by Tom O'haver, 2018. Modified
% by P. Zijlstra, 2025.

clear all; close all; clc

% === input parameters ===
% signal
A_sig=1; % signal amplitude (V)
f_sig=5; % signal frequency (rad/s)
integr = 200; % integration time in periods
SNR = 1; % SNR of the signal, noise is shotnoise (white spectrum)

% reference
f_ref=4.997; % Modulation frequency (rad/s)

% === end input ===
% =================

% Create signal and noisy baseline2
phi_sig=0; % absolute phase of signal (rad)
x=0:.1:integr*2*pi/(f_sig); % time axis (s)
noise=1/SNR*randn(size(x)); % noise
baseline=noise+40; % noise + baseline
y=A_sig.*(1+sin(f_sig.*x+phi_sig)); % pure signal
ynoise=y+baseline; % noisy signal
% calculate SNR of original signal
SignalToNoiseRatio=A_sig/std(baseline);


% Generate reference
phi_ref=0; % absolute phase of reference (rad)
reference=sin(f_ref.*x+phi_ref); % 50 percent duty-cycle sine wave modulation
% Synchronous Detection (e.g. Lock-in amplifier)
dy=ynoise.*reference;
V_avg=mean(dy);


 
%% plotting
figure('Position',[50 50 500 600])
subplot(3,2,3); plot(x,reference,'Color',"#77AC30"); xlim([0 10]); xlabel('time (s)'); ylabel('V_{ref} (V)')
title(strjoin(['reference f =' string(f_ref) 'rad/s']))

subplot(3,2,1); plot(x,y,'r'); xlim([0 10]); xlabel('time (s)'); ylabel('V_{s} (V)')
title(strjoin(['signal f =' string(f_sig) 'rad/s']))

subplot(3,2,2);plot(x,ynoise,'r'); xlim([0 10]); ylim([0 1.1*max(ynoise)]); xlabel('time (s)'); ylabel('V_{s} (V)')
title(strjoin(['signal + noise, SNR =' string(SNR)]))

subplot(3,2,4); plot(x,dy,'Color',"#EDB120"); xlim([0 10]); xlabel('time (s)'); ylabel('V_{s} (V)')
title('Mixed signal V_p')

subplot(3,2,[5 6]); barh(V_avg); xlabel('recovered V_{avg} (V)'); xlim([0 1])
legend(strjoin(['integrated over ' string(integr) ' periods']))
set(gca,'ytick',[])
