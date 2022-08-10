import json
import colorsys
import os
import argparse

parser = argparse.ArgumentParser(description="Generate an RGB wave effect for polychromatic.")
parser.add_argument("-d", "--duration", help="Wave period in seconds. Default is 5.", default="5")
parser.add_argument("-D", "--direction", help="Wave direction. `LR` for left to right, `RL` for right to left. Default is `LR`", default='LR')
parser.add_argument("--fps", help="Frames per seconds of the wave. Defaults to 24.", default='24')
parser.add_argument("-c", "--columns", help="Number of columns in the keyboard. Default is 22.", default="22")
parser.add_argument("-r", "--rows", help="Number of rows in the keyboard. Default is 6.", default="6")
parser.add_argument("--device", help="Name of the Razer device. Defaults to `Razer Ornata V2`. Please, enter the real name of the device, "
                                     "as it shows up in Polychromatic. You will probably need to fix the number of rows and columns"
                                     " so they fit your device, using `-r` and `-c` parameters. To know how many columns and rows your "
                                     "device has, you can create a dummy Polychromatic effect and check how many rows/columns appear in the "
                                     "matrix. Underglow should be supported with the correct values.", default="Razer Ornata V2")
parser.add_argument("-o", "--output", help="Output file path. Default is `~/.config/polychromatic/effects/wave.json`", default="~/.config/polychromatic/effects/wave.json")

args = parser.parse_args()
direction = args.direction
cols = int(args.columns)
rows = int(args.rows)
duration = float(args.duration)  # seconds
device = args.device
fps = int(args.fps)
name = args.output.split("/")[-1].split(".")[0].title()
frames = []

data = {"name": name,
        "type": 3,
        "author": "Teskann",
        "author_url": "https://github.com/Teskann/razer-waver",
        "icon": "img/options/wave.svg",
        "summary": "",
        "map_device": device,
        "map_device_icon": "keyboard",
        "map_graphic": "blackwidow_m_keys_en_GB.svg",
        "map_cols": cols,
        "map_rows": rows,
        "save_format": 8,
        "revision": 1,
        "fps": fps,
        "loop": True,
        "frames": frames
        }

nb_frames = int(duration * fps)
delta_hue_frames = 1 / nb_frames
for i_frame in range(nb_frames):
    frames.append({})
    delta_hue_col = 1 / (cols-2)
    hue = (i_frame * delta_hue_frames + 1  * delta_hue_col) % 1
    rgb = [int(255 * c) for c in colorsys.hsv_to_rgb(hue, 1, 1)]
    hex_color = "#FFFFFF".format(*rgb)
    frow_values = {}
    for i in range(rows):
        frow_values[str(i)] = hex_color
    frames[-1]['0'] = frow_values
    for i_col in range(1,cols-1):
        hue = (i_frame * delta_hue_frames + i_col * delta_hue_col) % 1
        rgb = [int(255 * c) for c in colorsys.hsv_to_rgb(hue, 1, 1)]
        hex_color = "#{:02x}{:02x}{:02x}".format(*rgb)
        row_values = {}
        for i_rows in range(rows):
            row_values[str(i_rows)] = hex_color  # Constant across rows
        frames[-1][str(i_col)] = row_values
    lrow_values = {}
    for i in range(6):
        lrow_values[str(i)] = frames[-1]['14']['0']
    frames[-1]['15'] = lrow_values
    frames[-1]['14']['5'] = frames[-1]['15']['5']
    frames[-1]['15']['5'] = frames[-1]['13']['5']
    frames[-1]['5']['5'] = frames[-1]['3']['5']
    frames[-1]['4']['5'] = frames[-1]['3']['5']
    frames[-1]['3']['5'] = frames[-1]['2']['5']
    frames[-1]['2']['5'] = frames[-1]['1']['5']
    frames[-1]['12']['5'] = frames[-1]['11']['5']
    frames[-1]['11']['5'] = frames[-1]['10']['5']
    for i in range(0,5):
        frames[-1]['15'][str(i)] = frames[-1]['14'][str(i)]
    frames[-1]['14']['0'] = frames[-1]['13']['0']
    frames[-1]['14']['5'] = frames[-1]['15']['4']
    for i in range(12,2,-1):
        frames[-1][str(i)]['4'] = frames[-1][str(i-1)]['4']

if direction == 'LR':
    data["frames"] = frames[::-1]


save_path = os.path.expanduser(args.output)
if os.path.exists(save_path):
    ans = input(f"The file {save_path} already exists. Do you want to overwrite it ? (y/[n]) ")
    if ans.lower() != 'y':
        print("Aborting ...")
        exit(-1)
try:
    with open(save_path, 'w') as f:
        f.write(json.dumps(data, indent=4))
    print("Wave effect file successfully created ! Open polychromatic to apply it on your keyboard !")
except FileNotFoundError as e:
    print(f"No such file or directory: '{save_path}'. Be sure you have "
          f"installed polychromatic ! If you have installed it, launch it and "
          f"retry. You can also use --output to save your file elsewhere.")
    exit(-1)
