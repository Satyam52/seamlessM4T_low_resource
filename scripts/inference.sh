LANG=Maithili
LANG_CODE=mai
EXP_NAME=maithili_len_adaptor_mai_all
DATASET_DIR=/slt/data


PARENT_DIR="/slt/results"
EXPERIMENT_NAME=$LANG_CODE_$EXP_NAME
DESCRIPTION="Maithili trained on IndicVoices dataset"
EXPERIMENT_DIR="$PARENT_DIR/$LANG/$EXPERIMENT_NAME"
CARDS_DIR="/slt/codebase/seamless/src/seamless_communication/cards/"

GPUs="0"
mkdir -p $EXPERIMENT_DIR

echo "Dataset directory: ${DATASET_DIR}"
echo "Language: ${LANG}"


#  Inference
echo "Step 2: Inference"
CUDA_VISIBLE_DEVICES=$GPUs python3 /slt/scripts/infer.py \
--path_test_dataset $DATASET_DIR/test_manifest.json \
--model_yaml_name $EXP_NAME \
--path_inference_file $EXPERIMENT_DIR/${EXPERIMENT_NAME}_$LANG.json \
--lang_code $LANG_CODE
echo 'Inference Completed'

# Calculate WER
python3 /slt/scripts/wer.py \
--path_stat $EXPERIMENT_DIR/${EXPERIMENT_NAME}_$LANG.wer \
--path_inference_file $EXPERIMENT_DIR/${EXPERIMENT_NAME}_$LANG.json
echo "WER Calculated"

