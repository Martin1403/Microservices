import requests
from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import login_required, current_user

from frontend.api import url_for_jobs, content_headers
from frontend.api.jobs.forms import CreateJobForm, CreateCompanyForm
from frontend.api.jobs.commands import (
    QUERY_COMPANY_BY_ID,
    QUERY_JOB_BY_ID,
    MUTATION_CREATE_JOB,
    QUERY_ALL_JOBS,
    MUTATION_CREATE_COMPANY,
)


jobs = Blueprint("jobs", __name__)


def post_request(query, id=None):
    return requests.request(
        method="POST",
        url=url_for_jobs,
        json={'query': query, "variables": {"id": id}},
        headers=content_headers
    )


def post_mutation(query, input):
    return requests.request(
        method="POST",
        url=url_for_jobs,
        json={'query': query, "variables": {"input": input}},
        headers=content_headers
    )


@jobs.route("/jobs")
@login_required
def get_all_jobs():
    return render_template(
        "index.html",
        current_user=current_user,
        jobs=post_request(QUERY_ALL_JOBS).json()["data"]["jobs"]
    )


@jobs.route("/jobs/<id>", methods=["POST", "GET"])
@login_required
def get_job_id(id):
    return render_template(
        "job.html",
        job=post_request(QUERY_JOB_BY_ID, id).json()["data"]["job"]
    )


@jobs.route("/companies/<company_id>", methods=["POST", "GET"])
@login_required
def get_company_id(company_id):
    return render_template(
        "company.html",
        company=post_request(QUERY_COMPANY_BY_ID, company_id).json()["data"]["company"]
    )


@jobs.route("/create", methods=["POST", "GET"])
@login_required
def create_job():
    company = post_request(QUERY_COMPANY_BY_ID, current_user.id).json()["data"]["company"]
    if company:
        form = CreateJobForm()
        if form.validate_on_submit():
            response = post_mutation(
                query=MUTATION_CREATE_JOB,
                input={
                    "companyId": current_user.id,
                    "title": form.data.get("title"),
                    "description": form.data.get("description")
                }
            )
            return redirect(url_for("jobs.get_all_jobs"))
        return render_template("create_job.html", form=form)

    return redirect(url_for("jobs.create_company"))


@jobs.route("/company", methods=["POST", "GET"])
def create_company():
    form = CreateCompanyForm()
    if form.validate_on_submit():
        response = post_mutation(
            query=MUTATION_CREATE_COMPANY,
            input={
                "id": current_user.id,
                "name": form.data.get("name"),
                "description": form.data.get("description")
            }
        )
        return redirect(url_for("jobs.create_job"))
    return render_template("create_company.html", form=form)


@jobs.app_errorhandler(404)
def error404(_):
    return {}, 404
