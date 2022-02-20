export PROJECT_DIR=$1
export FILES_DIR=files_$PROJECT_DIR
echo $FILES_DIR
cd $FILES_DIR
cat files_to_copy.txt | while read f; do cp --parents -r $f ../$PROJECT_DIR; done
