# heat pump model from https://oemof.github.io/heat-pump-tutorial/model/tespy-simple.html

from tespy.components import SimpleHeatExchanger, CycleCloser, Compressor, Valve
from tespy.connections import Connection
from tespy.networks import Network




wf = "R290"
nwk = Network(p_unit="bar", T_unit="C", iterinfo=False)



cp = Compressor("compressor")
ev = SimpleHeatExchanger("evaporator")
cd = SimpleHeatExchanger("condenser")
va = Valve("expansion valve")
cc = CycleCloser("cycle closer")


c0 = Connection(va, "out1", cc, "in1", label="0")
c1 = Connection(cc, "out1", ev, "in1", label="1")
c2 = Connection(ev, "out1", cp, "in1", label="2")
c3 = Connection(cp, "out1", cd, "in1", label="3")
c4 = Connection(cd, "out1", va, "in1", label="4")


nwk.add_conns(c0, c1, c2, c3, c4)



# connections
c2.set_attr(T=2)
c4.set_attr(T=40)

# components
cp.set_attr(eta_s=0.8)
cd.set_attr(Q=-9.1e3)


# connections
c2.set_attr(fluid={wf: 1}, x=1.0)
c4.set_attr(x=0.0)

# components
cd.set_attr(pr=1)
ev.set_attr(pr=1)



nwk.solve("design")
nwk.print_results()



cp.P.val

nwk.results["Compressor"].loc["compressor", "P"]



cop = abs(cd.Q.val) / cp.P.val
cop




eta_s_max = 0.8
eta_s_min = 0.4

i = 0

while True:
    eta_s = (eta_s_max + eta_s_min) / 2
    cp.set_attr(eta_s=eta_s)
    nwk.solve("design")
    COP = abs(cd.Q.val) / cp.P.val
    if round(COP - 4.9, 3) > 0:
        eta_s_max = eta_s
    elif round(COP - 4.9, 3) < 0:
        eta_s_min = eta_s
    else:
        break

    if i > 10:
        print("no solution found")
        break

    i += 1

efficiency = round(cp.eta_s.val, 3)




abs(cd.Q.val) / cp.P.val


########################### Auswertung #############################


import pandas as pd
import numpy as np


temperature_range = np.arange(-10, 21)
results = pd.DataFrame(index=temperature_range, columns=["COP", "COP_carnot"])

cp.eta_s.val

for T in temperature_range:
    c2.set_attr(T=T - 5)
    nwk.solve("design")
    results.loc[T, "COP"] = abs(cd.Q.val) / cp.P.val
    results.loc[T, "COP_carnot"] = c4.T.val_SI / (c4.T.val - c2.T.val)

results["efficiency"] = results["COP"] / results["COP_carnot"]



from matplotlib import pyplot as plt


T_for_eta = 7
eta_const = results.loc[T_for_eta, "efficiency"]

fig, ax = plt.subplots(2, sharex=True)

label = "$\mathrm{COP}_\mathrm{c}$"
ax[0].plot(temperature_range, results["COP_carnot"], label=label)
ax[0].plot(temperature_range, results["COP"], label="$\mathrm{COP}$")
label = "$\mathrm{COP}$: $\eta\left(T=" + str(T_for_eta) + "°C\\right)=" + str(round(eta_const, 3)) + "$"
ax[0].plot(temperature_range, results["COP_carnot"] * eta_const, label=label)
ax[0].set_ylabel("COP")
ax[0].legend()

ax[1].plot(temperature_range, results["efficiency"], color="tab:orange")
ax[1].plot(temperature_range, [eta_const for _ in temperature_range], color="tab:green")
ax[1].set_ylabel("Efficiency factor")

ax[1].set_xlabel("Ambient temperature in °C")

[(a.grid(), a.set_axisbelow(True)) for a in ax];


plt.show()
#plt.close()


export = results[["COP"]]
export.index.names = ["temperature"]
export.to_csv("waermepumpe/model/COP-T-tespy.csv")