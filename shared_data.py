import sched
import time


scheduler = sched.scheduler(time.time, time.sleep)
local_week_figs = 0
nation_week_figs = 0
nation_hospital_figs = 0
nation_deaths = 0


def get_scheduler():
    return scheduler


def update_scheduler(s):
    global scheduler
    scheduler = s


def get_covid_values():
    return local_week_figs, nation_week_figs, nation_hospital_figs, nation_deaths


def set_covid_values(local_figs, national_week_figs, national_hospital_figs, national_deaths):
    global local_week_figs, nation_week_figs, nation_hospital_figs, nation_deaths
    local_week_figs = local_figs
    nation_week_figs = national_week_figs
    nation_hospital_figs = national_hospital_figs
    nation_deaths = national_deaths
