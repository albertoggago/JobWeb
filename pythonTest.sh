cd pythonBatch/test
echo $0
#py.test --junitxml results.xml testread*.py testa*.py testmon* -v 
#py.test --junitxml results.xml testmon* -v 
#py.test --junitxml results.xml testanalyzerwebjobsfunctionstext.py -v
py.test --junitxml results.xml test*.py -v

