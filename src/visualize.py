import imageio
import os
import numpy as np
from matplotlib import pyplot, cm


def visualize(file_path: str, return_type: str = "contour"):
    with open(file_path) as f:
        results = f.readlines()

    nx = int(results[0].strip())
    ny = int(results[1].strip())
    nt = int(results[2].strip())
    xmax = float(results[5].strip())
    ymax = float(results[6].strip())
    dt = float(results[9].strip())

    u = np.zeros((ny, nx))
    v = np.zeros((ny, nx))
    p = np.zeros((ny, nx))

    start = 12
    for i in range(ny):
        result = results[start+i].strip().split()
        for j in range(nx):
            u[i][j] = float(result[j])

    start = ny + 12
    for i in range(ny):
        result = results[start+i].strip().split()
        for j in range(nx):
            v[i][j] = float(result[j])

    start = 2*ny + 12
    for i in range(ny):
        result = results[start+i].strip().split()
        for j in range(nx):
            p[i][j] = float(result[j])

    x = np.linspace(0, xmax, nx)
    y = np.linspace(0, ymax, ny)
    X, Y = np.meshgrid(x, y)
    if return_type == "contour":
        fig = pyplot.figure(figsize=(11, 7), dpi=100)
        # plotting the pressure field as a contour
        pyplot.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)
        pyplot.colorbar()
        # plotting the pressure field outlines
        pyplot.contour(X, Y, p, cmap=cm.viridis)
        # plotting velocity field
        pyplot.quiver(X, Y, u, v)
        implementation_type = "C" if ("cuda" not in file_path) else "CUDA"
        pyplot.title(f"{implementation_type} Countour Map at nt = {nt}, with dt = {dt}")

        pyplot.xlabel('X')
        pyplot.ylabel('Y')
    else:
        fig = pyplot.figure(figsize=(11, 7), dpi=100)
        pyplot.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)
        # pyplot.colorbar()
        pyplot.contour(X, Y, p, cmap=cm.viridis)
        pyplot.streamplot(X, Y, u, v)
        implementation_type = "C" if ("cuda" not in file_path) else "CUDA"
        pyplot.title(f"{implementation_type} Streamlines Map at nt = {nt}, with dt = {dt}")

        pyplot.xlabel('X')
        pyplot.ylabel('Y')
        pyplot.tight_layout()

        pyplot.savefig(f"streamline_{implementation_type}.png")


def convert_gif(file_path: str):
    with open(file_path) as f:
        results = f.readlines()
    nx = int(results[0].strip())
    ny = int(results[1].strip())
    nt = int(results[2].strip())
    xmax = float(results[5].strip())
    ymax = float(results[6].strip())
    dt = float(results[9].strip())
    startline = 12
    one_step_line = ny*3 + 1
    num_steps = int((len(results) - startline) / one_step_line)

    dict_results = {}
    for line in range(12, len(results), one_step_line):
        step = int(results[line].strip())

        u = np.zeros((ny, nx))
        v = np.zeros((ny, nx))
        p = np.zeros((ny, nx))

        start = line + 1
        for i in range(ny):
            result = results[start+i].strip().split()
            for j in range(nx):
                u[i][j] = float(result[j])

        start = ny + line + 1
        for i in range(ny):
            result = results[start+i].strip().split()
            for j in range(nx):
                v[i][j] = float(result[j])

        start = 2*ny + line + 1
        for i in range(ny):
            result = results[start+i].strip().split()
            for j in range(nx):
                p[i][j] = float(result[j])

        dict_results[step] = (u, v, p)

        # Visualisation
    FOLDER_SAVE = "fig_data/"
    if not os.path.exists(FOLDER_SAVE):
        os.makedirs(FOLDER_SAVE)

    for step in dict_results.keys():
        u, v, p = dict_results[step]

        x = np.linspace(0, xmax, nx)
        y = np.linspace(0, ymax, ny)

        X, Y = np.meshgrid(x, y)

        fig = pyplot.figure(figsize=(11, 7), dpi=100)
        # plotting the pressure field as a contour
        vmin = -3.2
        vmax = 3.2

        pyplot.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis, vmin=vmin, vmax=vmax)
        # pyplot.colorbar()
        # plotting the pressure field outlines
        pyplot.contour(X, Y, p, cmap=cm.viridis)
        # plotting velocity field
        pyplot.quiver(X, Y, u, v)
        pyplot.title(f"Countour Map at nt = {step}, with dt = {dt}")

        # pyplot.xlabel('X')
        # pyplot.ylabel('Y');
        pyplot.tight_layout()

        pyplot.savefig(os.path.join(FOLDER_SAVE, str(step).zfill(6) + ".png"))

    images = []
    filenames = sorted(os.listdir(FOLDER_SAVE))
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave('test.gif', images)
