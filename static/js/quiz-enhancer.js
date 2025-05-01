/**
 * Quiz Enhancement Script
 * Adds interactive features to improve the quiz taking experience
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize quiz enhancements
    initQuizEnhancements();
});

/**
 * Initialize all interactive elements for the quiz
 */
function initQuizEnhancements() {
    // Add smooth transitions between questions
    initQuestionTransitions();
    
    // Enhance choice selection
    initChoiceSelection();
    
    // Initialize timer animation
    initTimerAnimation();
    
    // Add keyboard navigation
    initKeyboardNavigation();
    
    // Add hover effects for choices
    initChoiceHoverEffects();
    
    // Add confetti on quiz completion
    checkForQuizCompletion();
}

/**
 * Add smooth transitions between questions
 */
function initQuestionTransitions() {
    const questionForm = document.querySelector('.question-form');
    if (!questionForm) return;
    
    // Add transition class to the form
    questionForm.classList.add('question-transition');
    
    // Listen for form submission
    questionForm.addEventListener('submit', function(e) {
        // Add exit animation class
        this.classList.add('question-exit');
        
        // Small delay to allow animation to complete
        setTimeout(() => {
            // Let the form submit normally
        }, 300);
    });
}

/**
 * Enhance the choice selection experience
 */
function initChoiceSelection() {
    const choiceLabels = document.querySelectorAll('.choice-label');
    const choiceInputs = document.querySelectorAll('.choice-input');
    
    choiceLabels.forEach(label => {
        // Add ripple effect on click
        label.addEventListener('click', function(e) {
            // Create ripple element
            const ripple = document.createElement('span');
            ripple.className = 'choice-ripple';
            this.appendChild(ripple);
            
            // Position the ripple
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            ripple.style.width = ripple.style.height = `${size}px`;
            ripple.style.left = `${e.clientX - rect.left - size/2}px`;
            ripple.style.top = `${e.clientY - rect.top - size/2}px`;
            
            // Remove ripple after animation completes
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Highlight selected choice
    choiceInputs.forEach(input => {
        // Check initial state
        if (input.checked) {
            const label = document.querySelector(`label[for="${input.id}"]`);
            if (label) {
                label.classList.add('selected');
            }
        }
        
        // Add change listener
        input.addEventListener('change', function() {
            // Remove all selected classes
            choiceLabels.forEach(lbl => lbl.classList.remove('selected'));
            
            // Add selected class to current choice
            if (this.checked) {
                const label = document.querySelector(`label[for="${this.id}"]`);
                if (label) {
                    label.classList.add('selected');
                }
            }
        });
    });
}

/**
 * Initialize timer animation for timed quizzes
 */
function initTimerAnimation() {
    const timerElement = document.querySelector('.quiz-timer');
    if (!timerElement) return;
    
    const timerBar = document.querySelector('.timer-bar');
    if (!timerBar) return;
    
    // Get total time from data attribute or default to 60 seconds
    const totalTime = parseInt(timerElement.dataset.totalTime || 60);
    
    // Update timer bar every second
    const timerInterval = setInterval(() => {
        const timeLeft = parseInt(timerElement.textContent);
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            return;
        }
        
        // Update timer bar width
        const percentage = (timeLeft / totalTime) * 100;
        timerBar.style.width = `${percentage}%`;
        
        // Change color as time runs out
        if (percentage < 25) {
            timerBar.classList.add('timer-critical');
            // Add pulse animation to timer
            timerElement.classList.add('timer-pulse');
        } else if (percentage < 50) {
            timerBar.classList.add('timer-warning');
            timerBar.classList.remove('timer-critical');
            timerElement.classList.remove('timer-pulse');
        }
    }, 1000);
}

/**
 * Initialize keyboard navigation for quiz
 */
function initKeyboardNavigation() {
    // Only add keyboard navigation if we're on a question page
    const choiceInputs = document.querySelectorAll('.choice-input');
    if (choiceInputs.length === 0) return;
    
    document.addEventListener('keydown', function(e) {
        // Number keys 1-9 select choices
        if (e.key >= '1' && e.key <= '9') {
            const index = parseInt(e.key) - 1;
            if (index < choiceInputs.length) {
                choiceInputs[index].checked = true;
                
                // Trigger change event to update UI
                const changeEvent = new Event('change');
                choiceInputs[index].dispatchEvent(changeEvent);
                
                // Scroll to the selected choice if needed
                const label = document.querySelector(`label[for="${choiceInputs[index].id}"]`);
                if (label) {
                    label.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        }
        
        // Enter or Space to submit if a choice is selected
        if ((e.key === 'Enter' || e.key === ' ') && e.target.tagName !== 'INPUT' && e.target.tagName !== 'BUTTON' && e.target.tagName !== 'TEXTAREA') {
            // Check if any choice is selected
            const selectedChoice = Array.from(choiceInputs).find(input => input.checked);
            if (selectedChoice) {
                // Get submit button and click it
                const submitButton = document.querySelector('.question-form button[type="submit"]');
                if (submitButton) {
                    submitButton.click();
                }
            }
        }
    });
}

/**
 * Add hover effects to quiz choices
 */
function initChoiceHoverEffects() {
    const choiceLabels = document.querySelectorAll('.choice-label');
    
    choiceLabels.forEach(label => {
        // Add shine effect on hover
        label.addEventListener('mouseenter', function() {
            this.classList.add('choice-hover');
        });
        
        label.addEventListener('mouseleave', function() {
            this.classList.remove('choice-hover');
        });
    });
}

/**
 * Check if the quiz is completing and add celebration effects
 */
function checkForQuizCompletion() {
    // Check if we're submitting the last question
    const questionForm = document.querySelector('.question-form');
    const progressBar = document.querySelector('.progress-bar');
    
    if (questionForm && progressBar) {
        const progress = parseInt(progressBar.style.width || '0');
        const totalQuestions = parseInt(questionForm.dataset.totalQuestions || '0');
        const currentQuestion = parseInt(questionForm.dataset.currentQuestion || '0');
        
        // If this is the last question, add completion animation
        if (currentQuestion === totalQuestions) {
            questionForm.addEventListener('submit', function() {
                // Add hidden canvas for confetti that will appear on results page
                const confettiPromise = document.createElement('input');
                confettiPromise.type = 'hidden';
                confettiPromise.name = 'celebrate';
                confettiPromise.value = 'true';
                this.appendChild(confettiPromise);
            });
        }
    }
} 