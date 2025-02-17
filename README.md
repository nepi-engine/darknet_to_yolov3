
# Converts a nepi darknet_ros models folder into a nepi yolov3 models folder

# 1) Connect your nepi device to the internet
# 2) ssh into your nepi system then run
cd /mnt/nepi_storage/ai_models
git https://github.com/nepi-engine/darknet_to_yolov3.git
cd darknet_to_yolov3
sudo python convert_nepi_darknet_files.py

