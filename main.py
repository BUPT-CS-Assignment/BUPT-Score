from crawl import crawler
import getpass

# Bupt Average Score - Fast Check
# By github@Jianxff
# Bug report on github-issue or qq 3109441270
from encrypt import AESUtil

if __name__ == '__main__':
    print('====================================================')
    print('                  柏油平均分速查                    ')
    print('====================================================\n')
    
    
    cl = crawler()
    cl.login(username=input(' - 学号: '),password=getpass.getpass(' - 教务密码: '))
    # cl.login(username=input(' - 学号: '),password=getpass.getpass(' - 教务密码: '))
    while(True):
        semester = str(input(' - 查询学期(逗号隔开): '))
        filter = bool(input(' - 是否过滤任选课(y/N): ').upper() == 'Y')
        
        semester = semester.split(',')
        # semester = ['2020-2021-1','2020-2021-2','2021-2022-1','2021-2022-2','2022-2023-1']
        
        cl.score_mean(semesters=semester,filter=filter)

        quit = input(' - 是否继续查询(Y/N): ')
        while(quit.upper() not in ['Y','N']):
            quit = input(' - 是否继续查询(Y/N): ')
        if quit.upper() == 'N':
            print('~')
            exit()
