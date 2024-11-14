from parser import Parser


parser = Parser(cv_job='DevOps', vac_job='DevOps', area=1)
# parser.to_file_cv(ex_period='all_time', limit_page=1)
parser.to_file_vac(limit_page=1)
