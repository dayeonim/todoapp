"""
CCTV 영상 데이터 전처리 스크립트

사용법:
    python preprocess_data.py

기능:
    1. data/raw/ 폴더의 영상 파일들을 읽어옴
    2. 프레임 추출 및 정규화
    3. Train/Val/Test로 분할
    4. data/processed/ 폴더에 저장
"""

import os
import cv2
import numpy as np
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import shutil

class DataPreprocessor:
    def __init__(self, 
                 raw_data_dir='data/raw',
                 processed_data_dir='data/processed',
                 frame_size=(224, 224),
                 frames_per_video=16,
                 train_ratio=0.7,
                 val_ratio=0.15):
        
        self.raw_data_dir = Path(raw_data_dir)
        self.processed_data_dir = Path(processed_data_dir)
        self.frame_size = frame_size
        self.frames_per_video = frames_per_video
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = 1 - train_ratio - val_ratio
        
        self.classes = [
            'fall', 'vandalism', 'fire', 'smoking',
            'abandonment', 'theft', 'assault', 'vulnerable', 'normal'
        ]
        
        # 지원 비디오 확장자
        self.video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
        
    def create_directories(self):
        """필요한 디렉토리 생성"""
        for split in ['train', 'val', 'test']:
            for cls in self.classes:
                (self.processed_data_dir / split / cls).mkdir(parents=True, exist_ok=True)
        
        print(f"✅ 디렉토리 생성 완료: {self.processed_data_dir}")
    
    def extract_frames(self, video_path, num_frames=16):
        """비디오에서 균등하게 프레임 추출"""
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            print(f"⚠️  영상 열기 실패: {video_path}")
            return None
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames < num_frames:
            print(f"⚠️  프레임 부족 ({total_frames} < {num_frames}): {video_path}")
            cap.release()
            return None
        
        # 균등한 간격으로 프레임 인덱스 계산
        frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
        
        frames = []
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            
            if ret:
                # 리사이즈 및 정규화
                frame = cv2.resize(frame, self.frame_size)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = frame.astype('float32') / 255.0
                frames.append(frame)
            else:
                print(f"⚠️  프레임 읽기 실패 (idx: {idx}): {video_path}")
        
        cap.release()
        
        if len(frames) != num_frames:
            return None
        
        return np.array(frames)
    
    def get_video_files(self, class_name):
        """특정 클래스의 모든 비디오 파일 경로 반환"""
        class_dir = self.raw_data_dir / class_name
        
        if not class_dir.exists():
            print(f"⚠️  폴더가 없습니다: {class_dir}")
            return []
        
        video_files = []
        for ext in self.video_extensions:
            video_files.extend(list(class_dir.glob(f'*{ext}')))
        
        return video_files
    
    def process_class(self, class_name):
        """특정 클래스의 모든 영상 처리"""
        video_files = self.get_video_files(class_name)
        
        if not video_files:
            print(f"⚠️  {class_name}: 영상 파일이 없습니다.")
            return []
        
        print(f"\n📹 {class_name} 클래스 처리 중... ({len(video_files)}개 파일)")
        
        processed_data = []
        
        for video_path in tqdm(video_files, desc=f"  {class_name}"):
            frames = self.extract_frames(video_path, self.frames_per_video)
            
            if frames is not None:
                processed_data.append({
                    'frames': frames,
                    'label': class_name,
                    'original_path': str(video_path)
                })
        
        print(f"  ✅ {len(processed_data)}/{len(video_files)} 영상 처리 완료")
        return processed_data
    
    def split_data(self, data_list):
        """데이터를 train/val/test로 분할"""
        # 먼저 train과 나머지 분할
        train_data, temp_data = train_test_split(
            data_list, 
            train_size=self.train_ratio, 
            random_state=42
        )
        
        # 나머지를 val과 test로 분할
        val_size = self.val_ratio / (self.val_ratio + self.test_ratio)
        val_data, test_data = train_test_split(
            temp_data,
            train_size=val_size,
            random_state=42
        )
        
        return {
            'train': train_data,
            'val': val_data,
            'test': test_data
        }
    
    def save_processed_data(self, split_data):
        """처리된 데이터 저장"""
        print("\n💾 데이터 저장 중...")
        
        stats = {split: {cls: 0 for cls in self.classes} for split in ['train', 'val', 'test']}
        
        for split, data_list in split_data.items():
            for idx, data in enumerate(tqdm(data_list, desc=f"  {split}")):
                label = data['label']
                frames = data['frames']
                
                # NumPy 배열로 저장
                save_path = self.processed_data_dir / split / label / f"{label}_{idx:05d}.npy"
                np.save(save_path, frames)
                
                stats[split][label] += 1
        
        # 통계 저장
        stats_path = self.processed_data_dir / 'dataset_stats.json'
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ 통계 정보 저장: {stats_path}")
        
        return stats
    
    def print_statistics(self, stats):
        """데이터 통계 출력"""
        print("\n" + "="*60)
        print("📊 데이터셋 통계")
        print("="*60)
        
        for split in ['train', 'val', 'test']:
            print(f"\n[{split.upper()}]")
            total = sum(stats[split].values())
            for cls in self.classes:
                count = stats[split][cls]
                percentage = (count / total * 100) if total > 0 else 0
                print(f"  {cls:12s}: {count:4d} ({percentage:5.1f}%)")
            print(f"  {'Total':12s}: {total:4d}")
        
        print("\n" + "="*60)
    
    def run(self):
        """전체 전처리 파이프라인 실행"""
        print("="*60)
        print("🎬 CCTV 영상 데이터 전처리 시작")
        print("="*60)
        
        # 1. 디렉토리 생성
        self.create_directories()
        
        # 2. 각 클래스별 데이터 처리
        all_data = []
        for class_name in self.classes:
            processed = self.process_class(class_name)
            all_data.extend(processed)
        
        if not all_data:
            print("\n❌ 처리할 데이터가 없습니다!")
            print("\n💡 data/raw/ 폴더에 다음과 같이 영상을 준비해주세요:")
            print("   data/raw/fall/*.mp4")
            print("   data/raw/theft/*.mp4")
            print("   ...")
            return
        
        print(f"\n✅ 총 {len(all_data)}개 영상 처리 완료")
        
        # 3. 데이터 분할
        print(f"\n🔀 데이터 분할 중 (train: {self.train_ratio*100}%, val: {self.val_ratio*100}%, test: {self.test_ratio*100}%)")
        split_data = self.split_data(all_data)
        
        # 4. 저장
        stats = self.save_processed_data(split_data)
        
        # 5. 통계 출력
        self.print_statistics(stats)
        
        print("\n" + "="*60)
        print("✨ 전처리 완료!")
        print("="*60)
        print(f"\n📁 처리된 데이터 위치: {self.processed_data_dir}")
        print(f"📄 통계 파일: {self.processed_data_dir / 'dataset_stats.json'}")
        print("\n다음 단계: python backend/train_model.py")


def main():
    """메인 함수"""
    preprocessor = DataPreprocessor(
        raw_data_dir='data/raw',
        processed_data_dir='data/processed',
        frame_size=(224, 224),
        frames_per_video=16
    )
    
    preprocessor.run()


if __name__ == '__main__':
    main()
