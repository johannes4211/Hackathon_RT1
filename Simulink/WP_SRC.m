%% === 1. CSV-Daten einlesen ===
T = readtable('Daten_Hackathon.csv');
T.timestamp = datetime(T.timestamp, "InputFormat", "yyyy-MM-dd HH:mm:ss");
dt = 300;  % 5 Minuten in Sekunden
n = height(T);


%% === 2. Systemparameter ===
A_PV = 100; eta_PV = 0.25;
C = 3e6; R = 3;
T_set = 20; T_min = 18; T_max = 22;
E_th_max = 10e3; E_th = 5e3;
E_bat_max = 5e3; E_bat = 2.5e3;
a = 6; b = 0.1;
Q_wp_max = 5000;  % Max. thermische WP-Leistung [W]

T_in = zeros(n,1); T_in(1) = 20;

sampleTime = 5;
numSteps = length(T.Aussentemperatur__C_);
time = sampleTime*(0:numSteps-1);
data = T.Aussentemperatur__C_;
simin = timeseries(data,time);

for t = 2:n
    Tout = T.Aussentemperatur__C_(t);
    T_in(t) = T_in(t-1) + (1 / C) * ((Tout - T_in(t-1)) / R + 0);
end;
plot(T_in)