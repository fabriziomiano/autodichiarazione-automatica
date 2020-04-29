import os
import time
import uuid

from flask import (
    Blueprint, render_template, request, current_app, redirect, url_for
)

from app.config import (
    REGIONS, PDF_OUT_FILENAME, INPUT_FORM_MAP
)
from app.utils import fill_template_from_input

frontend = Blueprint("frontend", __name__)


@frontend.route('/')
@frontend.route('/index')
def index():
    return render_template(
        "index.html",
        regions=REGIONS,
        ts=time.time()
    )


@frontend.route('/generate_pdf', methods=["POST"])
def generate_pdf():
    """
    Get a client-side validated form, create the PDF, and redirect to
    download_and_remove route
    """
    uu_id = uuid.uuid4().hex
    current_app.logger.debug(uu_id)
    current_app.logger.debug(request.form)
    pdf_filename = "{}.pdf".format(uu_id)
    out_pdf_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"], pdf_filename
    )
    fill_template_from_input(
        request.form,
        current_app.config["PDF_TEMPLATE_PATH"],
        out_pdf_path,
        INPUT_FORM_MAP
    )
    return pdf_filename


@frontend.route('/download_and_remove/<filename>')
def download_and_remove(filename):
    """
    Serve file with filename in UPLOAD_FOLDER before deleting it
    :param filename: str <uuid>.pdf
    """
    path = os.path.join(
        current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename)

    def generate():
        with open(path, "rb") as f:
            yield from f
        os.remove(path)

    r = current_app.response_class(generate(), mimetype='application/pdf')
    r.headers.set('Content-Disposition', 'attachment', filename=PDF_OUT_FILENAME)
    return r
