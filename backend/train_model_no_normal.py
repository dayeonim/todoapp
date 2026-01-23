"""
정상 데이터 없이 학습하는 모델

접근법: Multi-label Classification
- "정상" 클래스 없이 8가지 이상행동만 분류
- 모든 이상행동에 해당하지 않으면 "정상"으로 간주
- 신뢰도 임계값을 설정하여 불확실한 경우 "정상"으로 처리

사용법:
    python train_model_no_normal.py
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path
import json
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class AbnormalOnlyModelTrainer:
    def __init__(self, 
                 data_dir='data/processed',
                 model_save_dir='models',
                 input_shape=(16, 224, 224, 3),
                 batch_size=8,
                 epochs=50,
                 learning_rate=0.001,
                 confidence_threshold=0.6):
        
        self.data_dir = Path(data_dir)
        self.model_save_dir = Path(model_save_dir)
        self.model_save_dir.mkdir(parents=True, exist_ok=True)
        
        self.input_shape = input_shape
        self.batch_size = batch_size
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.confidence_threshold = confidence_threshold
        
        # 정상 클래스 제외 (이상행동만)
        self.classes = [
            'fall', 'vandalism', 'fire', 'smoking',
            'abandonment', 'theft', 'assault', 'vulnerable'
        ]
        self.num_classes = len(self.classes)
        
        self.class_to_idx = {cls: idx for idx, cls in enumerate(self.classes)}
    
    def load_data(self, split='train'):
        """데이터 로드 (정상 클래스 제외)"""
        print(f"📂 {split} 데이터 로드 중...")
        
        X = []
        y = []
        
        for class_name in self.classes:
            class_dir = self.data_dir / split / class_name
            
            if not class_dir.exists():
                print(f"  ⚠️  폴더가 없습니다: {class_dir}")
                continue
            
            npy_files = list(class_dir.glob('*.npy'))
            
            print(f"  {class_name}: {len(npy_files)}개")
            
            for npy_file in npy_files:
                try:
                    frames = np.load(npy_file)
                    X.append(frames)
                    y.append(self.class_to_idx[class_name])
                except Exception as e:
                    print(f"    ⚠️  로드 실패: {npy_file} - {e}")
        
        if not X:
            return None, None
        
        X = np.array(X)
        y = np.array(y)
        
        print(f"  ✅ {split}: X={X.shape}, y={y.shape}")
        
        return X, y
    
    def create_model(self):
        """3D CNN 모델 (이상행동만 분류)"""
        print("\n🏗️  모델 구축 중...")
        print(f"   출력 클래스: {self.num_classes}개 (이상행동만)")
        print(f"   신뢰도 임계값: {self.confidence_threshold}")
        
        model = keras.Sequential([
            # Conv3D Block 1
            layers.Conv3D(32, (3, 3, 3), activation='relu', 
                         padding='same', input_shape=self.input_shape),
            layers.MaxPooling3D((2, 2, 2)),
            layers.BatchNormalization(),
            layers.Dropout(0.25),
            
            # Conv3D Block 2
            layers.Conv3D(64, (3, 3, 3), activation='relu', padding='same'),
            layers.MaxPooling3D((2, 2, 2)),
            layers.BatchNormalization(),
            layers.Dropout(0.25),
            
            # Conv3D Block 3
            layers.Conv3D(128, (3, 3, 3), activation='relu', padding='same'),
            layers.MaxPooling3D((2, 2, 2)),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            # Conv3D Block 4
            layers.Conv3D(256, (3, 3, 3), activation='relu', padding='same'),
            layers.MaxPooling3D((1, 2, 2)),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            # Global pooling and Dense
            layers.GlobalAveragePooling3D(),
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.5),
            
            # 출력층 (이상행동만)
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        model.summary()
        
        return model
    
    def compile_model(self, model):
        """모델 컴파일"""
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top3_acc')]
        )
        
        return model
    
    def get_callbacks(self):
        """학습 콜백 설정"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        callbacks = [
            keras.callbacks.ModelCheckpoint(
                filepath=str(self.model_save_dir / f'model_no_normal_best_{timestamp}.h5'),
                monitor='val_accuracy',
                save_best_only=True,
                mode='max',
                verbose=1
            ),
            
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            ),
            
            keras.callbacks.TensorBoard(
                log_dir=f'logs/no_normal_{timestamp}',
                histogram_freq=1
            )
        ]
        
        return callbacks
    
    def plot_training_history(self, history, save_path):
        """학습 히스토리 시각화"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        axes[0].plot(history.history['accuracy'], label='Train Accuracy')
        axes[0].plot(history.history['val_accuracy'], label='Val Accuracy')
        axes[0].set_title('Model Accuracy (Abnormal Only)')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Accuracy')
        axes[0].legend()
        axes[0].grid(True)
        
        axes[1].plot(history.history['loss'], label='Train Loss')
        axes[1].plot(history.history['val_loss'], label='Val Loss')
        axes[1].set_title('Model Loss')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Loss')
        axes[1].legend()
        axes[1].grid(True)
        
        plt.tight_layout()
        plt.savefig(save_path)
        print(f"  ✅ 학습 히스토리 저장: {save_path}")
        plt.close()
    
    def evaluate_model(self, model, X_test, y_test):
        """모델 평가"""
        print("\n📊 모델 평가 중...")
        
        y_pred_probs = model.predict(X_test)
        y_pred = np.argmax(y_pred_probs, axis=1)
        
        print("\n" + "="*60)
        print("Classification Report (Abnormal Actions Only)")
        print("="*60)
        print(classification_report(y_test, y_pred, target_names=self.classes))
        
        cm = confusion_matrix(y_test, y_pred)
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Reds',
                   xticklabels=self.classes, yticklabels=self.classes)
        plt.title('Confusion Matrix (Abnormal Only)')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        cm_path = self.model_save_dir / 'confusion_matrix_no_normal.png'
        plt.savefig(cm_path)
        print(f"\n✅ Confusion Matrix 저장: {cm_path}")
        plt.close()
        
        # 신뢰도 분석
        max_confidences = np.max(y_pred_probs, axis=1)
        print("\n" + "="*60)
        print("신뢰도 분석")
        print("="*60)
        print(f"평균 신뢰도: {np.mean(max_confidences):.3f}")
        print(f"중간값 신뢰도: {np.median(max_confidences):.3f}")
        print(f"임계값 이하 비율: {np.mean(max_confidences < self.confidence_threshold)*100:.1f}%")
        print(f"\n💡 임계값({self.confidence_threshold}) 이하는 '정상'으로 분류됩니다.")
        
        class_accuracy = cm.diagonal() / cm.sum(axis=1)
        
        print("\n" + "="*60)
        print("클래스별 정확도")
        print("="*60)
        for cls, acc in zip(self.classes, class_accuracy):
            print(f"  {cls:12s}: {acc*100:6.2f}%")
        
        return {
            'classification_report': classification_report(y_test, y_pred, 
                                                          target_names=self.classes, 
                                                          output_dict=True),
            'confusion_matrix': cm.tolist(),
            'class_accuracy': {cls: float(acc) for cls, acc in zip(self.classes, class_accuracy)},
            'confidence_stats': {
                'mean': float(np.mean(max_confidences)),
                'median': float(np.median(max_confidences)),
                'threshold': self.confidence_threshold,
                'below_threshold_ratio': float(np.mean(max_confidences < self.confidence_threshold))
            }
        }
    
    def train(self):
        """전체 학습 파이프라인"""
        print("="*60)
        print("🚀 이상행동 전용 모델 학습 시작")
        print("="*60)
        print("\n💡 정상 데이터 없이 이상행동만 분류합니다.")
        print(f"   신뢰도가 {self.confidence_threshold} 미만이면 '정상'으로 간주됩니다.")
        print()
        
        # 데이터 로드
        X_train, y_train = self.load_data('train')
        X_val, y_val = self.load_data('val')
        X_test, y_test = self.load_data('test')
        
        if X_train is None or X_val is None:
            print("\n❌ 데이터가 없습니다!")
            print("💡 먼저 preprocess_data.py를 실행하세요")
            return
        
        # 모델 생성 및 컴파일
        model = self.create_model()
        model = self.compile_model(model)
        
        # 학습
        print(f"\n🎓 모델 학습 시작")
        print("="*60)
        
        callbacks = self.get_callbacks()
        
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            batch_size=self.batch_size,
            epochs=self.epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        # 학습 히스토리 저장
        history_path = self.model_save_dir / 'training_history_no_normal.png'
        self.plot_training_history(history, history_path)
        
        # 최종 모델 저장
        final_model_path = self.model_save_dir / 'abnormal_detector_no_normal.h5'
        model.save(final_model_path)
        print(f"\n✅ 최종 모델 저장: {final_model_path}")
        
        # 메타데이터 저장
        metadata = {
            'classes': self.classes,
            'num_classes': self.num_classes,
            'confidence_threshold': self.confidence_threshold,
            'input_shape': self.input_shape,
            'model_type': 'abnormal_only',
            'note': 'Predictions below confidence threshold are considered normal'
        }
        metadata_path = self.model_save_dir / 'model_metadata_no_normal.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✅ 메타데이터 저장: {metadata_path}")
        
        # 테스트 세트 평가
        if X_test is not None:
            eval_results = self.evaluate_model(model, X_test, y_test)
            
            results_path = self.model_save_dir / 'evaluation_results_no_normal.json'
            with open(results_path, 'w', encoding='utf-8') as f:
                json.dump(eval_results, f, indent=2, ensure_ascii=False)
            print(f"✅ 평가 결과 저장: {results_path}")
        
        print("\n" + "="*60)
        print("✨ 학습 완료!")
        print("="*60)
        print(f"\n📁 모델 파일: {final_model_path}")
        print("\n⚠️  주의사항:")
        print(f"   - 신뢰도 {self.confidence_threshold} 미만은 '정상'으로 처리")
        print("   - 정상 데이터로 검증 권장")
        print("   - 임계값 조정으로 민감도 조절 가능")
        print("\n다음 단계:")
        print("   app.py에서 이 모델 사용 (model_handler.py 수정)")


def main():
    """메인 함수"""
    trainer = AbnormalOnlyModelTrainer(
        data_dir='data/processed',
        model_save_dir='models',
        batch_size=8,
        epochs=50,
        learning_rate=0.001,
        confidence_threshold=0.6  # 이 값을 조정하여 민감도 변경
    )
    
    trainer.train()


if __name__ == '__main__':
    main()
