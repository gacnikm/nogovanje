import os
import random

import matplotlib.pyplot as plt
import numpy as np
import matplotlib._color_data as mcd

from db import db, Igralec

PATH = os.path.dirname(os.path.abspath(__file__))

db.init(os.path.join(PATH, 'db.sqlite'))
db.connect()

# naključne barve
barve_ekip = {}
ekipe = [l.ekipa for l in Igralec.select(Igralec.ekipa.distinct())]
for ekipa in ekipe:
    color = random.choice(list(set(mcd.CSS4_COLORS.values()) - set(barve_ekip.values())))
    barve_ekip[ekipa] = color

plt.tight_layout()

fig = plt.figure(figsize=(8, 40))

ax = fig.subplots()

igralci = []
rokovanja = []
barve = []
ekipe = []

for i, (rokovanj, ime, ekipa) in enumerate(
        Igralec.select(Igralec.rokovanj, Igralec.ime, Igralec.ekipa).order_by(Igralec.rokovanj.desc()).tuples()):
    igralci.append(ime)
    rokovanja.append(rokovanj)
    barve.append(barve_ekip[ekipa])
    ekipe.append(ekipa)

y_pos = np.arange(0, len(igralci))

ax.barh(y_pos, rokovanja, 0.75, align='center',
        color=barve, ecolor='black', tick_label=igralci)

ax.invert_yaxis()
ax.set_xlabel('Število rokovanj')
ax.set_title('Število rokovanj v sezoni 18/19, do 24. kroga')

for i, v in enumerate(rokovanja):
    # št rokovanj
    ax.text(v + 3, i + .25, str(v), color='blue', fontweight='bold')

    # ekipa
    if v < 100:
        ax.text(v + 30, i + .25, ekipe[i], color='blue', fontweight='bold')
    else:
        ax.text(3, i + .25, ekipe[i], color='blue', fontweight='bold')

plt.savefig('rokovanja.png', bbox_inches='tight')
