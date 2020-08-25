# OTUS_FinProject_Habr_test
To run tests email and password should be provided via pytest-config. Example:
```
pytest --tc=email:{email} --tc=password:{password} tests/test_habr.py
```

Other keys:  
  --alluredir=allure-report - is used to create allure report  
  --executor-url - is used if 'selenoid' was chosen as 'remote_type'. Provide the full URL with port and /wd/hub  
  --remote_type - is used to specify where to run tests either locally or in selenoid. Remember to start Selenoid before running tests in it.

## Jenkins
There're Jenkinsfile and Dockerfile in the project root directory. If run Jenkins in Docker container check if it's able to run 'docker' commands.
