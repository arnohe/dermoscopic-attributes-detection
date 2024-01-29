from itertools import product
import sys

from dermo_attributes.config import preprocess_arguments, training_config
from dermo_attributes.io.class_id import read_training_splits
from dermo_attributes.io.paths import create_new_processed_folders
from dermo_attributes.io.preprocess import process_all
from dermo_attributes.io.download_dataset import download_dataset as download_dataset_function
from dermo_attributes.learning.sweep import search
from dermo_attributes.learning.training import train_unet
from dermo_attributes.results.tables import print_formatted_table


def download_dataset():
    download_dataset_function()


def preprocess_dataset():
    args = preprocess_arguments()
    create_new_processed_folders(args["dataset_name"])
    read_training_splits(args["dataset_name"])
    process_all(args["dataset_name"], args["size"])


def sweep_gridsearch():
    input_size = 512
    batch_size = 28
    list_alpha_gamma = list(product([0.5, 0.6, 0.7, 0.8], [1.0 / 3.0, 0.5, 0.75, 1]))
    search(input_size, batch_size, "binary_focal_loss", list_alpha_gamma)

    list_alpha_gamma = list(product([0.5, 0.6, 0.7, 0.8], [0.25, 0.5, 0.75, 1]))
    search(input_size, batch_size, "focal_tversky_loss", list_alpha_gamma)


def train_model():
    config = training_config()
    train_unet(config)


# def image_main():
#     best_tversky = ["1d5do82w", "gj7umvnc", "3hzrhmt5", "mtl9gfbi", "1p0fs67i"]
#     best_crossentropy = ["1kneet9g", "6a8kdbri", "366b6soy", "21ihgwob", "3466ju2v"]
#     cv2.imwrite("best_tversky_outputs_horizontal.png", rgb_to_bgr(make_test_images(best_tversky)))
#     cv2.imwrite("best_focal_outputs_horizontal.png", rgb_to_bgr(make_test_images(best_crossentropy)))
#
#
# def test_main():
#     best_tversky = ["1d5do82w", "gj7umvnc", "3hzrhmt5", "mtl9gfbi", "1p0fs67i"]
#     best_crossentropy = ["1kneet9g", "6a8kdbri", "366b6soy", "21ihgwob", "3466ju2v"]
#     result_1 = run_tests(best_tversky)
#     print("jaccard for tversky:", result_1)
#     result_2 = run_tests(best_crossentropy)
#     print("jaccard for crossentropy:", result_2)


def table_main():
    print_formatted_table()


if __name__ == "__main__":
    main_methods = {"download": download_dataset,
                    "preprocess": preprocess_dataset,
                    "train": train_model,
                    "sweep": sweep_gridsearch}
    if len(sys.argv) > 1 and sys.argv[1] in main_methods.keys():
        main_methods[sys.argv[1]]()
    else:
        methods_string = ", ".join(main_methods.keys())
        print("Use one of the following arguments to choose method: " + methods_string)
