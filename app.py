import logging
import datetime
import threading
from flask import Flask, request, render_template, redirect, url_for, flash
import page_driver as pd
import auto_lab_manager as lm
import enums
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

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

            logging.info(f"Starting lab record entry: ID={ID}, Lab={lab}, Start Date={start_date}, End Date={end_date}")

            # 비동기 작업 시작
            threading.Thread(target=enter_lab_records, args=(ID, PW, lab, start_date, end_date, except_dates)).start()

            # 작업 중 페이지로 리디렉션
            return redirect(url_for('entry_in_progress'))

        return render_template('index.html', labs=list(enums.Lab))
    except Exception as e:
        logging.error(f"Error in index route: {e}")
        pd.logout_and_reset_driver()
        return redirect(url_for('error'))

def enter_lab_records(ID, PW, lab, start_date, end_date, except_dates):
    try:
        pd.start_and_enter_lab_manage_handling_except(ID, PW)
        lm.manage_lab_at_range_of_date(lab, start_date, end_date, except_dates)
        pd.log_out()
        # 작업 완료 후 성공 페이지로 리디렉션
        with app.app_context():
            redirect(url_for('entry_success'))
    except Exception as e:
        logging.error(f"Error in enter_lab_records: {e}")
        pd.logout_and_reset_driver()
        with app.app_context():
            redirect(url_for('error'))

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

        logging.info(f"Starting record deletion: ID={ID}, Lab={lab}, Start Date={start_date}, End Date={end_date}")

        # 비동기 작업 시작
        threading.Thread(target=delete_lab_records, args=(ID, PW, lab, start_date, end_date, except_dates)).start()

        # 작업 중 페이지로 리디렉션
        return redirect(url_for('delete_in_progress'))
    except Exception as e:
        logging.error(f"Error in delete_records route: {e}")
        pd.logout_and_reset_driver()
        return redirect(url_for('error'))

def delete_lab_records(ID, PW, lab, start_date, end_date, except_dates):
    try:
        pd.start_and_enter_lab_manage_handling_except(ID, PW)
        lm.delete_lab_records_at_range_of_date(lab, start_date, end_date, except_dates)
        pd.log_out()
        # 작업 완료 후 삭제 성공 페이지로 리디렉션
        with app.app_context():
            redirect(url_for('delete_success'))
    except Exception as e:
        logging.error(f"Error in delete_lab_records: {e}")
        pd.logout_and_reset_driver()
        with app.app_context():
            redirect(url_for('error'))

@app.route('/entry_in_progress')
def entry_in_progress():
    return '''
    입력 작업이 진행 중입니다. 잠시만 기다려 주세요...<br>
    <a href="/"><button>처음으로</button></a>
    '''

@app.route('/delete_in_progress')
def delete_in_progress():
    return '''
    삭제 작업이 진행 중입니다. 잠시만 기다려 주세요...<br>
    <a href="/"><button>처음으로</button></a>
    '''

@app.route('/entry_success')
def entry_success():
    return '''
    입력 작업이 성공적으로 완료되었습니다!<br>
    <a href="/"><button>처음으로</button></a>
    '''

@app.route('/delete_success')
def delete_success():
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
        logging.error(f"Invalid date format: {date_str}")
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
