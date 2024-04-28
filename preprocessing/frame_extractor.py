import cv2
import numpy as np
import time
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import svds
import os


class VideoKeyFrameExtractor:
    def __init__(self, video_path, output_dir='output', threshold=0.9, min_cluster_size=25):
        """
        Initializes the VideoKeyFrameExtractor class with the path to the video, the output directory, and parameters for processing.

        Args:
        video_path (str): Path to the video file.
        output_dir (str): Directory to store output key frames.
        threshold (float): Cosine similarity threshold for clustering frames.
        min_cluster_size (int): Minimum number of frames in a cluster to consider for key frame extraction.
        """
        self.video_path = video_path
        self.output_dir = output_dir
        self.cap = cv2.VideoCapture(video_path)
        self.threshold = threshold
        self.min_cluster_size = min_cluster_size
        self.frame_dict = {}
        self.feature_array = np.empty((0, 1944), int)

    def process_video(self):
        """
        Processes the video to extract frames and compute their features, performing SVD and dynamic clustering to find key frames.
        """
        print("Extracting Frames...")
        count = 0
        start_time = time.time()
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frame_dict[count] = frame_rgb
            feature_vector = self.extract_features(frame_rgb)
            self.feature_array = np.vstack(
                (self.feature_array, feature_vector))
            count += 1

        self.cap.release()
        print("Extraction Complete. Took --- %s seconds ---" %
              (time.time() - start_time))
        self.compute_svd()
        self.dynamic_clustering()

    def extract_features(self, frame_rgb):
        """
        Extracts color histogram features from a frame by dividing it into 3x3 blocks.

        Args:
        frame_rgb (numpy.ndarray): The RGB frame from which features are extracted.

        Returns:
        list: A flattened list of histogram features.
        """
        height, width, _ = frame_rgb.shape
        h_chunk, w_chunk = self.compute_chunk_sizes(height, width)
        feature_vector = []

        for a in range(3):
            h_start = h_chunk * a
            h_end = h_chunk * (a + 1)
            for b in range(3):
                w_start = w_chunk * b
                w_end = w_chunk * (b + 1)
                block = frame_rgb[h_start:h_end, w_start:w_end, :]
                hist = cv2.calcHist([block], [0, 1, 2], None, [
                                    6, 6, 6], [0, 256, 0, 256, 0, 256])
                feature_vector.extend(hist.flatten())

        return feature_vector

    def compute_chunk_sizes(self, height, width):
        """
        Computes the sizes of chunks for dividing the frame into 3x3 blocks.

        Args:
        height (int): The height of the frame.
        width (int): The width of the frame.

        Returns:
        tuple: The height and width of each chunk.
        """
        h_chunk = (height + 2) // 3
        w_chunk = (width + 2) // 3
        return h_chunk, w_chunk

    def compute_svd(self):
        """
        Computes the Singular Value Decomposition (SVD) of the feature matrix to reduce dimensionality.
        """
        A = csc_matrix(self.feature_array.T, dtype=float)
        _, s, vt = svds(A, k=63)
        self.vt = vt.T @ np.diag(s)

    def dynamic_clustering(self):
        """
        Performs dynamic clustering on the reduced dimensions from SVD to group similar frames.
        Determines key frames that represent significant changes in the video.
        """
        projections = self.vt
        # Initialize the first cluster with the first two frames
        self.clusters = {0: [0, 1]}
        # Initialize the first centroid
        self.centroids = {0: np.mean(projections[:2], axis=0)}

        for i in range(2, len(projections)):
            similarity = np.dot(projections[i], self.centroids[max(self.centroids)]) / (
                np.linalg.norm(projections[i]) * np.linalg.norm(self.centroids[max(self.centroids)]))
            if similarity < self.threshold:
                new_cluster_id = max(self.clusters) + 1
                self.clusters[new_cluster_id] = [i]
                self.centroids[new_cluster_id] = projections[i]
            else:
                last_cluster_id = max(self.clusters)
                self.clusters[last_cluster_id].append(i)
                self.centroids[last_cluster_id] = np.mean(
                    [projections[j] for j in self.clusters[last_cluster_id]], axis=0)
        self.cluster_sizes = [len(cluster)
                              for cluster in self.clusters.values()]
        print("Clustering complete...")
        self.identify_key_frames()

    def identify_key_frames(self):
        """
        Identifies key frames from each cluster by selecting the last frame of the cluster.
        Filters clusters to include only those with a sufficient number of frames.
        """
        self.key_frames_indices = []
        self.eligible_clusters = [cluster_id for cluster_id, size in enumerate(
            self.cluster_sizes) if size >= self.min_cluster_size]

        for cluster_id in self.eligible_clusters:
            last_frame_index = self.clusters[cluster_id][-1]
            self.key_frames_indices.append(last_frame_index)
        print("Keyframes identified...")
        self.output_key_frames()

    def output_key_frames(self):
        """
        Outputs the key frames as images to the specified directory.
        """
        print("Outputting to dir...")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        for i, frame_index in enumerate(self.key_frames_indices):
            frame_rgb = self.frame_dict[frame_index]
            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            file_name = os.path.join(self.output_dir, f'keyframe_{i}.png')
            cv2.imwrite(file_name, frame_bgr)


'''
Example Usage:


if __name__ == "__main__":
    video_path = 'sample_videos/bubble_sort.mp4'
    output_directory = 'output_frames'
    extractor = VideoKeyFrameExtractor(video_path, output_directory)
    extractor.process_video()

'''
