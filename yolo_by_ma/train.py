import os
import sys
sys.path.append(os.path.abspath('./pytorch_yolov3'))

import train_custom

if __name__ == "__main__":
    train_custom.main()
