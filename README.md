Link to Github Repo: https://github.com/Satyam52/seamlessM4T_low_resource

### **Requirements and Installation**
* **Create a directory named "slt"**
```cd slt``` then
```git clone https://github.com/Satyam52/seamlessM4T_low_resource.git . ```

* **Create a docker container and map to this directory so all data and codebase are accessible**
```docker run -d -it --name=seamless_slt  --gpus all --ipc=host -p 4587:8888 -v `pwd`:/slt nvidia/cuda:12.2.0-base-ubuntu22.04```

* **Enter into the docker container**
```docker exec -it seamless_slt bash``` then
```cd slt```

* **Upgrade the packages**
```apt upgrade``` and 
```apt upgrade -y```

* **Install pip, python, and libsndfile**
```apt install python-is-python3``` and 
```apt install python3-pip``` and 
```apt install libsndfile1```

* **Now finally install seamlessM4T in editable mode**
```cd codebase/seamless``` then
```pip install -e .```

* **Install some utility packages**
```pip install Levenshtein``` and 
```pip install soundfile``` and 
```pip install pydub```

### **Data Preparation for Inferencing**
Data for inference is present in the data directory, the audio is zipped into mai.tgz and the corresponding .json is present which is required by seamlessM4T. This inference data is taken from the IndicVoices validation split as the test split has yet to be released.

```cd data``` and extract maithili audio data 
```tar xvf mai.tgz```

**Inferencing**
Inferencing Script: https://github.com/Satyam52/seamlessM4T_low_resource/tree/main/scripts <br>
Model link: https://drive.google.com/drive/folders/1eQkLjzh5FBgwnZFgBh12bQwHB6CD4ypJ?usp=sharing <br> 
* Create a directory called checkpoint ```mkdir checkpoint``` and put the model there
Usage: provided in inference.sh present in the scripts directory

**If you are following all the above instructions just execute the ```bash inference.sh``` and it will generate a json file with original and predicted text along the utterance id and audio path.**

**It also generates .wer file with an average word error rate and char error rate.**

If you have changed the paths make appropriate changes in the inference.sh file.
