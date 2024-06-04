import json
import Levenshtein
import argparse

class ER:
    def __init__(self):
        pass
    
    def calculate_wer(self, ground_truth, asr_output):
        if len(ground_truth)==0 or len(asr_output)==0:
            print("CAN NOT CALCULTATE WER")
            exit()
        ground_truth_words = ground_truth.split()
        asr_output_words = asr_output.split()
        distance = Levenshtein.distance(ground_truth_words, asr_output_words)
        wer = distance / len(ground_truth_words)

        return wer
    def calculate_cer(self, ground_truth, asr_output):
        if len(ground_truth)==0 or len(asr_output)==0:
            print("CAN NOT CALCULTATE CER, cer")
            exit()
        distance = Levenshtein.distance(ground_truth, asr_output)
        cer = distance / len(ground_truth)
        
        return cer
    
    def read_file(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            parsed_data = json.load(file)
        GT=[]
        Pred=[]
        for data in parsed_data:
            GT.append(data['original_text'])
            Pred.append(data['predicted_text'])
        return GT, Pred

    def remove_punc(self, line):
        punc_list=['.',',','|','-','(',')',"'",'!','?','\n']
        line_1=line
        for p in punc_list:
            line_1=line_1.replace(p,'')
        line_1=line_1.rstrip()
        return line_1

    def replace_digits_dev(self, line):
        n_e=['0','1','2','3','4','5','6','7','8','9']
        h_e= ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९"]
        line_1=line
        for i in range(len(n_e)):
            line_1=line_1.replace(n_e[i],h_e[i])
        return line_1


    def calculate(self, GT, Pred):
        wer_arr=[]
        cer_arr=[]
        
        for gt, asr in zip(GT, Pred):
            if len(gt)==0 or len(asr)==0:
                continue
            wer = self.calculate_wer(gt, asr)
            cer = self.calculate_cer(gt, asr)
            wer_arr.append(wer)
            cer_arr.append(cer)
                
        average_wer = sum(wer_arr) /len(wer_arr)
        average_cer = sum(cer_arr)/len(cer_arr)

        return average_wer, average_cer
            
    def forward(self, infe_path, stat_path):
        GT, Pred = self.read_file(infe_path)
        for i in range(len(GT)):
            line = self.replace_digits_dev(self.remove_punc(GT[i]))
            GT[i]=line
            
        for i in range(len(Pred)):
            line=line = self.remove_punc(Pred[i])
            words = line.split()
            filt_words = [word for word in words if not word.startswith('#')]
            line=' '.join(filt_words)
            line=' '.join(filt_words)
            line = self.replace_digits_dev(line)
            Pred[i]=line
            
        assert len(GT)==len(Pred), f"Ground truth: {len(GT)} not matches {len(Pred)}" 
        wer, cer = self.calculate(GT, Pred)
        print(f"Average WER: {wer:.2f}\t Average CER: {cer:.2f}")
        with open(stat_path, 'w') as f:
            json.dump({'WER': wer, 'CER': cer}, f, indent=4)
            
        

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument('--path_stat', type=str, required=True)
    args.add_argument('--path_inference_file', type=str, required=True)
    args = args.parse_args()
    error_rate = ER()
    error_rate.forward(args.path_inference_file, args.path_stat)
        