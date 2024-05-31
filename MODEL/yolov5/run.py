from detect import *
import os, shutil
import time, datetime

start_time = time.time()

# weights = "runs/train/face_15k/weights/best.pt"
weights = "runs/train/face_15k_2/weights/best.pt"
# weights = "runs/train/face_16k/weights/best.pt"
# weights = "runs/train/face_32k/weights/best.pt"
# weights = "runs/train/face_39k/weights/best.pt"
# weights = "runs/train/face_237k/weights/best.pt"

# source = "../datasets/sample/KakaoTalk_20240521_112502845.png"
# source = "../datasets/gstar/"
# source = "../datasets/4k/PSY - 'That That (prod. & feat. SUGA of BTS)' MV.mp4"
# source = "../datasets/4k/PSY - 'That That (prod. & feat. SUGA of BTS)' MV_frame/"
# source = "../datasets/4k/Live Aid- Queen 1985 4K & HQ Sound_frame/"
# source = "../datasets/4k/KakaoTalk_20240530_124801658_frame/"
# source = "../datasets/4k/KakaoTalk_20240530_125122880_frame/"
# source = "../datasets/4k/NewJeans 'Super Shy' Official MV_frame/"
source = "../datasets/4k/NewJeans 'Super Shy' Official MV.mp4"
# source = 0

# name = "exp"
# name = "exp1"
# name = "smaple_16k"
# name = "G-star_2023_39k"
# name = "4k_15k"
# name = "PSY - 'That That (prod. & feat. SUGA of BTS)' MV_frame_16k"
# name = "Live Aid- Queen 1985 4K & HQ Sound_frame_237k"
# name = "KakaoTalk_20240530_124801658_frame_237k"
name = "NewJeans 'Super Shy' Official MV_frame_15k_2"
# name = "NewJeans 'Super Shy' Official MV_15k_2"

if os.path.exists("runs/detect/" + name):
    shutil.rmtree("runs/detect/" + name)

run(
    weights=weights,
    source=source,
    name=name,
    # conf_thres=0.4,
    # hide_conf=True,
    # hide_labels=True,
    # line_thickness=0,
    # mosaic_type=4,
)

end_time = time.time()
running_time = str(datetime.timedelta(seconds=(end_time - start_time)))
print(running_time)
