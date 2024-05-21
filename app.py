from flask import Flask, request, render_template, redirect, url_for, flash
import datetime
import page_driver as pd
import auto_lab_manager as lm
import enums

app = Flask(__name__)
app.secret_key = 'g2는_어떻게_강팀이_되었는가'

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            # 폼에서 입력값 처리
            ID = request.form['ID']
            PW = request.form['PW']
            lab = enums.Lab[request.form['lab']]
            start_date = parse_date(request.form['start_date'])
            end_date = parse_date(request.form['end_date'])
            except_dates_str = request.form['except_dates']

            # 예외 날짜 처리
            except_dates = []
            if except_dates_str:
                except_dates_list = except_dates_str.split(',')
                except_dates = [parse_date(date.strip()) for date in except_dates_list if date.strip()]

            # 입력값 검증
            if not start_date or not end_date:
                flash("Invalid start date or end date.", "error")
                return redirect(url_for('index'))

            if start_date > end_date:
                flash("Start date cannot be after end date.", "error")
                return redirect(url_for('index'))

            # 비즈니스 로직 실행
            pd.start_and_enter_lab_manage_handling_except(ID, PW)
            lm.manage_lab_at_range_of_date(lab, start_date, end_date, except_dates)
            return redirect(url_for('success'))

        return render_template('index.html', labs=list(enums.Lab))
    except Exception as e:
        print(f"Error: {e}")
        pd.logout_and_reset_driver()
        return redirect(url_for('error'))

@app.route('/delete', methods=['POST'])
def delete_records():
    try:
        ID = request.form['ID']
        PW = request.form['PW']
        lab = enums.Lab[request.form['lab']]
        start_date = parse_date(request.form['start_date'])
        end_date = parse_date(request.form['end_date'])
        except_dates_str = request.form['except_dates']

        # 예외 날짜 처리
        except_dates = []
        if except_dates_str:
            except_dates_list = except_dates_str.split(',')
            except_dates = [parse_date(date.strip()) for date in except_dates_list if date.strip()]

        # 입력값 검증
        if not start_date or not end_date:
            flash("Invalid start date or end date.", "error")
            return redirect(url_for('index'))

        if start_date > end_date:
            flash("Start date cannot be after end date.", "error")
            return redirect(url_for('index'))

        # 비즈니스 로직 실행
        pd.start_and_enter_lab_manage_handling_except(ID, PW)
        lm.delete_lab_records_at_range_of_date(lab, start_date, end_date, except_dates)
        return redirect(url_for('delete_success'))
    except Exception as e:
        print(f"Error: {e}")
        pd.logout_and_reset_driver()
        return redirect(url_for('error'))

@app.route('/success')
def success():
    pd.log_out()
    return '''
    작업이 성공적으로 완료되었습니다!<br>
    <a href="/"><button>처음으로</button></a>
    '''

@app.route('/delete_success')
def delete_success():
    pd.log_out()
    return '''
    삭제 작업이 성공적으로 완료되었습니다!<br>
    <a href="/"><button>처음으로</button></a>
    '''

@app.route('/error')
def error():
    return '''
    오류가 발생했습니다. 다시 시도해주세요.<br>
    <a href="/"><button>처음으로</button></a>
    '''

def parse_date(date_str):
    today = datetime.datetime.today()
    try:
        # 'yy.mm.dd' 형식
        if len(date_str.split('.')) == 3 and len(date_str.split('.')[0]) == 2:
            return datetime.datetime.strptime(date_str, "%y.%m.%d").date()
        # 'yyyy.mm.dd' 형식
        elif len(date_str.split('.')) == 3 and len(date_str.split('.')[0]) == 4:
            return datetime.datetime.strptime(date_str, "%Y.%m.%d").date()
        # 'mm.dd' 형식
        elif len(date_str.split('.')) == 2:
            return datetime.datetime.strptime(f"{today.year}.{date_str}", "%Y.%m.%d").date()
        # 'dd' 형식
        elif date_str.isdigit() and len(date_str) <= 2:
            return datetime.datetime(today.year, today.month, int(date_str)).date()
    except ValueError:
        print(f"Invalid date format: {date_str}")
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
