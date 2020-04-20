from selenium import webdriver
import urllib
import sys
import plotly.offline
import plotly.graph_objs as go
import numpy as np
import discplines_dict as d
import statistics
import time

sigaa = 'https://sigaa.ufpb.br/sigaa/logon.jsf'
login = str(sys.argv[1])
password = str(sys.argv[2])
f = open('results.txt', 'w')

class SigaaGradesMean():
    
    def __init__(self):
        super().__init__()
        self.driver = webdriver.Chrome()
        
    def accessSigaa(self):
        
        self.driver.get(sigaa)
        login_input = self.driver.find_element_by_id('form:login')
        login_input.send_keys(login)
        password_input = self.driver.find_element_by_id('form:senha')
        password_input.send_keys(password)
        enterPage = self.driver.find_element_by_id('form:entrar')
        enterPage.click()
        
    def getGrades(self):
        
        accessGrades = self.driver.find_element_by_id('main-menu')
        accessGrades = accessGrades.find_element_by_tag_name('li')
        accessGrades.click()
        accessGrades = accessGrades.find_element_by_tag_name('ul')
        accessGrades = accessGrades.find_element_by_tag_name('li') 
        accessGrades.click()

        
        all_semesters = self.driver.find_elements_by_class_name('tabelaRelatorio')
        num_semesters = len(all_semesters) + 1
        means, math, eng, prog, hware = [], [], [], [], []
        
        
        for table in all_semesters:
            
            num_semesters -= 1
            semester = table.find_element_by_tag_name('tbody')
            disciplines = semester.find_elements_by_tag_name('tr')
            sum_grades = []
            
            for index, discipline in enumerate(disciplines):
                discipline_info = discipline.find_elements_by_tag_name('td')
                
                discipline_tag = discipline_info[0]
                discipline_name = discipline_info[1]
                discipline_result = discipline_info[-3]
                
                result = round(float((discipline_result.text).replace(',', '.')), 2)
                sum_grades.append(result)
                
                if discipline_tag.text in d.mathematics:
                    math.append(result)
                elif discipline_tag.text in d.engineering:
                    eng.append(result)
                elif discipline_tag.text in d.hardware:
                    hware.append(result)
                elif discipline_tag.text in d.programming:
                    prog.append(result)
                else:
                    pass

                print(f'Discipline: {discipline_name.text} | Result: [{discipline_result.text}]')
                
            print()  
            means.append((round(statistics.mean(sum_grades), 2), num_semesters))
        
        [f.write(f'{e2}º Semester, mean: {e1}\n') for e1, e2 in means]
        f.write('\n')
        
        self.driver.quit()
        f.write(f'Mathematics: {math}\nEngineering: {eng}\nProgramming: {prog}\nHardware: {hware}\n')
        
        math_mean = round(statistics.mean(math), 2)
        eng_mean = round(statistics.mean(eng), 2)
        prog_mean = round(statistics.mean(prog), 2)
        hware_mean = round(statistics.mean(hware), 2)
        
        f.write(f'\nMath mean -> [{math_mean}]\nEngineering mean -> [{eng_mean}]\
                    \nProgramming mean -> [{prog_mean}]\nHardware mean -> [{hware_mean}]\n\n')
        
        
        best_mean = max(map(lambda l: l[0], means))
        best_sem = filter(lambda l: l[0] == best_mean, means)
        best_sem = list(best_sem)[0][1]
        
        worst_mean = min(map(lambda l: l[0], means))
        worst_sem = filter(lambda l: l[0] == worst_mean, means)
        worst_sem = list(worst_sem)[0][1]
        
        x = np.array(list(map(lambda l: l[1], means)))
        y = np.array(list(map(lambda l: l[0], means)))
        
        plotly.offline.plot({"data": [go.Scatter(x=x, y=y)],
                             "layout": go.Layout(title="Semesters Mean grades",
                                                xaxis_title="Semesters",
                                                yaxis_title="Grades")}, 
                             filename='grades.html')
        
        time.sleep(2)
        
        plotly.offline.plot({"data": [go.Scatterpolar(
                                r=[math_mean, eng_mean, prog_mean, hware_mean],
                                theta=['Mathematics', 'Engineering', 'Programming', 'Hardware'],
                                fill='toself',
                                name='Grades'
                            )],
                             "layout": go.Layout(title="Knowledge area radar chart",
                                                 polar=dict(
                                                    radialaxis=dict(
                                                        visible=True,
                                                        range=[0, 10]
                                                ),
                                            ),
                                        showlegend=False
                                        )}, 
                             filename='knowledge_areas.html'    
        )
        
        
        f.write(f'Best semester: {best_sem} || Mean: {best_mean}\n')
        f.write(f'Worst semester: {worst_sem} || Mean: {worst_mean}\n')
        
        f.close()
        
bot = SigaaGradesMean()
bot.accessSigaa()
bot.getGrades()