import matplotlib.pyplot as plt
import numpy as np


def drawSystem(solarVector, panelVector=None):

    fig = plt.figure(figsize=(8,8))

    ax = fig.add_subplot(
        111,
        projection="3d"
    )

    ax.quiver(
        0,0,0,
        solarVector[0],
        solarVector[1],
        solarVector[2],
        color="orange",
        linewidth=3,
        label="Sol"
    )

    if panelVector is not None:

        ax.quiver(
            0,0,0,
            panelVector[0],
            panelVector[1],
            panelVector[2],
            color="blue",
            linewidth=3,
            label="Panel"
        )

    ax.set_xlim([-1,1])
    ax.set_ylim([-1,1])
    ax.set_zlim([0,1])

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    ax.legend()

    plt.show()