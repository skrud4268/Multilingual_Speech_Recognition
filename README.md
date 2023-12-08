# Multilingual Speech Recognition Project

## Project Overview

In the realm of artificial intelligence, understanding multilingual sentences in audio clips presents a significant challenge. Current technologies like Siri, Alexa, and Google Nest are limited to understanding and performing tasks in a single pre-set language. Our project aims to advance these technologies, enabling them to comprehend and converse in multiple languages within the same sentence, thereby making interactions with AI more human-like.

## Objectives

The goal of this project is to develop a speech recognition system that can classify and identify languages at the word level in multilingual sentences. Using deep learning techniques and machine learning models, we aim to fine-tune a pre-trained wav2vec model with a custom dataset in WAV format. The objective is to enhance the model's ability to decode and process mixed-language audio clips efficiently.

### Specific Goals

- Create a dataset for audio sequence classification in multilingual sentences.
- Fine-tune a pre-trained wav2vec model with this dataset.
- Evaluate the performance of the model.

## How to Run the Code

### Prerequisites

- Python environment with necessary libraries installed.
- Access to a GPU for training (can use Google Colab with GPU runtime).

### Setup and Execution

1.  **Preparing the Data:**

    Files: `Koreanfood_data.py`, `sentence_to_word.py`

    - These scripts break down sentences into word-level segments, convert them to WAV format using TTS, and store them in the `segments` folder.
    - Each segment is labeled as either English or Korean, and a CSV file containing the segment audio file names and their corresponding labels is generated.
    - The individual segment audio files are merged with a 400-millisecond pause between them to form sentence audio files, which are stored in the `sentences` folder.

2.  **Fine-Tuning the Model:**

        File: `Multilingual.ipynb`

        - Utilizes the audio files and labels from the `segments` folder for model training.
        - Installation of required packages:

          ```bash
          pip install accelerate -U
          pip3 install datasets
          ```

        - Important imports:

          ```python
          import torch
          from transformers import AutoProcessor, Wav2Vec2ForSequenceClassification, TrainingArguments, Trainer
          from datasets import Dataset, DatasetDict, load_metric
          import librosa
          import pandas as pd
          from sklearn.model_selection import train_test_split
          ```

        - Load data, map data and load model

        - Preprocess audio files

        ```
        # Function to load and preprocess the audio file using librosa

        def preprocess_data(batch):
        batch_input_values = []
        batch_labels = []

        for file_path in batch["file"]:
            # Read audio file with librosa
            audio_input, sr = librosa.load(file_path, sr=16_000)
            # Process audio file
            inputs = processor(audio_input, sampling_rate=sr, return_tensors="pt", padding=True)
            batch_input_values.append(inputs.input_values.squeeze().numpy())
            batch_labels.append(label_to_id[file_label_map[file_path.split("/")[-1]]])
        batch["input_values"] = batch_input_values
        batch["labels"] = batch_labels
        return batch
        ```

        - Prepare and split dataset

        ```
        # Prepare dataset paths

        audio_files = df['Filename'].tolist()
        audio_files = ['segments/' + file for file in audio_files] # Ensure correct path formation

        # Split dataset into training and validation

        train_files, val_files = train_test_split(audio_files, test_size=0.2, random_state=42)
        train_df = pd.DataFrame(train_files, columns=['file'])
        val_df = pd.DataFrame(val_files, columns=['file'])
        ```

        - Convert DataFrames to Datasets and Apply Preprocessing

        ```
        # Convert DataFrames to Hugging Face Datasets
        train_dataset = Dataset.from_pandas(train_df)
        val_dataset = Dataset.from_pandas(val_df)

        # Apply preprocessing
        train_dataset = train_dataset.map(preprocess_data, batched=True)
        val_dataset = val_dataset.map(preprocess_data, batched=True)

        # Create a DatasetDict
        dataset_dict = DatasetDict({
            'train': train_dataset,
            'validation': val_dataset
        })
        ```

        - Define Training Arguments and Initialize Trainer

        ```
        # Define training arguments
        training_args = TrainingArguments(
            output_dir="./wav2vec2-language-classification",
            per_device_train_batch_size=2,  # Keeping the small batch size
            gradient_accumulation_steps=2,  # Adjusted accumulation steps
            evaluation_strategy="epoch",
            num_train_epochs=30,  # Keeping the increased epochs
            save_steps=500,
            eval_steps=250,  # Keeping more frequent evaluation
            learning_rate=3e-5,  # Further reduced learning rate
            weight_decay=0.02,  # Adjusted weight decay
        )

        # Initialize Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset_dict['train'],
            eval_dataset=dataset_dict['validation'],
            tokenizer=processor.feature_extractor,
        )
        ```

3.  **Model Evaluation:**

    - After training, save the model and processor.
    - Load the model, the processor, and the validation dataset.
    - Perform predictions on the validation dataset and generate a classification report and confusion matrix.

### Example Code Snippet for Evaluation

```python
import torch
from transformers import AutoProcessor, Wav2Vec2ForSequenceClassification, Trainer
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
from datasets import load_dataset

# Load model and processor
model_path = './saved_wav2vec2_model'
model = Wav2Vec2ForSequenceClassification.from_pretrained(model_path)
processor = AutoProcessor.from_pretrained(model_path)

# Initialize Trainer
trainer = Trainer(model=model, tokenizer=processor.feature_extractor)

# Perform predictions and generate report
# ... (code for prediction and evaluation)
```
