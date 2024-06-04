import torch
from seamless_communication.inference import Translator
from pathlib import Path
import json
import os
from tqdm import tqdm
import soundfile as sf
import argparse

device = torch.device("cuda")

import random
import numpy as np

def set_seed(seed: int = 42) -> None:
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    os.environ["PYTHONHASHSEED"] = str(seed)
    print(f"Random seed set as {seed}")
    
set_seed(42)


def main(test_path, infe_path, lang_code):
    data_list = []

    # show progress bar
    duration = 0
    with open(test_path, 'r', encoding='utf-8') as f:
        idx=0
        for line in tqdm(f):
            data = json.loads(line)
            wav_path = data['source']['audio_local_path']
            _id = data['source']['id']   
            orginal_text = data['target']['text']
            text_output, _ = translator.predict(
                input=wav_path,
                task_str="ASR",
                tgt_lang=lang_code,
                unit_generation_opts=None
            )
            s_data, sample_rate = sf.read(wav_path)
            file_duration = s_data.shape[0] / sample_rate
            duration += file_duration
            data_dict = {
                'id': _id,
                'original_text': orginal_text,
                'predicted_text': text_output[0].__str__(),
                'wav_path': wav_path
            }
            data_list.append(data_dict)
            idx+=1

    print("Test duration: ", duration/60/60)
    with open(infe_path, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--path_test_dataset', type=str, required=True)
    args.add_argument('--model_yaml_name', type=str, required=True)
    args.add_argument('--path_inference_file', type=str, required=True)
    args.add_argument('--lang_code', type=str, required=True)
    args = args.parse_args()    
    translator = Translator(args.model_yaml_name, "vocoder_36langs", device=device)
    main(args.path_test_dataset, args.path_inference_file, args.lang_code)