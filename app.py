import logging
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO
import logging_config
import threading
import enums
import secrets
from page_driver_pool import page_driver_pool

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
socketio = SocketIO(app)

# 로깅 설정
logging_config.setup_logging()
logging_config.setup_socket_logging(socketio)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            ID = request.form['ID']
            PW = request.form['PW']
            lab = enums.Lab[request.form['lab']]
            start_date = parse_date(request.form['start_date'])
            end_date = parse_date(request.form['end_date'])
            except_dates_str = request.form['except_dates']

            except_dates = []
            if except_dates_str:
                except_dates_list = except_dates_str.split(',')
                except_dates = [parse_date(date.strip()) for date in except_dates_list if date.strip()]

            if not start_date or not end_date:
                flash("Invalid start date or end date.", "error")
                return redirect(url_for('index'))

            if start_date > end_date:
                flash("Start date cannot be after end date.", "error")
                return redirect(url_for('index'))

            feedback_logger = logging.getLogger('feedback_logger')
            feedback_logger.info(f"Starting lab record entry: ID={ID}, Lab={lab}, Start Date={start_date}, End Date={end_date}")

            threading.Thread(target=enter_lab_records, args=(ID, PW, lab, start_date, end_date, except_dates)).start()

            return redirect(url_for('in_progress'))

        return render_template('index.html', labs=list(enums.Lab))
    except Exception as e:
        feedback_logger = logging.getLogger('feedback_logger')
        feedback_logger.error(f"Error in index route: {e}")
        return redirect(url_for('error'))

def enter_lab_records(ID, PW, lab, start_date, end_date, except_dates):
    feedback_logger = logging.getLogger('feedback_logger')
    try:
        driver_id = page_driver_pool.create_driver()
        if driver_id is None:
            raise Exception("Failed to create a new driver.")

        page_driver = page_driver_pool.get_driver(driver_id)
        page_driver.start_and_enter_lab_manage_handling_except(ID, PW)
        page_driver.manage_lab_at_range_of_date(lab, start_date, end_date, except_dates)
        page_driver.log_out()

        with app.app_context():
            socketio.emit('task_complete', {'status': 'success'})
    except Exception as e:
        feedback_logger.error(f"Error in enter_lab_records: {e}")
        with app.app_context():
            socketio.emit('task_complete', {'status': 'error'})
    finally:
        if driver_id is not None:
            page_driver_pool.remove_driver(driver_id)

@app.route('/in_progress')
def in_progress():
    return render_template('in_progress.html')

@app.route('/delete', methods=['POST'])
def delete_records():
    try:
        ID = request.form['ID']
        PW = request.form['PW']
        lab = enums.Lab[request.form['lab']]
        start_date = parse_date(request.form['start_date'])
        end_date = parse_date(request.form['end_date'])
        except_dates_str = request.form['except_dates']

        except_dates = []
        if except_dates_str:
            except_dates_list = except_dates_str.split(',')
            except_dates = [parse_date(date.strip()) for date in except_dates_list if date.strip()]

        if not start_date or not end_date:
            flash("Invalid start date or end date.", "error")
            return redirect(url_for('index'))

        feedback_logger = logging.getLogger('feedback_logger')
        feedback_logger.info(f"Starting record deletion: ID={ID}, Lab={lab}, Start Date={start_date}, End Date={end_date}")

        threading.Thread(target=delete_lab_records, args=(ID, PW, lab, start_date, end_date, except_dates)).start()

        return redirect(url_for('in_progress'))
    except Exception as e:
        feedback_logger = logging.getLogger('feedback_logger')
        feedback_logger.error(f"Error in delete_records route: {e}")
        return redirect(url_for('error'))

def delete_lab_records(ID, PW, lab, start_date, end_date, except_dates):
    feedback_logger = logging.getLogger('feedback_logger')
    try:
        driver_id = page_driver_pool.create_driver()
        if driver_id is None:
            raise Exception("Failed to create a new driver.")

        page_driver = page_driver_pool.get_driver(driver_id)
        page_driver.start_and_enter_lab_manage_handling_except(ID, PW)
        page_driver.delete_lab_records_at_range_of_date(lab, start_date, end_date, except_dates)
        page_driver.log_out()

        with app.app_context():
            socketio.emit('task_complete', {'status': 'success'})
    except Exception as e:
        feedback_logger.error(f"Error in delete_lab_records: {e}")
        with app.app_context():
            socketio.emit('task_complete', {'status': 'error'})


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
        console_logger = logging.getLogger('console_logger')
        console_logger.error(f"Invalid date format: {date_str}")
        return None

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)