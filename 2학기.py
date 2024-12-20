import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
from matplotlib.lines import Line2D

data = pd.read_csv("./data.csv")
del data['id']
del data['created_at']

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

colors = ['navy', 'darkgreen', 'maroon', 'purple', 'olive', 'teal', 'grey', 'orange']
weight = [0.5, 2, 0.4, 4, 5, 2, 3, 1.4]
origin = np.array([0, 0])

theta = np.linspace(0, 2 * np.pi, 8, endpoint=False)

x = np.cos(theta)
y = np.sin(theta)

emotion = []

fig, ax = plt.subplots(figsize=(20, 20))

ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)
ax.axvline(x=0, color='k', linestyle='--', alpha=0.5)

circle = plt.Circle((0, 0), 1, fill=False)
ax.add_artist(circle)

for i in range(len(theta)):
    vector = np.array([x[i], y[i]])
    emotion.append(vector)
    emotion[i] = emotion[i] * weight[i]
    ax.arrow(0, 0, emotion[i][0], emotion[i][1], head_width=0.09, head_length=0.1, fc=colors[i], ec=colors[i])

plt.xlim(-5, 5)
plt.ylim(-5, 5)
plt.title('The base of feelings')
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)

for i in range(8):
    j = 1

    while i + j < 8:
        point = emotion[i] + emotion[i + j]
        ax.fill([origin[0], emotion[i][0], point[0], emotion[i+j][0]],
                [origin[1], emotion[i][1], point[1], emotion[i+j][1]],
                alpha=0.3)

        j += 1

tag_to_vector = {
    'joy': emotion[0],
    'anticipation': emotion[1],
    'anger': emotion[2],
    'disgust': emotion[3],
    'sadness': emotion[4],
    'surprise': emotion[5],
    'fear': emotion[6],
    'trust': emotion[7]
}
emotion_labels = list(tag_to_vector.keys())

text_positions = []
text_contents = []

for idx, row in data.iterrows():
    tags = json.loads(row['tags'])
    text_position = np.array([0.0, 0.0])
  
    count = 0
    for tag in tags:
        if tag in tag_to_vector:
            text_position += tag_to_vector[tag]
            count += 1

    if count > 0:
        text_position /= count

    text_positions.append(text_position)
    text_contents.append(row['content'])

# 점 찍기
point_colors = []
for idx, row in data.iterrows():
    tags = json.loads(row['tags'])
    tag_colors = [colors[list(tag_to_vector.keys()).index(tag)] for tag in tags if tag in tag_to_vector]
    point_color = tag_colors[0] if tag_colors else 'black'
    point_colors.append(point_color)

text_positions_array = np.array(text_positions)
ax.scatter(text_positions_array[:, 0], text_positions_array[:, 1],
           color=point_colors, s=20, alpha=0.7, edgecolor='black')

annot = ax.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle='->'))
annot.set_visible(False)

def update_annot(ind: int):
    pos = text_positions[ind]
    annot.xy = pos
    text = text_contents[ind]
    annot.set_text(text)
    annot.get_bbox_patch().set_alpha(0.8)

# 마우스 포인터를 대면 실행되는 함수
def hover(event):
    vis = annot.get_visible()

    if event.inaxes == ax:
        for i, pos in enumerate(text_positions):
            distance = np.sqrt((event.xdata - pos[0]) ** 2 + (event.ydata - pos[1]) ** 2)

            if distance < 0.5:
                update_annot(i)
                annot.set_visible(True)
                fig.canvas.draw_idle()
                return

    if vis:
        annot.set_visible(False)
        fig.canvas.draw_idle()

# 모션 이벤트
fig.canvas.mpl_connect("motion_notify_event", hover)

# 범례
legend_elements = [
    Line2D([0], [0], color=colors[i], lw=1.75, label=emotion_labels[i]) 
    for i in range(len(emotion_labels))
]

ax.legend(handles=legend_elements, loc='upper right', fontsize=8, title="Emotions")

plt.show()
