FROM python:3.6

WORKDIR /home/app

COPY . .

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD ["pytest", "--alluredir=allure-report", "--tc=email:siarhei.ahafonau@gmail.com", "--tc=password:q_XEgUTnZnQ25aH", "--executor-url=http://192.168.0.104:4444/wd/hub/", "--remote_type=selenoid", "tests/test_habr.py"]
