from flask import Flask, render_template, request
import random, copy

app = Flask(__name__)

original_questions = {
 #Format is 'question':[options]
 'Find Action':['Ctrl+Shift+A','Ctrl+Shift+F','Ctrl+F','Ctrl+A'],
 'Find class, file, or symbol':['All of the above','Ctrl+N','Ctrl+Shift+N','Ctrl+Shift+Alt+N'],
 'View recent files':['Ctrl+E','Ctrl+Alt+E','Ctrl+Shift+R','Ctrl+R'],
 'Show intention actions':['Alt+Enter','Shift+Enter','Ctrl+Alt+Enter','Ctrl+Shift+Enter'],
 'Basic code completion':['Ctrl+Space','Ctrl+Alt+Space','Alt+Space','Shift+Alt+Space'],
 'Smart code completion':['Ctrl+Shift+Space','Ctrl+Space','Alt+Space','Ctrl+Alt+Space'],
 'Highlight usages in file':['Ctrl+Shift+F7','Ctrl+F5','Ctrl+Shift+F5','Ctrl+F7']
}

questions = copy.deepcopy(original_questions)

def shuffle(q):
 """
 This function is for shuffling
 the dictionary elements.
 """
 selected_keys = []
 i = 0
 while i < len(q):
  current_selection = random.choice(list(q.keys()))
  if current_selection not in selected_keys:
   selected_keys.append(current_selection)
   i = i+1
 return selected_keys

@app.route('/')
def quiz():
 questions_shuffled = shuffle(questions)
 for i in questions.keys():
  random.shuffle(questions[i])
 return render_template('quizHTML.html', q = questions_shuffled, o = questions)


@app.route('/quiz', methods=['POST'])
def quiz_answers():
 correct = 0
 for i in list(questions.keys()):
  answered = request.form[i]
  if original_questions[i][0] == answered:
   correct = correct+1
 return '<h1>Correct Answers: <u>'+str(correct)+'</u></h1>'

if __name__ == '__main__':
 app.run(debug=True)