% Script para representar el espectro de energía depositada
% Archivo: spc-NaI-enddet.txt
% Columnas: Energía (eV), Densidad de probabilidad (1/(eV*partícula)), Incertidumbre (3 sigma)

% Limpiar espacio de trabajo
clear; close all; clc;

% Nombre del archivo
filename = 'spc-NaI-enddet.txt';

% Leer datos: saltar líneas que empiezan con '#'
% Usamos readtable con opciones de formato
opts = detectImportOptions(filename, 'FileType', 'text');
opts.DataLines = [4, inf];  % Las primeras 3 líneas son comentarios
opts.VariableNames = {'Energy_eV', 'Probability_Density', 'Uncertainty'};
data = readtable(filename, opts);

% Extraer columnas
E = data.Energy_eV;          % eV
P = data.Probability_Density; % 1/(eV*particle)
dP = data.Uncertainty;       % 3 sigma

% Verificar que no haya valores anómalos (como el pico enorme)
% Se observa un valor atípico en E ≈ 1.17375e6 eV con P ≈ 1.66e-5

% Figura 1: Escala lineal
figure('Name', 'Espectro lineal', 'NumberTitle', 'off');
errorbar(E, P, dP, 'b.', 'MarkerSize', 2, 'LineWidth', 0.5);
xlabel('Energía depositada (eV)');
ylabel('Densidad de probabilidad (1/(eV·partícula))');
title('Espectro de energía depositada (escala lineal)');
grid on;
xlim([min(E) max(E)]);

% Figura 2: Escala semilogarítmica en Y (mejor para ver la cola)
figure('Name', 'Espectro semilog Y', 'NumberTitle', 'off');
semilogy(E, P, 'b.', 'MarkerSize', 2);
hold on;
% Añadir barras de error en semilog (requiere calcular límites manualmente)
% Para evitar barras negativas, usamos límites asimétricos
E_low = E;
E_high = E;
P_low = max(P - dP, 1e-35); % Evitar valores negativos/cero en log
P_high = P + dP;
% Usar errorbar con opción 'vertical' (las x son simétricas)
errorbar(E, P, P - P_low, P_high - P, 'b.', 'MarkerSize', 2, 'LineWidth', 0.5);
xlabel('Energía depositada (eV)');
ylabel('Densidad de probabilidad (1/(eV·partícula))');
title('Espectro de energía depositada (escala semilogarítmica en Y)');
grid on;
xlim([min(E) max(E)]);

% Ajustar límites Y para mejor visualización (excluyendo el pico si es necesario)
% Comentar la siguiente línea si se desea ver el pico completo
ylim([1e-35, 1e-4]);

% Figura 3: Zoom en la región de baja energía (0-500 keV) para ver la estructura
figure('Name', 'Zoom bajas energías', 'NumberTitle', 'off');
idx = E <= 5e5;  % hasta 500 keV
semilogy(E(idx), P(idx), 'b.', 'MarkerSize', 2);
hold on;
errorbar(E(idx), P(idx), dP(idx), 'b.', 'MarkerSize', 2, 'LineWidth', 0.5);
xlabel('Energía depositada (eV)');
ylabel('Densidad de probabilidad (1/(eV·partícula))');
title('Espectro de energía depositada (región de baja energía)');
grid on;
xlim([min(E(idx)) max(E(idx))]);

% Mostrar información estadística básica
fprintf('Estadísticas del espectro:\n');
fprintf('Energía máxima registrada: %.2e eV\n', max(E));
fprintf('Valor máximo de densidad de probabilidad: %.2e (en E = %.2e eV)\n', max(P), E(P==max(P)));
fprintf('Número de puntos: %d\n', length(E));

disp('Script completado. Se han generado 3 figuras.');