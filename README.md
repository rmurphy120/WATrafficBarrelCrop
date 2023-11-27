# WATrafficBarrelCrop
Stores cropped images of any traffic barrel in the input photo

This is done using image masking. It creates a mask of red-orange colors which is then used to find contours. After some noise eliminating, the contours are sent to an algorithm where it finds traffic barrels by finding 3 contours stacked upon each other. These contour groups are then cropped and saved in the output file. This code is intended to be a proof of concept that we can then adapt to the project.
