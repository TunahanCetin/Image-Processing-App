# Image Processing Application

## 📋 Overview
This is an **Object-Oriented Python GUI application** developed using **PyQt5** and **Scikit-Image** libraries.  
The project demonstrates **modular OOP design principles**, **Command Pattern (Undo/Redo)**, and **advanced GUI features** like toolbar, status bar, grouped actions.

---

## 🖼 Features
- **Open Image (From File or Sample Images)**
- **Conversion Operations**
  - RGB to Grayscale
  - RGB to HSV
- **Segmentation Operations**
  - Multi-Otsu Thresholding
  - Chan-Vese Segmentation
  - Morphological Snakes
- **Edge Detection Operations**
  - Sobel, Roberts, Scharr, Prewitt
- **Undo/Redo support (Command Pattern)**
- **Safe Save / Save As / Export As (supports automatic float/boolean handling)**
- **Status bar with user feedback**
- **Grouped toolbar with icons & tooltips**
- **Source and Output panels (with image metadata tooltip)**

---

## ⚙ Installation

```bash
pip install -r requirements.txt
