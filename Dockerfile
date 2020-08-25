FROM python:3.6

WORKDIR /home/app

COPY . .

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD ["pytest", "--alluredir=allure-report", "--tc=email:{email_registered_on_habr}", "--tc=password:{password}", "--executor-url={url_for_selenoid}:4444/wd/hub/", "--remote_type=selenoid", "tests/test_habr.py"]
