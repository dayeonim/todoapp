"""
테스트용 샘플 CCTV 영상 데이터 생성 스크립트

실제 데이터가 없을 때 빠른 테스트를 위해 사용합니다.
합성 비디오 데이터를 생성합니다.

사용법:
    python generate_sample_data.py
"""

import cv2
import numpy as np
from pathlib import Path
import random

class SampleDataGenerator:
    def __init__(self, output_dir='data/raw', videos_per_class=10):
        self.output_dir = Path(output_dir)
        self.videos_per_class = videos_per_class
        
        self.classes = [
            'fall', 'vandalism', 'fire', 'smoking',
            'abandonment', 'theft', 'assault', 'vulnerable', 'normal'
        ]
        
        self.class_descriptions = {
            'fall': '전도 - 사람이 넘어지는 시뮬레이션',
            'vandalism': '파손 - 물체가 파괴되는 시뮬레이션',
            'fire': '방화 - 불꽃 효과 시뮬레이션',
            'smoking': '흡연 - 연기 효과 시뮬레이션',
            'abandonment': '유기 - 물체가 방치되는 시뮬레이션',
            'theft': '절도 - 물체가 이동하는 시뮬레이션',
            'assault': '폭행 - 급격한 움직임 시뮬레이션',
            'vulnerable': '이동약자 - 느린 움직임 시뮬레이션',
            'normal': '정상 - 일반적인 움직임'
        }
        
        self.width = 640
        self.height = 480
        self.fps = 30
        self.duration = 5  # 초
    
    def create_directories(self):
        """디렉토리 생성"""
        for cls in self.classes:
            class_dir = self.output_dir / cls
            class_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ 디렉토리 생성 완료: {self.output_dir}")
    
    def generate_background(self):
        """배경 생성 (가게 바닥 느낌)"""
        bg = np.ones((self.height, self.width, 3), dtype=np.uint8) * 200
        
        # 그리드 패턴
        for i in range(0, self.width, 50):
            cv2.line(bg, (i, 0), (i, self.height), (180, 180, 180), 1)
        for i in range(0, self.height, 50):
            cv2.line(bg, (0, i), (self.width, i), (180, 180, 180), 1)
        
        return bg
    
    def add_person(self, frame, x, y, color=(100, 150, 200)):
        """사람 형태 추가 (간단한 막대기 사람)"""
        # 머리
        cv2.circle(frame, (int(x), int(y)), 15, color, -1)
        # 몸통
        cv2.line(frame, (int(x), int(y + 15)), (int(x), int(y + 60)), color, 8)
        # 팔
        cv2.line(frame, (int(x), int(y + 30)), (int(x - 20), int(y + 45)), color, 6)
        cv2.line(frame, (int(x), int(y + 30)), (int(x + 20), int(y + 45)), color, 6)
        # 다리
        cv2.line(frame, (int(x), int(y + 60)), (int(x - 15), int(y + 90)), color, 6)
        cv2.line(frame, (int(x), int(y + 60)), (int(x + 15), int(y + 90)), color, 6)
    
    def generate_fall_video(self, output_path):
        """전도 영상 생성"""
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, self.fps, (self.width, self.height))
        
        total_frames = self.fps * self.duration
        start_y = 150
        
        for i in range(total_frames):
            frame = self.generate_background()
            
            # 서있다가 넘어지는 애니메이션
            if i < total_frames * 0.5:
                y = start_y
                self.add_person(frame, self.width // 2, y)
            else:
                # 넘어지는 효과
                y = start_y + (i - total_frames * 0.5) * 3
                x = self.width // 2 + (i - total_frames * 0.5) * 2
                rotation = (i - total_frames * 0.5) * 3
                self.add_person(frame, x, y, (80, 120, 180))
            
            cv2.putText(frame, 'FALL DETECTION', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            out.write(frame)
        
        out.release()
    
    def generate_fire_video(self, output_path):
        """방화 영상 생성 (불꽃 효과)"""
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, self.fps, (self.width, self.height))
        
        total_frames = self.fps * self.duration
        
        for i in range(total_frames):
            frame = self.generate_background()
            
            # 불꽃 효과 (랜덤 빨간색 점들)
            intensity = min(i / total_frames * 2, 1.0)
            for _ in range(int(100 * intensity)):
                x = random.randint(self.width // 3, 2 * self.width // 3)
                y = random.randint(self.height // 2, self.height)
                radius = random.randint(5, 20)
                color = (0, random.randint(100, 255), random.randint(200, 255))
                cv2.circle(frame, (x, y), radius, color, -1)
            
            cv2.putText(frame, 'FIRE DETECTED', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            out.write(frame)
        
        out.release()
    
    def generate_theft_video(self, output_path):
        """절도 영상 생성 (물체 이동)"""
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, self.fps, (self.width, self.height))
        
        total_frames = self.fps * self.duration
        
        for i in range(total_frames):
            frame = self.generate_background()
            
            # 물체 (상자)
            box_x = 100 + i * 5
            box_y = self.height // 2
            cv2.rectangle(frame, (box_x, box_y), (box_x + 60, box_y + 60), (150, 100, 50), -1)
            
            # 사람
            person_x = 80 + i * 5
            self.add_person(frame, person_x, 200)
            
            cv2.putText(frame, 'THEFT DETECTED', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            out.write(frame)
        
        out.release()
    
    def generate_normal_video(self, output_path):
        """정상 영상 생성"""
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, self.fps, (self.width, self.height))
        
        total_frames = self.fps * self.duration
        
        for i in range(total_frames):
            frame = self.generate_background()
            
            # 천천히 걷는 사람
            x = 100 + i * 2
            y = 200 + np.sin(i * 0.1) * 10
            self.add_person(frame, x, y, (100, 200, 100))
            
            cv2.putText(frame, 'NORMAL', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            out.write(frame)
        
        out.release()
    
    def generate_generic_video(self, output_path, class_name):
        """일반적인 영상 생성"""
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, self.fps, (self.width, self.height))
        
        total_frames = self.fps * self.duration
        color = tuple(random.randint(50, 255) for _ in range(3))
        
        for i in range(total_frames):
            frame = self.generate_background()
            
            # 움직이는 사람
            x = 100 + i * random.randint(1, 4)
            y = 200 + np.sin(i * 0.2) * 30
            self.add_person(frame, x, y, color)
            
            cv2.putText(frame, class_name.upper(), (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            out.write(frame)
        
        out.release()
    
    def generate_class_videos(self, class_name):
        """특정 클래스의 비디오들 생성"""
        print(f"📹 {class_name} 영상 생성 중... ({self.videos_per_class}개)")
        print(f"   {self.class_descriptions[class_name]}")
        
        class_dir = self.output_dir / class_name
        
        for i in range(self.videos_per_class):
            output_path = class_dir / f"{class_name}_{i:03d}.mp4"
            
            # 클래스별 특화 생성 함수 호출
            if class_name == 'fall':
                self.generate_fall_video(output_path)
            elif class_name == 'fire':
                self.generate_fire_video(output_path)
            elif class_name == 'theft':
                self.generate_theft_video(output_path)
            elif class_name == 'normal':
                self.generate_normal_video(output_path)
            else:
                self.generate_generic_video(output_path, class_name)
        
        print(f"   ✅ 완료")
    
    def run(self):
        """전체 샘플 데이터 생성"""
        print("="*60)
        print("🎬 샘플 CCTV 영상 데이터 생성 시작")
        print("="*60)
        print(f"\n⚠️  주의: 이것은 테스트용 합성 데이터입니다.")
        print(f"   실제 CCTV 데이터로 학습하면 훨씬 좋은 성능을 얻을 수 있습니다.\n")
        
        # 1. 디렉토리 생성
        self.create_directories()
        
        # 2. 각 클래스별 영상 생성
        for class_name in self.classes:
            self.generate_class_videos(class_name)
        
        print("\n" + "="*60)
        print("✨ 샘플 데이터 생성 완료!")
        print("="*60)
        print(f"\n📁 생성된 데이터: {self.output_dir}")
        print(f"📊 총 {len(self.classes)} 클래스 × {self.videos_per_class}개 = {len(self.classes) * self.videos_per_class}개 영상")
        print("\n다음 단계:")
        print("  1. python backend/preprocess_data.py  (데이터 전처리)")
        print("  2. python backend/train_model.py      (모델 학습)")
        print("  3. python backend/app.py               (웹 서버 실행)")


def main():
    """메인 함수"""
    generator = SampleDataGenerator(
        output_dir='data/raw',
        videos_per_class=10  # 클래스당 10개 영상 생성
    )
    
    generator.run()


if __name__ == '__main__':
    main()
