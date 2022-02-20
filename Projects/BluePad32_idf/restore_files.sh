export WORKING_DIR=BluePad32_Uartremote
export PROJECT_DIR=files_Bluepad32_Uartremote
cat files_to_copy.txt | while read f; do cp --parents -r $f ../$PROJECT_DIR; done
