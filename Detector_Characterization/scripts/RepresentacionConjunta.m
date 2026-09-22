% Script de Comparación: Espectros Simulados vs Experimental (Con Calibración Integrada)
clear; clc; close all;

%% ---------------------------------------------------------
% 1. CALIBRACIÓN DE ENERGÍA (A partir de Datos.txt)
% ---------------------------------------------------------
filename_cal = 'Datos.txt';
if ~isfile(filename_cal)
    warning('Archivo %s no encontrado. Selecciona el archivo de calibración.', filename_cal);
    [file, path] = uigetfile('*.txt', 'Selecciona el archivo Datos.txt');
    if isequal(file, 0), error('Operación cancelada.'); else, filename_cal = fullfile(path, file); end
end

% Leer y procesar datos de calibración
texto = fileread(filename_cal);
texto_corregido = strrep(texto, ',', '.');
datos_extraidos = textscan(texto_corregido, '%f %f');

canales_cal = datos_extraidos{1};
energias_cal = datos_extraidos{2};

% Ajuste lineal
p = polyfit(canales_cal, energias_cal, 1);
cal_m = p(1); % Pendiente (ganancia)
cal_b = p(2); % Offset (ordenada en el origen)

fprintf('\n--- Resultados de la Calibración Integrada ---\n');
fprintf('Ecuación obtenida: E = %.4f * Canal %+.4f keV\n\n', cal_m, cal_b);

%% ---------------------------------------------------------
% 2. CARGAR DATOS SIMULADOS (.dat y .txt)
% ---------------------------------------------------------
% 2.1 Archivo original .dat
file_sim = 'spc-NaI-enddet.dat';
if ~isfile(file_sim)
    warning('Archivo %s no encontrado. Selecciona el archivo de simulación.', file_sim);
    [file, path] = uigetfile('*.dat', 'Selecciona el archivo de simulación (.dat)');
    if isequal(file, 0), error('Operación cancelada.'); else, file_sim = fullfile(path, file); end
end

opts = detectImportOptions(file_sim, 'FileType', 'text');
opts.DataLines = [4, inf];
opts.VariableNames = {'Energy_eV', 'Probability_Density', 'Uncertainty'};
data_sim = readtable(file_sim, opts);

% Extraer y convertir Energía de eV a keV
E_sim_keV = data_sim.Energy_eV / 1000; 
P_sim = data_sim.Probability_Density;

% 2.2 Archivo espectro_ideal.txt
file_ideal = 'espectro_ideal.txt';
if ~isfile(file_ideal)
    warning('Archivo %s no encontrado.', file_ideal);
    [file, path] = uigetfile('*.txt', 'Selecciona el archivo espectro_ideal.txt');
    if isequal(file, 0), error('Operación cancelada.'); else, file_ideal = fullfile(path, file); end
end
% Leer ignorando las líneas que empiezan con '#'
data_ideal = readmatrix(file_ideal, 'CommentStyle', '#');
E_ideal_keV = data_ideal(:, 1) * 1000; % Convertir de MeV a keV
P_ideal = data_ideal(:, 2);

% 2.3 Archivo espectro_realista.txt
file_realista = 'espectro_realista.txt';
if ~isfile(file_realista)
    warning('Archivo %s no encontrado.', file_realista);
    [file, path] = uigetfile('*.txt', 'Selecciona el archivo espectro_realista.txt');
    if isequal(file, 0), error('Operación cancelada.'); else, file_realista = fullfile(path, file); end
end
% Leer ignorando las líneas que empiezan con '#'
data_realista = readmatrix(file_realista, 'CommentStyle', '#');
E_realista_keV = data_realista(:, 1) * 1000; % Convertir de MeV a keV
P_realista = data_realista(:, 2);

% ---------------------------------------------------------
% 2.4 ESCALAMIENTO DEL SIMULADO (.dat) AL RESTO
% ---------------------------------------------------------
% Igualamos el pico máximo del .dat con el pico máximo del MCNP realista
% para que sean perfectamente comparables en el mismo eje Y.
factor_escala = max(P_realista) / max(P_sim);
P_sim = P_sim * factor_escala;

%% ---------------------------------------------------------
% 3. CARGAR DATOS EXPERIMENTALES (.Spe)
% ---------------------------------------------------------
file_spe = fullfile('Data', 'cesio1.Spe'); 
if ~isfile(file_spe)
    [file, path] = uigetfile('*.Spe', 'Selecciona el archivo experimental (.Spe)');
    if isequal(file, 0), error('Operación cancelada.'); else, file_spe = fullfile(path, file); end
end

lines = readlines(file_spe);
idxStart = find(startsWith(lines, "$DATA:"));
idxEnd = find(startsWith(lines, "$ROI:"));

counts_exp = str2double(lines(idxStart + 2 : idxEnd - 1));
channels = 0:(length(counts_exp)-1);

%% ---------------------------------------------------------
% 4. APLICAR CALIBRACIÓN Y ANÁLISIS DE PICOS 
% ---------------------------------------------------------
% Aplicamos la ecuación calculada en el Paso 1
E_exp_keV = (channels * cal_m) + cal_b;

% Suavizado y detección de picos 
counts_analisis = smoothdata(counts_exp, 'sgolay', 15);
umbral_prominencia = max(counts_analisis) * 0.05; 
altura_minima = max(counts_analisis) * 0.05; 

[picos_conteos, picos_idx, anchuras_fwhm, prominencias] = findpeaks(...
    counts_analisis, ...
    'MinPeakProminence', umbral_prominencia, ...
    'MinPeakHeight', altura_minima, ...
    'MinPeakDistance', 25, ...                
    'WidthReference', 'halfprom');             

% Convertir temporalmente los índices de los picos a energía
picos_energia_temp = E_exp_keV(picos_idx);

% Filtrar picos: Solo conservar aquellos cuya energía sea mayor o igual a 500 keV
idx_validos = picos_energia_temp >= 500; 

picos_idx = picos_idx(idx_validos);
picos_conteos = picos_conteos(idx_validos);
picos_energia = picos_energia_temp(idx_validos);
anchuras_fwhm = anchuras_fwhm(idx_validos);
prominencias = prominencias(idx_validos);

%% ---------------------------------------------------------
% 5. GRÁFICA DE COMPARACIÓN (Doble Eje Y - Escala Dinámica Proporcional)
% ---------------------------------------------------------
figure('Name', 'Comparación Simulación vs Experimental', 'NumberTitle', 'off', 'Color', 'w', 'Position', [100, 100, 950, 550]);

% --- Cálculo de límites dinámicos ---
E_min_escala = 150; % keV

% Experimental: Usamos el máximo normal
idx_exp_escala = E_exp_keV >= E_min_escala;
max_y_exp = max(counts_exp(idx_exp_escala));

% Simulaciones: Ignorar picos de resonancia infinitos usando el percentil 99
idx_sim_escala = E_sim_keV >= E_min_escala;
idx_realista_escala = E_realista_keV >= E_min_escala;

max_y_sim_dat = prctile(P_sim(idx_sim_escala), 99); 
max_y_sim_realista = prctile(P_realista(idx_realista_escala), 99); 

% Tomamos el máximo entre los continuos para escalar bien el eje Y izquierdo
max_y_sim_continuo = max(max_y_sim_dat, max_y_sim_realista);

% --- Eje Y Izquierdo: Simulaciones ---
yyaxis left;
plot(E_sim_keV, P_sim, 'b-', 'LineWidth', 1.5, 'DisplayName', 'Simulado (.dat)');
hold on;
plot(E_ideal_keV, P_ideal, 'g--', 'LineWidth', 1.2, 'DisplayName', 'MCNP Ideal (sin GEB)');
plot(E_realista_keV, P_realista, 'm-.', 'LineWidth', 1.5, 'DisplayName', 'MCNP Realista (con GEB)');

ylabel('Magnitud Simulada Normalizada', 'Color', 'b', 'FontWeight', 'bold');
set(gca, 'YColor', 'b');
% Autoajuste: Multiplicamos el continuo por 2.5 para igualar la proporción
ylim([0, max_y_sim_continuo * 2.5]); 

% --- Eje Y Derecho: Experimental ---
yyaxis right;
plot(E_exp_keV, counts_exp, 'k-', 'LineWidth', 1.2, 'DisplayName', 'Experimental (Cs-137)');
ylabel('Conteos (Experimental)', 'Color', 'k', 'FontWeight', 'bold');
set(gca, 'YColor', 'k');
% Autoajuste: Máximo experimental + 15% de margen visual
ylim([0, max_y_exp * 1.15]); 

% Marcar los picos experimentales
plot(picos_energia, picos_conteos, 'rv', 'MarkerFaceColor', 'r', 'MarkerSize', 6, 'HandleVisibility', 'off');

% Etiquetas de Energía para los picos
for i = 1:length(picos_idx)
    etiqueta = sprintf(' %.1f keV', picos_energia(i));
    text(picos_energia(i), picos_conteos(i), etiqueta, ...
         'FontSize', 9, 'Color', 'r', 'VerticalAlignment', 'bottom');
end

% --- Estética General ---
title('Comparación Múltiple de Espectros: Simulaciones vs Experimental', 'FontSize', 14, 'FontWeight', 'bold');
xlabel('Energía (keV)', 'FontSize', 12, 'FontWeight', 'bold');
xlim([0, 1500]); 
grid on;
legend('Location', 'northeast');

fprintf('Comparación generada con éxito (Simulaciones normalizadas para comparación visual).\n');