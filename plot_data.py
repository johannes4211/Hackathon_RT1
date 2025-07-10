import pandas as pd
import matplotlib.pyplot as plt




# Path to your CSV file
csv_path = "Daten_Hackathon.csv"

# Read the CSV file
df = pd.read_csv(csv_path, parse_dates=['timestamp'])

# Set timestamp as index for easier plotting
df.set_index('timestamp', inplace=True)

# List of columns to plot (excluding timestamp)
columns_to_plot = [
    'GHI',
    'DHI',
    'Aussentemperatur [°C]',
    'Solarthermie_Erzeugung [W] ',
    'Bedarf_thermisch [W]',
    'Strompreis [€/Wh]',
    'PV_Erzeugung',
    'Bedarf_elektrisch [W]'
]

# Plot each column in a separate subplot
fig, axs = plt.subplots(len(columns_to_plot), 1, figsize=(12, 2.5 * len(columns_to_plot)), sharex=True)
for i, col in enumerate(columns_to_plot):
    axs[i].plot(df.index, df[col])
    axs[i].set_ylabel(col)
    axs[i].grid(True)

axs[2].set_ylabel("Aussen \n -temperatur \n [°C]")
axs[3].set_ylabel("Solarthermie \nErzeugung \n [W] ")
axs[4].set_ylabel("Bedarf \n thermisch \n [W]")
axs[5].set_ylabel("Strompreis \n [€/Wh]")
axs[6].set_ylabel("PV \n Erzeugung")
axs[7].set_ylabel("Bedarf \n elektrisch \n [W]")

axs[-1].set_xlabel('Zeit')

plt.tight_layout()
plt.show()

