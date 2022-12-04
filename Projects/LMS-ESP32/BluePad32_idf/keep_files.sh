export PROJECT_DIR=$1
export FILES_DIR=files_$PROJECT_DIR
echo $FILES_DIR
cd $PROJECT_DIR
cat ../$FILES_DIR/files_to_copy.txt | while read f; do cp --parents -r $f ../$FILES_DIR; done
