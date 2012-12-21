import os

def application_root():
    return os.path.dirname(os.path.realpath(__file__))

def conversion_job_path():
    return os.path.join(application_root(), 'ConversionJobs')