# **Breast Cancer Prediction Using Logistic Regression**

## **Overview**  
This project analyzes a breast cancer dataset and builds a **Logistic Regression** model to predict cancer diagnosis. The dataset is explored through **EDA**, skewness handling, and feature correlation analysis before training the model.

## **Dataset**  
The dataset contains various numerical features related to cell characteristics, with the **target variable (`diagnosis`)** indicating:  
- `0` → **Benign**  
- `1` → **Malignant**  

## **Steps Performed**  

### **1. Data Loading & Exploration**  
- Loaded the dataset using `pandas`  
- Checked data structure using `.head()`, `.info()`, `.describe()`  
- Verified missing and duplicate values  

### **2. Handling Skewness & Kurtosis**  
- Skewness checked using `skew()` and histograms  
- Kurtosis checked using `kurt()`  
- **Yeo-Johnson & Box-Cox transformations** applied for normalization  

### **3. Exploratory Data Analysis (EDA)**  
- **Pairplots** to analyze feature relationships  
- **Countplot** for diagnosis distribution  
- **Boxplots** to detect outliers  
- **Correlation Heatmap** to examine feature dependencies  

### **4. Model Building (Logistic Regression)**  
- Split data into training & testing sets (`train_test_split`)  
- Mapped the `diagnosis` column to numerical values  
- Trained **Logistic Regression** model  
- Predicted on test data & evaluated using **accuracy score**  

## **Results**  
The **Logistic Regression model** successfully classified breast cancer cases with good accuracy. Handling skewness & feature scaling improved the model's performance.

## **Conclusion**  
This project demonstrates the importance of **EDA, feature transformation, and predictive modeling** in medical diagnosis. Further improvements can be made by experimenting with other machine learning models.

---

## **Installation & Usage**  
### **Requirements**  
- Python 3.x  
- Pandas, NumPy, Matplotlib, Seaborn, Sci-kit Learn  

### **Run the Project**  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/breast-cancer-prediction.git
   ```
2. Navigate to the directory:  
   ```bash
   cd breast-cancer-prediction
   ```
3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Jupyter Notebook or Python script.

---

### **Future Enhancements**  
- Use **other ML models** (Random Forest, SVM, etc.) for comparison  
- Perform **feature engineering** for better accuracy  
- Implement **deep learning models** for advanced predictions  
