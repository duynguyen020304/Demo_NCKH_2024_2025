# 🚀 Aspect-Based Sentiment Analysis System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![PyTorch](https://img.shields.io/badge/PyTorch-1.0+-orange.svg)](https://pytorch.org/)
[![Transformers](https://img.shields.io/badge/Transformers-4.0+-yellow.svg)](https://huggingface.co/transformers/)

## 📋 Overview

**Aspect-Based Sentiment Analysis System** is an advanced web application built to analyze and evaluate student sentiment in course feedback. The system uses state-of-the-art deep learning models to automatically extract aspects and classify sentiment from Vietnamese text.

### 🎯 Key Features

- **🔍 Aspect Extraction**: Automatically identify aspects mentioned in feedback
- **😊 Sentiment Classification**: Determine positive, negative, or neutral sentiment for each aspect
- **📊 Visual Analytics**: Detailed charts and reports on sentiment and aspect distribution
- **📁 Batch Processing**: Support for analyzing text files with multiple sentences
- **🌐 Web Interface**: User-friendly Streamlit application
- **🔌 API Integration**: Flask API for integration with other systems

## 🏗️ System Architecture

### Deep Learning Models

1. **PhoBERT + CNN + LSTM** (`PhoBERT_CNN_LSTM`)
   - Uses Vietnamese language model PhoBERT
   - Combines with CNN and LSTM for text processing
   - High accuracy for Vietnamese language
   - Download link: https://drive.google.com/file/d/16QgcMh3AQl7NKuzUdDDF_faFORVKJpHo/view?usp=sharing [https://drive.google.com/file/d/16QgcMh3AQl7NKuzUdDDF_faFORVKJpHo/view?usp=sharing]

2. **CNN + BiLSTM + Attention** (`CNN_LSTM_ATTENTION`)
   - CNN model for local feature extraction
   - Bidirectional LSTM for context understanding
   - Attention mechanism to focus on important parts
   

### Technologies Used

- **Frontend**: Streamlit - Web framework for Python
- **Backend**: Flask API - Request handling and model processing
- **Database**: SQLite - Analysis data storage
- **ML Framework**: PyTorch, Transformers
- **Data Processing**: NumPy, Pandas
- **Visualization**: Plotly, Seaborn, Matplotlib

## 📦 Installation

### System Requirements

- **Python**: 3.7 or higher
- **RAM**: Minimum 4GB (recommended 8GB+)
- **GPU**: Not required, but recommended for faster processing

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd Demo_NCKH_2024_2025
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download Models (If Needed)

Ensure the following model files are in the project directory:
- `best_vinai_phobert-base-v2_aspect_cateogry_analysis_sigmoid_prob.pth` (PhoBERT model)
- `cnn_lstm_attention_component/` (CNN-LSTM model files)
- `tokenizer_data.pkl` (Tokenizer data)

## 🚀 Usage

### Run Web Application

```bash
streamlit run app.py
```

The application will open at: `http://localhost:8501`

### Run Flask API

```bash
python flask_api_multi_model_host.py
```

API will run at: `http://localhost:5000`

## 📱 User Guide

### 1. Analysis Page 📊

- **Input Text**: Type directly the sentence to analyze
- **Upload File**: Select .txt file for batch analysis
- **Model Selection**: Choose between PhoBERT or CNN-LSTM-Attention
- **Results**: Display detected (aspect, sentiment) pairs

### 2. Statistics Page 📈

- **Distribution Charts**: Sentiment and aspects over time
- **Filters**: By semester, course, class
- **Data Export**: Download reports in CSV/Excel format

### 3. Settings Page ⚙️

- **Interface Customization**: Colors, fonts
- **Model Configuration**: Classification thresholds, parameters

## 🔌 API Endpoints

### Analyze Text

```http
POST /predict
Content-Type: application/json

{
    "text": "The instructor teaches very well and is easy to understand",
    "model": "PhoBERT_CNN_LSTM"
}
```

**Response:**
```json
{
    "success": true,
    "predictions": [
        {
            "aspect": "Instructor",
            "sentiment": "Positive"
        },
        {
            "aspect": "Teaching Method", 
            "sentiment": "Positive"
        }
    ]
}
```

### List Available Models

```http
GET /models
```

## 📊 Data Structure

### Database Schema

- **Sentence**: Original text
- **Aspect**: Mentioned aspect
- **Sentiment**: Sentiment (Positive/Negative/Neutral)
- **Course**: Subject
- **Class**: Class
- **Semester**: Academic term

### Data Files

- `data_20k.xlsx`: Sample dataset with 20,000 sentences
- `output_text_files/`: Sample text files for testing

## 🧪 Testing

### Test Models

```bash
# Test PhoBERT model
python -c "
from flask_api_multi_model_host import predict_pho
result = predict_pho('The instructor teaches very well')
print(result)
"

# Test CNN-LSTM model  
python -c "
from flask_api_multi_model_host import predict_cnn
result = predict_cnn('The instructor teaches very well')
print(result)
"
```

## 📈 Performance
- **Language Support**: Vietnamese (can be extended for other languages)

## 🤝 Contributing

We welcome all contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 👥 Authors

- **Research Group**: NCKH 2024-2025
- **Email**: [your-email@domain.com]
- **GitHub**: [your-github-username]

## 🙏 Acknowledgments

- PhoBERT team for Vietnamese language model
- Streamlit team for excellent web framework
- Python open source community

## 📞 Contact

If you have questions or encounter issues, please:

- Create an issue on GitHub
- Contact directly via email
- Join discussions in Discussions

---

⭐ **If this project is helpful, please give us a star on GitHub!**
