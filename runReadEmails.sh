cd pythonBatch
rm -R logOld
mv log logOld
mkdir log  
python runreademails.py "$@"
python runfindrepeated.py 0.9 True "$@" 
