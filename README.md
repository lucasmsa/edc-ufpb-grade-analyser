# Computer Engineering [UFPB] (grade analysis)
An easy way to view how grades behaved throughout the semesters, generating a txt and plotting graphs related to grades means and separating the student performance by knowledge area

## Installing
```
pip install selenium
pip install urllib
pip install plotly
pip install statistics
```
[Also install a webdriver](https://chromedriver.chromium.org/downloads)<br>
[You might also need to include it in system PATH](https://www.kenst.com/2015/03/including-the-chromedriver-location-in-macos-system-path/) (MacOSX)
[Windows](https://zwbetz.com/download-chromedriver-binary-and-add-to-your-path-for-automated-functional-testing/)

## How to run
The student should pass login and password from [sigaa] as command line arguments
```
python sigaa_grades.py <login> <password>
```
## Results 
![semesters](imgs/semesters.png)
______
![knowledge_areas](imgs/knowledge_areas.png)
