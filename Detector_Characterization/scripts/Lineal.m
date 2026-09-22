% 1. LEER LOS DATOS DESDE EL ARCHIVO
filename = 'Datos.txt';

% Leer todo el contenido del archivo como texto
texto = fileread(filename);

% Reemplazar todas las comas por puntos para evitar errores de formato
texto_corregido = strrep(texto, ',', '.');

% Extraer los números en dos columnas
datos_extraidos = textscan(texto_corregido, '%f %f');

% Asignar los canales (columna 1) y las energías (columna 2)
canales = datos_extraidos{1};
energias = datos_extraidos{2};

% 2. CÁLCULO DEL AJUSTE LINEAL Y R^2
% polyfit de grado 1 (recta)
p = polyfit(canales, energias, 1);

% Extracción de los parámetros del ajuste
m = p(1); % Pendiente (ganancia, keV/canal)
b = p(2); % Ordenada en el origen (offset, keV)

% --- NUEVO: Cálculo del coeficiente de determinación (R^2) ---
matriz_corr = corrcoef(canales, energias);
rsq = matriz_corr(1,2)^2;

% Mostrar la ecuación y el R^2 en la consola
fprintf('\n--- Resultados de la Calibración ---\n');
fprintf('Ecuación: E = %.4f * Canal %+.4f keV\n', m, b);
fprintf('Coeficiente de correlación (R^2): %.6f\n\n', rsq);

% Preparar datos para dibujar la línea de ajuste
x_recta = linspace(min(canales) - 50, max(canales) + 50, 100);
y_recta = polyval(p, x_recta);

% 3. CREACIÓN DE LA GRÁFICA
figure;
% Dibujar los puntos reales
plot(canales, energias, 'ko', 'MarkerSize', 8, 'MarkerFaceColor', 'r');
hold on;
% Dibujar la línea de tendencia
plot(x_recta, y_recta, 'b-', 'LineWidth', 2);
hold off;

% Formato y etiquetas de la gráfica
title('Calibración en Energía del Detector Gamma');
xlabel('Canal (C)');
ylabel('Energía (keV)');
grid on;

% Añadir una leyenda que incluya la ecuación y el R^2
leyenda_ajuste = sprintf('Ajuste: E = %.3f \\cdot C %+.3f (R^2 = %.5f)', m, b, rsq);
legend('Datos Experimentales', leyenda_ajuste, 'Location', 'northwest');