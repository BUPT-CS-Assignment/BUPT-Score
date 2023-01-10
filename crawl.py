import requests
import json
import execjs

# for password encode
def encodeInp(input):
    with open('./encodeInp.js',encoding='utf-8') as f:
        js = execjs.compile(f.read())
        return js.call('encodeInp',input)


class crawler:
    headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
    # redis = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
    session = requests.session()
    logged_in = False
    level2score = {'优':95,'良':85,'中':75,'及格':65,'通过':65,'不及格':59}
    
    # encap get method
    def get(self,url,params = None):
        return self.session.get(url=url, headers=self.headers, params=params)

    # encap post method
    def post(self,url,data = None, params = None):
        return self.session.post(url=url, headers=self.headers,params=params,data=data)

    def login(self,username,password):
        self.get(url='http://jwglweixin.bupt.edu.cn/sjd/')
        login_url = 'http://jwglweixin.bupt.edu.cn/bjyddx/login'
        param = {
            'userNo':username,
            'pwd':encodeInp(password),
            'encode':1
        }
        response = self.post(login_url,param)
        try:
            res = json.loads(response.text)
            if res['code'] != '1':
                print('登录失败')
                return
        except Exception:
            print('登录失败')
            return

        self.logged_in = True
        print('登录成功')
        self.headers['token'] = res['data']['token']
        
        
    def score_semester(self, semester):
        score = []
        if not self.logged_in:
            print('未登录')
            return
        
        score_url = 'http://jwglweixin.bupt.edu.cn/bjyddx/student/termGPA'
        param = {
            'semester':semester,
            'type':1
        }
        response = self.post(url=score_url, params=param)
        score_data = json.loads(response.text)['data'][0]['achievement']
        print(f'{semester}学期查询到{len(score_data)}门课程')
        
        # check and insert
        for item in score_data:
            if item['fraction'] in self.level2score:
                item['fraction'] = self.level2score[item['fraction']]
            score.append({'type':item['curriculumAttributes'],'credit':float(item['credit']),'fraction':float(item['fraction']),'courseName':item['courseName'],'nature':item['courseNature']})

        return score
    
    # get mean on semesters 
    def score_mean(self,semesters,filter = False,print_item = True):
        if not self.logged_in:
            print('未登录')
            return 0
        
        s_list = []
        if isinstance(semesters,str):
            s_list.append(semesters)
        elif isinstance(semesters, list):
            s_list.extend(semesters)
        else:
            print('学期格式不正确')
            return 0

        print('查询中...')
        score_list = []
        for s in s_list:
            if len(str(s).strip()) == 0:
                continue
            score_list.extend(self.score_semester(s))

        print(f'共查询到{len(score_list)}门课程')

        if len(score_list) == 0:
            return

        total_fraction = 0
        total_credit = 0
        
        if print_item:
            print('****************************************************')
        for item in score_list:
            special = False
            if item['type'] == '任选' and (item['nature'] == '公共选修课' or item['nature'] == '校级双创课'):
                special = True
            
            if print_item:
                print(f"{'*' if special else ' '} 课程:{item['courseName']} | 分数:{item['fraction']} | 学分:{item['credit']} | 类型:{item['type']},{item['nature']}")
            
            if filter and special:
                continue
            
            total_fraction += item['fraction'] * item['credit']
            total_credit += item['credit']

        if print_item:
            print('****************************************************')
        print('平均分: %.3f'%(total_fraction / total_credit))
        print('****************************************************')
        return total_fraction / total_credit
        

