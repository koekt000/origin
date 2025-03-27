const urlParams = new URLSearchParams(window.location.search);
const level = urlParams.get('level');

document.getElementById('level-number').innerText = level;
function back(){
    window.location.href = "index.html"
}
const questionsByLevel = {
    1: [
        { question: `вопрос 1`, answer: `1` },
        { question: `вопрос 2`, answer: `1` },
        { question: `вопрос 3`, answer: `1` }
    ],
    2: [
        { question: `вопрос 1`, answer: `1` },
        { question: `вопрос 2`, answer: `1` },
        { question: `вопрос 3`, answer: `1` }
    ],
    3: [
        { question: `вопрос 1`, answer: `1` },
        { question: `вопрос 2`, answer: `1` },
        { question: `вопрос 3`, answer: `1` }
    ],
    daily: [
        { question: `вопрос 1`, answer: `1` },
        { question: `вопрос 2`, answer: `1` },
        { question: `вопрос 3`, answer: `1` }
    ]
};

let currentQuestionIndex = 0;
let currentQuestions = questionsByLevel[level];
let incorrectAnswers = [];
const correctSound = document.getElementById('correct-sound');
const incorrectSound = document.getElementById('incorrect-sound');

correctSound.volume = 0.1;
incorrectSound.volume = 0.1;


function displayQuestion() {
    const task = document.getElementById('task');
    task.innerHTML = `
        <label>${currentQuestions[currentQuestionIndex].question}</label>
        <div>
            <input type="text" class="underline-input" name="answer${currentQuestionIndex + 1}" required>
        </div>
    `;
}

document.getElementById('next-button').addEventListener('click', function() {
    let url = location.href;
    const input = document.querySelector(`input[name="answer${currentQuestionIndex + 1}"]`);
    const userAnswer = input.value.trim().toLowerCase();
    if (userAnswer === currentQuestions[currentQuestionIndex].answer) {
        document.body.style.backgroundColor = "lightgreen";
        correctSound.play();;
    } else {
        document.body.style.backgroundColor = "lightcoral";
        location.href = "#zatemnenie";
        a = document.getElementById("correct-answer")
        a.innerHTML = currentQuestions[currentQuestionIndex].answer;
        incorrectSound.play();
        incorrectAnswers.push(currentQuestions[currentQuestionIndex]);
    }

    currentQuestionIndex++;

    if (currentQuestionIndex < currentQuestions.length) {
        setTimeout(() => {
            displayQuestion();
            updateProgress(currentQuestionIndex, currentQuestions.length);
            document.body.style .backgroundColor = "";
        }, 1000);
    } else {
        if (incorrectAnswers.length > 0) {
            currentQuestions = incorrectAnswers;
            currentQuestionIndex = 0;
            incorrectAnswers = [];
            displayQuestion();

            //location.href = "#zatemnenie3"
            document.body.style.backgroundColor = ""
        } else {
            location.href = "#zatemnenie2"
        }
    }
});

function updateProgress(current, total) {
    const progressBar = document.getElementById('progress-bar');
    const percentage = (current / total) * 100;
    progressBar.style.width = percentage + '%';
}

displayQuestion();
updateProgress(currentQuestionIndex, currentQuestions.length);