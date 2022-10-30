import cv2
import os
import youtube_dl
import sys
import numpy as np

videos = [
    # {
    #     "link": "https://www.youtube.com/watch?v=CI7Dxbt_ayk",
    #     "filename": "sentry_bright"
    # },
    {
        "link": "https://github.com/uw-advanced-robotics/aruw-vision-platform-2019/raw/master/.github/sentinel_practice-opt.gif",
        "filename": "sentry_practice"
    },
    {
        "link": "https://github.com/uw-advanced-robotics/aruw-vision-platform-2019/raw/master/.github/ohio23-opt.gif",
        "filename": "competition_gif1"
    },
    {
        "link": "https://github.com/uw-advanced-robotics/aruw-vision-platform-2019/raw/master/.github/ohio48-opt.gif",
        "filename": "competition_gif2"
    },
    {
        "link": "https://github.com/TAMU-Robomasters/cv_main/raw/master/data/short_clip.mp4",
        "filename": "TAMU_short_clip"
    },
    {
        "link": "https://github.com/TAMU-Robomasters/cv_main/raw/master/data/test_video.mp4",
        "filename": "TAMU_test_video"
    },
    {
        "link": "https://github.com/TAMU-Robomasters/cv_main/raw/master/data/test.avi",
        "filename": "TAMU_game_footage"
    },
    # {
    #     "link": "link to video",
    #     "filename": "file name to save video to"
    # }
]
folder = "CVideos"

def download(video):
    print("Downloading "+video.get("filename")+" from "+video.get("link")+" ... ", end="")
    save_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")  # supressing print
    ydl_opts = {
        "outtmpl": folder+"/"+video.get("filename")+".%(ext)s"
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video.get("link")])
    sys.stdout = save_stdout # enabling print
    print("finished")

def downloadAll(refreshAll=False):
    def file_exists(filename):
        for file in os.listdir(folder):
            if os.path.splitext(file)[0] == filename:
                return True
        return False
    if not os.path.isdir(folder):
        os.makedirs(folder)
    for video in videos:
        if not file_exists(video.get("filename")):
            download(video)

def imagefeed(cvfunction):
    print("here for now")

def videofeed(cvfunction, file=None, sidebyside=False):
    play = False

    def feedfile(filename):
        nonlocal play

        video = cv2.VideoCapture(folder+"/"+filename)
    
        while True:
            success,frame = video.read()
            if success:
                image = cvfunction(frame)
                if sidebyside:

                    original_shape = frame.shape
                    augmented_shape = image.shape

                    if (original_shape[0] > augmented_shape[0]):
                        image.resize(original_shape[0],augmented_shape[1],augmented_shape[2])
                    elif (augmented_shape[0] > original_shape[0]):
                        image.resize(augmented_shape[0],original_shape[1],original_shape[2])
                    
                    THEsidebyside = np.concatenate((frame, image), axis=1)

                    cv2.imshow("CVideos", THEsidebyside)
                else:
                    cv2.imshow("CVideos", image)
            else:
                return
            key = cv2.waitKey(60 if play else 0)
            if key == ord(' '):
                play = not play
            if key == 13: # return key
                return

    if not file:
        for filename in os.listdir(folder):
            feedfile(filename)
    else:
        feedfile(file)


downloadAll()