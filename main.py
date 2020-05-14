import cv2
import pickle
import czifile
import numpy as np
import os
from time import time

def read_preprocessed(file_name, cell_id, image_number):
    image = cv2.imread(f"images/{file_name}_{cell_id}/Images{image_number}.jpg")
    return image

def get_landmarks(image):
    saturation_epsilon = 20
    no_grayscale = image.copy()
    for i in range(0, no_grayscale.shape[0]):
        for j in range(0, no_grayscale.shape[1]):

            distance = abs(int(no_grayscale[i][j][0]) - int(no_grayscale[i][j][1]))
            distance2 = abs(int(no_grayscale[i][j][1]) - int(no_grayscale[i][j][2]))

            if no_grayscale[i][j][0] == no_grayscale[i][j][1] == no_grayscale[i][j][2]:
                no_grayscale[i][j][0], no_grayscale[i][j][1], no_grayscale[i][j][2] = (0, 0, 0)
            elif distance <= saturation_epsilon and distance2 <= saturation_epsilon and no_grayscale[i][j][2] <= 160:
                no_grayscale[i][j][0], no_grayscale[i][j][1], no_grayscale[i][j][2] = (0, 0, 0)
            else:
                #print(no_grayscale[i][j][0], no_grayscale[i][j][1],no_grayscale[i][j][2])
                no_grayscale[i][j][0], no_grayscale[i][j][1],no_grayscale[i][j][2] = (0, 0, 255)

    #cv2.imshow('noname', no_grayscale)
    landmarks = cv2.Canny(no_grayscale, 100, 200)
    return landmarks

def get_centroid(image_shape):
    avg_x = 0.0
    avg_y = 0.0
    points_count = 0
    for i in range(0, image_shape.shape[0]):
        for j in range(0, image_shape.shape[1]):
            if image_shape[i][j] > 0:
                avg_x += i
                avg_y += j
                points_count += 1
    print(int(avg_x/points_count), int(avg_y/points_count))
    return (int(avg_x/points_count), int(avg_y/points_count))

def translate(to, centroid, image_shape):

    for i in range(0, image_shape.shape[0]):
        for j in range(0, image_shape.shape[1]):
            if image_shape[i][j] > 0:
                image_shape[i][j] = 0
                new_i = int(i - centroid[0]) + to[0]
                new_j = int(j - centroid[1]) + to[1]
                image_shape[new_i][new_j] = 255

    return image_shape

# distance between pixels
def in_rangeof(landmarks, point, distance=3):
    for landmark in landmarks:
        if abs(landmark[0]-point[0])+ abs(landmark[1]-point[1]) < distance:
            return True
    return False


if __name__ == "__main__":

    "(start_slice, cell_id, data_file)"
    images_data = [(29, 0, "p3.dat"),
                (29, 1, "p3.dat"),
                (25, 2, "p3.dat"),
                (35, 0, "p6.dat")]
    z_resolution = 4.0
    first = True
    recommended = 100
    shapes = []
    for element in images_data:
        print("---NEW image data---")
        shape_data = []
        start_slice = element[0]
        cell_id = element[1]
        file_name = element[2]

        preprocessed_image = read_preprocessed(file_name, cell_id, start_slice)

        land_marks = get_landmarks(preprocessed_image)
        centroid = get_centroid(land_marks)
        cv2.imwrite(f"images/landmarks/image{start_slice}.jpg", land_marks)

        translated = translate((300, 300), centroid, land_marks)
        new_imagesize = (600, 600)
        cropped = translated[0:new_imagesize[0], 0:new_imagesize[1]]

        reduced_landmarks = np.zeros((600, 600))
        current_landmarks = []

        default_distance = 12
        while len(current_landmarks) != recommended:
            for i in range(0, cropped.shape[0]):
                for j in range(0, cropped.shape[1]):
                    if cropped[i][j] > 0:
                        point = (i, j)
                        if not in_rangeof(current_landmarks, point, default_distance):
                            current_landmarks.append((i,j, 0*z_resolution))
                            reduced_landmarks[i][j] = 255
                            if len(current_landmarks) == recommended:
                                break
                if len(current_landmarks) == recommended:
                    break
            if len(current_landmarks) == recommended:
                break
            default_distance -= 1
            if default_distance < 0:
                print("fail")
                break

        cv2.imwrite(f"images/reduced/image{start_slice}{time()}.jpg", reduced_landmarks)
        print("landmarks: " + str(len(current_landmarks)))

        current_landmarks.sort()
        print(current_landmarks)
        shape_data += current_landmarks

        slices_count = 15
        for k in range(start_slice+1, start_slice+slices_count):

            cropped = None
            if not os.path.exists(f"images/cropped_cache/{file_name}_{cell_id}_r{k}_cache.dat"):
                preprocessed_image = read_preprocessed(file_name, cell_id, k)

                land_marks = get_landmarks(preprocessed_image)
                cv2.imwrite(f"images/landmarks/image{k}.jpg", land_marks)

                translated = translate((300, 300), centroid, land_marks)

                new_imagesize = (600, 600)
                cropped = translated[0:new_imagesize[0], 0:new_imagesize[1]]
                with open(f"images/cropped_cache/{file_name}_{cell_id}_r{k}_cache.dat", 'wb+') as f:
                    pickle.dump(cropped, f)
            else:
                with open(f"images/cropped_cache/{file_name}_{cell_id}_r{k}_cache.dat", mode="rb+") as f:
                    cropped = pickle.load(f)


            reduced_landmarks = np.zeros((600, 600))
            current_landmarks = []

            default_distance = 12
            while len(current_landmarks) != recommended:
                for i in range(0, cropped.shape[0]):
                    for j in range(0, cropped.shape[1]):
                        if cropped[i][j] > 0:
                            point = (i, j)
                            if not in_rangeof(current_landmarks, point, default_distance):
                                current_landmarks.append((i,j, (k-start_slice)*z_resolution))
                                reduced_landmarks[i][j] = 255
                                if len(current_landmarks) == recommended:
                                    break
                    if len(current_landmarks) == recommended:
                        break
                if len(current_landmarks) == recommended:
                    break
                default_distance -= 1
                if default_distance < 0:
                    print("fail")
                    break

            print("landmarks: " + str(len(current_landmarks)))
            current_landmarks.sort()
            print(current_landmarks)
            shape_data += current_landmarks
            cv2.imwrite(f"images/reduced/image{k}{time()}.jpg", reduced_landmarks)

        shapes.append(shape_data)

    if True:
        with open("shapes.dat", mode="wb+") as f_shapes:
            pickle.dump(shapes, f_shapes)
