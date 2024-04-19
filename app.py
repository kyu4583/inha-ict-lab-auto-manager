from flask import Flask, request, render_template, redirect, url_for
import datetime
import page_driver as pd
import auto_lab_manager as lm
import enums

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 폼에서 입력값 처리
        ID = request.form['ID']
        PW = request.form['PW']
        lab = enums.Lab[request.form['lab']]
        start_date = parse_date(request.form['start_date'])
        end_date = parse_date(request.form['end_date'])
        except_dates = request.form['except_dates'].split(',')

        except_dates = [date.strip() for date in except_dates if date.strip()]
        except_dates = [parse_date(date) for date in except_dates]

        # 비즈니스 로직 실행
        pd.start_and_enter_lab_manage(ID, PW)
        lm.manage_lab_at_range_of_date(lab, start_date, end_date, except_dates)
        return redirect(url_for('success'))

    return render_template('index.html', labs=list(enums.Lab))

@app.route('/success')
def success():
    return '''
    작업이 성공적으로 완료되었습니다!<br>
    <a href="/"><button>처음으로</button></a>
    '''

def parse_date(date_str):
    today = datetime.datetime.today()
    try:
        # 'yy.mm.dd' 형식
        if len(date_str.split('.')) == 3:
            return datetime.datetime.strptime(date_str, "%y.%m.%d").date()
        # 'mm.dd' 형식
        elif len(date_str.split('.')) == 2:
            return datetime.datetime.strptime(f"{today.year}.{date_str}", "%Y.%m.%d").date()
        # 'dd' 형식
        elif date_str.isdigit():
            return datetime.datetime(today.year, today.month, int(date_str)).date()
    except ValueError:
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
