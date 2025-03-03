import os
import random
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score

def preprocess_and_extract_cells(image_path):
    """Preprocess the Sudoku image, extract the grid, and split it into cells."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    grid = binary[y:y + h, x:x + w]

    grid = cv2.resize(grid, (450, 450))
    cells = []
    cell_size = 50
    for i in range(9):
        for j in range(9):
            cell = grid[i * cell_size:(i + 1) * cell_size, j * cell_size:(j + 1) * cell_size]
            cell = cv2.resize(cell, (28, 28))
            cells.append(cell)

    return cells

def recognize_and_print_numbers_random(cells):
    """Generate random numbers for Sudoku cells and print the grid."""
    grid = []
    for _ in cells:
        random_digit = random.randint(1, 9) 
        grid.append(random_digit)

    # Print the 9x9 grid
    for i in range(9):
        print(grid[i * 9:(i + 1) * 9])

    return grid

# Paths
sudoku_images_folder = "C:/Users/asaf0/OneDrive/sudoku_deepLearning/dataset"

# Extract the cells from the first image for demonstration purposes
image_files = [
    os.path.join(sudoku_images_folder, f)
    for f in os.listdir(sudoku_images_folder)
    if f.endswith(('.png', '.jpg', '.jpeg'))
]

if len(image_files) > 0:
    test_image_path = image_files[0]  # Use the first image for testing
    test_cells = preprocess_and_extract_cells(test_image_path)  # Extract cells from the test image

    # Generate and print random numbers for the cells
    random_predictions = recognize_and_print_numbers_random(test_cells)

    # Display the full image
    image = cv2.imread(test_image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(10, 10))
    plt.imshow(image_rgb)
    plt.title("Full Sudoku Grid (Unseen by Model during Training)")
    plt.axis('off')
    plt.show()

    # Show the extracted cells
    plt.figure(figsize=(10, 10))
    for i in range(9):
        for j in range(9):
            plt.subplot(9, 9, i * 9 + j + 1)
            plt.imshow(test_cells[i * 9 + j], cmap="gray")
            plt.axis("off")
    plt.suptitle("Extracted Cells from the First Image")
    plt.show()

    true_labels = [random.randint(1, 9) for _ in range(81)]

    # Calculate and display precision and recall
    precision = precision_score(true_labels, random_predictions, average='weighted', zero_division=0)
    recall = recall_score(true_labels, random_predictions, average='weighted', zero_division=0)
    print(f"Precision of random predictions: {precision:.2f}")
    print(f"Recall of random predictions: {recall:.2f}")

    # Calculate and display accuracy
    true_labels = [random.randint(0, 9) for _ in range(81)]
    predictions = [random.randint(0, 9) for _ in range(81)]
    correct = sum([1 for true, pred in zip(true_labels, predictions) if true == pred])
    accuracy = correct / len(true_labels) * 100
    print(f"Accuracy of random predictions: {accuracy:.2f}%")
