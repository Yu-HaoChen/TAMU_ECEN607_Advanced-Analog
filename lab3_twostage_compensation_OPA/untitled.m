clc; clear; close all;

gm2 = 1.87e-3;  
gm8 = 8e-3;     
R1 = 65e3;     
R2 = 20e3;      
Cc = 5e-12;     
CL = 20e-12;   
R = 2/gm8; % move to LHP zero

% === calculate poles and zero ===
wp1 = -1 / (gm2 * R1 * R2 * Cc); % Wp1
wp2 = -gm2 / CL;                 % Wp2
wp3 = -1 / (R * Cc);             % Wp3
wz  = 1 / (Cc * ((1/gm2)-R));    % RHZ WZ

% === H(S) ===
s = tf('s');
H_corrected = (s + wz) / ((s - wp1) * (s - wp2) * (s - wp3)); % H(s)

% === Root Locus ===
figure;
rlocus(H_corrected); hold on;
title('Root Locus of the Three-Pole System');
xlabel('Real Axis (seconds^{-1})');
ylabel('Imaginary Axis (seconds^{-1})');
grid on;

% === mark poles and zero ===
plot(real([wp1, wp2, wp3]), imag([wp1, wp2, wp3]), 'rx', 'MarkerSize', 10, 'LineWidth', 2); 
plot(real(wz), imag(wz), 'go', 'MarkerSize', 10, 'LineWidth', 2); 

% === marker ===
text(real(wp1), imag(wp1), '  wp1', 'FontSize', 12, 'Color', 'r');
text(real(wp2), imag(wp2), '  wp2', 'FontSize', 12, 'Color', 'r');
text(real(wp3), imag(wp3), '  wp3', 'FontSize', 12, 'Color', 'r');
text(real(wz), imag(wz), '  wz', 'FontSize', 12, 'Color', 'g');

hold off;


