from flask import redirect, flash, Blueprint, render_template, request, jsonify,url_for, send_file
import cv2
import shutil
import os
import sys
from flask import Flask, render_template, send_file
import subprocess
from threading import Thread
from flask import copy_current_request_context

# detect.py 파일이 있는 디렉토리 경로
# c:\Users\kdp\KDT-5\wk_Project\WEB
root_dir = os.path.dirname(os.path.dirname(__file__))


detect_dir = os.path.join(root_dir, 'static', 'model', 'yolov5')

# sys.path에 detect.py가 있는 디렉토리 경로를 추가
sys.path.append(detect_dir)

# 이제 detect.py를 import 할 수 있음
from detect import *



# #bp instance
databp = Blueprint(name='DATA',
                   import_name= __name__,
                   static_folder= 'templates',
                   url_prefix='/input')

# upload 폴더, download 폴더 삭제
upload_directory = os.path.join(root_dir, 'static', 'upload')
upload_file_path = os.path.join(root_dir, 'static', 'upload', 'video.mp4')

download_directory = os.path.join(root_dir, 'static', 'download')
download_file_path = os.path.join(root_dir, 'static', 'download', 'de_video.mp4')

if os.path.exists(upload_directory):
    shutil.rmtree(upload_directory)
    
if os.path.exists(download_directory):
    shutil.rmtree(download_directory)

if os.path.exists(os.path.join(root_dir, 'static', 'model', 'yolov5', 'runs', 'detect')):
    shutil.rmtree(os.path.join(root_dir, 'static', 'model', 'yolov5', 'runs', 'detect'))


# 비디오 인코딩 함수
def encode_video(input_path, output_path):
    command = [
        'ffmpeg', '-y', '-i', input_path,
        '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental',
        output_path
    ]
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Command executed successfully")
        print("Output:", result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error {e.returncode}")
        print("Output:", e.stdout.decode())
        print("Error:", e.stderr.decode())


# /input 페이지
#url 메인 페이지 기능
@databp.route('/') #http://127.0.0.1:5000/input
def input_data():
    if os.path.exists(upload_directory):
        shutil.rmtree(upload_directory)
        
    if os.path.exists(download_directory):
        shutil.rmtree(download_directory)

    if os.path.exists(os.path.join(root_dir, 'static', 'model', 'yolov5', 'runs', 'detect')):
        shutil.rmtree(os.path.join(root_dir, 'static', 'model', 'yolov5', 'runs', 'detect'))
    return  render_template('input.html')


# /input/preview/ 페이지
# 비디오 업로드 및 미리보기 기능
@databp.route('/preview/', methods=['POST'])
def upload_file():
    # 디렉토리 다시 생성
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)
    
    if os.path.exists(download_directory):
        shutil.rmtree(download_directory)

    if os.path.exists(os.path.join(root_dir, 'static', 'model', 'yolov5', 'runs', 'detect')):
        shutil.rmtree(os.path.join(root_dir, 'static', 'model', 'yolov5', 'runs', 'detect'))
    
    # 비디오 파일
    file = request.files['file']

    file.save(upload_file_path)

    output_path = os.path.join(upload_directory, 'preview.mp4')
    
    # 프리뷰 비디오 인코딩
    encode_video(upload_file_path, output_path)

    return render_template('preview.html', file_path=output_path)



@databp.route('/upload/', methods=['POST'])
def run_model():

    # 모드 선택 : 기본값 타원 블러 
    drop_down = request.form.get('MODE')
    if drop_down == 'mode1':
        mode = 1
    elif drop_down == 'mode2':
        mode = 2
    elif drop_down == 'mode3':
        mode = 3
    elif drop_down == 'mode4':
        mode = 4
    else:
        mode = 4

    # YOLO 모델 실행 및 결과 파일 경로 가져오기

    result_path = run_yolo_detection(upload_file_path,mode)
    return redirect(url_for('DATA.output', result = result_path))


# YOLO 모델 실행
def run_yolo_detection(file_path, mode):
    name = 'de_id'
    # YOLO 결과 파일 경로: 파일 존재하면 삭제
    download_directory = os.path.join(root_dir, 'static', 'model', 'yolov5', 'runs', 'detect', name)

    # YOLOv5 모델 실행
    run(
        weights=os.path.join(root_dir, 'static', 'model', 'yolov5', 'runs', 'train', 'face_49k', 'weights', 'best.pt'),
        source=file_path,
        hide_conf=True,
        hide_labels=True,
        line_thickness=0,
        mosaic_type=mode,
        name=name,
        conf_thres=0.5,
    )

    # 오디오 입히기

    save_path = os.path.join(root_dir, 'static', 'model', 'yolov5', 'runs', 'detect', name, 'video.mp4')

    
    # download 폴더 생성
    
    if not os.path.exists(os.path.dirname(download_file_path)):
        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)

    # 비식별화 비디오 인코딩
    encode_video(save_path, download_file_path)

    return download_file_path




@databp.route('/result/', methods=['GET'])
def output():
    result_path = request.args.get('result')
    if result_path and os.path.exists(result_path):
        # 파일 다운로드 링크를 생성하여 템플릿에 전달
        return render_template('result.html', result=result_path)
    else:
        flash('결과를 찾을 수 없습니다')
        return render_template('result.html', result=None)

@databp.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    # 다운로드할 파일 경로
    file_path = os.path.join(root_dir, 'static', 'download', filename)
    # 파일 다운로드
    return send_file(file_path, as_attachment=True)