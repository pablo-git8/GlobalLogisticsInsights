import torch
import joblib
from sklearn.preprocessing import LabelEncoder
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Function to classify text with BERT model
def ml_classification(input_text='Sample'):
    # Load the models and tokenizer
    path_to_bert_model = '../models/bert_risk/'
    cls_model = AutoModelForSequenceClassification.from_pretrained(path_to_bert_model)
    tokenizer_cls = AutoTokenizer.from_pretrained(path_to_bert_model)

    label_column_values = ["risks", "opportunities", "neither"]
    label_encoder = LabelEncoder()
    label_encoder.fit(label_column_values)
    # Save the fitted LabelEncoder for future use
    joblib.dump(label_encoder, f'{path_to_bert_model}/encoder_labels.pkl')

    # Set the device (GPU or CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Tokenize the input text
    inputs_cls = tokenizer_cls(input_text, return_tensors="pt", max_length=512, truncation=True)
    inputs_cls = {key: value.to(device) for key, value in inputs_cls.items()}
        
    # Move cls_model to the specified device
    cls_model = cls_model.to(device)

    # Perform classification
    outputs_cls = cls_model(**inputs_cls)
    logits_cls = outputs_cls.logits
    predicted_class = torch.argmax(logits_cls, dim=1).item()
        
    # Decode the predicted class index into the label string
    classification = label_encoder.inverse_transform([predicted_class])[0]

    return classification
