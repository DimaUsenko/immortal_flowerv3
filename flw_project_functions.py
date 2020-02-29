import numpy as np
from shapely.geometry import LineString, Polygon
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import cv2
import glob


def on_connect(clinet, userdata, flags, rc):
    print("Connected with Code :"+str(rc))
    #client.subscribe("immortal_flower/#") turn it on if u wanna see messages during modeling


def on_message(client, userdata, msg):
    print(str(msg.payload))


def intersection(segment, plane):
    p0, p1 = np.array(segment.coords)
    q0, q1, q2 = np.array(plane.exterior)[:-1]
    vector_plane_1 = q1 - q2
    vector_plane_2 = q2 - q0
    n = np.cross(vector_plane_1, vector_plane_2) / np.linalg.norm(np.cross(vector_plane_1, vector_plane_2))
    u = p1 - p0
    w = p0 - q0
    if np.dot(n, u) == 0:
        return None
    else:
        si = np.dot(-n, w) / np.dot(n, u)
        intersection = p0 + si * u
        return intersection


def is_intersection(sun, cloud, flower):
    line = LineString([flower.point(), sun.vec()])
    p = Polygon(cloud.vec()[0:3])
    c = intersection(line, p)
    if cloud.x3 <= c[0] <= cloud.x1 and cloud.y2 <= c[1] <= cloud.y1:
        return True
    else:
        return False


def update_field(cloud_list, sun,number_of_clouds):
    for i in range(number_of_clouds):
        cloud_list[i].move()
    sun.vec()


def modeling(number_of_simulated_hours):
    img1 = cv2.imread('gift0.jpg')

    height, width, layers = img1.shape

    video = cv2.VideoWriter('MODELING.mp4', -1, 1, (width, height))
    for timer in range(0, number_of_simulated_hours * 60):
        img = cv2.imread(f'gift{timer}.jpg')
        video.write(img)

    cv2.destroyAllWindows()
    video.release()


def plotting(sun, cloud_list, flower, t,number_of_clouds):
    xs = [flower.x, (sun.vec()[0])]
    ys = [flower.y, (sun.vec()[1])]
    zs = [flower.z, (sun.vec()[2])]
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    for i in range(number_of_clouds):
        x = cloud_list[i].getx()
        y = cloud_list[i].gety()
        z = cloud_list[i].getz()
        ax.plot_trisurf(x, y, z, linewidth=0.2,color='b')
    ax.plot(xs, ys, zs, label='parametric curve',color='y')
    ax.set_xlim(-150, 150)
    ax.set_ylim(-150, 150)
    ax.set_zlim(0, 200)
    plt.xlabel('X')
    plt.ylabel('Y')
    #plt.show()
    plt.savefig(f'gift{t}.jpg')
    plt.close(fig)


def path_clear():
    for i in glob.glob("*.jpg"):
        os.remove(i)
    #for fi in glob.glob("*.mp4"):
        #os.remove(fi)
