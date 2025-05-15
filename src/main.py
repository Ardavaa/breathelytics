import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import librosa
import optuna
import joblib
import os
import pickle

# notebook extensions
from IPython import display
from tqdm.notebook import tqdm

# feature engineering + selection
from glob import glob
from librosa import feature
from sklearn.preprocessing import LabelEncoder
from sklearn.base import BaseEstimator, TransformerMixin

# modelling + evaluation
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report, confusion_matrix, f1_score, accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold

# MLops
from zenml import pipeline, step
from zenml.client import Client
from typing_extensions import Annotated
from typing import Tuple, Dict, List, Any

warnings.filterwarnings('ignore')


base_audio_files = glob('../../audioscopeAI/src/audioscopeAI_AI-ML/Respiratory_Sound_Database/audio_and_txt_files/*.wav')


class DataIngestion:
    def __init__(self, audio_files: list):
        self.audio_files = audio_files
        self.audio_data = {}

    def load_audio_files(self) -> dict:
        for audio_file in self.audio_files:
            filename = os.path.basename(audio_file)
            y, sr = librosa.load(audio_file, mono=True)
            self.audio_data[filename] = {
                'data': y,
                'sample_rate': sr
            }
        print(f'Loaded {len(self.audio_data)} audio files')
        return self.audio_data
    
    def calculate_durations(self) -> dict:
        """Calculate duration for each audio file"""
        for filename, audio_info in self.audio_data.items():
            duration = len(audio_info['data']) / audio_info['sample_rate']
            self.audio_data[filename]['duration'] = duration
        
        return self.audio_data
    
    def get_min_duration(self) -> float:
        """Find the minimum duration among all audio files"""
        if not any('duration' in audio_info for audio_info in self.audio_data.values()):
            self.calculate_durations()
            
        min_duration = min(audio_info['duration'] for audio_info in self.audio_data.values())
        return min_duration


class DataPreprocessor:
    def __init__(self, audio_files: list = None, audio_data: dict = None, target_duration: float = 7.86):
        self.audio_files = audio_files
        self.audio_data = audio_data or {}
        self.target_duration = target_duration
        self.trimmed_audio = {}

    def get_trimmed_audio(self, audio_file: str) -> Tuple[np.ndarray, int]:
        y, sr = librosa.load(audio_file, mono=True)
        target_length = int(self.target_duration * sr)
        
        if len(y) < target_length:
            y = np.pad(y, (0, target_length - len(y)), mode='constant')
        else:
            y = y[:target_length]
        
        return y, sr
    
    def trim_audio_data(self) -> dict:
        """Trim all audio files to target duration"""
        for filename, audio_info in self.audio_data.items():
            target_samples = int(self.target_duration * audio_info['sample_rate'])
            
            # If audio is shorter than target, pad with zeros
            if len(audio_info['data']) < target_samples:
                trimmed_data = np.pad(audio_info['data'], 
                                     (0, target_samples - len(audio_info['data'])), 
                                     mode='constant')
            else:
                trimmed_data = audio_info['data'][:target_samples]
                
            self.trimmed_audio[filename] = {
                'data': trimmed_data,
                'sample_rate': audio_info['sample_rate'],
                'duration': self.target_duration
            }
        
        print(f'Trimmed all {len(self.trimmed_audio)} audio files to {self.target_duration} seconds')
        return self.trimmed_audio

    def feature_extraction(self, audio_file: str) -> dict:
        y, sr = self.trimmed_audio(audio_file)
        features = {
            'chroma_stft': np.mean(librosa.feature.chroma_stft(y=y, sr=sr).T, axis=0),
            'mfcc': np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13).T, axis=0),
            'mel_spectrogram': np.mean(librosa.feature.melspectrogram(y=y, sr=sr).T, axis=0),
            'spectral_contrast': np.mean(librosa.feature.spectral_contrast(y=y, sr=sr).T, axis=0),
            'spectral_bandwidth': np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr).T, axis=0),
            'spectral_centroid': np.mean(librosa.feature.spectral_centroid(y=y, sr=sr).T, axis=0),
            'spectral_rolloff': np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr).T, axis=0),
            'zero_crossing_rate': np.mean(librosa.feature.zero_crossing_rate(y=y).T, axis=0)
        }
        return features
    
    def extract_all_features(self) -> dict:
        """Extract features from all trimmed audio files"""
        audio_features = {}
        
        for filename, audio_info in self.trimmed_audio.items():
            y = audio_info['data']
            sr = audio_info['sample_rate']
            
            audio_features[filename] = {}
            
            audio_features[filename]['chroma_stft'] = feature.chroma_stft(y=y, sr=sr)
            audio_features[filename]['mfcc'] = feature.mfcc(y=y, sr=sr, n_mfcc=13)
            audio_features[filename]['mel_spectrogram'] = feature.melspectrogram(y=y, sr=sr)
            audio_features[filename]['spectral_contrast'] = feature.spectral_contrast(y=y, sr=sr)
            audio_features[filename]['spectral_centroid'] = feature.spectral_centroid(y=y, sr=sr)
            audio_features[filename]['spectral_bandwidth'] = feature.spectral_bandwidth(y=y, sr=sr)
            audio_features[filename]['spectral_rolloff'] = feature.spectral_rolloff(y=y, sr=sr)
            audio_features[filename]['zero_crossing_rate'] = feature.zero_crossing_rate(y=y)
            
        return audio_features
    
    def feature_stats(self, features: dict) -> dict:
        stats = {}
        for feature_name, feature_values in features.items():
            stats[feature_name + '_mean'] = np.mean(feature_values)
            stats[feature_name + '_std'] = np.std(feature_values)
            stats[feature_name + '_min'] = np.min(feature_values)
            stats[feature_name + '_max'] = np.max(feature_values)
        return stats
    
    def calculate_all_feature_stats(self, audio_features: dict) -> pd.DataFrame:
        """Calculate statistics for all features"""
        feature_stats = []
        
        for filename, features in audio_features.items():
            file_stats = {'filename': filename}
            
            # Calculate statistics for each feature
            for feature_name, feature_data in features.items():
                file_stats[f'{feature_name}_mean'] = np.mean(feature_data)
                file_stats[f'{feature_name}_std'] = np.std(feature_data)
                file_stats[f'{feature_name}_max'] = np.max(feature_data)
                file_stats[f'{feature_name}_min'] = np.min(feature_data)
            
            feature_stats.append(file_stats)
        
        # Create dataframe
        return pd.DataFrame(feature_stats)


class FeatureProcessor:
    def __init__(self, features_df: pd.DataFrame = None):
        self.features_df = features_df
        self.excluded_features = ['mel_spectrogram_min', 'chroma_stft_max']
        self.label_encoder = LabelEncoder()
        
    def load_patient_diagnosis(self, diagnosis_path: str) -> pd.DataFrame:
        """Load patient diagnosis data and merge with features"""
        patient_diagnosis = pd.read_csv(diagnosis_path)
        
        # Map diagnosis to features based on patient ID from filename
        self.features_df['patient_id'] = self.features_df['filename'].apply(
            lambda x: int(x.split('_')[0])
        )
        
        # Merge with diagnosis data
        self.features_df['diagnosis'] = self.features_df['patient_id'].apply(
            lambda pid: patient_diagnosis.loc[
                patient_diagnosis['patient_id'] == pid, 'diagnosis'
            ].values[0] if pid in patient_diagnosis['patient_id'].values else None
        )
        
        return self.features_df
    
    def encode_target(self) -> Tuple[np.ndarray, np.ndarray]:
        """Encode target variable and return feature matrix and target vector"""
        # Encode diagnosis
        y = self.label_encoder.fit_transform(self.features_df['diagnosis'])
        
        # Select only numeric features
        X = self.features_df.select_dtypes(exclude=['object'])
        
        # Drop excluded features
        for feature in self.excluded_features:
            if feature in X.columns:
                X = X.drop(feature, axis=1)
                
        return X, y
    

class ModelTrainer:
    def __init__(self, X: pd.DataFrame = None, y: np.ndarray = None):
        self.X = X
        self.y = y
        self.best_params = None
        self.model = None
        
    def compute_class_weights(self) -> dict:
        """Compute class weights for imbalanced data"""
        class_weights = compute_class_weight(
            class_weight='balanced',
            classes=np.unique(self.y),
            y=self.y
        )
        return dict(zip(np.unique(self.y), class_weights))
    
    def optimize_hyperparameters(self, n_trials: int = 30) -> dict:
        """Optimize hyperparameters using Optuna"""
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        class_weights_dict = self.compute_class_weights()
        
        def objective(trial):
            # Define hyperparameters to optimize
            params = {
                'n_estimators': trial.suggest_int('n_estimators', 50, 300),
                'max_depth': trial.suggest_int('max_depth', 5, 50),
                'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
                'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 20),
                'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None])
            }
            
            cv_scores = []
            
            for train_idx, test_idx in skf.split(self.X, self.y):
                X_train, X_test = self.X.iloc[train_idx], self.X.iloc[test_idx]
                y_train, y_test = self.y[train_idx], self.y[test_idx]
                
                rf = RandomForestClassifier(
                    **params,
                    random_state=42,
                    class_weight=class_weights_dict,
                    n_jobs=-1
                )
                rf.fit(X_train, y_train)
                
                y_pred = rf.predict(X_test)
                f1 = f1_score(y_test, y_pred, average='weighted')
                cv_scores.append(f1)
            
            return np.mean(cv_scores)

        # Run Optuna study
        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=n_trials)
        
        # Get best parameters
        self.best_params = study.best_params
        return self.best_params
    
    def train_model(self, params: dict = None) -> RandomForestClassifier:
        """Train model with given or optimized parameters"""
        if params is None:
            if self.best_params is None:
                raise ValueError("No parameters provided. Run optimize_hyperparameters first.")
            params = self.best_params
            
        class_weights_dict = self.compute_class_weights()
        
        self.model = RandomForestClassifier(
            n_estimators=params['n_estimators'],
            max_depth=params['max_depth'],
            min_samples_split=params['min_samples_split'],
            min_samples_leaf=params['min_samples_leaf'],
            max_features=params['max_features'],
            random_state=42,
            class_weight=class_weights_dict,
            n_jobs=-1
        )
        
        self.model.fit(self.X, self.y)
        return self.model
    
    def evaluate_model(self) -> dict:
        """Evaluate model using cross-validation"""
        if self.model is None:
            raise ValueError("Model not trained. Run train_model first.")
            
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        all_metrics = {
            'f1_scores': [],
            'accuracy_scores': [],
            'reports': [],
            'confusion_matrices': []
        }
        
        for train_idx, test_idx in skf.split(self.X, self.y):
            X_train, X_test = self.X.iloc[train_idx], self.X.iloc[test_idx]
            y_train, y_test = self.y[train_idx], self.y[test_idx]
            
            # Train model on this fold
            class_weights_dict = self.compute_class_weights()
            rf = RandomForestClassifier(
                **self.best_params,
                random_state=42,
                class_weight=class_weights_dict,
                n_jobs=-1
            )
            rf.fit(X_train, y_train)
            
            # Predict
            y_pred = rf.predict(X_test)
            
            # Calculate metrics
            f1 = f1_score(y_test, y_pred, average='weighted')
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred, output_dict=True)
            cm = confusion_matrix(y_test, y_pred)
            
            all_metrics['f1_scores'].append(f1)
            all_metrics['accuracy_scores'].append(accuracy)
            all_metrics['reports'].append(report)
            all_metrics['confusion_matrices'].append(cm)
        
        # Add mean scores
        all_metrics['mean_f1'] = np.mean(all_metrics['f1_scores'])
        all_metrics['mean_accuracy'] = np.mean(all_metrics['accuracy_scores'])
        
        return all_metrics
    
    def save_model(self, filepath: str = 'respiratory_classifier.pkl'):
        """Save trained model to file"""
        if self.model is None:
            raise ValueError("Model not trained. Run train_model first.")
            
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")


# ZenML pipeline steps
@step
def ingest_data(audio_file_path: str) -> Dict:
    """Step to ingest audio data"""
    audio_files = glob(audio_file_path)
    data_ingestion = DataIngestion(audio_files)
    audio_data = data_ingestion.load_audio_files()
    audio_data_with_duration = data_ingestion.calculate_durations()
    min_duration = data_ingestion.get_min_duration()
    
    return {
        "audio_data": audio_data_with_duration,
        "min_duration": min_duration
    }

@step
def preprocess_data(ingestion_result: Dict) -> Dict:
    """Step to preprocess audio data"""
    audio_data = ingestion_result["audio_data"]
    min_duration = ingestion_result["min_duration"]
    
    preprocessor = DataPreprocessor(audio_data=audio_data, target_duration=min_duration)
    trimmed_audio = preprocessor.trim_audio_data()
    audio_features = preprocessor.extract_all_features()
    features_df = preprocessor.calculate_all_feature_stats(audio_features)
    
    return {
        "features_df": features_df
    }

@step
def process_features(preprocessing_result: Dict, diagnosis_path: str) -> Tuple[pd.DataFrame, np.ndarray]:
    """Step to process features and prepare for modeling"""
    features_df = preprocessing_result["features_df"]
    
    processor = FeatureProcessor(features_df)
    features_with_diagnosis = processor.load_patient_diagnosis(diagnosis_path)
    X, y = processor.encode_target()
    
    return X, y

@step
def train_and_evaluate_model(X: pd.DataFrame, y: np.ndarray, n_trials: int = 30) -> Dict:
    """Step to train and evaluate model"""
    trainer = ModelTrainer(X, y)
    best_params = trainer.optimize_hyperparameters(n_trials)
    model = trainer.train_model(best_params)
    evaluation_metrics = trainer.evaluate_model()
    trainer.save_model()
    
    return {
        "best_params": best_params,
        "evaluation_metrics": evaluation_metrics
    }

@step
def prediction_function(model_path: str, audio_file: str) -> Dict:
    """Step to make predictions on new data"""
    # Load the saved model
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file {model_path} not found")
    
    model = joblib.load(model_path)
    
    # Process audio file
    preprocessor = DataPreprocessor(target_duration=7.8560090702947845)
    y, sr = preprocessor.get_trimmed_audio(audio_file)
    features = preprocessor.feature_extraction(audio_file)
    stats = preprocessor.feature_stats(features)
    
    # Convert to DataFrame for prediction
    features_df = pd.DataFrame([stats])
    
    # Exclude features that weren't used in training
    excluded_features = ['mel_spectrogram_min', 'chroma_stft_max']
    for feature in excluded_features:
        if feature in features_df.columns:
            features_df = features_df.drop(feature, axis=1)
    
    # Make prediction
    prediction_code = model.predict(features_df)[0]
    probabilities = model.predict_proba(features_df)[0]
    
    # Map to diagnosis labels (assuming original order from training)
    diagnosis_labels = ['Asthma', 'Bronchiectasis', 'Bronchiolitis', 'COPD', 
                        'Healthy', 'LRTI', 'Pneumonia', 'URTI']
    
    prediction = diagnosis_labels[prediction_code]
    all_probs_dict = {diagnosis_labels[i]: prob for i, prob in enumerate(probabilities)}
    
    return {
        'prediction': prediction,
        'probability': np.max(probabilities),
        'all_probabilities': all_probs_dict
    }

# Define ZenML pipeline
@pipeline
def respiratory_sound_classification_pipeline(
    audio_file_path: str, 
    diagnosis_path: str,
    n_trials: int = 30
):
    """Full pipeline for respiratory sound classification"""
    ingestion_result = ingest_data(audio_file_path)
    preprocessing_result = preprocess_data(ingestion_result)
    X, y = process_features(preprocessing_result, diagnosis_path)
    model_result = train_and_evaluate_model(X, y, n_trials)
    
    return model_result


# Function to run the pipeline
def run_pipeline():
    """Run the ZenML pipeline"""
    audio_path = '../../audioscopeAI/src/audioscopeAI_AI-ML/Respiratory_Sound_Database/audio_and_txt_files/*.wav'
    diagnosis_path = '../../audioscopeAI/src/audioscopeAI_AI-Ml/Respiratory_Sound_Database/patient_diagnosis.csv'
    
    # Run the pipeline
    pipeline_result = respiratory_sound_classification_pipeline(
        audio_file_path=audio_path,
        diagnosis_path=diagnosis_path,
        n_trials=30
    )

    # Connect to ZenML and fetch the last run
    client = Client()
    run = client.get_pipeline_run(pipeline_result.id)

    # Get the step run for 'train_and_evaluate_model'
    step_run = run.steps["train_and_evaluate_model"]

    # Inspect the outputs
    output_artifacts = step_run.outputs["output"]  # This is likely a list
    if isinstance(output_artifacts, list):
        # Assuming the first item in the list contains the artifact URI
        artifact_uri = output_artifacts[0].uri
    else:
        artifact_uri = output_artifacts.uri

    # Load the dictionary from the artifact
    with open(artifact_uri, "rb") as f:
        model_results = pickle.load(f)

    # Access and print the values
    print(f"Best parameters: {model_results['best_params']}")
    print(f"Mean F1 score: {model_results['evaluation_metrics']['mean_f1']:.4f}")
    print(f"Mean accuracy: {model_results['evaluation_metrics']['mean_accuracy']:.4f}")

# Pipeline for making predictions
@pipeline
def respiratory_prediction_pipeline(model_path: str, audio_file: str):
    """Pipeline for making predictions on a single audio file"""
    return prediction_function(model_path, audio_file)


# Function to predict respiratory condition
def predict_respiratory_condition(audio_file: str, model_path: str = 'respiratory_classifier.pkl'):
    """Predict respiratory condition from audio file"""
    result = respiratory_prediction_pipeline(
        model_path=model_path,
        audio_file=audio_file
    )
    
    return result


if __name__ == "__main__":
    # Run the pipeline
    run_pipeline()
    
    # Example prediction
    # prediction = predict_respiratory_condition(
    #     audio_file='../../audioscopeAI/src/audioscopeAI_AI-ML/Respiratory_Sound_Database/audio_and_txt_files/149_1b1_Pl_sc_Meditron.wav'
    # )
    # print(f"Predicted condition: {prediction['prediction']} (confidence: {prediction['probability']:.2f})")

