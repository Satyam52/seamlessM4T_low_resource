import os
import soundfile as sf
import json
import uuid
import re
from pydub import AudioSegment
import soundfile
import argparse
from tqdm import tqdm

def clean_text(text):
    # text = re.sub(r"\[.+?\]", "", text).strip()
    text = re.sub(r"(\[|\])*[a-zA-Z]*", '', text).strip()
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r'[.,"!@#$%^&*()_+?<>{}-]', '', text)
    return text


def split_and_save(input_file, output_dir, min_duration=0):
    ## Search .wav file and corresponding .json file
    complete_data_list = []
    for split in ['train', 'valid', 'test']:
        data_list = []
        split_duration = 0
        short_duration = 0
        no_text_duration = 0
        if not os.path.exists(input_file + split):
            print(f"Skipping {split} split as it does not exist")
            continue
        for file in tqdm(os.listdir(input_file + split)):
            if file.endswith(".wav"):
                json_file = input_file + split + '/' + file.replace(".wav", ".json")
                audio_file = input_file + split + '/' + file
                audio_segment = AudioSegment.from_wav(audio_file)
                if not os.path.exists(json_file):
                    print(f"JSON file not found for {audio_file}")
                    raise FileNotFoundError

                with open(json_file) as f:
                    data = json.load(f)
                    for i, segment in enumerate(data["normalized"]):
                        start = segment["start"]
                        end = segment["end"]
                        duration = end - start
                        if duration < min_duration:
                            # print(f"Skipping {audio_file} segment {i} as it is too short")
                            short_duration += duration
                            continue
                        chunk = audio_segment[start * 1000: end * 1000]
                        text = segment["text"]
                        clear_text = clean_text(text)
                        if len(clear_text) == 0:
                            # print(f"Skipping {audio_file} segment {i} as cleaned text length either 0")
                            no_text_duration += duration
                            continue
                        output_file = os.path.join(output_dir, f"{os.path.basename(audio_file).replace('.wav', '')}_chunk_{i}.wav")
                        # print(f"Writing {output_file}")
                        chunk = chunk.set_frame_rate(16_000)
                        chunk.export(output_file, format="wav")
                        split_duration += duration
                        data_list.append({
                            "audio_filepath": output_file,
                            "duration": duration,
                            "text": clear_text,
                            "id": file.replace(".wav", f"_chunk_{i}"),
                            "sample_rate": chunk.frame_rate,
                            "lang": lang_code
                        })
                        complete_data_list.append({
                            "audio_filepath": output_file,
                            "duration": duration,
                            "text": clear_text,
                            "id": file.replace(".wav", f"_chunk_{i}"),
                            "sample_rate": chunk.frame_rate,
                            "lang": lang_code
                        })
        
        with open(f"{manifest_dir}/stats.txt", "a") as stats_f:
            stats_f.write(f"Total duration of valid files in {split} split: {split_duration}\n, \
                          skip duration:{short_duration}\n, \
                          no_text_duratin:{no_text_duration}\n")
            
        re_split = "test" if split == "valid" else split
        with open(f"{manifest_dir}/{re_split}_manifest.json", "w") as json_file:
            duration = 0
            for item in data_list:
                temp = {}
                duration += item['duration']
                temp_dict = {}
                temp_dict['source'] = {
                    'id': item['id'], 
                    'text': item['text'], 
                    'lang': item['lang'], 
                    'audio_local_path': item['audio_filepath'], 
                    'sample_rate': item['sample_rate'],
                    'waveform': None,
                    'units': None
                    } 
                temp_dict['target'] = temp_dict['source']
                json.dump(temp_dict, json_file, ensure_ascii=True)
                json_file.write('\n')
                
    with open(f"{manifest_dir}/data.json", "w") as f:
        json.dump(complete_data_list, f, ensure_ascii=False, indent=4)

    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang_code", type=str, default="mal")
    parser.add_argument("--audio_file", type=str, default="/slt/data/indicvoices/Malayalam/v1a/")
    parser.add_argument("--output_dir", type=str, default="/slt/data/indicvoices/")
    parser.add_argument("--manifest_dir", type=str, default="/slt/experiments_indicvoices/dataset/")
    parser.add_argument("--min_duration", type=int, default=1)
    args = parser.parse_args()

    lang_code = args.lang_code
    audio_file = args.audio_file
    output_dir = args.output_dir
    manifest_dir = args.manifest_dir
    os.makedirs(output_dir, exist_ok=True)  
    os.makedirs(manifest_dir, exist_ok=True)
    min_duration = 1
    split_and_save(audio_file, output_dir, min_duration)
