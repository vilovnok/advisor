from cv_vac_p import CV_parser


cv_parser = CV_parser(cv_job='python', vac_job='python', area=1)
# cv_parser.to_file(ex_period='all_time', limit_page=1)

cv_parser.to_file_vac(limit_page=2)


# def get_links(text):
#     ua = fake_useragent.UserAgent()
#     data = requests.get(
#         url=f"https://hh.ru/search/resume?text={text}&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=false&page=1",
#         headers={"user-agent": ua.random}
#     )
#     if data.status_code != 200:
#         return
#     soup = BeautifulSoup(data.content, "lxml")
#     try:
#         page_count = int(
#             soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find(
#                 "span").text)
#     except:
#         return
#     for page in range(page_count):
#         try:
#             data = requests.get(
#                 url=f"https://hh.ru/search/resume?text={text}&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=false&page=1",
#                 headers={"user-agent": ua.random}
#             )
#             if data.status_code != 200:
#                 continue
#             soup = BeautifulSoup(data.content, "lxml")
#             for a in soup.find_all("a", attrs={"class": "serp-item__name"}):
#                 yield f"https://hh.ru{a.attrs['href'].split('?')[0]}"
#         except Exception as e:
#             print(f"{e}")
#             time.sleep(1)


# def get_resume(link):
#     ua = fake_useragent.UserAgent()
#     data = requests.get(
#         url=link,
#         headers={"user-agent": ua.random}
#     )
#     if data.status_code != 200:
#         return
#     soup = BeautifulSoup(data.content, "lxml")
#     try:
#         name = soup.find(attrs={"class": "resume-block__title-text"}).text
#     except:
#         name = ""
#     try:
#         experience = soup.find(attrs={"class": "resume-block__title-text_sub"}).text.replace(" ", " ").replace(" ", " ")
#     except:
#         experience = ""
#     try:
#         salary = soup.find(attrs={"class": "resume-block__title-text_salary"}).text.replace("\u2009", " ").replace(
#             "\xa0", " ")
#     except:
#         salary = ""
#     try:
#         skills = [skill.text for skill in soup.find(attrs={"class": "bloko-tag-list"}).find_all(attrs={"class": "bloko-tag__section_text"})]
#     except:
#         skills = []
#     resume = {
#         "name": name,
#         "salary": salary,
#         "skills": skills,
#         "experience": experience
#     }
#     return resume


# if __name__ == "__main__":
#     data = []
#     for a in get_links("python"):
#         data.append(get_resume(a))
#         time.sleep(1)
#         with open("data.json", "w", encoding="utf-8") as f:
#             json.dump(data, f, indent=4, ensure_ascii=False)
