const $guessForm = $("#guessForm");
const $guessResponse = $("#guessResponse");
const $score = $("#score");
const $timer = $("#timer");
const $guess = $("#guess");


let scoreCount = 0;


async function guessValueClick(evt) {
    evt.preventDefault();
    $guessResponse.text("");
    if (timeLeft != -1) {
        const guess = $guessForm.children()[0].value;
        console.log(guess);
        const response = await axios({
            url: `http://localhost:5000/guess`,
            method: "POST",
            data: { guess: guess },
        });
        const guessResult = response.data.result;
        $guessResponse.text(`Guess is: ${guessResult}`);
        if (guessResult === 'ok') {
            scoreCount += guess.length;
            $score.text(`Score: ${scoreCount}`);
        }
    }
    $guessForm.trigger("reset");
}

$guessForm.on('submit', guessValueClick);


let timeLeft = 60;

const interval = setInterval(async function () {
    $timer.text(`Timer: ${timeLeft}`);

    timeLeft--;

    if (timeLeft < 0) {
        clearInterval(interval);
        $timer.text("Time's up!");
        const response = await axios({
            url: `http://localhost:5000/update`,
            method: "POST",
            data: { score: scoreCount },
        });
        window.location.href = '/results';
    }
}, 1000);