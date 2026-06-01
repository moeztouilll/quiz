// State variables
let questions = [];
let currentIndex = 0;
let selectedAnswers = []; // for choice questions (indices)
let matchingAnswers = {}; // for matching questions (leftTerm -> selectedRightDef)
let scores = {
  correct: 0,
  incorrect: 0,
  states: {} // questionNum -> true (correct), false (incorrect), undefined (unanswered)
};
let activeFilter = 'all';

// DOM elements
const elQuizCard = document.getElementById('quiz-card');
const elQuestionBadge = document.getElementById('question-badge');
const elQuestionTypeBadge = document.getElementById('question-type-badge');
const elQuestionText = document.getElementById('question-text');
const elImageContainer = document.getElementById('image-container');
const elQuestionImage = document.getElementById('question-image');
const elAnswersContainer = document.getElementById('answers-container');
const elBtnSubmit = document.getElementById('btn-submit');
const elBtnNext = document.getElementById('btn-next');
const elBtnReset = document.getElementById('btn-reset');

const elFeedbackPanel = document.getElementById('feedback-panel');
const elFeedbackStatus = document.getElementById('feedback-status');
const elScrapedExplanationBox = document.getElementById('scraped-explanation-box');
const elScrapedExplanationText = document.getElementById('scraped-explanation-text');
const elAiExplanationBox = document.getElementById('ai-explanation-box');
const elAiLoader = document.getElementById('ai-loader');
const elAiExplanationText = document.getElementById('ai-explanation-text');

const elScoreCorrect = document.getElementById('score-correct');
const elScoreIncorrect = document.getElementById('score-incorrect');
const elScorePercent = document.getElementById('score-percent');
const elProgressVal = document.getElementById('progress-val');
const elProgressBarFill = document.getElementById('progress-bar-fill');
const elQuestionGrid = document.getElementById('question-grid');
const elFilterButtons = document.querySelectorAll('.filter-btn');

// Initialize app
async function init() {
  try {
    // Try to load session data
    const sessionData = sessionStorage.getItem('ccna_quiz_session');
    
    if (sessionData) {
      const data = JSON.parse(sessionData);
      questions = data.questions;
      scores = data.scores;
      currentIndex = data.currentIndex;
    } else {
      // Fresh start: Fetch questions
      const response = await fetch('questions.json?v=7');
      if (!response.ok) throw new Error("Failed to load questions.json");
      let loadedQuestions = await response.json();
      
      // Shuffle questions
      shuffleArray(loadedQuestions);
      
      // Setup questions and shuffle choices
      loadedQuestions.forEach((q, i) => {
        q.original_num = q.num;
        q.num = i + 1; // renumber 1 to N
        if (q.choices && q.choices.length > 0) {
          shuffleArray(q.choices);
        }
      });
      
      questions = loadedQuestions;
      saveState();
    }
    
    // Render sidebar grid
    renderGrid();
    updateStats();
    
    // Load current question
    loadQuestion(currentIndex);
    
    // Setup listeners
    elBtnSubmit.addEventListener('click', submitAnswer);
    elBtnNext.addEventListener('click', nextQuestion);
    elBtnReset.addEventListener('click', resetQuiz);
    
    // Filter click handlers
    elFilterButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        elFilterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeFilter = btn.dataset.filter;
        renderGrid();
      });
    });

  } catch (error) {
    console.error("Error starting app:", error);
    elQuestionText.textContent = "Erreur : Impossible de charger questions.json. Avez-vous bien uploadé ce fichier sur votre serveur ?";
  }
}

// Utility to shuffle an array (Fisher-Yates)
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

// Load a specific question by index
function loadQuestion(index) {
  currentIndex = index;
  const q = questions[currentIndex];
  if (!q) return;

  // Update URL active class in grid
  document.querySelectorAll('.q-btn').forEach((btn, i) => {
    if (i === currentIndex) {
      btn.classList.add('current');
    } else {
      btn.classList.remove('current');
    }
  });

  // Reset question state variables
  selectedAnswers = [];
  matchingAnswers = {};

  // UI elements updates
  elQuestionBadge.textContent = `Question ${q.num}`;
  elQuestionText.textContent = q.question_text;
  
  // Handle image
  if (q.image) {
    elQuestionImage.style.opacity = '0'; // Hide temporarily
    elQuestionImage.src = q.image + '?v=3'; // Bypass browser cache
    elQuestionImage.onload = () => { elQuestionImage.style.opacity = '1'; }; // Show when loaded
    elImageContainer.style.display = 'flex';
  } else {
    elImageContainer.style.display = 'none';
    elQuestionImage.src = '';
  }

  // Clear feedack and hide NEXT button, show SUBMIT button
  elFeedbackPanel.style.display = 'none';
  elScrapedExplanationBox.style.display = 'none';
  elAiExplanationBox.style.display = 'none';
  elBtnNext.style.display = 'none';
  elBtnSubmit.style.display = 'inline-block';
  elBtnSubmit.disabled = true;

  // Determine question type
  const isMatching = !!q.table;
  
  if (isMatching) {
    elQuestionTypeBadge.textContent = "Mise en Relation";
    renderMatchingQuestion(q);
  } else if (q.choices && q.choices.length > 0) {
    const correctCount = q.choices.filter(c => c.is_correct).length;
    elQuestionTypeBadge.textContent = correctCount > 1 ? `Choix Multiples (${correctCount})` : "Choix Unique";
    renderChoiceQuestion(q, correctCount > 1);
  } else {
    // No interactive choices available
    elQuestionTypeBadge.textContent = "Information / Image";
    elAnswersContainer.innerHTML = '<div class="choice-item" style="justify-content:center; cursor:default; pointer-events:none;"><span class="choice-text" style="color:var(--text-muted); font-style:italic;">Les réponses interactives ne sont pas disponibles pour cette question (elles figurent probablement dans l\'image). Cliquez sur Valider pour continuer.</span></div>';
    elBtnSubmit.disabled = false;
  }
  
  // If the user already completed this question, reveal correct answers directly
  const state = scores.states[q.num];
  if (state !== undefined) {
    revealAnswers(q, state);
  }
}

// Render choice list (Single or Multiple responses)
function renderChoiceQuestion(q, isMultiple) {
  elAnswersContainer.innerHTML = '';
  
  q.choices.forEach((choice, idx) => {
    const item = document.createElement('div');
    item.className = 'choice-item';
    item.dataset.index = idx;
    
    const checkbox = document.createElement('div');
    checkbox.className = 'choice-checkbox';
    
    const textSpan = document.createElement('span');
    textSpan.className = 'choice-text';
    textSpan.textContent = choice.text;
    
    item.appendChild(checkbox);
    item.appendChild(textSpan);
    
    // Add click handler (only if question not already answered)
    if (scores.states[q.num] === undefined) {
      item.addEventListener('click', () => {
        if (isMultiple) {
          if (selectedAnswers.includes(idx)) {
            selectedAnswers = selectedAnswers.filter(i => i !== idx);
            item.classList.remove('selected');
          } else {
            selectedAnswers.push(idx);
            item.classList.add('selected');
          }
        } else {
          selectedAnswers = [idx];
          document.querySelectorAll('.choice-item').forEach(el => el.classList.remove('selected'));
          item.classList.add('selected');
        }
        
        elBtnSubmit.disabled = selectedAnswers.length === 0;
      });
    }
    
    elAnswersContainer.appendChild(item);
  });
}

// Render matching rows with dropdowns
function renderMatchingQuestion(q) {
  elAnswersContainer.innerHTML = '';
  
  // Shuffled definitions for dropdown options
  const rightOptions = q.table.map(row => row.right);
  // Shuffle options array
  const shuffledOptions = [...rightOptions].sort(() => Math.random() - 0.5);

  q.table.forEach((row, idx) => {
    const rowEl = document.createElement('div');
    rowEl.className = 'matching-pair-row';
    
    const leftEl = document.createElement('div');
    leftEl.className = 'matching-left';
    leftEl.textContent = row.left;
    
    const connector = document.createElement('div');
    connector.className = 'matching-connector';
    connector.textContent = '➔';
    
    const select = document.createElement('select');
    select.className = 'matching-select';
    select.dataset.left = row.left;
    
    // Placeholder option
    const placeholder = document.createElement('option');
    placeholder.value = '';
    placeholder.textContent = 'Sélectionner la correspondance...';
    select.appendChild(placeholder);
    
    shuffledOptions.forEach(opt => {
      const option = document.createElement('option');
      option.value = opt;
      option.textContent = opt;
      select.appendChild(option);
    });
    
    // Add change handler (only if not already answered)
    if (scores.states[q.num] === undefined) {
      select.addEventListener('change', (e) => {
        matchingAnswers[row.left] = e.target.value;
        
        // Enable submit button if all left choices are paired
        const allAnswered = q.table.every(r => matchingAnswers[r.left]);
        elBtnSubmit.disabled = !allAnswered;
      });
    } else {
      select.disabled = true;
    }
    
    rowEl.appendChild(leftEl);
    rowEl.appendChild(connector);
    rowEl.appendChild(select);
    
    elAnswersContainer.appendChild(rowEl);
  });
}

// Submit answer action
async function submitAnswer() {
  const q = questions[currentIndex];
  if (!q || scores.states[q.num] !== undefined) return;

  const isMatching = !!q.table;
  let isCorrect = true;

  if (isMatching) {
    // Check if each matched option matches the correct mapping
    q.table.forEach(row => {
      const userVal = matchingAnswers[row.left];
      if (userVal !== row.right) {
        isCorrect = false;
      }
    });
  } else {
    // For choice questions:
    // User must select ALL correct answers and NO incorrect answers
    q.choices.forEach((choice, idx) => {
      const shouldBeSelected = choice.is_correct;
      const isSelected = selectedAnswers.includes(idx);
      if (shouldBeSelected !== isSelected) {
        isCorrect = false;
      }
    });
  }

  // Update score state
  scores.states[q.num] = isCorrect;
  if (isCorrect) {
    scores.correct++;
  } else {
    scores.incorrect++;
  }

  saveState();
  updateStats();
  renderGrid();

  // Show visual feedback and explanation
  await revealAnswers(q, isCorrect);
}

// Reveal correct/incorrect answers and explain
async function revealAnswers(q, isCorrect) {
  elBtnSubmit.style.display = 'none';
  elBtnNext.style.display = 'inline-block';

  // Apply colors to choices/selects
  const isMatching = !!q.table;
  
  if (isMatching) {
    document.querySelectorAll('.matching-select').forEach(select => {
      const leftTerm = select.dataset.left;
      const correctRow = q.table.find(r => r.left === leftTerm);
      const userVal = matchingAnswers[leftTerm] || scores.states[q.num] !== undefined && correctRow.right;
      
      select.value = correctRow.right; // force correct value to show
      select.disabled = true;
      
      if (userVal === correctRow.right) {
        select.classList.add('correct-match');
      } else {
        select.classList.add('incorrect-match');
      }
    });
  } else if (q.choices && q.choices.length > 0) {
    document.querySelectorAll('.choice-item').forEach(item => {
      const idx = parseInt(item.dataset.index);
      if (isNaN(idx)) return; // skip the fallback message div
      const isChoiceCorrect = q.choices[idx].is_correct;
      const isSelected = selectedAnswers.includes(idx);
      
      item.classList.remove('selected');
      
      if (isChoiceCorrect) {
        item.classList.add('correct-reveal');
      } else if (isSelected) {
        item.classList.add('incorrect-reveal');
      }
      // Disable click interaction by removing event listeners
      const newItem = item.cloneNode(true);
      item.parentNode.replaceChild(newItem, item);
    });
  }

  // Render Feedback box
  elFeedbackPanel.style.display = 'block';
  if (isCorrect) {
    elFeedbackStatus.innerHTML = '<span style="font-size:1.5rem">🎉</span> Correct !';
    elFeedbackStatus.className = 'feedback-status correct';
  } else {
    elFeedbackStatus.innerHTML = '<span style="font-size:1.5rem">❌</span> Incorrect';
    elFeedbackStatus.className = 'feedback-status incorrect';
  }

  // Show course explanation if it exists
  if (q.explanation) {
    elScrapedExplanationText.textContent = q.explanation;
    elScrapedExplanationBox.style.display = 'block';
  }

  // If answer is incorrect, load AI explanation
  if (!isCorrect) {
    elAiExplanationBox.style.display = 'block';
    elAiLoader.style.display = 'flex';
    elAiExplanationText.textContent = '';

    // Prepare information for LLM
    let correctStr = '';
    let userStr = '';

    if (isMatching) {
      correctStr = q.table.map(row => `${row.left} ➔ ${row.right}`).join('\n');
      userStr = Object.entries(matchingAnswers).map(([k, v]) => `${k} ➔ ${v}`).join('\n');
    } else {
      correctStr = q.choices.filter(c => c.is_correct).map(c => c.text).join(', ');
      userStr = selectedAnswers.map(idx => q.choices[idx].text).join(', ') || '(Aucune réponse)';
    }

    try {
      const response = await fetch('/api/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: q.question_text,
          userAnswer: userStr,
          correctAnswer: correctStr
        })
      });

      const data = await response.json();
      elAiLoader.style.display = 'none';
      if (data.explanation) {
        elAiExplanationText.textContent = data.explanation;
      } else {
        // API unavailable - hide the AI box silently
        elAiExplanationBox.style.display = 'none';
      }
    } catch (err) {
      console.error("AI Explain API Error:", err);
      elAiLoader.style.display = 'none';
      // Hide AI box instead of showing an error message
      elAiExplanationBox.style.display = 'none';
    }
  }
}

// Next question action
function nextQuestion() {
  if (currentIndex < questions.length - 1) {
    loadQuestion(currentIndex + 1);
  } else {
    alert("Vous avez terminé toutes les questions de ce test ! Félicitations !");
  }
}

// Reset quiz state
function resetQuiz() {
  if (confirm("Voulez-vous vraiment réinitialiser vos scores et générer un nouveau test aléatoire ?")) {
    sessionStorage.removeItem('ccna_quiz_session');
    location.reload(); // Reload page for a fresh randomized session
  }
}

// Render the index buttons in the sidebar
function renderGrid() {
  elQuestionGrid.innerHTML = '';
  
  questions.forEach((q, idx) => {
    const state = scores.states[q.num];
    const isAnswered = state !== undefined;
    
    // Apply filters
    if (activeFilter === 'incorrect' && (!isAnswered || state === true)) return;
    if (activeFilter === 'unanswered' && isAnswered) return;

    const btn = document.createElement('button');
    btn.className = 'q-btn';
    btn.textContent = q.num;
    
    if (idx === currentIndex) btn.classList.add('current');
    if (isAnswered) {
      if (state === true) btn.classList.add('correct');
      else btn.classList.add('incorrect');
    }
    
    btn.addEventListener('click', () => {
      loadQuestion(idx);
    });
    
    elQuestionGrid.appendChild(btn);
  });
}

// Update score values and progress bar in UI
function updateStats() {
  elScoreCorrect.textContent = scores.correct;
  elScoreIncorrect.textContent = scores.incorrect;
  
  const totalCompleted = scores.correct + scores.incorrect;
  const percent = totalCompleted > 0 ? Math.round((scores.correct / totalCompleted) * 100) : 0;
  elScorePercent.textContent = `${percent}%`;

  const totalQuestions = questions.length || 158;
  const progressPercent = Math.round((totalCompleted / totalQuestions) * 100);
  elProgressVal.textContent = `${totalCompleted} / ${totalQuestions} (${progressPercent}%)`;
  elProgressBarFill.style.width = `${progressPercent}%`;
}

// Save scores to sessionStorage
function saveState() {
  const sessionData = {
    questions,
    scores,
    currentIndex
  };
  sessionStorage.setItem('ccna_quiz_session', JSON.stringify(sessionData));
}

// Session state is loaded in init()


// Run app init
init();
