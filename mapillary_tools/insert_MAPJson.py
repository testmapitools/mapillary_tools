import os
import time
import uuid
import sys
import processing
import uploader


def insert_MAPJson(import_path,
                   master_upload=False,
                   verbose=False,
                   rerun=False,
                   skip_subfolders=False,
                   skip_EXIF_insert=False,
                   keep_original=False,
                   video_path=None):

    # sanity check if video file is passed
    if video_path and not (os.path.isdir(video_path) or os.path.isfile(video_path)):
        print("Error, video path " + video_path +
              " does not exist, exiting...")
        sys.exit(1)

    # in case of video processing, adjust the import path
    if video_path:
        # set sampling path
        video_sampling_path = processing.sampled_video_frames_rootpath(
            video_path)
        import_path = os.path.join(os.path.abspath(import_path), video_sampling_path) if import_path else os.path.join(
            os.path.dirname(video_path), video_sampling_path)

    # basic check for all
    if not import_path or not os.path.isdir(import_path):
        print("Error, import directory " + import_path +
              " does not exist, exiting...")
        sys.exit(1)

    # get list of file to process
    process_file_list = processing.get_process_file_list(import_path,
                                                         "mapillary_image_description",
                                                         rerun,
                                                         verbose,
                                                         skip_subfolders)
    if not len(process_file_list):
        print("No images to run process finalization")
        print("If the images have already been processed and not yet uploaded, they can be processed again, by passing the argument --rerun")

    for image in process_file_list:
        # check the processing logs
        log_root = uploader.log_rootpath(image)

        duplicate_path = os.path.join(log_root,
                                      "duplicate")

        if os.path.isfile(duplicate_path):
            continue

        final_mapillary_image_description = processing.get_final_mapillary_image_description(log_root,
                                                                                             image,
                                                                                             master_upload,
                                                                                             verbose,
                                                                                             skip_EXIF_insert,
                                                                                             keep_original)

        processing.create_and_log_process(image,
                                          "mapillary_image_description",
                                          "success",
                                          final_mapillary_image_description,
                                          verbose=verbose)
