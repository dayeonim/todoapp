"""
정상 데이터 생성 스크립트

이상행동 데이터만 있을 때 정상 데이터를 생성하는 방법:
1. 배경 영상 생성 (사람 없는 빈 화면)
2. 이상행동 영상에서 정상 부분만 추출
3. 웹캠으로 정상 활동 촬영
4. 공개 데이터셋 다운로드

사용법:
    python generate_normal_data.py --method [background|webcam|extract]
"""

import cv2
import numpy as np
from pathlib import Path
import argparse
import time
from datetime import datetime

class NormalDataGenerator:
    def __init__(self, output_dir='data/raw/normal'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.width = 640
        self.height = 480
        self.fps = 30
        self.duration = 5
    
    def generate_background_videos(self, num_videos=50):
        """
        방법 1: 배경 영상 생성 (사람 없는 빈 화면)
        - 이상행동이 없는 빈 배경을 정상으로 간주
        """
        print("\n" + "="*60)
        print("📹 배경 영상 생성 중...")
        print("="*60)
        print(f"생성할 영상 수: {num_videos}개")
        print("설명: 사람이 없거나 아무 일도 일어나지 않는 정상 상태")
        print()
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        total_frames = self.fps * self.duration
        
        backgrounds = [
            ('empty_store', self._create_empty_store),
            ('quiet_corridor', self._create_quiet_corridor),
            ('static_shelves', self._create_static_shelves),
        ]
        
        for i in range(num_videos):
            bg_name, bg_func = backgrounds[i % len(backgrounds)]
            output_path = self.output_dir / f"normal_bg_{i:03d}_{bg_name}.mp4"
            
            out = cv2.VideoWriter(str(output_path), fourcc, self.fps, 
                                 (self.width, self.height))
            
            for frame_num in range(total_frames):
                frame = bg_func(frame_num)
                
                # 약간의 노이즈 추가 (실제 카메라 느낌)
                noise = np.random.normal(0, 5, frame.shape).astype(np.int16)
                frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
                
                # 타임스탬프 추가
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cv2.putText(frame, timestamp, (10, self.height - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)
                
                out.write(frame)
            
            out.release()
            
            if (i + 1) % 10 == 0:
                print(f"  진행: {i + 1}/{num_videos}")
        
        print(f"\n✅ {num_videos}개 배경 영상 생성 완료!")
        print(f"📁 저장 위치: {self.output_dir}")
    
    def _create_empty_store(self, frame_num):
        """빈 가게 배경"""
        frame = np.ones((self.height, self.width, 3), dtype=np.uint8) * 220
        
        # 바닥 타일
        for i in range(0, self.width, 50):
            cv2.line(frame, (i, 0), (i, self.height), (200, 200, 200), 1)
        for i in range(0, self.height, 50):
            cv2.line(frame, (0, i), (self.width, i), (200, 200, 200), 1)
        
        # 약간의 움직임 (조명 변화)
        brightness = 220 + int(5 * np.sin(frame_num * 0.05))
        frame = np.clip(frame.astype(np.int16) + (brightness - 220), 0, 255).astype(np.uint8)
        
        return frame
    
    def _create_quiet_corridor(self, frame_num):
        """조용한 복도"""
        frame = np.ones((self.height, self.width, 3), dtype=np.uint8) * 180
        
        # 복도 원근
        pts1 = np.array([[50, 100], [self.width-50, 100], 
                        [self.width-20, self.height-50], [20, self.height-50]], np.int32)
        cv2.fillPoly(frame, [pts1], (200, 200, 210))
        
        return frame
    
    def _create_static_shelves(self, frame_num):
        """정적인 선반"""
        frame = np.ones((self.height, self.width, 3), dtype=np.uint8) * 190
        
        # 선반
        for i in range(3):
            y = 100 + i * 100
            cv2.rectangle(frame, (50, y), (self.width-50, y+60), (150, 120, 100), -1)
            cv2.rectangle(frame, (50, y), (self.width-50, y+60), (100, 80, 60), 2)
        
        return frame
    
    def record_from_webcam(self, num_videos=20):
        """
        방법 2: 웹캠으로 정상 활동 촬영
        - 실제 사람이 평범하게 걷거나 물건을 보는 등의 정상 활동
        """
        print("\n" + "="*60)
        print("📹 웹캠으로 정상 활동 촬영")
        print("="*60)
        print("녹화할 영상 수:", num_videos)
        print("\n지침:")
        print("  - 평범하게 걷기")
        print("  - 물건 보기")
        print("  - 서서 대기하기")
        print("  - 천천히 이동하기")
        print("\n각 영상은 5초씩 녹화됩니다.")
        print("준비되면 Enter를 누르세요...")
        input()
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ 웹캠을 열 수 없습니다!")
            return
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        for i in range(num_videos):
            print(f"\n📹 영상 {i+1}/{num_videos} 녹화 중...")
            print("3초 후 녹화 시작...")
            
            # 카운트다운
            for countdown in range(3, 0, -1):
                ret, frame = cap.read()
                if ret:
                    frame = cv2.resize(frame, (self.width, self.height))
                    cv2.putText(frame, str(countdown), (self.width//2-50, self.height//2),
                               cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)
                    cv2.imshow('Recording', frame)
                    cv2.waitKey(1000)
            
            # 녹화 시작
            output_path = self.output_dir / f"normal_webcam_{i:03d}.mp4"
            out = cv2.VideoWriter(str(output_path), fourcc, self.fps, 
                                 (self.width, self.height))
            
            start_time = time.time()
            frame_count = 0
            
            while (time.time() - start_time) < self.duration:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.resize(frame, (self.width, self.height))
                
                # 녹화 중 표시
                remaining = self.duration - (time.time() - start_time)
                cv2.circle(frame, (20, 20), 10, (0, 0, 255), -1)
                cv2.putText(frame, f'REC {remaining:.1f}s', (40, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                out.write(frame)
                cv2.imshow('Recording', frame)
                cv2.waitKey(1)
                frame_count += 1
            
            out.release()
            print(f"✅ 영상 {i+1} 저장 완료 ({frame_count} 프레임)")
            
            if i < num_videos - 1:
                print("다음 촬영 준비... (Enter를 눌러 계속)")
                input()
        
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n✅ 총 {num_videos}개 영상 녹화 완료!")
        print(f"📁 저장 위치: {self.output_dir}")
    
    def extract_from_abnormal_videos(self, abnormal_dir='data/raw', threshold_duration=2.0):
        """
        방법 3: 이상행동 영상에서 정상 부분 추출
        - 이상행동이 시작되기 전 부분
        - 이상행동이 끝난 후 부분
        """
        print("\n" + "="*60)
        print("📹 이상행동 영상에서 정상 부분 추출")
        print("="*60)
        print(f"대상 폴더: {abnormal_dir}")
        print(f"추출 기준: 움직임이 적은 {threshold_duration}초 구간")
        print()
        
        abnormal_dir = Path(abnormal_dir)
        video_count = 0
        extracted_count = 0
        
        # 이상행동 폴더들 순회
        for class_dir in abnormal_dir.iterdir():
            if not class_dir.is_dir() or class_dir.name == 'normal':
                continue
            
            print(f"📂 {class_dir.name} 폴더 처리 중...")
            
            for video_path in class_dir.glob('*.mp4'):
                video_count += 1
                
                # 영상의 앞부분과 뒷부분에서 정상 구간 추출
                segments = self._extract_calm_segments(video_path, threshold_duration)
                
                for idx, segment in enumerate(segments):
                    output_path = self.output_dir / f"normal_extracted_{class_dir.name}_{video_path.stem}_{idx}.mp4"
                    if self._save_segment(video_path, segment, output_path):
                        extracted_count += 1
        
        print(f"\n✅ {video_count}개 영상에서 {extracted_count}개 정상 구간 추출 완료!")
        print(f"📁 저장 위치: {self.output_dir}")
    
    def _extract_calm_segments(self, video_path, duration):
        """움직임이 적은 구간 찾기"""
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames < fps * duration:
            cap.release()
            return []
        
        # 간단한 방법: 영상의 처음 30%와 마지막 30%에서 추출
        segments = []
        
        # 앞부분
        if total_frames * 0.3 > fps * duration:
            segments.append((0, int(fps * duration)))
        
        # 뒷부분
        end_start = total_frames - int(fps * duration)
        if end_start > total_frames * 0.7:
            segments.append((end_start, total_frames))
        
        cap.release()
        return segments
    
    def _save_segment(self, video_path, segment, output_path):
        """비디오 세그먼트 저장"""
        start_frame, end_frame = segment
        
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, 
                             (self.width, self.height))
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        for _ in range(end_frame - start_frame):
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (self.width, self.height))
            out.write(frame)
        
        cap.release()
        out.release()
        
        return True


def main():
    parser = argparse.ArgumentParser(description='정상 데이터 생성')
    parser.add_argument('--method', type=str, default='background',
                       choices=['background', 'webcam', 'extract', 'all'],
                       help='생성 방법 선택')
    parser.add_argument('--num', type=int, default=50,
                       help='생성할 영상 수')
    
    args = parser.parse_args()
    
    generator = NormalDataGenerator()
    
    print("="*60)
    print("🎬 정상 데이터 생성기")
    print("="*60)
    print("\n💡 이상행동 데이터만 있을 때 정상 데이터를 만드는 도구입니다.")
    print()
    
    if args.method == 'background' or args.method == 'all':
        print("\n[방법 1] 배경 영상 생성")
        print("  장점: 빠르고 간편, 대량 생성 가능")
        print("  단점: 실제 사람 활동이 없음")
        generator.generate_background_videos(num_videos=args.num)
    
    if args.method == 'webcam' or args.method == 'all':
        print("\n[방법 2] 웹캠 촬영")
        print("  장점: 실제 정상 활동 데이터")
        print("  단점: 시간 소요, 수동 작업 필요")
        response = input("\n웹캠 촬영을 시작하시겠습니까? (y/n): ")
        if response.lower() == 'y':
            generator.record_from_webcam(num_videos=20)
    
    if args.method == 'extract' or args.method == 'all':
        print("\n[방법 3] 이상행동 영상에서 정상 구간 추출")
        print("  장점: 기존 데이터 활용")
        print("  단점: 정상 구간이 충분하지 않을 수 있음")
        response = input("\n이상행동 영상에서 추출하시겠습니까? (y/n): ")
        if response.lower() == 'y':
            generator.extract_from_abnormal_videos()
    
    print("\n" + "="*60)
    print("✨ 완료!")
    print("="*60)
    print(f"\n📁 생성된 정상 데이터: data/raw/normal/")
    print("\n다음 단계:")
    print("  python preprocess_data.py")
    print("  python train_model.py")


if __name__ == '__main__':
    main()
