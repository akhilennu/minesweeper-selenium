from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

driver = webdriver.Chrome("chromedriver.exe")

driver.maximize_window()
driver.get("https://minesweeper.online/")

# driver.find_element(By.XPATH, '//*[@id="homepage"]/div[1]/div[3]').click()

driver.find_element(By.XPATH, '//*[@id="homepage"]/div[1]/div[2]').click() #beginner
sleep(1)
class Sentence:
    ids:set 
    count: int 
    probability: float

    def __init__(self, ids:set, count:int) -> None:
        self.ids = ids
        self.count = count
        if(len(ids)>0):
            self.probability = count*1.0/len(ids)
        else:
            self.probability = 1

class Solver:
    height = 16
    width = 30
    

    def __init__(self, h, w) -> None:
        self.height = h
        self.width = w
        self.initalize()
    
    def initalize(self):
        self.sentences = [[None for i in range(self.width)] for j in range(self.height)]
        
    def mark_mine(self, id: str, coming_from: str):
        aa = id.split('_')
        x = int(aa[1])
        y = int(aa[2])
        if(x<0 or x>=self.height or y<0 or y>=self.width):
            return
        id = 'cell_'+str(x)+'_'+str(y)
        actionChains = ActionChains(driver)
        actionChains.context_click(driver.find_element(By.ID, id)).perform()
        
        for i in range(-1,2):
            for j in range(-1,2):
                if(i==j==0):
                    continue
                xx = x+i
                yy = y+j
                if(xx<0 or xx>=self.height or yy<0 or yy>=self.width):
                    continue
                tmp: Sentence = self.sentences[xx][yy]
                tmp_id = 'cell_'+str(xx)+'_'+str(yy)
                if(tmp_id==coming_from):
                    continue
                if(tmp!=None):
                    if(id in tmp.ids):
                        tmp.ids.remove(id)
                        tmp.count -= 1
                        self.make_inferences(xx, yy)

    """
    1. Click on the spot, if mine, end the game 
	2. Explore Cell
    3. Mark all neibhoring sentences //not necessary
    """
    def mark_safe(self, x: int, y: int):
        if(x<0 or x>=self.height or y<0 or y>=self.width):
            return
        id = 'cell_'+str(x)+'_'+str(y)
        driver.find_element(By.ID, id).click()
        self.explore_cell(x,y)
        print(id+" is marked safe")
    
    """
    DFS to 
    1. add knowledge base
    """
    def explore_cell(self, x: int, y: int):
        t = self.get_cell(x,y)
        if(t==None or t==9):
            return
        if(self.sentences[x][y]!=None):
            return
        if(t == 11):
            print("WASTED")
            return
        
        if(t==0):
            self.sentences[x][y] = Sentence(set(), t)
        else:
            ids = set()
            for i in range(-1,2):
                for j in range(-1,2):
                    if(i==j==0):
                        continue
                    a = self.get_cell(x+i,y+j)
                    if(a==9):
                        xx = x+i
                        yy = y+j
                        id = 'cell_'+str(xx)+'_'+str(yy)
                        print(id)
                        ids.add(id)
            self.sentences[x][y] = Sentence(ids,t)
        self.make_inferences(int(x),int(y))
        for i in range(-1,2):
            for j in range(-1,2):
                if(i==j==0):
                    continue
                self.explore_cell(x+i,y+j)

    """
    Compare the current sentence with all 

    1. If Count is 0, all the neibhors are safe, it will be marked by the website
    2. 
    """
    def make_inferences(self, x: int, y: int):
        print("Trying to make inferences at "+str(x)+", "+str(y))
        cur: Sentence = self.sentences[x][y]
        cur_id = 'cell_'+str(x)+'_'+str(y)
        if(cur.count==0):
            for a in cur.ids:
                c_a = s_ci.split('_')
                self.mark_safe(int(c_a[1]),int(c_a[2]))
        elif(len(cur.ids)==cur.count):
            for a in cur.ids:
                self.mark_mine(id=a, coming_from=cur_id)
        for i in range(-1,2):
            for j in range(-1,2):
                if(i==j==0):
                    continue
                # print("Trying to make inferences at "+str(x)+", "+str(y))
                xx = int(x)+int(i)
                yy = int(y)+int(j)
                if(xx<0 or xx>=self.height or yy<0 or yy>=self.width):
                    continue
                tmp: Sentence = self.sentences[xx][yy]
                if(tmp==None or len(tmp.ids)==0 or len(tmp.ids)>=len(cur.ids)):
                    continue
                if(tmp.ids.issubset(cur.ids)):
                    print(str(tmp.ids) +" is a subset of "+str(cur.ids))
                    for s_i in tmp.ids:
                        cur.ids.remove(s_i)
                    cur.count -= tmp.count
                    if(cur.count==0):
                        for s_ci in cur.ids:
                            s_a = s_ci.split('_')
                            self.mark_safe(int(s_a[1]),int(s_a[2]))
                    elif(len(cur.ids)==cur.count):
                        for s_ci in cur.ids:
                            self.mark_mine(id=s_ci, coming_from=cur_id)
                        return
        

    def get_cell(self, x: int, y: int):
        if(x<0 or x>=self.height or y<0 or y>=self.width):
            return None
        id = 'cell_'+str(x)+'_'+str(y)
        # print("getting for id "+id)
        elem = driver.find_element(By.ID, id)
        t = elem.get_attribute("class").split(' ') #['cell', 'size24', 'hd_opened', 'hd_type1']
        if(len(t)==3): # cell size24 hd_closed
            return 9
        t = t[3] #'hd_type1'
        if(t=='hd_flag'):
            return 12
        elif(t=='hd_closed'):
            return 9
        t = int(t[7:]) # 1
        return t
        


s = Solver(30,16)
s.mark_safe(0,0)


# print(s.sentences)