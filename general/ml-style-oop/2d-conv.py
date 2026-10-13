# PROBLEM: Implement 2D Convolution 
#
# Given a 2D image and a 2D kernel, compute the valid
# convolution output without NumPy or external libraries.
#
# Rules:
# - Stride = 1
# - No padding
# - Do not flip the kernel
# - Inputs are nonempty, rectangular matrices
# - Kernel fits inside the image
#
# Example:
# image = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9]
# ]
#
# kernel = [
#     [1,  0],
#     [0, -1]
# ]
#
# Expected:
# [
#     [-4, -4],
#     [-4, -4]
# ]
#
# FOLLOW-UPS (do not implement yet):
# 1. Arbitrary stride
# 2. Zero padding
# 3. Multi-channel inputs and multiple filters

def conv2d(image, kernel, stride=1, padding=0):

    # add padding
    if padding > 0:
        cols = len(image[0]) + 2 * padding

        padded = [[0] * cols for _ in range((padding))]

        for row in image:
            padded.append([0] * padding + row + [0] * padding)

        padded += [[0] * cols for _ in range((padding))]
        image = padded

    image_rows = len(image)
    image_cols = len(image[0])
    kernel_rows = len(kernel)
    kernel_cols = len(kernel[0])
    
    col_shift = image_cols - kernel_cols + 1
    row_shift = image_rows - kernel_rows + 1

    conv = []
    print(col_shift, row_shift, kernel_rows, kernel_cols)
    for x in range(0, row_shift, stride):
        row = []
        for y in range(0, col_shift, stride):
            total = 0
            for r in range(kernel_rows):
                for c in range(kernel_cols):
                    total += image[x + r][y + c] * kernel[r][c]
            row.append(total)
            print("TOTAL", total)
        print("ROW:", row)
        conv.append(row)

    print(conv)
    return conv


# image = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9]
# ]

# kernel = [
#     [1,  0],
#     [0, -1]
# ]

# image = [
#     [1,  2,  3,  4,  5],
#     [6,  7,  8,  9, 10],
#     [11, 12, 13, 14, 15],
#     [16, 17, 18, 19, 20]
# ]

# kernel = [
#     [1, 0],
#     [0, 1]
# ]

# image = [
#     [1, 2],
#     [3, 4]
# ]

# kernel = [
#     [1, 1],
#     [1, 1]
# ]

# image = [
#     # Channel 0
#     [[1, 2, 3],
#      [4, 5, 6],
#      [7, 8, 9]],

#     # Channel 1
#     [[9, 8, 7],
#      [6, 5, 4],
#      [3, 2, 1]]
# ]

# filters = [
#     # Filter 0
#     [
#         [[1, 0],
#          [0, 1]],

#         [[0, 1],
#          [1, 0]]
#     ],

#     # Filter 1
#     [
#         [[1, 1],
#          [1, 1]],

#         [[0, 0],
#          [0, 0]]
#     ]
# ]

print("RESULT: ", conv2d(image, kernel, stride=1, padding=1))