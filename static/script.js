// // Load voices asynchronously
// window.speechSynthesis.onvoiceschanged = function () {
//     window.speechSynthesis.getVoices();
// };

// let phase = "reset";  // Initial phase
// let timerElement = document.getElementById("timer");
// let messageElement = document.getElementById("message");
// let progressBar = document.querySelector(".progress-bar");
// let modeElement = document.getElementById("mode");
// let setNumberElement = document.getElementById("set-number");

// function triggerTimer(feedback) {
//     timerElement = document.getElementById("timer");
//     messageElement = document.getElementById("message");
//     progressBar = document.querySelector(".progress-bar");
//     modeElement = document.getElementById("mode");
//     setNumberElement = document.getElementById("set-number");

//     if (feedback === "start") {
//         startTimer();
//     } else if (feedback === "pause") {
//         pauseTimer();
//     } else if (feedback === "resume") {
//         resumeTimer();
//     }
// }

// function fetchFeedback() {
//     fetch('/feedback')
//         .then(response => response.json())
//         .then(data => {
//             // Update feedback text
//             let feedbackText = data.message;
//             document.getElementById("feedback").innerText = feedbackText;
//             if (feedbackText === "Great job! Your pose is perfectly aligned.") {
//                 if (phase === "pause") {
//                     phase = "resume";
//                 } else if(phase === "reset") {
//                     phase = "start";
//                 }
//                 else{
//                     phase = "workout";
//                 }
//             } else {
//                 phase = "pause";
//             }


//             const utterance = new SpeechSynthesisUtterance(feedbackText);
//             utterance.rate = 1;
//             utterance.pitch = 1;
//             utterance.volume = 1;

//             const voices = window.speechSynthesis.getVoices();
//             utterance.voice = voices.find(voice => voice.lang === 'en-US');

//             window.speechSynthesis.speak(utterance);
//             console.log("Done speaking");
//             triggerTimer(phase);
//         })
//         .catch(error => console.error('Error fetching feedback:', error));
// }

// // Call fetchFeedback every 3 seconds
// setInterval(fetchFeedback, 3000);

// // ====================================
// //          Script for timer
// // ====================================


// let repetitionTime = 15;  // Workout duration in seconds
// let relaxTime = 5;  // Relax duration in seconds
// let totalRepetitions = 3;  // Number of cycles
// let currentRepetition = 0;
// let timeRemaining = 0;
// let timer;
// let running = false;
// let isPaused = false;
// // let feedback = "Your pose is accurate!";

// function startTimer() {
//     if (running) return; // Prevent multiple starts
//     running = true;
//     messageElement.innerText = "";
//     currentRepetition = 1;
//     isPaused = false;
//     phase = "workout";
//     timeRemaining = repetitionTime;
//     updateSetNumber();
//     nextPhase();
// }

// function pauseTimer() {
//     isPaused = true;
//     clearTimeout(timer);
// }

// function resumeTimer() {
//     if (isPaused) {
//         isPaused = false;
//         updateTimer();
//     }
// }

// function nextPhase() {
//     if (currentRepetition > totalRepetitions) {
//         messageElement.innerText = "🎉 Workout Completed!";
//         running = false;
//         return;
//     }

//     progressBar.style.stroke = "#4caf50"; // Restore progress bar color

//     modeElement.innerText = phase === "workout" ? "Workout 🔥" : "Relax 😌";
//     timeRemaining = phase === "workout" ? repetitionTime : relaxTime;
//     updateTimer();
// }

// function reset() {
//     clearTimeout(timer);
//     running = false;
//     isPaused = false;
//     phase = "reset";
//     currentRepetition = 0;
//     timeRemaining = 0;
//     timerElement.innerText = "00:00";
//     messageElement.innerText = "";
//     modeElement.innerText = "Waiting...";
//     setNumberElement.innerText = "Set 0";
//     progressBar.style.strokeDashoffset = 440;
// }

// function updateTimer() {
//     if (isPaused) return;

//     timerElement.innerText = formatTime(timeRemaining);
//     progressBar.style.strokeDashoffset = (timeRemaining / (phase === "workout" ? repetitionTime : relaxTime)) * 377;

//     if (timeRemaining > 0) {
//         timeRemaining--;
//         timer = setTimeout(updateTimer, 1000);
//     } else {
//         if (phase === "workout") {
//             messageElement.innerText = "✅ Workout Completed! Relax Time Starts...";
//             phase = "relax";
//         } else {
//             messageElement.innerText = "💪 Get Ready for Next Workout!";
//             phase = "workout";
//             currentRepetition++;
//             updateSetNumber();
//         }
//         setTimeout(nextPhase, 2000);
//     }
// }

// function formatTime(seconds) {
//     let min = Math.floor(seconds / 60);
//     let sec = seconds % 60;
//     return `${String(min).padStart(2, "0")}:${String(sec).padStart(2, "0")}`;
// }

// function updateSetNumber() {
//     setNumberElement.innerText = `Set ${currentRepetition}`;
// }

// // function updateFeedback(feedbackText, isCorrect) {
// //     let feedbackElement = document.getElementById("feedback");
// //     feedbackElement.innerText = feedbackText;

// //     // Remove existing styles
// //     feedbackElement.classList.remove("correct", "incorrect");

// //     // Apply correct or incorrect styling
// //     if (isCorrect) {
// //         feedbackElement.classList.add("correct");
// //     } else {
// //         feedbackElement.classList.add("incorrect");
// //     }
// // }

// // // Example Usage
// // updateFeedback("Great Pose! Keep it up! 💪", true); // Green Feedback
// // updateFeedback("Incorrect Posture! Adjust your back. ❌", false); // Red Feedback


// let totalTime = 15; // Time required to show extra buttons
// let elapsedTime = 0;
// let extraButtons = document.getElementById("extra-buttons");

// function updateTimer() {
//     if (isPaused) return;

//     timerElement.innerText = formatTime(timeRemaining);
//     progressBar.style.strokeDashoffset = (timeRemaining / (phase === "workout" ? repetitionTime : relaxTime)) * 377;

//     if (timeRemaining > 0) {
//         timeRemaining--;
//         elapsedTime++; // Track time passed
//         timer = setTimeout(updateTimer, 1000);
//     } else {
//         if (phase === "workout") {
//             messageElement.innerText = "✅ Workout Completed! Relax Time Starts...";
//             phase = "relax";
//         } else {
//             messageElement.innerText = "💪 Get Ready for Next Workout!";
//             phase = "workout";
//             currentRepetition++;
//             updateSetNumber();
//         }
//         setTimeout(nextPhase, 2000);
//     }

//     // Show "Repeat" and "Next" buttons after 15 seconds
//     if (elapsedTime >= totalTime) {
//         extraButtons.style.display = "block";
//     }
// }

// function repeatExercise() {
//     currentRepetition++; // Increase set count
//     reset(); // Reset timer
//     messageElement.innerText = "🔄 Repeating exercise...";
//     extraButtons.style.display = "none"; // Hide buttons again
//     elapsedTime = 0; // Reset elapsed time
// }

// function nextPose() {
//     window.location.href = "{{ url_for('home') }}"; // Redirect to homepage
// }


// Load voices asynchronously
window.speechSynthesis.onvoiceschanged = function () {
    window.speechSynthesis.getVoices();
};


let phase = "reset";  // Initial phase
let timerElement = document.getElementById("timer");
let messageElement = document.getElementById("message");
let progressBar = document.getElementById("progress-bar");
let modeElement = document.getElementById("mode");
let setNumberElement = document.getElementById("set-number");
let extraButtons = document.getElementById("extra-buttons");
let setCount = 0;
let setCountElement = document.getElementById("set-count");

let manualTime = 15;  // Timer starts at 15 seconds
let manualTimer;
let isRunning = false;

function initialize_elements() {
    phase = "reset";  // Initial phase
    timerElement = document.getElementById("timer");
    messageElement = document.getElementById("message");
    progressBar = document.getElementById("progress-bar");
    modeElement = document.getElementById("mode");
    setNumberElement = document.getElementById("set-number");
    extraButtons = document.getElementById("extra-buttons");
    setCount = 0;
    setCountElement = document.getElementById("set-count");
}

function startManualTimer() {
    initialize_elements();
    if (!isRunning && manualTime > 0) {
        isRunning = true;
        manualTimer = setInterval(() => {
            if (manualTime > 0) {
                manualTime--;
                timerElement.innerText = formatTime(manualTime);
                updateProgressBar();
            } else {
                clearInterval(manualTimer);
                messageElement.innerText = "✅ Workout Completed!";
                isRunning = false;

                // Show "Repeat" & "Next" buttons after first completion
                extraButtons.style.display = "block";
                document.getElementById("repeat-btn").addEventListener("click", repeatExercise);
                document.getElementById("next-pose").addEventListener("click", nextPose);
            }
        }, 1000);
    }
}

function stopManualTimer() {
    initialize_elements();
    clearInterval(manualTimer);
    isRunning = false;
}

function resetManualTimer() {
    clearInterval(manualTimer);
    isRunning = false;
    manualTime = 15;  // Reset to 15 seconds
    timerElement.innerText = "00:15";
    messageElement.innerText = "";
    progressBar.style.strokeDashoffset = "0";  // Reset progress bar
}

function repeatExercise() {
    setCount++;  // Increase set count
    setCountElement.innerText = `Set:${setCount}`;  // Update UI
    resetManualTimer();  // Reset timer
    messageElement.innerText = "🔄 Repeating exercise...";
    extraButtons.style.display = "none";  // Hide buttons until next completion
}

function nextPose() {
    let homeUrl = document.getElementById("next-pose").getAttribute("data-url");
    window.location.href = homeUrl;  // Redirect to homepage
}

function formatTime(seconds) {
    let min = Math.floor(seconds / 60);
    let sec = seconds % 60;
    return `${String(min).padStart(2, "0")}:${String(sec).padStart(2, "0")}`;
}

function updateProgressBar() {
    let progress = (manualTime / 15) * 440;  // Calculate progress
    progressBar.style.strokeDashoffset = progress.toString();
}

// Attach event listeners
// document.getElementById("start-btn").addEventListener("click", startManualTimer);
// document.getElementById("stop-btn").addEventListener("click", stopManualTimer);
// document.getElementById("reset-btn").addEventListener("click", resetManualTimer);
// document.getElementById("repeat-btn").addEventListener("click", repeatExercise);
// document.getElementById("next-pose").addEventListener("click", nextPose);




function fetchFeedback() {
    fetch('/feedback')
        .then(response => response.json())
        .then(data => {
            // Update feedback text
            let feedbackText = data.message;
            document.getElementById("feedback").innerText = feedbackText;
            if (feedbackText === "Great job! Your pose is perfectly aligned.") {
                startManualTimer();
            } else {
                stopManualTimer();
            }


            const utterance = new SpeechSynthesisUtterance(feedbackText);
            utterance.rate = 1;
            utterance.pitch = 1;
            utterance.volume = 1;

            const voices = window.speechSynthesis.getVoices();
            utterance.voice = voices.find(voice => voice.lang === 'en-US');

            window.speechSynthesis.speak(utterance);
            console.log("Done speaking");
            // triggerTimer(phase);
        })
        .catch(error => console.error('Error fetching feedback:', error));
}

// Call fetchFeedback every 3 seconds
setInterval(fetchFeedback, 5000);





// function updateFeedback(feedbackText, isCorrect) {
//     let feedbackElement = document.getElementById("feedback");
//     feedbackElement.innerText = feedbackText;

//     // Remove existing styles
//     feedbackElement.classList.remove("correct", "incorrect");

//     // Apply correct or incorrect styling
//     if (isCorrect) {
//         feedbackElement.classList.add("correct");
//     } else {
//         feedbackElement.classList.add("incorrect");
//     }
// }

// // Example Usage
// updateFeedback("Great Pose! Keep it up! 💪", true); // Green Feedback
// updateFeedback("Incorrect Posture! Adjust your back. ❌", false); // Red Feedback







// let totalTime = 15; // Time required to show extra buttons
// let elapsedTime = 0;
// let extraButtons = document.getElementById("extra-buttons");

// function updateTimer() {
//     if (isPaused) return;

//     timerElement.innerText = formatTime(timeRemaining);
//     progressBar.style.strokeDashoffset = (timeRemaining / (phase === "workout" ? repetitionTime : relaxTime)) * 377;

//     if (timeRemaining > 0) {
//         timeRemaining--;
//         elapsedTime++; // Track time passed
//         timer = setTimeout(updateTimer, 1000);
//     } else {
//         if (phase === "workout") {
//             messageElement.innerText = "✅ Workout Completed! Relax Time Starts...";
//             phase = "relax";
//         } else {
//             messageElement.innerText = "💪 Get Ready for Next Workout!";
//             phase = "workout";
//             currentRepetition++;
//             updateSetNumber();
//         }
//         setTimeout(nextPhase, 2000);
//     }

//     // Show "Repeat" and "Next" buttons after 15 seconds
//     if (elapsedTime >= totalTime) {
//         extraButtons.style.display = "block";
//     }
// }

// function repeatExercise() {
//     currentRepetition++; // Increase set count
//     reset(); // Reset timer
//     messageElement.innerText = "🔄 Repeating exercise...";
//     extraButtons.style.display = "none"; // Hide buttons again
//     elapsedTime = 0; // Reset elapsed time
// }

// function nextPose() {
//     window.location.href = "{{ url_for('home') }}"; // Redirect to homepage
// }