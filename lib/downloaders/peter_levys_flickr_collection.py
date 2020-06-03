#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import requests

def get_url_to_wallpaper():
    """Retrieves the URL of the latest image of Peter Levi's Flickr Collection,
    downloads the image, stores it in a temporary folder and returns the path
    to it
    """
    # get image url
    response = requests.get("https://www.flickr.com/photos/peter-levi/")
    match = re.search('([0-9]{10})_.*\.jpg\)', response.text)
    image_id = match.group(1)
    image_url = "https://www.flickr.com/photos/peter-levi/"+image_id+"/sizes/h/"
    response = requests.get(image_url)
    pattern = 'http.*'+image_id+'.*_h\.jpg'
    match = re.search(pattern, response.text)
    full_image_url = match.group(0)

    # image's name
    image_name = getGeneratedImageName(full_image_url)

    # Check and maintain DB
    if not existsImageInDatabase(full_image_url):
        addImageToDatabase(full_image_url, image_name, "flickr")
        # download and save image
        full_image_path = downloadImage(full_image_url, image_name)
        updateImageInDatabase(full_image_url, full_image_path)
    else:
        full_image_path = getImagePathFromDatabase(full_image_url)

    # Return full path to image
    return full_image_path