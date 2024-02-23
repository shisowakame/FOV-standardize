from dicom_viewer import dicom_viewer
from arguments import dicom_viewer_arguments

#python3 main.py RT-CT_41 preCBCT_41

if __name__ == '__main__':
    args, skip = dicom_viewer_arguments()
    dicom_viewer(args, skip)
