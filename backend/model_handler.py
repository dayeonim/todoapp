import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
import os

class ModelHandler:
    """이상행동 감지 모델 핸들러"""
    
    def __init__(self, model_path='models/abnormal_detector.h5', use_no_normal_model=False):
        self.model_path = model_path
        self.model = None
        self.use_no_normal_model = use_no_normal_model
        self.confidence_threshold = 0.6  # 정상 없는 모델용 임계값
        
        # 정상 데이터 없는 모델 사용 시
        if use_no_normal_model:
            self.model_path = 'models/abnormal_detector_no_normal.h5'
            self.classes = [
                'fall',        # 전도
                'vandalism',   # 파손
                'fire',        # 방화
                'smoking',     # 흡연
                'abandonment', # 유기
                'theft',       # 절도
                'assault',     # 폭행
                'vulnerable'   # 이동약자
            ]
        else:
            self.classes = [
                'normal',      # 정상
                'fall',        # 전도
                'vandalism',   # 파손
                'fire',        # 방화
                'smoking',     # 흡연
                'abandonment', # 유기
                'theft',       # 절도
                'assault',     # 폭행
                'vulnerable'   # 이동약자
            ]
        
        self.severity_map = {
            'normal': 'low',
            'fall': 'high',
            'vandalism': 'high',
            'fire': 'critical',
            'smoking': 'medium',
            'abandonment': 'medium',
            'theft': 'high',
            'assault': 'critical',
            'vulnerable': 'medium'
        }
        
        self.load_model()
    
    def load_model(self):
        """모델 로드 (학습된 모델이 있을 경우)"""
        if os.path.exists(self.model_path):
            try:
                self.model = keras.models.load_model(self.model_path)
                print(f'Model loaded from {self.model_path}')
            except Exception as e:
                print(f'Error loading model: {e}')
                print('Using demo mode with random predictions')
                self.model = None
        else:
            print('No trained model found. Using demo mode.')
            self.model = None
    
    def preprocess_frame(self, frame):
        """프레임 전처리"""
        # 리사이즈
        resized = cv2.resize(frame, (224, 224))
        # 정규화
        normalized = resized.astype('float32') / 255.0
        # 배치 차원 추가
        return np.expand_dims(normalized, axis=0)
    
    def predict(self, frame):
        """단일 프레임 예측"""
        # 전처리
        processed_frame = self.preprocess_frame(frame)
        
        if self.model is not None:
            # 실제 모델 추론
            predictions = self.model.predict(processed_frame, verbose=0)
            class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][class_idx])
            
            # 정상 없는 모델: 신뢰도가 임계값 이하면 정상으로 처리
            if self.use_no_normal_model:
                if confidence < self.confidence_threshold:
                    action = 'normal'
                    is_abnormal = False
                    severity = 'low'
                else:
                    action = self.classes[class_idx]
                    is_abnormal = True
                    severity = self.severity_map.get(action, 'medium')
            else:
                action = self.classes[class_idx]
                is_abnormal = action != 'normal'
                severity = self.severity_map.get(action, 'low')
        else:
            # 데모 모드: 랜덤 예측 (실제로는 대부분 정상)
            if np.random.random() > 0.95:  # 5% 확률로 이상행동
                start_idx = 0 if not self.use_no_normal_model else 0
                end_idx = len(self.classes) if not self.use_no_normal_model else len(self.classes)
                if not self.use_no_normal_model:
                    class_idx = np.random.randint(1, end_idx)  # 정상 제외
                else:
                    class_idx = np.random.randint(start_idx, end_idx)
                confidence = np.random.uniform(0.7, 0.95)
                action = self.classes[class_idx]
                is_abnormal = True
            else:
                action = 'normal'
                confidence = np.random.uniform(0.85, 0.99)
                is_abnormal = False
            
            severity = self.severity_map.get(action, 'low')
        
        return {
            'action': action,
            'confidence': confidence,
            'is_abnormal': is_abnormal,
            'severity': severity,
            'threshold_used': self.confidence_threshold if self.use_no_normal_model else None,
            'all_predictions': {
                cls: float(conf) for cls, conf in 
                zip(self.classes, [confidence if i == class_idx else 0.01 
                                  for i in range(len(self.classes))])
            }
        }
    
    def predict_video(self, video_path, camera_id='camera_1'):
        """비디오 파일 전체 분석"""
        cap = cv2.VideoCapture(video_path)
        results = []
        frame_count = 0
        
        # 매 30프레임마다 분석 (약 1초마다, 30fps 기준)
        frame_skip = 30
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % frame_skip == 0:
                result = self.predict(frame)
                result['frame_number'] = frame_count
                result['camera_id'] = camera_id
                results.append(result)
            
            frame_count += 1
        
        cap.release()
        
        # 이상행동만 필터링
        abnormal_results = [r for r in results if r['is_abnormal']]
        
        return {
            'total_frames': frame_count,
            'analyzed_frames': len(results),
            'abnormal_detections': len(abnormal_results),
            'detections': abnormal_results
        }
