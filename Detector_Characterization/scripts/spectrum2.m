% Initial environment cleanup
clear; clc; close all;

% 1. Definir ruta del archivo
filename = fullfile('Data', 'cesio1.Spe'); 

% --- Verificación de existencia ---
if ~isfile(filename)
    fprintf('Archivo no encontrado en %s. Por favor, selecciónalo manualmente.\n', filename);
    [file, path] = uigetfile('*.Spe', 'Selecciona el archivo de espectro (.Spe)');
    if isequal(file, 0)
        error('Operación cancelada por el usuario. No se puede continuar sin un archivo.');
    else
        filename = fullfile(path, file);
    end
end

% 2 & 3. Lectura inteligente y sección de datos
lines = readlines(filename);
idxStartLine = find(startsWith(lines, "$DATA:"));
idxEndLine = find(startsWith(lines, "$ROI:"));

if isempty(idxStartLine) || isempty(idxEndLine)
    error('El archivo no tiene el formato esperado (faltan etiquetas $DATA o $ROI).');
end

% 4 & 5. Extraer cuentas y crear eje de canales
counts = str2double(lines(idxStartLine + 2 : idxEndLine - 1));
channels = 0:(length(counts)-1);

% ---------------------------------------------------------
% 5.5. Calibración de Energía
% ---------------------------------------------------------
% ¡IMPORTANTE! Sustituye estos valores por los de la calibración de tu detector.
% E = m * Canal + n
cal_m = 1.0; % Pendiente (keV / canal)
cal_n = 0.0; % Intersección (keV)

% ---------------------------------------------------------
% 6. Análisis de Picos (Máximos y FWHM)
% ---------------------------------------------------------
% Suavizamos la señal para mitigar el ruido estadístico (Poisson).
counts_analisis = smoothdata(counts, 'sgolay', 15);

% Ajustes de sensibilidad
umbral_prominencia = max(counts_analisis) * 0.05; 
altura_minima = max(counts_analisis) * 0.05; 

[picos_conteos, picos_canales, anchuras_fwhm, prominencias] = findpeaks(...
    counts_analisis, channels, ...
    'MinPeakProminence', umbral_prominencia, ...
    'MinPeakHeight', altura_minima, ...
    'MinPeakDistance', 25, ...                
    'WidthReference', 'halfprom');             

% --- Filtro de exclusión: Canal 80 ---
canal_minimo = 80;
idx_validos = picos_canales >= canal_minimo; 

% Aplicamos el filtro a todos los vectores
picos_canales = picos_canales(idx_validos);
picos_conteos = picos_conteos(idx_validos);
anchuras_fwhm = anchuras_fwhm(idx_validos);
prominencias = prominencias(idx_validos);

% --- Cálculo de la Energía de los Picos ---
picos_energia = (picos_canales * cal_m) + cal_n;

% ---------------------------------------------------------
% Mostrar resultados en la consola de comandos
% ---------------------------------------------------------
fprintf('\n--- Resultados del Análisis de Picos (Rayos X / Gamma) ---\n');
fprintf('Filtro: Picos por debajo del canal %d han sido excluidos.\n', canal_minimo);
fprintf('Calibración usada: E = %.4f * Canal + %.4f\n', cal_m, cal_n);
fprintf('----------------------------------------------------------\n');

if isempty(picos_canales)
    fprintf('No se encontraron picos con los criterios actuales.\n');
else
    for i = 1:length(picos_canales)
        fprintf('Pico %d: Canal = %6.1f | Energía = %6.1f keV | Conteos = %6.0f | FWHM = %5.2f canales\n', ...
            i, picos_canales(i), picos_energia(i), picos_conteos(i), anchuras_fwhm(i));
    end
end
fprintf('----------------------------------------------------------\n\n');

% ---------------------------------------------------------
% 7. Creación del Gráfico (Plot) 
% ---------------------------------------------------------
figure('Name', 'Spettro Gamma / Raggi X', 'NumberTitle', 'off', 'Color', 'w');
plot(channels, counts, 'k-', 'LineWidth', 1.2); 
hold on;

% Marcar los picos
plot(picos_canales, picos_conteos, 'rv', 'MarkerFaceColor', 'r', 'MarkerSize', 6);

% Dibujar FWHM y Etiquetas de Energía
for i = 1:length(picos_canales)
    altura_fwhm = picos_conteos(i) - prominencias(i)/2;
    line([picos_canales(i) - anchuras_fwhm(i)/2, picos_canales(i) + anchuras_fwhm(i)/2], ...
         [altura_fwhm, altura_fwhm], 'Color', 'b', 'LineWidth', 2);
     
    % Etiqueta con Energía y FWHM
    etiqueta = sprintf(' %.1f keV\n FWHM: %.1f', picos_energia(i), anchuras_fwhm(i));
    text(picos_canales(i) + 15, picos_conteos(i), etiqueta, ...
         'FontSize', 9, 'Color', 'r', 'VerticalAlignment', 'bottom');
end
hold off;

% Estética
title('Espectro de Emisión y Análisis de Picos', 'FontSize', 14, 'FontWeight', 'bold');
xlabel('Canal', 'FontSize', 12);
ylabel('Conteos', 'FontSize', 12);
xlim([0 max(channels)]); % Ajuste dinámico del límite X
grid on;

% 8. Guardado automático
if ~exist('Figures', 'dir')
    mkdir('Figures');
end

try
    exportgraphics(gcf, 'Figures/spettro_analizado.png', 'Resolution', 300);
    fprintf('Gráfico guardado en Figures/spettro_analizado.png\n');
catch
    warning('No se pudo exportar la imagen. Verifica los permisos de escritura.');
end